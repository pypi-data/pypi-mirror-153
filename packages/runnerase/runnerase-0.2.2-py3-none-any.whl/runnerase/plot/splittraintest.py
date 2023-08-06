#!/usr/bin/env python3
"""Plot splitting between training and testing data."""

from typing import Optional, List

import numpy as np
import matplotlib.pyplot as plt

from .setup import GenericPlots


class RunnerSplitTrainTestPlots(GenericPlots):
    """A plotting interface for the split between training and testing data."""

    def __init__(self, train: List[int], test: List[int]) -> None:
        """Initialize the class."""
        self.train = train
        self.test = test

    def pie(self, axes: Optional[plt.Axes] = None) -> plt.Axes:
        """Create a pie chart of the training and testing points.

        This routine generates a pie chart showing the split between training
        and testing data from RuNNer Mode 1.

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

        # Create the data.
        data = [len(self.train), len(self.test)]

        def inner_label(percentage, data):
            """Format inner labels of the pie slices."""
            absolute = int(percentage / 100. * np.sum(data))
            return f'{percentage:.1f}% \n {absolute:d}'

        with plt.style.context(self.styles):
            axes.pie(data, labels=['Train', 'Test'],
                     autopct=lambda pct: inner_label(pct, data),
                     colors=self.colors)

        return axes
