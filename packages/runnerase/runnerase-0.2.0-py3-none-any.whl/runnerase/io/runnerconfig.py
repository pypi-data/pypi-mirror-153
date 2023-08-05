"""Implementation of readers and writers for the input.nn configuration file.

This module provides readers and writers for RuNNer input.nn files.
"""

from typing import Union, List, TextIO, Optional

from ase.utils import reader, writer
from ase.calculators.calculator import Parameters, CalculatorSetupError

from runnerase.symmetryfunctions import SymmetryFunction, SymmetryFunctionSet


class UnrecognizedKeywordError(Exception):
    """Error class for marking format mistakes in input.nn parameter files."""

    def __init__(self, keyname: str) -> None:
        """Initialize exception with custom error message."""
        super().__init__(f"The keyword {keyname} is not recognized.")


class FileFormatError(Exception):
    """Generic error class for marking format mistakes in RuNNer files."""

    def __init__(self, message: Optional[str] = None) -> None:
        """Initialize exception with custom error message."""
        if not message:
            message = "File formatted incorrectly."

        super().__init__(message)


def _read_arguments(
    keyword: str,
    arguments: List[str]
) -> Union[List[Union[bool, int, float, str]], SymmetryFunction]:
    """Format the arguments of one keyword when reading the input.nn file.

    Parameters
    ----------
    keyword : str
        The keyword to which the `arguments` belong.
    arguments : List[str]
        The arguments to be formatted.

    Returns
    -------
    arguments_formatted : List of Bool, float, int, str, or SymmetryFunction.
        A list of formatted arguments.
    """
    arguments_formatted: List[Union[bool, int, float, str]] = []
    for arg in arguments:
        try:
            arguments_formatted.append(int(arg))
        except ValueError:
            try:
                arguments_formatted.append(float(arg))
            except ValueError:
                arguments_formatted.append(str(arg))

    # Wrap symmetry function arguments in a symmetry function container.
    if 'symfunction' in keyword:
        return SymmetryFunction(sflist=arguments_formatted)  # type: ignore

    return arguments_formatted


def _write_arguments(
    keyword: str,
    arguments: Union[bool, float, int, str, List[Union[bool, float, int, str]]]
) -> str:
    """Format the arguments of one keyword when writing the input.nn file.

    Parameters
    ----------
    keyword : str
        The keyword to which the `arguments` belong.
    arguments : Bool or float or int or str or a list of those.
        The arguments to be formatted.

    Returns
    -------
    arguments_formatted : str
        A string of formatted arguments.
    """
    # Treat even single-argument `arguments` as a list.
    if not isinstance(arguments, list):
        arguments = [arguments]

    arguments_formatted = ''
    for arg in arguments:
        if isinstance(arg, bool):
            continue

        if isinstance(arg, float):
            arguments_formatted += f' {arg:.8f}'

        elif isinstance(arg, (int, str)):
            arguments_formatted += f' {arg}'

        else:
            raise FileFormatError(f"Argument '{arg}' is invalid for keyword "
                                  f"'{keyword}'. If the value is `None`, "
                                  'chances are you forgot to specify a '
                                  'mandatory parameter.')

    return arguments_formatted


@reader
def read_runnerconfig(infile: TextIO) -> Parameters:
    """Read an input.nn file and store the contained dictionary data.

    Parameters
    ----------
    infile : TextIOWrapper
        The fileobj in RuNNer input.nn format from which the data will be read.
    """
    runneroptions: Parameters = Parameters()

    # Initialize the symmetry function containers.
    runneroptions['symfunction_short'] = SymmetryFunctionSet()

    for line in infile:

        # Strip all comments (all text after '#' or '!') and skip blank lines.
        line = line.split('#')[0].split('!')[0]
        if line.strip() == '':
            continue

        # Extract the keyword, it is always the first word in a line.
        spline = line.split()
        keyword = spline[0]

        # Format the parameters. If there are no parameters, the keyword is a
        # Boolean and directly set to True here.
        if len(spline) == 1:
            arguments: Union[List[Union[bool, int, float, str]],
                             SymmetryFunction] = [True]
        else:
            arguments = _read_arguments(keyword, spline[1:])

        # Add the keyword to `runneroptions` if it is not already contained.
        if keyword not in runneroptions:
            runneroptions[keyword] = []

        if not isinstance(arguments, SymmetryFunction) and len(arguments) == 1:
            runneroptions[keyword].append(arguments[0])
        else:
            runneroptions[keyword].append(arguments)

    # When a keyword has only one argument, do not store it as a list.
    for keyword, options in runneroptions.items():
        # Skip symfuns, this does not apply to them.
        if isinstance(options, SymmetryFunctionSet):
            continue

        if len(options) == 1:
            runneroptions[keyword] = options[0]

    return runneroptions


@writer
def write_runnerconfig(
    outfile: TextIO,
    parameters: Parameters
) -> None:
    """Write the central RuNNer parameter file input.nn.

    Parameters
    ----------
    outfile : TextIOWrapper
        The fileobj to which the parameters will be written.
    parameters : Parameters
        A dict-like collection of RuNNer parameters.
    """
    # Write the header.
    outfile.write("### This input file for RuNNer was generated with ASE.\n")

    for keyword, arguments in parameters.items():

        # `SymmetryFunction`s have their own write routine.
        if isinstance(arguments, SymmetryFunctionSet):
            # Check whether at least one symmetry functions was supplied.
            if len(arguments) == 0:
                raise CalculatorSetupError('No symmetry functions found. The '
                                           'specification of symmetry '
                                           'functions is mandatory in RuNNer.')

            for symmetryfunction in arguments:
                outfile.write(f'{keyword:30} {symmetryfunction.to_runner()}\n')

        else:
            # Elements are treated separately. Usually, all lists are stored as
            # lists of lists to make them distinguishable from keywords which
            # occur multiple times. This is not possible for `elements`, because
            # this is an ASE standard.
            if not isinstance(arguments, list) or keyword == 'elements':
                # Skip all Boolean flags which are set to False.
                if isinstance(arguments, bool) and arguments is False:
                    continue

                outfile.write(f'{keyword:30}')
                outfile.write(f'{_write_arguments(keyword, arguments)}\n')
            else:
                # Some keywords can occur multiple times. This is marked by the
                # fact that `arguments` is a list of lists. For each sublist,
                # one line will be written in the input.nn file.
                if all(isinstance(i, list) for i in arguments):
                    for occur in arguments:
                        outfile.write(f'{keyword:30}')
                        outfile.write(f'{_write_arguments(keyword, occur)}\n')
                else:
                    outfile.write(f'{keyword:30}')
                    outfile.write(f'{_write_arguments(keyword, arguments)}\n')
