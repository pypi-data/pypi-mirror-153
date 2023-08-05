#!/usr/bin/env python3
"""Plot symmetry functions."""

from typing import Optional

import numpy as np

import matplotlib.pyplot as plt

from .setup import GenericPlots


def _calc_radial_type2(symfun, xrange):
    if symfun.sftype != 2:
        raise RuntimeError('Wrong type of symmetry function. Only type 2!')
    coeff1, coeff2 = symfun.coefficients

    return np.exp(-coeff1 * (xrange - coeff2)**2)


def _calc_angular_type3(symfun, xrange):
    if symfun.sftype != 3:
        raise RuntimeError('Wrong type of symmetry function. Only type 3!')
    _, coeff2, coeff3 = symfun.coefficients

    return 2**(1 - coeff3) * (1 + coeff2 * np.cos(xrange))**coeff3


class SymmetryFunctionSetPlots(GenericPlots):
    """A plotting interface for a set of symmetry functions."""

    def __init__(
        self,
        symmetryfunctions  # type: ignore
    ) -> None:
        """Initialize the class."""
        self.symmetryfunctions = symmetryfunctions

    def radial(self,  axes: Optional[plt.Axes] = None) -> plt.Axes:
        """Create lineplots of radial symmetry functions.

        Parameters
        ----------
        axes : plt.Axes
            A maplotlib.pyplot `Axes` instance to which the data will be added.
            If no axis is supplied, a new one is generated and returned instead.
        """
        # If no axis object was provided, use the last one or create a new one.
        if axes is None:
            axes = plt.gca()

        # Choose the right style for a bar plot.
        self.add_style('line')

        # Use a context manager to apply styles locally.
        with plt.style.context(self.styles):

            for symfun in self.symmetryfunctions:

                xrange = np.linspace(0.0, symfun.cutoff, 100)

                # Plot only radial symmetry functions of type 2.
                if symfun.sftype != 2:
                    continue

                sfvalues = _calc_radial_type2(symfun, xrange)
                label = r'$\eta = $' + f'{symfun.coefficients[0]:.3f}' \
                        + r' $a_0^2$,' \
                        + r' $R_\mathrm{s} = $' \
                        + f'{symfun.coefficients[1]:.3f}'

                axes.plot(xrange, sfvalues, '-', label=label)

            # Set title and labels.
            axes.set_title('Radial Symmetry Functions')
            axes.set_xlabel('Pairwise Distance $r$ / $a_0$')
            axes.set_ylabel('Symmetry Function Value')
            axes.legend()

        return axes

    def angular(self,  axes: Optional[plt.Axes] = None) -> plt.Axes:
        """Create lineplots of angular symmetry functions.

        Parameters
        ----------
        axes : plt.Axes
            A maplotlib.pyplot `Axes` instance to which the data will be added.
            If no axis is supplied, a new one is generated and returned instead.
        """
        # If no axis object was provided, use the last one or create a new one.
        if axes is None:
            axes = plt.gca()

        # Choose the right style for a bar plot.
        self.add_style('line')

        # Use a context manager to apply styles locally.
        with plt.style.context(self.styles):

            for symfun in self.symmetryfunctions:

                xrange = np.linspace(0.0, 2 * np.pi, 360)

                # Plot only radial symmetry functions of type 2.
                if symfun.sftype != 3:
                    continue

                sfvalues = _calc_angular_type3(symfun, xrange)
                label = r'$\lambda = $' + f'{symfun.coefficients[1]:.1f},' \
                        + r' $\zeta = $' \
                        + f'{symfun.coefficients[2]:.1f}'

                axes.plot(xrange, sfvalues, '-', label=label)

            # Set title and labels.
            axes.set_title('Angular Symmetry Functions')
            axes.set_xlabel(r'Angle $\Theta$ / degree')
            axes.set_ylabel('Symmetry Function Value')
            axes.legend()

        return axes
