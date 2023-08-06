"""Implementation of classes for storing RuNNer parameters and results.

This module provides custom classes for storing the different types of data
produced and/or read by RuNNer.

Attributes
----------
SymmetryFunction : object
    Storage container for a single symmetry function.
SymmetryFunctionSet : object
    Storage container for a collection of symmetry functions.
get_element_groups : utility function
    Create a list of element pairs and triples from a list of chemical symbols.
get_minimum_distances : utility function
    Find the minimum distance for each pair of elements in a list of images.
"""

from typing import Optional, Dict, List, Union, Tuple, Iterator

from itertools import combinations_with_replacement, product

import numpy as np

from ase.geometry import get_distances
from ase.atoms import Atoms
from ase.units import Bohr

from runnerase.utils import get_elements

from runnerase.plot import SymmetryFunctionSetPlots

# Custom type specification for lists of symmetry function parameters. Can be
# two kinds of tuples, depending on whether it is a radial or an angular
# symmetry function.
SFListType = Union[Tuple[str, int, str, float, float, float],
                   Tuple[str, int, str, str, float, float, float, float]]


class SymmetryFunction:
    """Generic class for one single symmetry function."""

    # Symmetry functions have a few arguments which need to be given upon
    # class initialization.
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        sftype: Optional[int] = None,
        cutoff: Optional[float] = None,
        elements: Optional[List[str]] = None,
        coefficients: Optional[List[float]] = None,
        sflist: Optional[SFListType] = None
    ) -> None:
        """Initialize the class.

        Parameters
        ----------
        sftype : int
            The type of symmetry function.
        cutoff : float
            The symmetry function cutoff radius in units of Bohr.
        elements : List[str]
            Symbols of the elements described by this symmetry function.
            The first entry of the list gives the central atom, while all
            following entries stand for neighbor atoms. Usually, the number of
            neighbors should be 1 (= radial symfun) or 2 (= angular symfun)
        coefficients : List[float]
            The coefficients of this symmetry function. The number of necessary
            coefficients depends on the `sftype` as documented in the RuNNer
            manual.
        sflist : SFListType
            A symmetry function in list form. When supplied, the list
            will be parsed into an object of this class.
        """
        self.sftype = sftype
        self.cutoff = cutoff
        self.elements = elements
        self.coefficients = coefficients

        if sflist is not None:
            self.from_list(sflist)

    def __repr__(self) -> str:
        """Show a clean summary of the class object and its contents."""
        return f'{self.__class__.__name__}(sftype={self.sftype}, ' \
               + f'cutoff={self.cutoff}, ' \
               + f'elements={self.elements}, coefficients={self.coefficients})'

    def __add__(
        self,
        blob: Union['SymmetryFunctionSet', 'SymmetryFunction']
    ) -> Union['SymmetryFunctionSet', 'SymmetryFunction']:
        """Define addition behaviour.

        `SymmetryFunction`s can be treated like mathematical objects. A SF may
        be added to another SF which will return a `SymmetryFunctionSet`. A SF
        may also be added to an existing `SymmetryFunctionSet`.

        Parameters
        ----------
        blob : SymmetryFunctionSet or SymmetryFunction
            The object to which this object will be added.

        Returns
        -------
        blob/sfset : SymmetryFunctionSet
            If a `SymmetryFunctionSet` was supplied as the input argument
            `blob`, it will be returned with this object added to its storage.
            Otherwise, a new `sfset` will be created and returned.
        """
        if isinstance(blob, SymmetryFunctionSet):
            blob += self
            return blob

        if isinstance(blob, SymmetryFunction):
            sfset = SymmetryFunctionSet()
            sfset += self
            sfset += blob
            return sfset

        raise TypeError('unsupported operand type(s) for multiplication.')

    def __mul__(self, multiplier: int) -> 'SymmetryFunctionSet':
        """Define multiplication behaviour.

        `SymmetryFunction`s can be treated like mathematical objects. A SF may
        be multiplied by an integer to replicate it.

        Parameters
        ----------
        multiplier : int
            The number of times this object will be replicated.

        Returns
        -------
        sfset : SymmetryFunctionSet
            A set of symmetry functions containing the replicated object.
        """
        sfset = SymmetryFunctionSet()
        for _ in range(multiplier):
            sfset += self.copy()

        return sfset

    def __rmul__(self, multiplier: int) -> 'SymmetryFunctionSet':
        """Multiply the object from the left."""
        return self.__mul__(multiplier)

    def copy(self) -> 'SymmetryFunction':
        """Make the object copyable."""
        return SymmetryFunction(self.sftype, self.cutoff, self.elements,
                                self.coefficients)

    @property
    def tag(self) -> str:
        """Show a human-readable equivalent of the `sftype` parameter."""
        if self.sftype in [2, 22, 23]:
            tag = 'radial'
        elif self.sftype in [3, 4, 5, 25, 26, 27]:
            tag = 'angular'
        else:
            tag = 'unknown'

        return tag

    def to_runner(self, fmt: str = '16.8f') -> str:
        """Convert the symmetry function into RuNNer input.nn format."""
        if self.coefficients is None or self.elements is None:
            raise Exception('Symmetryfunction is not fully defined yet.')

        centralatom = self.elements[0]
        neighbors = self.elements[1:]
        coefficients = [f'{c:{fmt}}' for c in self.coefficients]

        string = f'{centralatom} {self.sftype} ' \
                 + ' '.join(neighbors) \
                 + ' '.join(coefficients) \
                 + f' {self.cutoff:{fmt}}'

        return string

    def to_list(self) -> SFListType:
        """Create a list representation of the symmetry function."""
        if (self.elements is None or self.coefficients is None
           or self.sftype is None or self.cutoff is None):
            raise AttributeError('Symmetry function not fully defined.')

        if self.tag == 'radial':
            return (self.elements[0], self.sftype, self.elements[1],
                    self.coefficients[0], self.coefficients[1], self.cutoff)

        if self.tag == 'angular':
            return (self.elements[0], self.sftype, self.elements[1],
                    self.elements[2], self.coefficients[0],
                    self.coefficients[1], self.coefficients[2], self.cutoff)

        raise NotImplementedError('Cannot convert symmetry functions of '
                                  + f'type {self.tag} to list.')

    def from_list(self, sflist: SFListType) -> None:
        """Fill storage from a list of symmetry function parameters."""
        self.sftype = sflist[1]
        self.cutoff = sflist[-1]

        # The type: ignore statements are justified because the len() checks in
        # the if-statements make sure that the number of parameters is
        # compatible with the sftype.
        if self.tag == 'radial' and len(sflist) == 6:
            self.elements = [sflist[0], sflist[2]]
            self.coefficients = [float(sflist[3]), float(sflist[4])]

        elif self.tag == 'angular' and len(sflist) == 8:
            self.elements = [sflist[0], sflist[2], sflist[3]]  # type: ignore
            self.coefficients = [float(sflist[4]), float(sflist[5]),
                                 float(sflist[6])]  # type: ignore
        else:
            raise ValueError('sftype incompatible with number of parameters.')


class SymmetryFunctionSet:
    """Class for storing groups/sets of symmetry functions."""

    def __init__(
        self,
        sflist: Optional[List[SFListType]] = None,
        min_distances: Optional[Dict[str, float]] = None
    ) -> None:
        """Initialize the class.

        This class can be nested to group symmetry functions together.

        Parameters
        ----------
        sflist : List[SFListType]
            A list of symmetry functions in list format.
        min_distances : List[float]
            The minimum distances for all element pairs in the dataset.
        """
        self._sets: List[SymmetryFunctionSet] = []
        self._symmetryfunctions: List[SymmetryFunction] = []
        self.min_distances = min_distances

        if sflist is not None:
            self.from_list(sflist)

    def __str__(self) -> str:
        """Show a clean summary of the class object and its contents."""
        n_sets = len(self._sets)
        n_symmetryfunctions = len(self._symmetryfunctions)

        return f'{self.__class__.__name__}(type={self.sftypes}, ' \
               + f'sets={n_sets}, symmetryfunctions={n_symmetryfunctions})'

    def __repr__(self) -> str:
        """Show a unique summary of the class object."""
        return f'{self.to_list()}'

    def __len__(self) -> int:
        """Return the number of symmetry functions as the object length."""
        return len(self._sets) + len(self._symmetryfunctions)

    def __add__(
        self,
        blob: Union['SymmetryFunctionSet', SymmetryFunction]
    ) -> 'SymmetryFunctionSet':
        """Overload magic routine to enable nesting of multiple sets."""
        # Add a new subset of symmetry functions.
        if isinstance(blob, SymmetryFunctionSet):
            self._sets += blob.sets
            self._symmetryfunctions += blob.symmetryfunctions

        # Add a single symmetry function to storage.
        elif isinstance(blob, SymmetryFunction):
            self._symmetryfunctions.append(blob)
        else:
            raise NotImplementedError

        return self

    def __iter__(self) -> Iterator[SymmetryFunction]:
        """Iterate over all stored symmetry functions."""
        for symmetryfunction in self.storage:
            yield symmetryfunction

    def to_list(self) -> List[SFListType]:
        """Create a list of all stored symmetryfunctions."""
        symmetryfunction_list = []
        for symmetryfunction in self.storage:
            symmetryfunction_list.append(symmetryfunction.to_list())
        return symmetryfunction_list

    def from_list(
        self,
        symmetryfunction_list: List[SFListType]
    ) -> None:
        """Fill storage from a list of symmetry functions."""
        for entry in symmetryfunction_list:
            self.append(SymmetryFunction(sflist=entry))

    @property
    def sets(self) -> List['SymmetryFunctionSet']:
        """Show a list of all stored `SymmetryFunctionSet` objects."""
        return self._sets

    @property
    def symmetryfunctions(self) -> List[SymmetryFunction]:
        """Show a list of all stored `SymmetryFunction` objects."""
        return self._symmetryfunctions

    @property
    def storage(self) -> List[SymmetryFunction]:
        """Show all stored symmetry functions recursively."""
        storage = self.symmetryfunctions.copy()
        for sfset in self.sets:
            storage += sfset.storage

        return storage

    @property
    def sftypes(self) -> Optional[str]:
        """Show a list of symmetry function types in self.symmetryfunctions."""
        sftypes = list(set(sf.tag for sf in self.symmetryfunctions))
        if len(sftypes) == 1:
            return sftypes[0]

        if len(sftypes) > 1:
            return 'mixed'

        return None

    @property
    def elements(self) -> Optional[List[str]]:
        """Show a list of all elements covered in self.symmetryfunctions."""
        # Store all elements of all symmetryfunctions.
        elements = []
        for symfun in self.symmetryfunctions:
            if symfun.elements is not None:
                elements += symfun.elements

        # Remove duplicates.
        elements = list(set(elements))

        # If the list is empty, return None instead.
        if len(elements) == 0:
            return None

        return elements

    @property
    def cutoffs(self) -> Optional[List[Optional[float]]]:
        """Show a list of all cutoffs in self.symmetryfunctions."""
        # Collect the cutoff values of all symmetryfunctions.
        cutoffs = list(set(sf.cutoff for sf in self.storage))

        # If the list is empty, return None instead.
        if len(cutoffs) == 0:
            return None

        return cutoffs

    def append(
        self,
        blob: Union['SymmetryFunctionSet', SymmetryFunction]
    ) -> None:
        """Append a data `blob` to the internal storage."""
        if isinstance(blob, SymmetryFunctionSet):
            self._sets.append(blob)

        elif isinstance(blob, SymmetryFunction):
            self._symmetryfunctions.append(blob)

        else:
            raise Exception(f'{self.__class__.__name__} can only store data of'
                            + 'type SymmetryFunctionSet or SymmetryFunction.')

    def reset(self):
        """Clear all symmetryfunctions and sets from storage."""
        self._sets: List[SymmetryFunctionSet] = []
        self._symmetryfunctions: List[SymmetryFunction] = []

    @property
    def plot(self) -> SymmetryFunctionSetPlots:
        """Create a plotting interface."""
        return SymmetryFunctionSetPlots(self.storage)


def get_element_groups(
    elements: List[str],
    groupsize: int
) -> List[List[str]]:
    """Create doubles or triplets of elements from all `elements`.

    Arguments
    ---------
    elements : list of str
        A list of all the elements from which the groups shall be built.
    groupsize : int
        The desired size of the group.

    Returns
    -------
    groups : list[lists[str]]
        A list of elements groups.
    """
    # Build pairs of elements.
    if groupsize == 2:
        doubles = list(product(elements, repeat=2))
        groups = [[a, b] for (a, b) in doubles]

    # Build triples of elements.
    elif groupsize == 3:
        pairs = combinations_with_replacement(elements, 2)
        triples = product(elements, pairs)
        groups = [[a, b, c] for a, (b, c) in triples]

    return groups


def get_minimum_distances(
    dataset: List[Atoms],
    elements: List[str]
) -> Dict[str, float]:
    """Calculate min. distance between all `elements` pairs in `dataset`.

    Parameters
    ----------
    dataset : List[Atoms]
        The minimum distances will be returned for each element pair across all
        images in `dataset`.
    elements : List[str]
        The list of elements from which a list of element pairs will be built.

    Returns
    -------
    minimum_distances: Dict[str, float]
        A dictionary where the keys are strings of the format 'C-H' and the
        values are the minimum distances of the respective element pair.

    """
    minimum_distances: Dict[str, float] = {}
    for elem1, elem2 in get_element_groups(elements, 2):
        for structure in dataset:
            elems = structure.get_chemical_symbols()

            # All positions of one element.
            pos1 = structure.positions[np.array(elems) == elem1]
            pos2 = structure.positions[np.array(elems) == elem2]

            # If there is only one atom of this element, skip.
            if pos1.shape[0] <= 1 or pos2.shape[0] <= 1:
                continue

            distmatrix = get_distances(pos1, pos2)[1]

            # Remove same atom interaction.
            flat = distmatrix.flatten()
            flat = flat[flat > 0.0]

            dmin: float = min(flat)
            label = '-'.join([elem1, elem2])

            if label not in minimum_distances:
                minimum_distances[label] = dmin

            # Overwrite the currently saved minimum distances if a smaller one
            # has been found.
            if minimum_distances[label] > dmin:
                minimum_distances[label] = dmin

    return minimum_distances


# This wrapper needs all the possible symmetry function arguments.
# pylint: disable=R0913
def generate_symmetryfunctions(
    dataset: List[Atoms],
    sftype: int = 2,
    cutoff: float = 10.0,
    amount: int = 6,
    algorithm: str = 'half',
    elements: Optional[List[str]] = None,
    min_distances: Optional[Dict[str, float]] = None,
    lambda_angular: Optional[List[float]] = None,
    eta_angular: Optional[Union[Dict[str, float], SymmetryFunctionSet]] = None
) -> SymmetryFunctionSet:
    """Generate a set of radial or angular symmetry functions.

    Parameters
    ----------
    dataset : List[Atoms]
        A list of structures to which the symmetry function parameters will be
        adapted.
    sftype : int
        The type of symmetry function. At the moment, only types `2` and `3` are
        supported.
    cutoff : float
        Symmetry function cutoff radius.
    amount : int
        The number of symmetry function to be generated for each pair/triplet
        of elements.
    algorithm : str
        The algorithm for determination of either the `eta` parameter of the
        radial symmetry functions or the `zeta` parameter of the angular
        symmetry functions. Can be 'half' or 'turn' for radial SFs and 'half',
        'turn', 'literature', or 'eta_mean' for angular symmetry functions.
    elements : List[str]
        A list of elements. If not supplied the elements will be determined
        from `dataset` instead. Symmetry functions will always be generated
        for all possible combinations of `element`s.
    min_distances : Dict[str, float]
        A dictionary that contains the minimum distances between atoms
        belonging to an element pair, e.g. {'C-H': 1.2}. This is required for
        the parametrization of radial symmetry functions.
    lambda_angular : List[float]
        A set of lambda parameters for the angular symmetry functions. If not
        supplied, the default [-1.0, +1.0] will be set.
    lambda_angular : List[float]
        A set of lambda parameters for the angular symmetry functions. If not
        supplied, the default [-1.0, +1.0] will be set.
    eta_angular : Dict[str, float] or SymmetryFunctionSet
        For each `eta` in `eta_angular`, one separate set of angular symmetry
        functions will be generated.
        When `algorithm` == 'eta_mean' is set and a set of radial symmetry
        functions is supplied with `eta_angular`, two sets of angular symmetry
        functions will be generated: one with the parameter `eta` set to 0.0 and
        one with the parameter `eta` equal to the mean of the radial symmetry
        function `eta` parameters for all pairs in the current triplet of atoms.

    Returns
    -------
    parent_symfunset : SymmetryFunctionSet
        A set of newly created symmetry functions.
    """
    # If no elements were provided use all elements of this set.
    if elements is None:
        elements = get_elements(dataset)

    # Generate the parent symmetry function set.
    parent_symfunset = SymmetryFunctionSet()

    # Generate radial symmetry functions.
    if sftype == 2:
        generate_symmetryfunctions_sftype2(parent_symfunset, dataset, cutoff,
                                           amount, algorithm, elements,
                                           min_distances)

    # Generate angular symmetry functions.
    elif sftype == 3:
        generate_symmetryfunctions_sftype3(parent_symfunset, elements,
                                           cutoff, amount, algorithm,
                                           lambda_angular, eta_angular)

    else:
        raise NotImplementedError('Cannot generate symmetry functions for '
                                  + '`sftype`s other than 2 or 3.')

    return parent_symfunset


def generate_symmetryfunctions_sftype2(
    parent_symfunset: SymmetryFunctionSet,
    dataset: List[Atoms],
    cutoff: float = 10.0,
    amount: int = 6,
    algorithm: str = 'half',
    elements: Optional[List[str]] = None,
    min_distances: Optional[Dict[str, float]] = None,
) -> None:
    """Based on a dataset, generate a set of type 2 symmetry functions."""
    # If no elements were provided use all elements of this set.
    if elements is None:
        elements = get_elements(dataset)

    # For radial symmetry functions, minimum element distances are required.
    if min_distances is None:
        min_distances_ang = get_minimum_distances(dataset, elements)
        min_distances = {}
        for element, dist in min_distances_ang.items():
            min_distances[element] = dist / Bohr

    # Create one set of symmetry functions for each element pair.
    for element_group in get_element_groups(elements, 2):
        # Get label and save the min_distances for this element pair.
        label = '-'.join(element_group)
        rmin = {label: min_distances[label]}

        # Add `amount` symmetry functions to a fresh symmetry function set.
        element_symfunset = SymmetryFunctionSet(min_distances=rmin)
        for _ in range(amount):
            element_symfunset += SymmetryFunction(sftype=2, cutoff=cutoff,
                                                  elements=element_group)

        # Set the symmetry function coefficients. This modifies symfunset.
        set_radial_coefficients(element_symfunset, cutoff,
                                algorithm=algorithm,
                                elements=element_group)

        parent_symfunset.append(element_symfunset)


def set_radial_coefficients(
    sfset: SymmetryFunctionSet,
    cutoff: float,
    algorithm: str,
    elements: List[str]
) -> None:
    """Calculate the coefficients of radial symmetry functions."""
    if sfset.min_distances is not None:
        rmin = sfset.min_distances['-'.join(elements)]
    else:
        rmin = 1.0

    dturn: float = 0.5 * cutoff - rmin
    interval: float = dturn / float(len(sfset) - 1.0)

    for idx, symfun in enumerate(sfset.symmetryfunctions):
        rturn: float = 0.5 * cutoff - interval * float(idx)

        # Equally spaced at G(r) = 0.5.
        if algorithm == 'half':
            symfun.coefficients = get_radial_coefficients_half(rturn, cutoff)

        # Equally spaced turning points.
        elif algorithm == 'turn':
            symfun.coefficients = get_radial_coefficients_turn(rturn, cutoff)

        else:
            raise NotImplementedError(f"Unknown algorithm '{algorithm}'.")


def get_radial_coefficients_turn(
    rturn: float,
    cutoff: float
) -> List[float]:
    """Calculate coefficients of one radial symfun with turnpoint at `rturn`."""
    phi = np.pi * rturn / cutoff
    cosphi: float = np.cos(phi)
    sinphi: float = np.sin(phi)

    df1 = 2.0 * (cosphi + 1.0)
    df2 = 8.0 * df1 * rturn**2
    df3 = 2.0 * df1 - 4.0 * phi * sinphi
    sqrtterm: float = np.sqrt(df3**2 + df2 * np.pi**2 / cutoff**2 * cosphi)
    eta = (df3 + sqrtterm) / df2

    return [eta, 0.0]


def get_radial_coefficients_half(
    rturn: float,
    cutoff: float
) -> List[float]:
    """Calculate coefficients of one radial symfun where f(`rturn`) = 0.5."""
    phi = np.pi * rturn / cutoff
    cosphi: float = np.cos(phi)
    logphi: float = np.log(cosphi + 1.0)
    eta = logphi / rturn**2

    return [eta, 0.0]


# pylint: disable=R0914
def generate_symmetryfunctions_sftype3(
    parent_symfunset: SymmetryFunctionSet,
    elements: List[str],
    cutoff: float = 10.0,
    amount: int = 6,
    algorithm: str = 'half',
    lambda_angular: Optional[List[float]] = None,
    eta_angular: Optional[Union[Dict[str, float], SymmetryFunctionSet]] = None
) -> None:
    """Generate a set of type 3 symmetry functions."""
    if isinstance(eta_angular, SymmetryFunctionSet):
        all_etas: Dict[str, List[float]] = {}
        for symfun in eta_angular:

            # Check that the symmetry function has a coefficient.
            if symfun.coefficients is None or symfun.elements is None:
                raise Exception(f'SymmetryFunction {symfun} is not defined.')

            label = '-'.join(symfun.elements)
            eta = symfun.coefficients[0]

            if label not in all_etas:
                all_etas[label] = []
            all_etas[label].append(eta)

        eta_angular = {}
        for label, etas in all_etas.items():
            eta_angular[label] = sorted(etas)[-2]

    # Create one set of symmetry functions for each element triplet.
    for element_group in get_element_groups(elements, 3):

        eta_list = [0.0]

        # Choose the right radial eta values for this triplet, if provided.
        if eta_angular is not None and algorithm == 'eta_mean':
            radial_etas = []
            for pair in get_element_groups(element_group, 2):
                label = '-'.join(pair)
                radial_etas.append(eta_angular[label])

            eta_list += [np.mean(radial_etas)]

        if lambda_angular is None:
            lambda_angular = [-1.0, +1.0]

        for lamb in lambda_angular:
            for eta in eta_list:
                # Add `amount` symmetry functions to a fresh set.
                element_symfunset = SymmetryFunctionSet()
                for _ in range(amount):
                    element_symfunset += SymmetryFunction(
                        sftype=3,
                        cutoff=cutoff,
                        elements=element_group
                    )

                # Set the symmetry function coefficients. This modifies
                # symfunset.
                set_angular_coefficients(element_symfunset, algorithm, lamb,
                                         eta)

                parent_symfunset.append(element_symfunset)


def set_angular_coefficients(
    sfset: SymmetryFunctionSet,
    algorithm: str,
    lambda_angular: float,
    eta_angular: float = 0.0
) -> None:
    """Calculate the coefficients for a set of angular symmetry functions."""
    # Calculate the angular range that has to be covered.
    interval = 160.0 / len(sfset)

    for idx, symfun in enumerate(sfset.symmetryfunctions):
        turn: float = (160.0 - interval * idx) / 180.0 * np.pi

        # Equally spaced at G(r) = 0.5.
        if algorithm == 'half':
            symfun.coefficients = get_angular_coefficients_half(turn,
                                                                lambda_angular,
                                                                eta_angular)

        # Equally spaced turning points.
        elif algorithm == 'turn':
            symfun.coefficients = get_angular_coefficients_turn(turn,
                                                                lambda_angular,
                                                                eta_angular)

        # Library of literature values or algorithm based on mean of radial
        # eta values.
        elif algorithm in ['literature', 'eta_mean']:
            symfun.coefficients = [eta_angular, lambda_angular, 2**idx]

        else:
            raise NotImplementedError(f"Unknown algorithm '{algorithm}'.")


def get_angular_coefficients_turn(
    turn: float,
    lamb: float,
    eta: float
) -> List[float]:
    """Calculate coefficients of one radial symfun with turnpoint at `rturn`."""
    costurn: float = np.cos(turn)
    sinturn: float = np.sin(turn)
    rho = 1.0 + lamb * costurn
    zeta = 1.0 + (costurn / sinturn**2) * rho / lamb

    return [eta, lamb, zeta]


def get_angular_coefficients_half(
    turn: float,
    lamb: float,
    eta: float
) -> List[float]:
    """Calculate coefficients of one radial symfun with turnpoint at `rturn`."""
    costurn: float = np.cos(turn)
    rho = 1.0 + lamb * costurn
    logrho: float = np.log(rho)
    zeta: float = -np.log(2) / (logrho - np.log(2))

    return [eta, lamb, zeta]
