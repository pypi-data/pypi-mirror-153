"""Implementation of readers and writers for RuNNer structural data.

This module provides the part of the Python I/O-interface to the RuNNer Neural
Network Energy Representation (RuNNer) that is concerned with structural
information about chemical configurations.
"""

from typing import Optional, Union, Iterator, Tuple, List, TextIO

import numpy as np

from ase.atoms import Atoms
from ase.utils import reader, writer
from ase.units import Hartree, Bohr
from ase.data import atomic_numbers

from runnerase.singlepoint import RunnerSinglePointCalculator


# A lot of structural information has to be stored.
# pylint: disable=too-many-instance-attributes
class TempAtoms:
    """Container for storing data about one atomic structure.

    This class is intended for fast I/O of structural data. It is required as
    the builtin ASE `Atoms` and `Atom` classes are a bottleneck for large data
    files. This is mostly because adding an `Atom` to an `Atoms` object over
    and over again comes with a lot of overhead because the attached arrays
    have to be checked and copied.
    In constrast, it is very efficient to store atomic positions, symbols, etc.
    in long lists and simply create one ASE `Atoms` object once all atoms have
    been collected. In summary, `TempAtoms` is simply a container to hold all
    these lists in one convenient place.
    """

    def __init__(self, atoms: Optional[Atoms] = None) -> None:
        """Initialize the object."""
        self.positions: List[List[float]] = []
        self.symbols: List[str] = []
        self.charges: List[float] = []
        self.magmoms: List[float] = []

        self.cell: List[List[float]] = []

        self.energy: float = np.NaN
        self.totalcharge: float = np.NaN
        self.forces: List[List[float]] = []

        # If given, read values from a given ASE Atoms object.
        if atoms is not None:
            self.from_aseatoms(atoms)

    def __iter__(
        self
    ) -> Iterator[Tuple[List[float], str, float, float, List[float]]]:
        """Iterate over tuples of information for each atom in storage."""
        for idx, xyz in enumerate(self.positions):
            element = self.symbols[idx]
            charge = self.charges[idx]
            atomenergy = self.magmoms[idx]
            force_xyz = self.forces[idx]

            yield (xyz, element, charge, atomenergy, force_xyz)

    @property
    def pbc(self) -> List[bool]:
        """Show the periodicity of the object along the Cartesian axes."""
        pbc = [False, False, False]
        for idx, vector in enumerate(self.cell):
            if len(vector) == 3:
                pbc[idx] = True

        return pbc

    def to_aseatoms(self) -> Atoms:
        """Convert the object to an ASE Atoms object."""
        atoms = Atoms(
            positions=self.positions,
            symbols=self.symbols,
            pbc=self.pbc
        )

        # Add the unit cell information.
        if any(self.pbc):
            atoms.set_cell(self.cell)

        atoms.set_initial_charges(self.charges)
        atoms.set_initial_magnetic_moments(self.magmoms)

        calc = RunnerSinglePointCalculator(
            atoms,
            energy=self.energy,
            forces=self.forces,
            totalcharge=self.totalcharge
        )

        # The calculator has to be attached at the very end,
        # otherwise, it is overwritten by `set_cell()`, `set_pbc()`, ...
        atoms.calc = calc

        return atoms

    def from_aseatoms(self, atoms: Atoms) -> None:
        """Convert an ASE Atoms object to this class."""
        self.positions = list(atoms.positions)
        self.symbols = list(atoms.symbols)
        self.charges = list(atoms.get_initial_charges())
        self.magmoms = list(atoms.get_initial_magnetic_moments())

        if any(atoms.pbc):
            self.cell = atoms.cell

        if atoms.calc is not None:
            self.energy = atoms.get_potential_energy()
            self.forces = list(atoms.get_forces())
            if isinstance(atoms.calc, RunnerSinglePointCalculator):
                self.totalcharge = atoms.calc.get_property('totalcharge')
            else:
                self.totalcharge = np.sum(atoms.get_initial_charges())
        else:
            self.energy = 0.0
            self.forces = [[0.0, 0.0, 0.0] for i in self.positions]
            self.totalcharge = 0.0

    def convert(self, input_units: str, output_units: str) -> None:
        """Convert all data from `input_units` to `output_units`."""
        # Transform lists into numpy arrays for faster processing.

        if input_units == output_units:
            pass

        elif input_units == 'atomic' and output_units == 'si':
            self.positions = [[i * Bohr for i in xyz] for xyz in self.positions]
            self.cell = [[i * Bohr for i in xyz] for xyz in self.cell]
            self.energy *= Hartree
            self.forces = [[i * Hartree / Bohr for i in xyz]
                           for xyz in self.forces]

        elif input_units == 'si' and output_units == 'atomic':
            self.positions = [[i / Bohr for i in xyz] for xyz in self.positions]
            self.cell = [[i / Bohr for i in xyz] for xyz in self.cell]
            self.energy /= Hartree
            self.forces = [[i / Hartree * Bohr for i in xyz]
                           for xyz in self.forces]


@reader
def read_runnerdata(
    infile: TextIO,
    index: Union[int, slice] = -1,
    input_units: str = 'atomic',
    output_units: str = 'si'
) -> Iterator[Atoms]:
    """Parse all structures within a RuNNer input.data file.

    input.data files contain all structural information needed to train a
    Behler-Parrinello-type neural network potential, e.g. Cart. coordinates,
    atomic forces, and energies. This function reads the file object `infile`
    and returns the slice of structures given by `index`. All structures will
    be converted to SI units by default.

    Parameters
    ----------
    infile : TextIOWrapper
        Python fileobj with the target input.data file.
    index : int or slice
        The slice of structures which should be returned. Returns only the last
        structure by default.
    input_units : str
        The given input units. Can be 'si' or 'atomic'.
    output_units : str
        The desired output units. Can be 'si' or 'atomic'.

    Returns
    -------
    images : Atoms
        All information about the structures within `index` of `infile`,
        including symbols, positions, atomic charges, and cell lattice. Every
        `Atoms` object has a `RunnerSinglePointCalculator` attached with
        additional information on the total energy, atomic forces, and total
        charge.

    References
    ----------
    Detailed information about the RuNNer input.data file format can be found
    in the program's
    [documentation](https://runner.pages.gwdg.de/runner/reference/files/)
    """
    # Container for all images in the file.
    images: List[Atoms] = []

    for line in infile:

        # Jump over blank lines and comments.
        if not line.strip() or line.strip().startswith('#'):
            continue

        # Split the line into the keyword and the arguments.
        keyword, arguments = line.split()[0], line.split()[1:]

        # 'begin' marks the start of a new structure.
        if keyword == 'begin':
            atoms = TempAtoms()

        # Read one atom.
        elif keyword == 'atom':
            xyz = [float(i) for i in arguments[:3]]
            symbol = arguments[3].lower().capitalize()
            charge = float(arguments[4])
            magmom = float(arguments[5])
            force_xyz = [float(i) for i in arguments[6:9]]

            atoms.positions.append(xyz)
            atoms.symbols.append(symbol)
            atoms.charges.append(charge)
            atoms.magmoms.append(magmom)
            atoms.forces.append(force_xyz)

        # Read one cell lattice vector.
        elif keyword == 'lattice':
            atoms.cell.append([float(i) for i in arguments[:3]])

        # Read the total energy of the structure.
        elif keyword == 'energy':
            atoms.energy = float(arguments[0])

        # Read the total charge of the structure.
        elif keyword == 'charge':
            atoms.totalcharge = float(arguments[0])

        # 'end' statement marks the end of a structure.
        elif keyword == 'end':

            # Convert all data to the specified output units.
            atoms.convert(input_units, output_units)

            # Append the structure to the list of all structures.
            aseatoms = atoms.to_aseatoms()
            images.append(aseatoms)

    yield images[index]


@writer
def write_runnerdata(
    outfile: TextIO,
    images: List[Atoms],
    comment: str = '',
    fmt: str = '16.10f',
    input_units: str = 'si'
) -> None:
    """Write series of ASE Atoms to a RuNNer input.data file.

    For further details see the `read_runnerdata` routine.

    Parameters
    ----------
    outfile : TextIOWrapper
        Python fileobj with the target input.data file.
    images : array-like
        List of `Atoms` objects.
    comment : str
        A comment message to be added to each structure.
    fmt : str
        A format specifier for float values.
    input_units : str
        The given input units. Can be 'si' or 'atomic'.

    Raises
    ------
    ValueError : exception
        Raised if the comment line contains newline characters.
    """
    # Preprocess the comment.
    comment = comment.rstrip()
    if '\n' in comment:
        raise ValueError('Comment line cannot contain line breaks.')

    for atoms in images:

        # Transform into a TempAtoms object.
        tempatoms = TempAtoms(atoms)

        # Convert, if necessary.
        tempatoms.convert(input_units=input_units, output_units='atomic')

        # Begin writing this structure to file.
        outfile.write('begin\n')

        if comment != '':
            outfile.write(f'comment {comment}\n')

        # Write lattice vectors if the structure is marked as periodic.
        if any(tempatoms.pbc):
            for vector in tempatoms.cell:
                outfile.write(f'lattice {vector[0]:{fmt}} {vector[1]:{fmt}} '
                              f'{vector[2]:{fmt}}\n')

        for xyz, element, charge, atomenergy, force_xyz in tempatoms:
            outfile.write(f'atom {xyz[0]:{fmt}} {xyz[1]:{fmt}} {xyz[2]:{fmt}} '
                          f'{element:2s} {charge:{fmt}} {atomenergy:{fmt}} '
                          f'{force_xyz[0]:{fmt}} {force_xyz[1]:{fmt}} '
                          f'{force_xyz[2]:{fmt}}\n')

        # Write the energy and total charge, then end this structure.
        outfile.write(f'energy {tempatoms.energy:{fmt}}\n')
        outfile.write(f'charge {tempatoms.totalcharge:{fmt}}\n')
        outfile.write('end\n')


@writer
def write_trainteststruct(
    outfile: TextIO,
    images: Union[Atoms, List[Atoms]],
    index: Union[int, slice] = slice(0, None),
    fmt: str = '16.10f',
    input_units: str = 'si'
) -> None:
    """Write a series of ASE Atoms to trainstruct.data / teststruct.data format.

    Parameters
    ----------
    outfile : TextIOWrapper
        The fileobj where the data will be written.
    images : List[Atoms]
        List of ASE `Atoms` objects.
    index : int or slice, _default_ `slice(0, None)`
        Only the selection of `images` given by `index` will be written.
    fmt : str, _default_ '16.10f'
        A format specifier for float values.
    input_units : str, _default_ 'si'
        The units within `images`. Can be 'si' or 'atomic'. All data will
        automatically be converted to atomic units.
    """
    # Filter the images which should be printed according to `index`.
    if isinstance(index, (int, slice)):
        images = images[index]
    else:
        images = [images[i] for i in index]

    for idx_atoms, atoms in enumerate(images):

        # Transform into a TempAtoms object and do unit conversion, if needed.
        tempatoms = TempAtoms(atoms)
        tempatoms.convert(input_units=input_units, output_units='atomic')

        # Write structure index. White space at the end is important.
        outfile.write(f'{idx_atoms + 1:8} ')

        # Write lattice vectors for periodic structures.
        if any(tempatoms.pbc):
            outfile.write('T\n')
            for vector in tempatoms.cell:
                outfile.write(f'{vector[0]:{fmt}} {vector[1]:{fmt}} '
                              f'{vector[2]:{fmt}} \n')
        else:
            outfile.write('F\n')

        # Write atomic data to file.
        for xyz, element, charge, atomenergy, force_xyz in tempatoms:
            atomic_number = atomic_numbers[element]
            outfile.write(f'{atomic_number:4d} {xyz[0]:{fmt}} {xyz[1]:{fmt}} '
                          f'{xyz[2]:{fmt}} '
                          f'{charge:{fmt}} {atomenergy:{fmt}} '
                          f'{force_xyz[0]:{fmt}} {force_xyz[1]:{fmt}} '
                          f'{force_xyz[2]:{fmt}}\n')


@reader
def read_traintestpoints(
    infile: TextIO,
    input_units: str = 'atomic',
    output_units: str = 'si'
) -> np.ndarray:
    """Read RuNNer trainpoint.XXXXXX.out / testpoint.XXXXXX.out.

    Parameters
    ----------
    infile : TextIOWrapper
        The fileobj where the data will be read.
    input_units : str, _default_ 'atomic'
        The units within `images`. Can be 'si' or 'atomic'. All data will
        automatically be converted to `output_units`.
    output_units : str, _default_ 'si'
        The desired units in `data`. Can be 'si' or 'atomic'.

    Returns
    -------
    data : np.ndarray
        An array holding the following columns: image ID, number of atoms,
        reference energy, neural network energy, difference between ref. and
        neural network energy.
    """
    # The first row holds the column names.
    data: np.ndarray = np.loadtxt(infile, skiprows=1)

    # Unit conversion.
    if input_units == 'atomic' and output_units == 'si':
        data[:, 2:] *= Hartree

    elif input_units == 'si' and output_units == 'atomic':
        data[:, 2:] /= Hartree

    return data


@reader
def read_traintestforces(
    infile: TextIO,
    input_units: str = 'atomic',
    output_units: str = 'si'
) -> np.ndarray:
    """Read RuNNer trainforces.XXXXXX.our / testpoint.XXXXXX.out.

    Parameters
    ----------
    infile : TextIOWrapper
        The fileobj where the data will be read.
    input_units : str, _default_ 'atomic'
        The units within `images`. Can be 'si' or 'atomic'. All data will
        automatically be converted to `output_units`.
    output_units : str, _default_ 'si'
        The desired units in `data`. Can be 'si' or 'atomic'.

    Returns
    -------
    data : np.ndarray
        An array holding the following columns: image ID, atom ID, reference
        force x, reference force y, reference force z, neural network force x,
        neural network force y, neural network force z.
    """
    # The first row holds the column names.
    data: np.ndarray = np.loadtxt(infile, skiprows=1)

    # Unit conversion.
    if input_units == 'atomic' and output_units == 'si':
        data[:, 2:] *= Hartree * Bohr

    elif input_units == 'si' and output_units == 'atomic':
        data[:, 2:] /= Hartree * Bohr

    return data


@writer
def write_traintestforces(
    outfile: TextIO,
    images: Union[Atoms, List[Atoms]],
    index: Union[int, slice, List[int]] = slice(0, None),
    fmt: str = '16.10f',
    input_units: str = 'si'
) -> None:
    """Write a series of ASE Atoms to trainforces.data / testforces.data format.

    Parameters
    ----------
    outfile : TextIOWrapper
        The fileobj where the data will be written.
    images : List[Atoms]
        List of ASE `Atoms` objects.
    index : int or slice, _default_ `slice(0, None)`
        Only the selection of `images` given by `index` will be written.
    fmt : str, _default_ '16.10f'
        A format specifier for float values.
    input_units : str, _default_ 'si'
        The units within `images`. Can be 'si' or 'atomic'. All data will
        automatically be converted to atomic units.
    """
    # Filter the images which should be printed according to `index`.
    if isinstance(index, (int, slice)):
        images = images[index]
    else:
        images = [images[i] for i in index]

    for idx_atoms, atoms in enumerate(images):

        # Transform into a TempAtoms object and do unit conversion, if needed.
        tempatoms = TempAtoms(atoms)
        tempatoms.convert(input_units=input_units, output_units='atomic')

        # Write structure index. White space at the end is important.
        outfile.write(f'{idx_atoms + 1:8}\n')

        # Write atomic data to file.
        for _, _, _, _, force_xyz in tempatoms:
            outfile.write(f'{force_xyz[0]:{fmt}} {force_xyz[1]:{fmt}} '
                          f'{force_xyz[2]:{fmt}}\n')
