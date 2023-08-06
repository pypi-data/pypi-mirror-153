#!/usr/bin/env python3
"""Plot symmetry function values."""

from typing import Optional, List, Dict

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from .setup import GenericPlots


class RunnerStructureSymmetryFunctionValuesPlots(GenericPlots):
    """A plotting interface for symmetry function values of one structure."""

    def __init__(
        self,
        data: Dict[str, np.ndarray]
    ) -> None:
        """Initialize the class."""
        self.data = data

    def boxplot(
        self,
        axes: Optional[plt.Axes] = None,
        normalize: Optional[bool] = False
    ) -> plt.Axes:
        """Create a boxplot of the distribution of symmetry function values.

        This routine generates a statistical analysis of the different RuNNer
        symmetry functions in the form of a boxplot.

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
        self.add_style('bar')

        legend_elements = []
        for idx_element, (element, sfvalues) in enumerate(self.data.items()):
            # Stack the arrays of each element and remove the first column
            # which contains the atomic index.
            sfdata = sfvalues[:, 1:]
            labels = np.arange(0, sfdata.shape[1], 1)

            # Normalize the values.
            if normalize is True:
                norm = sfdata.max()
                sfdata /= norm

            # Shift boxes to accomodate multiple elements.
            if len(self.data) == 1:
                direction = 0
            else:
                direction = +1 if (idx_element % 2) else -1

            barcenter = labels + direction * \
                self.boxplot_style['widths'] / len(self.data)

            # Use a context manager to apply styles locally.
            with plt.style.context(self.styles):
                boxplot = axes.boxplot(sfdata, positions=barcenter,
                                       **self.boxplot_style)

            # Fill the boxes with colors.
            for patch in boxplot['boxes']:
                patch.set_facecolor(self.colors[idx_element])

            # Add a legend entry.
            legend_elements += [Patch(facecolor=self.colors[idx_element],
                                label=element)]

        with plt.style.context(self.styles):
            axes.set_xticks(labels)
            axes.set_xticklabels(labels)
            axes.set_xlabel('Symmetry Function ID')

            if normalize is True:
                axes.set_ylabel('Normalized Symmetry Function Values / a. u.')
            else:
                axes.set_ylabel('Symmetry Function Values / a. u.')

            axes.set_title('Atom-centered Symmetry Function Values')
            axes.legend(handles=legend_elements, loc='upper right')

        return axes


class RunnerSymmetryFunctionValuesPlots(GenericPlots):
    """A plotting interface for all symmetry function values of one dataset."""

    def __init__(
        self,
        data  # type: ignore
    ) -> None:
        """Initialize the class."""
        self.data = data

    # pylint: disable=too-many-locals
    def boxplot(
        self,
        axes: Optional[plt.Axes] = None,
        normalize: Optional[bool] = False
    ) -> plt.Axes:
        """Create a boxplot of the distribution of symmetry function values.

        This routine generates a statistical analysis of the different RuNNer
        symmetry functions in the form of a boxplot.

        Parameters
        ----------
        axes : plt.Axes
            A maplotlib.pyplot `Axes` instance to which the data will be added.
            If no axis is supplied, a new one is generated and returned instead.
        normalize : bool
            Whether all data should be normalized individually or not.
        """
        # If no axis object was provided, use the last one or create a new one.
        if axes is None:
            axes = plt.gca()

        # Choose the right style for a bar plot.
        self.add_style('bar')

        # Collect the symmetry function values of all structures in one dict
        # of lists of np arrays.
        allsfvalues: Dict[str, List[np.ndarray]] = {}
        for structure in self.data:
            for element, sfvalues in structure.data.items():
                if element not in allsfvalues:
                    allsfvalues[element] = []

                allsfvalues[element].append(sfvalues)

        legend_elements = []
        for idx_element, (element, sfvalues) in enumerate(allsfvalues.items()):
            # Stack the arrays of each element and remove the first column
            # which contains the atomic index.
            sfdata = np.vstack(sfvalues)[:, 1:]
            labels = np.arange(0, sfdata.shape[1], 1)

            # Normalize the values.
            if normalize is True:
                norm = sfdata.max(axis=0)
                sfdata /= norm

            # Shift boxes to accomodate multiple elements.
            if len(allsfvalues) == 1:
                direction = 0
            else:
                direction = +1 if (idx_element % 2) else -1

            barcenter = labels + direction * \
                self.boxplot_style['widths'] / len(allsfvalues)

            # Use a context manager to apply styles locally.
            with plt.style.context(self.styles):
                boxplot = axes.boxplot(sfdata, positions=barcenter,
                                       **self.boxplot_style)

            # Fill the boxes with colors.
            for patch in boxplot['boxes']:
                patch.set_facecolor(self.colors[idx_element])

            # Add a legend entry.
            legend_elements += [Patch(facecolor=self.colors[idx_element],
                                label=element)]

        with plt.style.context(self.styles):
            axes.set_xticks(labels)
            axes.set_xticklabels(labels)
            axes.set_xlabel('Symmetry Function ID')

            if normalize is True:
                axes.set_ylabel('Normalized Symmetry Function Values / a. u.')
            else:
                axes.set_ylabel('Symmetry Function Values / a. u.')

            axes.set_title('Atom-centered Symmetry Function Values')
            axes.legend(handles=legend_elements, loc='upper right')

        return axes
