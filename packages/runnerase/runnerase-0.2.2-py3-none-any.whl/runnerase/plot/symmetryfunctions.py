#!/usr/bin/env python3
"""Plot symmetry functions."""

from typing import Optional

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

from .setup import GenericPlots


def _calc_radial_type2(symfun, xrange):
    if symfun.sftype != 2:
        raise RuntimeError('Wrong type of symmetry function. Only type 2!')
    coeff1, coeff2 = symfun.coefficients

    return np.exp(-coeff1 * (xrange - coeff2)**2)


def _calc_radial_type2_cutoff(symfun, xrange):
    if symfun.sftype != 2:
        raise RuntimeError('Wrong type of symmetry function. Only type 2!')
    coeff1, coeff2 = symfun.coefficients
    cutoff = 0.5 * (np.cos(np.pi * xrange / symfun.cutoff) + 1)

    return np.exp(-coeff1 * (xrange - coeff2)**2) * cutoff


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

    # The plots need to be flexible, so we allow multiple kwarg options.
    # pylint: disable=too-many-branches
    def radial(
        self,
        axes: Optional[plt.Axes] = None,
        show_legend: bool = False,
        cutoff_function: bool = False
    ) -> plt.Axes:
        """Create lineplots of radial symmetry functions.

        Parameters
        ----------
        axes : plt.Axes
            A maplotlib.pyplot `Axes` instance to which the data will be added.
            If no axis is supplied, a new one is generated and returned instead.
        show_legend : boolean
            Whether a legend will be shown in each subplot or not.
        cutoff_function : boolean
            Whether to include the cutoff function in the calculation.
        """
        # Get a list of all element groups.
        elements = []
        for symfun in self.symmetryfunctions:
            if symfun.sftype != 2:
                continue

            if symfun.elements not in elements:
                elements.append(symfun.elements)

        max_cols = int(len(elements) / 2)

        # If no axis object was provided, use the last one or create a new one.
        if axes is None:
            if len(elements) == 1:
                axes = plt.gca()
            else:
                # Create subplots for each group of elements.
                _, axes = plt.subplots(max_cols, max_cols)

        # Choose the right style for a bar plot.
        self.add_style('line')

        # Use a context manager to apply styles locally.
        with plt.style.context(self.styles):

            row_index = 0
            col_index = 0
            for element_group in elements:

                if isinstance(axes, matplotlib.axes.Axes):
                    axis = axes
                else:
                    axis = axes[col_index, row_index]

                for symfun in self.symmetryfunctions:

                    xrange = np.linspace(0.0, symfun.cutoff, 100)

                    # Skip all symmetry functions which do not belong to the
                    # element_group.
                    if symfun.elements != element_group:
                        continue

                    # Plot only radial symmetry functions of type 2.
                    if symfun.sftype != 2:
                        continue

                    # Calculate the function values w/ or w/o cutoff function.
                    if cutoff_function is True:
                        sfvalues = _calc_radial_type2_cutoff(symfun, xrange)
                    else:
                        sfvalues = _calc_radial_type2(symfun, xrange)

                    # Generate the label.
                    label = r'$\eta = $' + f'{symfun.coefficients[0]:.3f}' \
                            + r' $a_0^2$,' \
                            + r' $R_\mathrm{s} = $' \
                            + f'{symfun.coefficients[1]:.3f}'

                    axis.plot(xrange, sfvalues, '-', label=label)

                    # Set title and labels.
                    # For multiple plots, set subplot title.
                    if not isinstance(axes, matplotlib.axes.Axes):
                        axis.set_title(f'Elements {element_group}')

                    axis.set_xlabel('Pairwise Distance $r$ / $a_0$')
                    axis.set_ylabel('Symmetry Function Value')
                    axis.set_ylim([0.0, 1.1])
                    axis.set_xlim([0.0, symfun.cutoff + 1])

                    if show_legend is True:
                        axis.legend()

                # Switch over to the next panel in the row.
                col_index += 1

                # Switch to the next row if we reached the end of this one.
                if col_index == max_cols:
                    row_index += 1
                    col_index = 0

            # Set super title.
            plt.suptitle('Radial Symmetry Functions')

        return axes

    def angular(
        self,
        axes: Optional[plt.Axes] = None,
        show_legend: bool = False
    ) -> plt.Axes:
        """Create lineplots of angular symmetry functions.

        Parameters
        ----------
        axes : plt.Axes
            A maplotlib.pyplot `Axes` instance to which the data will be added.
            If no axis is supplied, a new one is generated and returned instead.
        show_legend : boolean
            Whether to show a legend for each subplot.
        """
        # Get a list of all element groups.
        elements = []
        for symfun in self.symmetryfunctions:
            if symfun.sftype != 3:
                continue

            if symfun.elements not in elements:
                elements.append(symfun.elements)

        max_cols = int(len(elements) / 2)

        # If no axis object was provided, use the last one or create a new one.
        if axes is None:
            if len(elements) == 1:
                axes = plt.gca()
            else:
                # Create subplots for each group of elements.
                _, axes = plt.subplots(max_cols, max_cols - 1)

        # Choose the right style for a bar plot.
        self.add_style('line')

        # Use a context manager to apply styles locally.
        with plt.style.context(self.styles):

            row_index = 0
            col_index = 0
            for element_group in elements:

                if isinstance(axes, matplotlib.axes.Axes):
                    axis = axes
                else:
                    axis = axes[col_index, row_index]

                for symfun in self.symmetryfunctions:

                    xrange = np.linspace(0.0, 2 * np.pi, 360)

                    # Skip all symmetry functions which do not belong to the
                    # element_group.
                    if symfun.elements != element_group:
                        continue

                    # Plot only angular symmetry functions of type 3.
                    if symfun.sftype != 3:
                        continue

                    sfvalues = _calc_angular_type3(symfun, xrange)

                    # Generate the label.
                    label = r'$\lambda = $' + f'{symfun.coefficients[1]:.1f},' \
                            + r' $\zeta = $' \
                            + f'{symfun.coefficients[2]:.1f}'

                    axis.plot(xrange, sfvalues, '-', label=label)

                    # Set title and labels.
                    # For multiple plots, set subplot title.
                    if not isinstance(axes, matplotlib.axes.Axes):
                        axis.set_title(f'Elements {element_group}')

                    axis.set_xticks([0, 0.5 * np.pi, np.pi, 1.5 * np.pi,
                                     2 * np.pi])
                    axis.set_xticklabels([0, 90, 180, 270, 360])
                    axis.set_xlabel(r'Angle $\Theta$ / degree')
                    axis.set_ylabel('Symmetry Function Value')

                    if show_legend is True:
                        axis.legend()

                # Switch over to the next panel in the row.
                col_index += 1

                # Switch to the next row if we reached the end of this one.
                if col_index == max_cols:
                    row_index += 1
                    col_index = 0

            # Set super title.
            plt.suptitle('Angular Symmetry Functions')

        return axes
