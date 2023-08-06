#!/usr/bin/env python3
# encoding: utf-8
"""Utility Functions for runnerase.

Provides
--------

writer : Function
    This function is meant to be used as a decorator for output functions. It
    enables the function to be called with either a `str` path or a
    TextIOWrapper.
reader : Function
    This function is meant to be used as a decorator for input functions. It
    enables the function to be called with either a `str` path or a
    TextIOWrapper.
"""

from typing import Callable, Any, Union, Dict, TextIO, List

import functools

from ase.atoms import Atoms
from ase.data import atomic_numbers


# Custom type specifications for specific I/O function signatures.
IOFunction = Callable[..., Any]

IOFunctionDecorated = Callable[..., Any]


def writer(
    function: IOFunction
) -> IOFunctionDecorated:
    """Decorate `function` to write to both `str` path and TextIO."""
    return _io_decorator('w', function)


def reader(
    function: IOFunction
) -> IOFunctionDecorated:
    """Decorate `function` to read from both `str` path and TextIO."""
    return _io_decorator('r', function)


def _io_decorator(
    mode: str,
    function: IOFunction
) -> IOFunctionDecorated:
    """Transform `str` path arguments of I/O functions to TextIOWrapper.

    This function enables any I/O function to work with both a `str` argument
    specifying the path to read from/write to, and an already opened
    TextIOWrapper object.

    The routine works for both singular functions (`IOFunction` signature) and
    class methods (`IOClassMethod` signature).
    The routine only works when the first argument of the function (the first
    argument after `self` in the case of a class method) is either a path or
    a TextIOWrapper object.

    Arguments
    ---------
    mode : str
        Whether the file should be read (='r') or written (='w').
    function : IOFunction or IOClassMethod
        The I/O function to be transformed.

    Returns
    -------
    iofunction : IOFunctionDecorated
    """
    @functools.wraps(function)
    def iofunction(
        path_to_file: Union[str, TextIO],
        *args: Dict[Any, Any],
        **kwargs: Dict[Any, Any]
    ) -> IOFunctionDecorated:
        """Wrap `function` in a context manager that opens `path_to_file`."""
        if isinstance(path_to_file, str):
            with open(path_to_file, mode, encoding='utf8') as infile:
                obj: IOFunctionDecorated = function(infile, *args, **kwargs)

        else:
            obj = function(path_to_file, *args, **kwargs)

        return obj

    @functools.wraps(function)
    def iofunction_class(
        class_instance: object,
        path_to_file: Union[str, TextIO],
        *args: Dict[Any, Any],
        **kwargs: Dict[Any, Any]
    ) -> IOFunctionDecorated:
        """Wrap `function` in a context manager that opens `path_to_file`.

        In contrast to `iofunction`, this function works for class methods.
        Class methods usually carry `self` as the first function argument,
        which is extracted here as `class_instance`.
        """
        if isinstance(path_to_file, str):
            with open(path_to_file, mode, encoding='utf8') as infile:
                obj: IOFunctionDecorated = function(class_instance, infile,
                                                    *args, **kwargs)

        else:
            obj = function(class_instance, path_to_file, *args, **kwargs)

        return obj

    if '.' in str(function):
        return iofunction_class

    return iofunction


def get_elements(images: List[Atoms]) -> List[str]:
    """Extract a list of elements from a given list of ASE Atoms objects.

    Parameters
    ----------
    images : List[Atoms]
        A list of ASE atoms objects.

    Returns
    -------
    elements : List[str]
        A list of all elements contained in `images`.

    """
    # Get the chemical symbol of all elements.
    elements: List[str] = []
    for atoms in images:
        for element in atoms.get_chemical_symbols():
            elements.append(element)

    # Remove repeated elements.
    elements = list(set(elements))

    # Sort the elements by atomic number.
    elements.sort(key=lambda i: atomic_numbers[i])
    return elements
