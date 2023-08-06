#!/usr/bin/env python3
# encoding: utf-8
"""Implementation of classes for storing RuNNer parameters and results.

This module provides custom classes for storing the different types of data
produced and/or read by RuNNer.

Attributes
----------
ElementStorageMixin : object
    A mixin for all storage containers storing data in element-wise fashion.
RunnerScaling : ElementStorageMixin
    Storage container for RuNNer symmetry function scaling data.
RunnerWeights : ElementStorageMixin
    Storage container for weights and bias values of atomic neural networks.
RunnerStructureSymmetryFunctionValues: ElementStorageMixin
    Storage container for all symmetry function values of one single structure.
RunnerSymmetryFunctionValues : object
    Storage container for many `RunnerStructureSymmetryFunctionValues` objects,
    i.e. for a collection of symmetry function values in one training dataset.
RunnerFitResults : object
    Storage container for fit quality indicators in RuNNer Mode 2 stdout.
RunnerSplitTrainTest : object
    Storage container for the train and test set split in RuNNer Mode 1.
RunnerResults : TypedDict
    Type specifications for all results that the RuNNer calculator can produce.
    Essentially a collection of all the previously mentioned storage container
    classes plus energies and forces.
"""

from typing import Optional, Union, Iterator, Tuple, List, Dict, TextIO

import os
import re

import numpy as np
from ase.data import atomic_numbers, chemical_symbols

from runnerase.utils import reader, writer
from runnerase.plot import (RunnerSplitTrainTestPlots,
                            RunnerSymmetryFunctionValuesPlots,
                            RunnerStructureSymmetryFunctionValuesPlots,
                            RunnerFitResultsPlots,
                            RunnerScalingPlots)


class ElementStorageMixin:
    """Abstract mixin for storing element-specific RuNNer parameters/results.

    When constructing a neural network potential with RuNNer, one atomic neural
    network is built for every element in the system. As a result, many RuNNer
    parameters are element-specific.
    This mixin transforms any class into a storage container for
    element-specific data by
        - defining an abstract `data` container, i.e. a dictionary with
          str-np.ndarray pairs holding one numpy ndarray for each element.
          The keys are chemical symbols of elements.
        - defining magic methods like __iter__ and __setitem__ for convenient
          access back to that data storage.

    The storage of data in elementwise format is more efficient, as data can
    often be compressed into non-ragged numpy arrays.
    """

    def __init__(self) -> None:
        """Initialize the object."""
        # Data container for element - data pairs.
        self.data: Dict[str, np.ndarray] = {}

    def __iter__(self) -> Iterator[Tuple[str, np.ndarray]]:
        """Iterate over all key-value pairs in the `self.data` container."""
        for key, value in self.data.items():
            yield key, value

    def __len__(self) -> int:
        """Show the combined length of all stored element data arrays."""
        length = 0
        for value in self.data.values():
            shape: Tuple[int, ...] = value.shape
            length += shape[0]

        return length

    def __setitem__(
        self,
        key: Union[str, int],
        value: np.ndarray
    ) -> None:
        """Set one key-value pair in the self.data dictionary.

        Each key in self.data is supposed to be the chemical symbol of an
        element. Therefore, when an integer key is provided it is translated
        into the corresponding chemical symbol.

        Parameters
        ----------
        key : str or int
            The dictionary key were `value` will be stored. Integer keys are
            translated into the corresponding chemical symbol.
        value : np.ndarray
            The element-specific data to be stored in the form of a numpy array.
        """
        if isinstance(key, int):
            symbol: str = chemical_symbols[key]
            key = symbol

        self.data[key] = value

    def __getitem__(self, key: Union[str, int]) -> np.ndarray:
        """Get the data associated with `key` in the self.data dictionary.

        The data can either be accessed by the atomic number or the chemical
        symbol.

        Parameters
        ----------
        key : str or int
            Atomic number of chemical symbol of the desired `self.data`.
        """
        if isinstance(key, int):
            symbol: str = chemical_symbols[key]
            key = symbol

        return self.data[key]

    @property
    def elements(self) -> List[str]:
        """Show a list of elements for which data is available in storage."""
        return list(self.data.keys())


class RunnerScaling(ElementStorageMixin):
    """Storage container for RuNNer symmetry function scaling data.

    Resources
    ---------
    For more information on the `scaling.data` file format in RuNNer please
    visit the
    [docs](https://theochemgoettingen.gitlab.io/RuNNer/1.3/reference/files/).
    """

    def __init__(self, infile: Optional[Union[str, TextIO]] = None) -> None:
        """Initialize the object.

        Parameters
        ----------
        infile : str or TextIO
            If given, data will be read from this fileobj upon initialization.
        """
        # Initialize the base class. This creates the main self.data storage.
        super().__init__()

        # Store additional non-element-specific properties.
        self.target_min: float = np.NaN
        self.target_max: float = np.NaN

        # Read data from fileobj, if given.
        if infile is not None:
            self.read(infile)

    def __repr__(self) -> str:
        """Show a string representation of the object."""
        return f'{self.__class__.__name__}(elements={self.elements}, ' \
               + f'min={self.target_min}, max={self.target_max})'

    @reader
    def read(self, infile: Union[str, TextIO]) -> None:
        """Read symmetry function scaling data.

        Parameters
        ----------
        infile : str or TextIO
            The fileobj containing the scaling data in RuNNer format.
        """
        scaling: Dict[str, List[List[float]]] = {}
        for line in infile:
            data = line.split()

            # Lines of length five hold scaling data for each symmetry function.
            if len(data) == 5:
                element_id = data[0]

                if element_id not in scaling:
                    scaling[element_id] = []

                scaling[element_id].append([float(i) for i in data[1:]])

            # The final line holds only the min. and max. of the target
            # property.
            elif len(data) == 2:
                self.target_min = float(data[0])
                self.target_max = float(data[1])

        # Transform data into numpy arrays.
        for element_id, scalingdata in scaling.items():
            npdata: np.ndarray = np.array(scalingdata)
            self.data[element_id] = npdata

    @writer
    def write(self, outfile: TextIO) -> None:
        """Write symmetry function scaling data.

        Parameters
        ----------
        outfile : str or TextIO
            The fileobj or path to which the scaling data will be written.
        """
        for element_id, data in self.data.items():
            # First, write the scaling data for each symmetry function.
            for line in data:
                outfile.write(f'{element_id:5s} {int(line[0]):5d}'
                              + f'{line[1]:18.9f} {line[2]:18.9f} '
                              + f'{line[3]:18.9f}\n')

        # The last line contains the minimum and maximum of the target property.
        outfile.write(f'{self.target_min:18.9f} {self.target_max:18.9f}\n')

    @property
    def plot(self) -> RunnerScalingPlots:
        """Create a plotting interface."""
        return RunnerScalingPlots(self.data)


class RunnerWeights(ElementStorageMixin):
    """Storage container for RuNNer neural network weights and bias values.

    Resources
    ---------
    For more information on the `weights.XXX.data` file format in RuNNer please
    visit the
    [docs](https://theochemgoettingen.gitlab.io/RuNNer/1.3/reference/files/).
    """

    # Weights can be read either from a single file (`infile` argument) or from
    # a set of files under the given `path`. In the latter case, `elements`,
    # `prefix`, and `suffix` need to be exposed to the user.
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        infile: Optional[TextIO] = None,
        path: Optional[str] = None,
        elements: Optional[List[str]] = None,
        prefix: str = 'weights',
        suffix: str = 'data'
    ) -> None:
        """Initialize the object.

        Upon initialization, the user may specify to read weights either from
        a fileobj (`infile`) or from weight files residing under `path`.

        Parameters
        ----------
        infile : TextIO
            If given, data will be read from this fileobj upon initialization.
        path : str, optional, _default_ `None`
            If given, data will be read from all weight files under the given
            directory.
        elements : List[str]
            A selection of chemical symbols for which the weights under `path`
            will be read. Only active when `path` is given.
        prefix : str
            The filename prefix of weight files under `path`. Only necessary
            when path is specified.
        suffix : str
            The filename suffix of weight files under `path`. Only necessary
            when path is specified.
        """
        super().__init__()

        if infile is not None:
            self.read(infile)

        if path is not None:
            self.readall(path, elements, prefix, suffix)

    def __repr__(self) -> str:
        """Show a string representation of the object."""
        # Get the number of weights for each element in storage.
        num_weights = []
        for element, data in self.data.items():
            num_weights.append(f'{element}: {data.shape[0]}')
        return f"{self.__class__.__name__}({', '.join(num_weights)})"

    def read(self, infile: TextIO) -> None:
        """Read the atomic neural network weights and biases for one element.

        Parameters
        ----------
        infile : TextIO
            Data will be read from this fileobj.
        """
        # Obtain the chemical symbol of the element. RuNNer names weights files
        # like `prefix`.{atomic_number}.`suffix`.
        atomic_number = int(infile.name.split('.')[1])
        element = chemical_symbols[atomic_number]

        # Store the weights as a np.ndarray.
        self.data[element] = np.genfromtxt(infile, usecols=(0))

    # For some reason pylint thinks that this function has the same signature as
    # ase.io.storageclasses.write_weights.
    # pylint: disable=R0801
    def readall(
        self,
        path: str = '.',
        elements: Optional[List[str]] = None,
        prefix: str = 'weights',
        suffix: str = 'data'
    ) -> None:
        """Read atomic neural network weights and bias values of many elements.

        Read all atomic neural network weight and bias files found under the
        specified path. The selection may be constrained by additional keywords.

        Parameters
        ----------
        path : str, _default_ '.'
            Data will be read from all weight files found under the given
            path.
        elements : List[str]
            A selection of chemical symbols for which the weights under `path`
            will be read.
        prefix : str
            The filename prefix of weight files under `path`.
        suffix : str
            The filename suffix of weight files under `path`.
        """
        # If no elements were supplied, find all the element weights files at
        # the given path.
        if elements is None:
            elements = []
            for file in os.listdir(path):
                if file.startswith(prefix):
                    # Transform the atomic numbers into the chemical symbol.
                    element = chemical_symbols[int(file.split('.')[1])]
                    elements.append(element)

        # Read in all desired element neural network weights.
        for element in elements:

            # Obtain the atomic number of the element and the path to the file.
            number = atomic_numbers[element]
            fullpath = os.path.join(path, f'{prefix}.{number:03d}.{suffix}')

            # Store the weights as a np.ndarray.
            self.data[element] = np.genfromtxt(fullpath, usecols=(0))

    def write(
        self,
        path: str = '.',
        elements: Optional[List[str]] = None,
        prefix: str = 'weights',
        suffix: str = 'data'
    ) -> None:
        """Write atomic neural network weights and biases for one element.

        Parameters
        ----------
        path : str
            Data will be read from all weight files found under the given
            path.
        elements : List[str]
            A selection of chemical symbols for which the weights under `path`
            will be read.
        prefix : str
            The filename prefix of weight files under `path`.
        suffix : str
            The filename suffix of weight files under `path`.
        """
        for element, weights in self.data.items():
            # Skip over unspecified elements, if given.
            if elements is not None and element not in elements:
                continue

            # Write the data to file.
            number = atomic_numbers[element]
            element_path = os.path.join(path, f'{prefix}.{number:03d}.{suffix}')
            np.savetxt(element_path, weights, fmt='%.10f')


class RunnerStructureSymmetryFunctionValues(ElementStorageMixin):
    """Storage container for the symmetry function values of one structure."""

    def __init__(
        self,
        energy_total: float = np.NaN,
        energy_short: float = np.NaN,
        energy_elec: float = np.NaN,
        charge: float = np.NaN,
    ) -> None:
        """Initialize the object.

        Parameters
        ----------
        energy_total : float
            The total energy of the structure. Unit: Hartree.
        energy_short : float
            The short-range part of the energy of the structure. Unit: Hartree.
        energy_elec : float
            The electrostatic contribution to the energy of the structure.
            Unit: Hartree.
        charge : float
            The total charge of the structure. Unit: electron charge.
        """
        # Initialize the base class. This will create the main data storage.
        super().__init__()

        # Save additional non-element-specific parameters.
        # Each parameter is stored in one large array for all structures.
        self.energy_total = energy_total
        self.energy_short = energy_short
        self.energy_elec = energy_elec
        self.charge = charge

    def __repr__(self) -> str:
        """Show a string representation of the object."""
        return f'{self.__class__.__name__}(n_atoms={len(self)})'

    def by_atoms(self) -> List[Tuple[str, np.ndarray]]:
        """Expand dictionary of element symmetry functions into atom tuples."""
        data_tuples = []
        index = []

        for element, element_sfvalues in self.data.items():
            index += list(element_sfvalues[:, 0])
            sfvalues_list: List[np.ndarray] = list(element_sfvalues[:, 1:])

            for atom_sfvalues in sfvalues_list:
                data_tuples.append((element, atom_sfvalues))

        return [x for _, x in sorted(zip(index, data_tuples))]

    @property
    def plot(self) -> RunnerStructureSymmetryFunctionValuesPlots:
        """Create a plotting interface."""
        return RunnerStructureSymmetryFunctionValuesPlots(self.data)


class RunnerSymmetryFunctionValues:
    """Storage container for RuNNer symmetry function values.

    In RuNNer Mode 1, many-body symmetry functions (SFs) are calculated aiming
    to describe the chemical environment of every atom. As a result, every atom
    is characterized by a vector of SF values. These SF vectors always have the
    same size for each kind of element in the system.

    In the RuNNer Fortran code, this information is written to two files,
    'function.data' (for train set structures) and 'testing.data' (for test set
    structures). The files also contain additional information for each
    structure (all atomic units): the total energy, the short-range energy,
    the electrostatic energy, and the charge.
    """

    def __init__(self, infile: Optional[Union[str, TextIO]] = None) -> None:
        """Initialize the object.

        Parameters
        ----------
        infile : str or TextIO
            If given, data will be read from this fileobj upon initialization.
        """
        # Initialize the base class. This will create the main data storage.
        super().__init__()

        self.data: List[RunnerStructureSymmetryFunctionValues] = []

        # If given, read data from `infile`.
        if infile is not None:
            self.read(infile)

    def __len__(self) -> int:
        """Show the number of structures in storage."""
        return len(self.data)

    def __getitem__(self, index: int) -> RunnerStructureSymmetryFunctionValues:
        """Get the data for one structure at `index` in storage."""
        return self.data[index]

    def __repr__(self) -> str:
        """Show a string representation of the object."""
        return f'{self.__class__.__name__}(n_structures={len(self)})'

    def __add__(
        self,
        blob: 'RunnerSymmetryFunctionValues'
    ) -> 'RunnerSymmetryFunctionValues':
        """Add a blob of symmetry function values to storage."""
        self.append(blob)
        return self

    def sort(self, index: List[int]) -> None:
        """Sort the structures in storage by `index`."""
        self.data = [x for _, x in sorted(zip(index, self.data))]

    def append(self, blob: 'RunnerSymmetryFunctionValues') -> None:
        """Append another blob of symmetry function values to storage."""
        for structure in blob.data:
            self.data.append(structure)

    @reader
    def read(self, infile: Union[str, TextIO]) -> None:
        """Read symmetry function values from `infile`."""
        allsfvalues: Dict[str, List[List[float]]] = {}
        idx_atom = 0
        for line in infile:
            spline = line.split()

            # Line of length 1 marks a new structure and holds the # of atoms.
            if len(spline) == 1:
                idx_atom = 0
                allsfvalues = {}
                structure = RunnerStructureSymmetryFunctionValues()

            # Line of length 4 marks the end of a structure.
            elif len(spline) == 4:
                structure.charge = float(spline[0])
                structure.energy_total = float(spline[1])
                structure.energy_short = float(spline[2])
                structure.energy_elec = float(spline[3])

                for element, data in allsfvalues.items():
                    structure.data[element] = np.array(data)

                self.data.append(structure)

            # All other lines hold symmetry function values.
            else:
                # Store the symmetry function values in the element dictionary.
                element = chemical_symbols[int(spline[0])]
                sfvalues = [float(i) for i in spline[1:]]

                if element not in allsfvalues:
                    allsfvalues[element] = []

                allsfvalues[element].append([float(idx_atom)] + sfvalues)
                idx_atom += 1

    @writer
    def write(
        self,
        outfile: TextIO,
        index: Union[int, slice, List[int]] = slice(0, None),
        fmt: str = '16.10f'
    ) -> None:
        """Write symmetry function scaling data."""
        # Retrieve the data.
        images: List[RunnerStructureSymmetryFunctionValues] = self.data

        # Filter the images which should be printed according to `index`.
        if isinstance(index, slice):
            images = images[index]
        elif isinstance(index, int):
            images = [images[index]]
        else:
            images = [images[i] for i in index]

        for image in images:
            # Start a structure by writing the number of atoms.
            outfile.write(f'{len(image):6}\n')

            # Write one line for each atom containing the atomic number followed
            # by the symmetry function values.
            for element, sfvalues in image.by_atoms():
                number = atomic_numbers[element]

                outfile.write(f'{number:3}')
                outfile.write(''.join(f'{i:{fmt}}' for i in sfvalues))
                outfile.write('\n')

            # End a structure by writing charge and energy information.
            outfile.write(f'{image.charge:{fmt}} {image.energy_total:{fmt}} '
                          + f'{image.energy_short:{fmt}} '
                          + f'{image.energy_elec:{fmt}}\n')

    @property
    def plot(self) -> RunnerSymmetryFunctionValuesPlots:
        """Create a plotting interface."""
        return RunnerSymmetryFunctionValuesPlots(self.data)


class RunnerFitResults:
    """Storage container for RuNNer training results.

    RuNNer Mode 2 generates a neural network potential in an iterative training
    process typical when working with neural networks. The information generated
    in course of this procedure enables the evaluation of the potential quality.
    This class stores typical quality markers to facilitate training process
    analysis:

    epochs : int
        The number of epochs in the training process.
    rmse_energy : Dict[str, float]
        Root mean square error of the total energy. Possible keys are 'train',
        for the RMSE in the train set, and 'test', for the RMSE in the test set.
    rmse_force : Dict[str, float]
        Root mean square error of the atomic forces. See `rmse_energy`.
    rmse_charge : Dict[str, float]
        Root mean square error of the atomic charges. See `rmse_energy`.
    opt_rmse_epoch : int, optional, _default_ `None`
        The number of the epoch were the best fit was obtained.
    units : Dict[str, str]
        The units of the energy and force RMSE.
    """

    def __init__(self, infile: Optional[Union[str, TextIO]] = None) -> None:
        """Initialize the object.

        Parameters
        ----------
        infile : str or TextIO
            If given, data will be read from this fileobj upon initialization.
        """
        # Helper type hint definition for code brevity.
        RMSEDict = Dict[str, List[Optional[float]]]

        self.epochs: List[Optional[int]] = []
        self.rmse_energy: RMSEDict = {'train': [], 'test': []}
        self.rmse_forces: RMSEDict = {'train': [], 'test': []}
        self.rmse_charge: RMSEDict = {'train': [], 'test': []}
        self.opt_rmse_epoch: Optional[int] = None
        self.units: Dict[str, str] = {'rmse_energy': '', 'rmse_force': ''}

        # If given, read data from `infile`.
        if infile is not None:
            self.read(infile)

    def __repr__(self) -> str:
        """Show a string representation of the object."""
        num_epochs = len(self.epochs)
        return f'{self.__class__.__name__}(num_epochs={num_epochs}, ' \
               + f'best epoch={self.opt_rmse_epoch})'

    @reader
    def read(self, infile: Union[str, TextIO]) -> None:
        """Read RuNNer Mode 2 results.

        Parameters
        ----------
        infile : str or TextIO
            Data will be read from this fileobj.
        """
        for line in infile:
            data = line.split()

            # Read the RMSEs of energies, forces and charges, and the
            # corresponding epochs.
            if line.strip().startswith('ENERGY'):
                if '*****' in line:
                    epoch, rmse_train, rmse_test = None, None, None
                else:
                    epoch = int(data[1])
                    rmse_train, rmse_test = float(data[2]), float(data[3])

                self.epochs.append(epoch)
                self.rmse_energy['train'].append(rmse_train)
                self.rmse_energy['test'].append(rmse_test)

            elif line.strip().startswith('FORCES'):
                if '*****' in line:
                    rmse_train, rmse_test = None, None
                else:
                    rmse_train, rmse_test = float(data[2]), float(data[3])

                self.rmse_forces['train'].append(rmse_train)
                self.rmse_forces['test'].append(rmse_test)

            elif line.strip().startswith('CHARGE'):
                rmse_train, rmse_test = float(data[2]), float(data[3])
                self.rmse_charge['train'].append(rmse_train)
                self.rmse_charge['test'].append(rmse_test)

            # Read the fitting units, indicated by the heading 'RMSEs'.
            if 'RMSEs' in line:
                # Use regular expressions to find the units. All units
                # conveniently start with two letters ('Ha', or 'eV'), followed
                # by a slash and some more letters (e.g. 'Bohr', or 'atom').
                units: List[str] = re.findall(r'\w{2}/\w+', line)
                self.units['rmse_energy'] = units[0]
                self.units['rmse_force'] = units[1]

            # Read in the epoch where the best fit was obtained.
            if 'Best short range fit has been obtained in epoch' in line:
                self.opt_rmse_epoch = int(data[-1])

            # Explicitely handle the special case that the fit did not yield any
            # improvement. This also means that no weights were written.
            if 'No improvement' in line:
                self.opt_rmse_epoch = None

    # Table returns many different pieces of information, therefore many
    # variables are needed.
    # pylint: disable=too-many-locals
    def table(self) -> None:
        """Print a tabular summary of the fitting results."""
        # Get the results of the fit.
        energy_train = self.rmse_energy['train']
        energy_test = self.rmse_energy['test']
        force_train = self.rmse_forces['train']
        force_test = self.rmse_forces['test']
        unit_energy = self.units['rmse_energy']
        unit_force = self.units['rmse_force']
        epochs = self.epochs

        if len(force_train) != len(energy_train):
            force_train = [np.nan for i in energy_train]
            force_test = [np.nan for i in energy_test]

        # Build the table header.
        colhead_energy = 'RMSE(E) / ' + unit_energy
        colhead_force = 'RMSE(F) / ' + unit_force
        header = (f"Epoch | {colhead_energy:^18} | {colhead_force:^18} |")

        # Build the table subheader.
        subtraintest = f"{'Train':^8} | {'Test':^7}"
        subheader = f"{'':5s} | {subtraintest} | {subtraintest} |"

        # Print header, subheader, and their separator lines.
        print(header)
        print('=' * len(header))

        print(subheader)
        print('-' * len(subheader))

        # Print the results of each epoch.
        results = zip(epochs, energy_train, energy_test, force_train,
                      force_test)
        for epoch, e_train, e_test, f_train, f_test in results:
            print(f'{epoch:5d} '
                  + f'| {e_train:^9.4f}'
                  + f'| {e_test:^8.4f}'
                  + f'| {f_train:^9.4f}'
                  + f'| {f_test:^8.4f}|',
                  end='')

            if epoch == self.opt_rmse_epoch:
                print(' <- Best Epoch')
            else:
                print('')

    @property
    def plot(self) -> RunnerFitResultsPlots:
        """Create a plotting interface."""
        return RunnerFitResultsPlots(self.epochs, self.rmse_energy,
                                     self.rmse_forces, self.rmse_charge,
                                     self.opt_rmse_epoch, self.units)


class RunnerSplitTrainTest:
    """Storage container for the split between train and test set in RuNNer.

    In RuNNer Mode 1, the dataset presented to the program is separated into
    a training portion, presented to the neural networks for iteratively
    improving the weights, and a testing portion which is only used for
    evaluation.
    This class stores this data and enables to read it from Mode 1 output files.
    """

    def __init__(self, infile: Optional[Union[str, TextIO]] = None) -> None:
        """Initialize the object.

        Parameters
        ----------
        infile : str or TextIO
            If provided, data will be read from this fileobj.
        """
        self.train: List[int] = []
        self.test: List[int] = []

        # If given, read data from `infile`.
        if infile is not None:
            self.read(infile)

    def __repr__(self) -> str:
        """Show a string representation of the object."""
        return f'{self.__class__.__name__}(n_train={len(self.train)}, ' \
               + f'n_test={len(self.test)})'

    @reader
    def read(self, infile: Union[str, TextIO]) -> None:
        """Read RuNNer splitting data.

        Parameters
        ----------
        infile : str or TextIO
            Data will be read from this fileobj. The file should contain the
            stdout from a RuNNer Mode 1 run.
        """
        self.train = []
        self.test = []

        for line in infile:
            if 'Point is used for' in line:
                # In Python, indices start at 0, therefore we subtract 1.
                point_idx = int(line.split()[0]) - 1
                split_type = line.split()[5]

                if split_type == 'training':
                    self.train.append(point_idx)
                elif split_type == 'testing':
                    self.test.append(point_idx)

    @property
    def plot(self) -> RunnerSplitTrainTestPlots:
        """Create a plotting interface."""
        return RunnerSplitTrainTestPlots(self.train, self.test)

# Originally inherited from TypedDict, but this was removed for now to retain
# backwards compatibility with Python 3.6 and 3.7.
# class RunnerResults(TypedDict, total=False)
#     """Type hints for RuNNer results dictionaries."""
#
#     fitresults: RunnerFitResults
#     sfvalues: RunnerSymmetryFunctionValues
#     weights: RunnerWeights
#     scaling: RunnerScaling
#     splittraintest: RunnerSplitTrainTest
#     energy: Union[float, NDArray]
#     forces: NDArray
