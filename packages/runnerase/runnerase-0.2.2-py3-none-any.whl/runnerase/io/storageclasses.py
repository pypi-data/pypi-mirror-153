"""Implementation of readers and writers for runnerase storageclasses.

This modules essentially provides wrapper functions around all storage classes.
Every storage class in runnerase has its own `read` and `write` routines.
This means, that in principle one can simply create an empty object of a storage
class and then call the reader themself to fill it with information.
However, users are typically more familiar with calling a public function
directly which yields an object. Such functions are provided in this module.
"""

from typing import Optional, Union, List, TextIO

from runnerase.utils import reader, writer

from runnerase.storageclasses import (RunnerScaling, RunnerFitResults,
                                      RunnerSplitTrainTest, RunnerWeights,
                                      RunnerSymmetryFunctionValues)


@reader
def read_scaling(infile: TextIO) -> RunnerScaling:
    """Read symmetry function scaling data contained in 'scaling.data' files.

    Parameters
    ----------
    infile : TextIOWrapper
        The fileobj from which the data will be read.

    Returns
    -------
    RunnerScaling : RunnerScaling
        A RunnerScaling object containing the data in `infile`.
    """
    return RunnerScaling(infile)


@writer
def write_scaling(outfile: TextIO, scaling: RunnerScaling) -> None:
    """Write symmetry function scaling data to RuNNer 'scaling.data' format.

    Parameters
    ----------
    outfile : TextIOWrapper
        The fileobj to which the data will be written.
    scaling : RunnerScaling
        The scaling data.
    """
    scaling.write(outfile)


def read_weights(
    path: str = '.',
    elements: Optional[List[str]] = None,
    prefix: str = 'weights',
    suffix: str = 'data'
) -> RunnerWeights:
    """Read the weights of atomic neural networks.

    Parameters
    ----------
    path : str
        Data will be read from all weight files under the given directory.
    elements : List[str]
        A selection of chemical symbols for which the weights under `path`
        will be read.
    prefix : str
        The filename prefix of weight files under `path`.
    suffix : str
        The filename suffix of weight files under `path`.

    Returns
    -------
    RunnerWeights : RunnerWeights
        A RunnerWeights object containing the data of all weights, ordered by
        element.
    """
    return RunnerWeights(path=path, elements=elements, prefix=prefix,
                         suffix=suffix)


# For some reason pylint thinks that this function has the same signature as
# ase.io.storageclasses.write_weights.
# pylint: disable=R0801
def write_weights(
    weights: RunnerWeights,
    path: str = '.',
    elements: Optional[List[str]] = None,
    prefix: str = 'weights',
    suffix: str = 'data'
) -> None:
    """Write the weights of atomic neural networks in RuNNer format.

    Parameters
    ----------
    weights : RunnerWeights
        The weights data.
    path : str
        Data will be read from all weight files under the given directory.
    elements : List[str]
        A selection of chemical symbols for which the weights under `path`
        will be read.
    prefix : str
        The filename prefix of weight files under `path`.
    suffix : str
        The filename suffix of weight files under `path`.
    """
    weights.write(path, elements, prefix, suffix)


@reader
def read_fitresults(infile: TextIO) -> RunnerFitResults:
    """Read training process results from stdout of RuNNer Mode 2.

    Parameters
    ----------
    infile : TextIOWrapper
        The fileobj from which the data will be read.

    Returns
    -------
    RunnerFitResults : RunnerFitResults
        A RunnerFitResults object containing the data in `infile`.
    """
    return RunnerFitResults(infile)


@reader
def read_splittraintest(infile: TextIO):
    """Read the split between train and test set from stdout of RuNNer Mode 1.

    Parameters
    ----------
    infile : TextIOWrapper
        The fileobj from which the data will be read.

    Returns
    -------
    RunnerSplitTrainTest : RunnerSplitTrainTest
        A RunnerSplitTrainTest object containing the data in `infile`.
    """
    return RunnerSplitTrainTest(infile)


@reader
def read_functiontestingdata(
    infile: TextIO
) -> RunnerSymmetryFunctionValues:
    """Read symmetry function values from function.data or testing.data files.

    Parameters
    ----------
    infile : TextIOWrapper
        The fileobj from which the data will be read.

    Returns
    -------
    RunnerSymmetryFunctionValues : RunnerSymmetryFunctionValues
        A RunnerSymmetryFunctionValues object containing the data in `infile`.
    """
    return RunnerSymmetryFunctionValues(infile)


@writer
def write_functiontestingdata(
    outfile: TextIO,
    sfvalues: RunnerSymmetryFunctionValues,
    index: Union[int, slice] = slice(0, None),
    fmt: str = '22.12f'
) -> None:
    """Write symmetry function values to function.data or testing.data files.

    Parameters
    ----------
    outfile : TextIOWrapper
        The fileobj from which the data will be read.
    sfvalues : RunnerSymmetryFunctionValues
        The symmetry function values.
    index : int or slice
        A selection of structures for which the data will be written. By
        default, all data in storage is written.
    fmt : str
        A format specifier for float values.
    """
    sfvalues.write(outfile, index, fmt)
