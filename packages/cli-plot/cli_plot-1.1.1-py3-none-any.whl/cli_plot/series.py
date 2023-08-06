#!/usr/bin/env python

"""
TODO
"""

from enum import Enum
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt

# import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backend_bases import KeyEvent

from .config import Config
from .mouse_event_handlers import MouseEventHandlers
from .util import exit_cli, unique_filename

# from matplotlib.collections import PathCollection


config = Config(
    figure_size=(11, 8.5),
    figure_face_color="#CCCCCC",  # rc
    text_color="dimgrey",
    savefig_dpi=300,
    plot_face_color="#002000",  # rc
    series_colors=(  # rc.axes.prop_cycle
        "lime",
        "orange",
        "cyan",
        "magenta",
        "red",
        "blue",
        "green",
        "gray",
    ),
    legend_face_color="#001000",
    legend_edge_color="#00FF00",
    legend_text_color="#00FF00",  # Cannot be set by RC
    grid_on=True,
    grid_major_color="#00FF00",
    grid_major_alpha=0.2,
    grid_width=1.5,
    grid_minor_on=True,
    grid_minor_color="#008000",  # Cannot be set by RC
    grid_minor_alpha=0.2,  # Cannot be set by RC
)


class Context(str, Enum):
    """Seaborn context set the size of the plot"""

    # Smallest to largest
    paper = "paper"
    notebook = "notebook"
    talk = "talk"
    poster = "poster"


def setup(context: Context = Context.notebook) -> None:
    """Setup matplotlib/seaborn using context and config

    :param context: Controls the size of the plot
    """

    rc = {
        "axes.axisbelow": False,
        "axes.edgecolor": "lightgrey",
        "axes.facecolor": config.plot_face_color,
        "axes.grid": config.grid_on,
        "axes.grid.axis": "both",
        "axes.grid.which": "both" if config.grid_minor_on else "major",
        "axes.labelcolor": config.text_color,
        "axes.prop_cycle": plt.cycler(color=config.series_colors),
        "axes.spines.right": False,
        "axes.spines.top": False,
        "figure.facecolor": config.figure_face_color,
        "figure.figsize": config.figure_size,
        "grid.alpha": config.grid_major_alpha,
        "grid.color": config.grid_major_color,
        "grid.linestyle": "-",
        "grid.linewidth": config.grid_width,
        "legend.loc": "upper right",
        "legend.frameon": False,
        "legend.facecolor": config.legend_face_color,
        "legend.edgecolor": config.legend_edge_color,
        "lines.solid_capstyle": "round",
        "patch.edgecolor": "w",
        "patch.force_edgecolor": True,
        "savefig.dpi": config.savefig_dpi,
        "text.color": config.text_color,
        "xtick.bottom": False,
        "xtick.color": config.text_color,
        "xtick.direction": "out",
        "xtick.top": False,
        "ytick.color": config.text_color,
        "ytick.direction": "out",
        "ytick.left": False,
        "ytick.right": False,
        "toolbar": "None",
    }

    sns.set(
        context=context,
        palette="deep",
        font="DejaVu Sans",
        font_scale=1,
        color_codes=True,
        rc=rc,
    )


class Series:
    """All information necessary to show a set of data."""

    def __init__(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        color: str,
        share_x: bool = True,
        alpha: float = 0.75,
        marker: str = "o",
        size: int = 0,  # TODO: set
        width: int = 1,  # TODO: set
    ):
        """
        :param df: xxx
        :param x_column: xxx
        :param y_column: xxx
        :param color: xxx
        :param share_x: xxx
        :param alpha: xxx
        :param marker: xxx
        :param size: xxx
        :param width: xxx
        """
        self.x = df[x_column].values
        self.y = df[y_column].values

        self.share_x = share_x
        self.label = y_column if share_x else f"{x_column}, {y_column}"

        self.color = color
        self.alpha = alpha

        self.marker = marker
        self.size = size
        self.width = width

        self.plotted = None

    def draw(self, ax: plt.Axes, show_values: bool = False) -> None:
        """Draw the series using the appropriate plot_type,
        showing markers and values if requested

        :param ax: plot Axes
        :param show_values: Whether to show values next to point
        """

        self.plotted = self.line(ax)[0]

        if show_values:
            self.display_values(ax)

    def line(self, ax: plt.Axes) -> List:
        """Draw an x/y line plot

        :param ax: Plot Axes.
        :returns: the result of ax.plot
        """

        return ax.plot(
            self.x,
            self.y,
            label=self.label,
            # color=self.color,
            alpha=self.alpha,
            marker=self.marker,
            markersize=self.size,
            linewidth=self.width,
        )

    def display_values(self, ax: plt.Axes) -> None:
        """Draw series values next to points

        :param ax: Plot Axes.
        """

        xytext = (self.size, -self.size // 2)
        for xy in zip(self.x, self.y):
            ax.annotate(
                xy[1] if self.share_x else f"{xy[0]}, {xy[1]}",
                xy=xy,
                color=self.color,
                xytext=xytext,
                textcoords="offset points",
                # arrowprops={"color": "#00FF00"},
            )


class Plot:
    """All information necessary to plot the data."""

    def __init__(
        self,
        figure: plt.Figure = None,
        ax: plt.Axes = None,
        xlim: Optional[Tuple[float, float]] = None,
        ylim: Optional[Tuple[float, float]] = None,
        title: Optional[str] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        show_values: bool = False,
        marker_size: int = 0,
        line_width: int = 1,
    ):
        """
        :param figure: xxx
        :param ax: xxx
        :param xlim: xxx
        :param ylim: xxx
        :param title: xxx
        :param xlabel: xxx
        :param ylabel: xxx
        :param show_values: xxx
        :param marker_size: xxx
        :param line_width: xxx
        """
        self.figure = figure or plt.figure()
        self.ax = ax or self.figure.add_subplot(1, 1, 1)

        self.series = ()
        self.show_series = []

        self.show_values = show_values
        self.marker_size = marker_size
        self.line_width = line_width

        self.xlim = xlim
        self.ylim = ylim
        #self.xlog = False
        #self.ylog = False

        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

        self.grid_on = config.grid_on

        self.ax.grid(
            which="minor",
            color=config.grid_minor_color,
            alpha=config.grid_minor_alpha,
        )

        self.mouse_handlers = MouseEventHandlers(self.ax)
        self.replace_key_handler()

    def add(self, series: List[Series]) -> None:
        """Add a series to the plot

        :param series: List of series to add to the plot
        """

        self.series = series
        self.show_series = [True for _ in self.series]

    def draw(self) -> None:
        """Draw the plot"""

        ax = self.ax
        ax.clear()

        for index, s in enumerate(self.series):
            visible = self.show_series[index]
            s.draw(ax, self.show_values and visible)
            s.plotted.set_visible(visible)

        if self.xlim:
            ax.set_xlim(xmin=self.xlim[0], xmax=self.xlim[1])
        if self.ylim:
            ax.set_ylim(ymin=self.ylim[0], ymax=self.ylim[1])

        if self.title:
            ax.set_title(self.title)
        if self.xlabel:
            ax.set_xlabel(self.xlabel)
        if self.ylabel:
            ax.set_ylabel(self.ylabel)

        # if self.xlog:
        #     ax.set_xscale("log")
        # if self.ylog:
        #     ax.set_yscale("log")

        if len(self.series) > 1:
            self.legend()

        self.gridlines()

    def legend(self) -> None:
        """Draw the plot's legend"""

        legend = self.ax.legend()
        for text in legend.get_texts():
            text.set_color(config.legend_text_color)

    def gridlines(self) -> None:
        """Draw the plot's gridlines"""

        if self.grid_on:
            self.ax.grid(True)
            self.ax.minorticks_on()
        else:
            self.ax.grid(False)
            self.ax.minorticks_off()

    def replace_key_handler(self) -> None:
        """Replace standard key and mouse handler and then show figure"""

        # Remove default handlers
        canvas = self.figure.canvas
        canvas.mpl_disconnect(canvas.manager.key_press_handler_id)
        canvas.mpl_connect("key_release_event", self._on_key_press)
        # canvas.mpl_connect("key_press_event", self._on_key_press)

    def _shift_x(self, amount: float) -> None:
        left, right = self.ax.set_xlim()
        delta = (right - left) * amount
        self.ax.set_xlim(left + delta, right + delta)
        self.figure.canvas.draw()

    def _shift_y(self, amount: float) -> None:
        bottom, top = self.ax.set_ylim()
        delta = (top - bottom) * amount
        self.ax.set_ylim(bottom + amount, top + amount)
        self.figure.canvas.draw()

    def _on_key_press(self, event: KeyEvent) -> None:
        """Key handler

        :param event: KeyEvent to handle
        """

        if event.key == "escape":  # Quit
            exit_cli()

        elif event.key == "enter":  # Save to image
            title = self.title or "plot"
            filename = unique_filename(f"{title}.png")
            self.figure.savefig(filename)
            print(f"Saved {filename}")

        elif event.key == "g":  # Toggle Grid
            self.grid_on = not self.grid_on
            self.gridlines()
            self.figure.canvas.draw()

        elif event.key in "123456789":  # Toggle Series Display
            n = ord(event.key) - ord("1")
            self.show_series[n] = not self.show_series[n]
            for index, s in enumerate(self.series):
                s.plotted.set_visible(self.show_series[index])
            self.figure.canvas.draw()

        elif event.key == "m":  # Toggle Series Markers
            self.marker_size = (self.marker_size + 4) % 12
            for s in self.series:
                s.plotted.set_markersize(self.marker_size)
            self.figure.canvas.draw()
            return

        elif event.key == "l":  # Toggle Series Lines
            self.line_width = (self.line_width + 1) % 3
            for s in self.series:
                s.plotted.set_linewidth(self.line_width)
            self.figure.canvas.draw()
            return

        elif event.key == "left":
            self._shift_x(0.1)
            return

        elif event.key == "right":
            self._shift_x(-0.1)
            return

        elif event.key == "up":
            self._shift_y(-0.1)
            return

        elif event.key == "down":
            self._shift_y(0.1)
            return

        # elif event.key == "v":  # Toggle Value Display
        #    self.show_values = not self.show_values
        #    self.draw()
        #    self.figure.canvas.draw()

        else:
            print(f"|{event.key}|")


    # def scatter(self, ax: plt.Axes) -> PathCollection:
    #     """Draw an x/y scatter plot
    #
    #     :param ax: Plot Axes.
    #     :returns: the result of ax.scatter
    #     """
    #
    #     return ax.scatter(
    #         self.x,
    #         self.y,
    #         label=self.label,
    #         alpha=self.alpha,
    #         marker=self.marker,
    #         s=np.ones_like(self.x) * (self.size * 10),  # ???
    #     )
