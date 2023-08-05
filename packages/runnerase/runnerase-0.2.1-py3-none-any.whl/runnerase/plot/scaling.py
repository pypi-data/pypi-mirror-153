#!/usr/bin/env python3
"""Plot symmetry function scaling data."""

from typing import Optional, Dict

import numpy as np

import matplotlib.pyplot as plt

from .setup import GenericPlots


class RunnerScalingPlots(GenericPlots):
    """A plotting interface for symmetry function scaling data."""

    def __init__(self, data: Dict[str, np.ndarray]) -> None:
        """Initialize the class."""
        self.data = data

    def barplot(self,  axes: Optional[plt.Axes] = None) -> plt.Axes:
        """Create a bar plot of the scaling data.

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

        barwidth = 0.35

        # scaling.data contains a dictionary of np.ndarrays.
        for idx, (element, data) in enumerate(self.data.items()):
            labels = data[:, 0]
            mins = data[:, 1]
            maxes = data[:, 2]
            means = data[:, 3]

            # Calculate the bar heights and center positions.
            barheights = maxes - mins
            direction = +1 if (idx % 2) else - 1
            barcenter = labels + direction * barwidth / len(self.data)

            # Use a context manager to apply styles locally.
            with plt.style.context(self.styles):
                # Create bars for minimum and maximum values.
                axes.bar(barcenter, barheights, barwidth,
                         bottom=mins, label=f'Element {element}')

                # Create black horizontal lines for the mean values.
                axes.hlines(means, barcenter - barwidth / len(self.data),
                            barcenter + barwidth / len(self.data),
                            color='black')

                # Set title and labels.
                axes.set_xlabel('Symmetry Function ID')
                axes.set_ylabel('Symmetry Function Values / a. u.')
                axes.set_title('RuNNer Symmetry Function Scaling Information')

                axes.legend()

            return axes
