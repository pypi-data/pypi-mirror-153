#!/usr/bin/env python3
"""Plot the results of training a NNP."""

from typing import Optional, List, Dict

import numpy as np

import matplotlib.pyplot as plt

from .setup import GenericPlots


class RunnerFitResultsPlots(GenericPlots):
    """A plotting interface for the results of training a NNP."""

    # Helper type hint definition for code brevity.
    RMSEDict = Dict[str, List[Optional[float]]]

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        epochs: List[Optional[int]],
        rmse_energy: RMSEDict,
        rmse_forces: RMSEDict,
        rmse_charge: RMSEDict,
        opt_rmse_epoch: Optional[int],
        units: Dict[str, str]
    ) -> None:
        """Initialize the class."""
        self.epochs = epochs
        self.rmse_energy = rmse_energy
        self.rmse_forces = rmse_forces
        self.rmse_charge = rmse_charge
        self.opt_rmse_epoch = opt_rmse_epoch
        self.units = units

    def rmse_e(self,  axes: Optional[plt.Axes] = None) -> plt.Axes:
        """Create a lineplot of the evolution of the energy RMSE.

        This routine generates a lineplot of the evolution of the energy RMSE
        between epochs.

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

        # Shorthands for the data.
        epochs = np.array(self.epochs)
        rmse_train = np.array(self.rmse_energy['train'])
        rmse_test = np.array(self.rmse_energy['test'])
        unit = self.units['rmse_energy']

        # Convert to meV/atom or mHa/atom.
        rmse_train *= 1000
        rmse_test *= 1000

        # Use a context manager to apply styles locally.
        with plt.style.context(self.styles):
            # Plot the data.
            axes.plot(epochs, rmse_train, 'o-', label='Train set',
                      c=self.colors[0])
            axes.plot(epochs, rmse_test, 'o-', label='Test set',
                      c=self.colors[1])

            # Set title and labels.
            axes.set_title('Energy RMSE')
            axes.set_xlabel('Epoch')
            axes.set_ylabel(f'RMSE($E$) / m{unit}')
            axes.legend()

        return axes

    def rmse_f(self,  axes: Optional[plt.Axes] = None) -> plt.Axes:
        """Create a lineplot of the evolution of the atomic forces RMSE.

        This routine generates a lineplot of the evolution of the atomic force
        components RMSE between epochs.

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

        # Shorthands for the data.
        epochs = np.array(self.epochs)
        rmse_train = np.array(self.rmse_forces['train'])
        rmse_test = np.array(self.rmse_forces['test'])
        unit = self.units['rmse_force']

        # Convert to meV/atom or mHa/atom.
        rmse_train *= 1000
        rmse_test *= 1000

        # Use a context manager to apply styles locally.
        with plt.style.context(self.styles):
            # Plot the data.
            axes.plot(epochs, rmse_train, 'o-', label='Train set',
                      c=self.colors[0])
            axes.plot(epochs, rmse_test, 'o-', label='Test set',
                      c=self.colors[1])

            # Set title and labels.
            axes.set_title('Atomic Force Components RMSE')
            axes.set_xlabel('Epoch')
            axes.set_ylabel(f'RMSE($F$) / m{unit}')
            axes.legend()

        return axes
