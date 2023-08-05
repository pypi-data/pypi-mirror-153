#!/usr/bin/env python3
"""Setup and utility functions for RuNNer plots."""

from typing import List, Union, Dict, Any

import os


class GenericPlots:
    """Generic plotting interface for runnerase results."""

    # The path to the matplotlib stylesheets.
    path_styles_mpl = os.path.join(os.path.split(__file__)[0], 'mpl_styles')

    # The internal list of currently applied styles.
    _styles: List[str] = []

    # Builtin style names for which stylesheets exist as part of runnerase.
    builtin_styles = ['presentation', 'paper', 'bar', 'scatter', 'line']

    # Default color cycler.
    # blue, orange, green, red, purple, brown.
    colors = ['#5975A4', '#CC8963', '#55a868', '#c44f53', '#8172b3', '#937860']
    light_colors = ['#9cadc9', '#d9a88c', '#99cca5', '#d98c8f', '#a69cc9',
                    '#c3b2a2']

    # Deep red.
    highlight_color = '#6F1A07'
    black = '#4C4C4C'

    # Style attributes for boxplots.
    boxplot_style: Dict[str, Any] = dict(
        widths=0.35,
        medianprops=dict(color=black),
        patch_artist=True,
        flierprops=dict(marker='d', markerfacecolor=black,
                        markersize=4, markeredgecolor=None)
    )

    @property
    def styles(self):
        """Show the list of styles applied to the plot."""
        return self._styles

    @styles.setter
    def styles(self, styles: List[str]):
        """Set the list of styles applied to the plot."""
        self._styles = styles

    def add_style(self, style: str):
        """Add `style` to `self.styles`."""
        # Catch module styles and direct them to the correct style sheets.
        if style in self.builtin_styles:
            style = os.path.join(self.path_styles_mpl, f'{style}.mplstyle')

        # Prevent from adding styles multiple times.
        if style not in self.styles:
            self.styles += [style]

    def set_style(self, styles: Union[str, List[str]]) -> None:
        """Provide paths to suitable matplotlib style sheets.

        This routine generates a pie chart showing the split between training
        and testing data from RuNNer Mode 1.

        Parameters
        ----------
        style : str
            The visualize style settings for this plot. Any valid matplotlib
            stylesheet may be passed here as an argument. Predefined styles with
            sensible defaults are 'presentation' (nonserif font) and 'thesis'
            (default LaTeX font).
        """
        # Reset the current list of styles.
        self.styles = []

        if isinstance(styles, str):
            styles = [styles]

        for style in styles:
            self.add_style(style)
