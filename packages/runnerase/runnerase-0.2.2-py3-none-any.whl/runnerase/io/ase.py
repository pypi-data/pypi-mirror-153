"""Read and write routines required by the `Runner` calculator.

This module provides all I/O routines directly required or called by the
`Runner` calculator.
"""

from typing import Optional, Union, Tuple, List, Dict, TextIO

import os
import numpy as np

from ase.io import read as aseread
from ase.io import write as asewrite
from ase.atoms import Atoms
from ase.calculators.calculator import Parameters
from ase.io.formats import string2index

from runnerase.storageclasses import (RunnerSplitTrainTest, RunnerWeights,
                                      RunnerSymmetryFunctionValues,
                                      RunnerScaling)
from runnerase.symmetryfunctions import SymmetryFunctionSet

from runnerase.io.runnerconfig import read_runnerconfig, write_runnerconfig
from runnerase.io.storageclasses import (read_functiontestingdata,
                                         write_functiontestingdata,
                                         read_fitresults,
                                         read_scaling, write_scaling,
                                         read_weights, write_weights,
                                         read_splittraintest)
from runnerase.io.structuredata import (read_runnerdata, write_runnerdata,
                                        write_trainteststruct,
                                        write_traintestforces)

from runnerase.utils import reader, writer


# ASE uses the 'format' argument, so for consistency this is also used here.
# pylint: disable=redefined-builtin
@reader
def read(
    filename: TextIO,
    index: Union[int, slice] = -1,
    format: Optional[str] = None
) -> Union[Atoms, List[Atoms]]:
    """Read structure files into ASE Atoms objects.

    This routine wraps ASE's native `read` routine. It is necessary because,
    as runnerase is an external package, ASE does not know how to read RuNNer
    structure files.

    Parameters
    ----------
    filename : TextIO
        The file from which the structure should be read. If `filename` ends
        in '.data', the file will be treated like a
        RuNNer structure file (input.data file), unless `format` says otherwise.
    index : int or slice
        The index of the images to be read.
    format : str
        The file format of `filename`. Usually ASE can automatically detect
        this. When 'runner' is specified, the file will be treated like a
        RuNNer structure file (input.data file).

    Returns
    -------
    images : Atoms or List[Atoms]
        The ASE atoms objects read from `filename`.
    """
    # Transform `index` as ASE does as well.
    if isinstance(index, str):
        index = string2index(index)

    # Read in the images, either with the `runnerase` functions or calling
    # ASE's `read` routine.
    if (format == 'runner' or
       (format is None and filename.name.endswith('.data'))):
        images = read_runnerdata(filename, index=index)
        return next(images)

    images = aseread(filename, index, format=format)
    return images


# ASE uses the 'format' argument, so for consistency this is also used here.
# pylint: disable=redefined-builtin
@writer
def write(
    filename: TextIO,
    images: Union[Atoms, List[Atoms]],
    format: Optional[str] = None
) -> None:
    """Write ASE Atoms objects to a file.

    This routine wraps ASE's native `write` routine. It is necessary because,
    as runnerase is an external package, ASE does not know how to write RuNNer
    structure files.

    Parameters
    ----------
    filename : TextIO
        The file to which `images` will be written.
    images : Atoms or List[Atoms]
        The images to be written.
    format : str
        The file format of `filename`. Usually ASE can automatically detect
        this.
    """
    if format == 'runner':
        write_runnerdata(filename, images)
    else:
        asewrite(filename, images, format=format)


def read_runnerase(
    label: str
) -> Tuple[Union[Atoms, List[Atoms], None], Parameters]:
    """Read structure and parameter options from a previous calculation.

    Parameters
    ----------
    label : str
        The ASE-internal calculation label, i.e. the prefix of the ASE
        parameters file.

    Returns
    -------
    atoms : ASE Atoms or List[Atoms]
        A list of all structures associated with the given calculation.
    parameters : Parameters
        A dictionary containing all RuNNer settings of the calculation.
    """
    # Extract the directory path.
    directory = ''.join(label.split('/')[:-1])

    # Join the paths to all relevant files.
    inputdata_path = os.path.join(directory, 'input.data')
    aseparams_path = f'{label}.ase'
    inputnn_path = os.path.join(directory, 'input.nn')

    # Read structural information from the input.data file.
    if os.path.exists(inputdata_path):
        atoms: Optional[Union[Atoms, List[Atoms]]] = read(
            inputdata_path, ':', format='runner'
        )
    else:
        atoms = None

    # Read RuNNer options first from the ASE parameter file and second from
    # the input.nn file.
    if os.path.exists(aseparams_path):
        parameters: Parameters = Parameters.read(aseparams_path)
        if 'symfunction_short' in parameters:
            parameters['symfunction_short'] = SymmetryFunctionSet(
                parameters['symfunction_short']
            )

    elif os.path.exists(inputnn_path):
        parameters = read_runnerconfig(inputnn_path)

    else:
        parameters = Parameters()

    return atoms, parameters


# RuNNer operates in several modi, all of which take different arguments.
# For clarity it is intentionally chosen to pass these explicitely, even though
# it increases the number of parameters.
# pylint: disable=too-many-arguments
def write_all_inputs(
    atoms: Union[Atoms, List[Atoms]],
    parameters: Parameters,
    label: str = 'runner',
    directory: str = '.',
    scaling: Optional[RunnerScaling] = None,
    weights: Optional[RunnerWeights] = None,
    splittraintest: Optional[RunnerSplitTrainTest] = None,
    sfvalues: Optional[RunnerSymmetryFunctionValues] = None
) -> None:
    """Write all necessary input files for performing a RuNNer calculation."""
    # All functions take a list of atoms objects as input.
    if not isinstance(atoms, list):
        atoms = [atoms]

    # Write all parameters to a .ase parameters file.
    parameters.write(f'{label}.ase')

    # Write the input.data file containing all structures.
    path = os.path.join(directory, 'input.data')
    write_runnerdata(path, atoms)

    # Write the input.nn file containing all parameters.
    path = os.path.join(directory, 'input.nn')
    write_runnerconfig(path, parameters)

    # Write scaling data.
    if scaling is not None:
        path = os.path.join(directory, 'scaling.data')
        write_scaling(path, scaling)

    # Write weights data.
    if weights is not None:
        write_weights(weights, path=directory)

    if splittraintest is not None:
        path = os.path.join(directory, 'function.data')
        write_functiontestingdata(path, sfvalues, splittraintest.train)

        path = os.path.join(directory, 'testing.data')
        write_functiontestingdata(path, sfvalues, splittraintest.test)

        path = os.path.join(directory, 'trainstruct.data')
        write_trainteststruct(path, atoms, splittraintest.train)

        path = os.path.join(directory, 'teststruct.data')
        write_trainteststruct(path, atoms, splittraintest.test)

        path = os.path.join(directory, 'trainforces.data')
        write_traintestforces(path, atoms, splittraintest.train)

        path = os.path.join(directory, 'testforces.data')
        write_traintestforces(path, atoms, splittraintest.test)


def read_results_mode1(label: str, directory: str) -> Dict[str, object]:
    """Read all results of RuNNer Mode 1.

    Parameters
    ----------
    label : str
        The ASE calculator label of the calculation. Typically this is the
        joined path of the `directory` and the .ase parameter file prefix.
    directory : str
        The path of the directory which holds the calculation files.

    Returns
    -------
    dict : RunnerResults
        A dictionary with two entries

            - sfvalues : RunnerSymmetryFunctionValues
                The symmetry function values.
            - splittraintest : RunnerSplitTrainTest
                The split between train and test set.
    """
    sfvalues_train = read_functiontestingdata(f'{directory}/function.data')
    sfvalues_test = read_functiontestingdata(f'{directory}/testing.data')
    splittraintest = read_splittraintest(f'{label}.out')

    # Store only one symmetry function value container.
    sfvalues = sfvalues_train + sfvalues_test
    sfvalues.sort(splittraintest.train + splittraintest.test)

    return {'sfvalues': sfvalues, 'splittraintest': splittraintest}


def read_results_mode2(label: str, directory: str) -> Dict[str, object]:
    """Read all results of RuNNer Mode 2.

    Parameters
    ----------
    label : str
        The ASE calculator label of the calculation. Typically this is the
        joined path of the `directory` and the .ase parameter file prefix.
    directory : str
        The path of the directory which holds the calculation files.

    Returns
    -------
    dict : RunnerResults

        A dictionary with three entries
            - fitresults : RunnerFitResults
                Details about the fitting process.
            - weights : RunnerWeights
                The atomic neural network weights and bias values.
            - scaling : RunnerScaling
                The symmetry function scaling data.
    """
    # Store training results, weights, and symmetry function scaling data.
    # Mode 2 writes best weights to the optweights.XXX.out file.
    fitresults = read_fitresults(f'{label}.out')
    weights = read_weights(path=directory, prefix='optweights', suffix='out')
    scaling = read_scaling(f'{directory}/scaling.data')

    return {'fitresults': fitresults, 'weights': weights, 'scaling': scaling}


def read_results_mode3(directory: str) -> Dict[str, object]:
    """Read all results of RuNNer Mode 3.

    Parameters
    ----------
    directory : str
        The path of the directory which holds the calculation files.

    Returns
    -------
    dict : RunnerResults

        A dictionary with two entries
            - energy : float or np.ndarray
                The total energy of all structures. In case of a single
                structure only one float value is returned.
            - forces : np.ndarray
                The atomic forces of all structures.
    """
    # Read predicted structures from the output.data file.
    # `read` automatically converts all properties to SI units.
    path = f'{directory}/output.data'
    pred_structures = read(path, ':', format='runner')
    energies = np.array([i.get_potential_energy() for i in pred_structures])
    forces = np.array([i.get_forces() for i in pred_structures])

    # For just one structure, flatten the energy and force arrays.
    if forces.shape[0] == 1:
        forces = forces[0, :, :]

    if energies.shape[0] == 1:
        return {'energy': float(energies[0]), 'forces': forces}

    return {'energy': energies, 'forces': forces}
