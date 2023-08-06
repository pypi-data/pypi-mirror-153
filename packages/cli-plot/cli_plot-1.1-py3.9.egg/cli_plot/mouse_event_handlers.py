#!/usr/bin/env python

"""
Event name 	Class and description
'button_press_event' 	MouseEvent    - mouse button is pressed
'button_release_event' 	MouseEvent    - mouse button is released
'motion_notify_event' 	MouseEvent    - mouse motion
'scroll_event' 	        MouseEvent    - mouse scroll wheel is rolled
'figure_enter_event' 	LocationEvent - mouse enters a new figure
'figure_leave_event' 	LocationEvent - mouse leaves a figure
'axes_enter_event' 	    LocationEvent - mouse enters a new axes
'axes_leave_event' 	    LocationEvent - mouse leaves an axes
'key_press_event' 	    KeyEvent      - key is pressed
'key_release_event' 	KeyEvent      - key is released
'pick_event' 	        PickEvent     - an object in the canvas is selected
'resize_event' 	        ResizeEvent   - figure canvas is resized
'draw_event' 	        DrawEvent     - canvas draw (but before screen update)

event:
    button, canvas, dblclick, guiEvent, inaxes, key, lastevent,
    name, step, x, xdata, y, ydata
"""


from typing import Callable, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseEvent


class MouseEventHandlers:
    """Collection of mouse event handlers for matplotlib"""

    def __init__(
        self,
        ax: plt.Axes,
    ):
        """
        :param ax: xxx
        """
        canvas = ax.get_figure().canvas
        canvas.mpl_connect("button_press_event", self._on_press)
        canvas.mpl_connect("button_release_event", self._on_release)
        canvas.mpl_connect("scroll_event", self._on_scroll_event)

        self.ax = ax
        self.canvas = canvas
        self.last_point: Optional[Tuple[float, float]] = None
        self.motion_handler: Optional[Callable] = None

    def _on_press(self, event: MouseEvent) -> None:
        """Handle mouse down event,
        storing the mouse down point and starting the motion handler

        :param event: xxx
        """

        if event.inaxes is not self.ax:
            return
        self.last_point = event.x, event.y
        self.motion_handler = self.canvas.mpl_connect(
            "motion_notify_event", self._on_motion
        )

    def _on_release(self, _event: MouseEvent) -> None:
        """Handle mouse up event, cancelling the motion handler

        :param _event: xxx
        """

        self.last_point = None
        self.canvas.mpl_disconnect(self.motion_handler)

    def _on_motion(self, event: MouseEvent) -> None:
        """Handle mouse motion: pan the plot to move with the mouse

        :param event: xxx
        """

        if event.inaxes is not self.ax or self.last_point is None:
            return

        x1_data, y1_data = event.xdata, event.ydata
        pixel_to_data = self.ax.transData.inverted()
        x0_data, y0_data = pixel_to_data.transform_point(self.last_point)
        dx = x1_data - x0_data
        dy = y1_data - y0_data
        self.last_point = event.x, event.y

        self._pan(dx, dy)

    def _on_scroll_event(self, event: MouseEvent):
        """Handle scroll event by zooming in or out at the mouse location

        :param event: xxx
        """

        self._zoom(event.xdata, event.ydata, zoom_in=(event.button == "up"))

    def _pan(self, dx: int, dy: int) -> None:
        """Pan the plot dx,dy pixels

        :param dx: xxx
        :param dy: xxx
        """

        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()

        self.ax.axis(
            xmin=xmin - dx,
            xmax=xmax - dx,
            ymin=ymin - dy,
            ymax=ymax - dy,
        )

        self.canvas.draw()

    def _zoom(self, x: int, y: int, zoom_in: bool = True, scale: float = 0.8) -> None:
        """Zoom in or out at x/y by scale.

        :param x: xxx
        :param y: xxx
        :param zoom_in: xxx
        :param scale: xxx
        """

        # Get current limits
        x0, x1 = self.ax.get_xlim()
        y0, y1 = self.ax.get_ylim()

        # If x or y outside limits, set to middle
        if x is None:
            x = (x0 + x1) * 0.5
        if y is None:
            y = (y0 + y1) * 0.5

        if not zoom_in:
            scale = 1 / scale  # zoom out

        dx = x1 - x0
        dy = y1 - y0

        # Get position as a fraction
        xs = (x - x0) / dx
        ys = (y - y0) / dy

        # Set new limits
        self.ax.axis(
            xmin=x - dx * scale * xs,
            xmax=x + dx * scale * (1 - xs),
            ymin=y - dy * scale * ys,
            ymax=y + dy * scale * (1 - ys),
        )

        self.canvas.draw()


def demo() -> None:
    """Simple demonstration of pan/zoom mouse events"""

    x, y, size, color = np.random.rand(4, 200)
    size *= 200

    _, ax = plt.subplots()
    _handlers = MouseEventHandlers(
        ax
    )  # Keep ui to prevent it from being garbage collected

    ax.scatter(x, y, size, color, alpha=0.75)
    ax.set(
        xlim=(0, 1), ylim=(0, 1), autoscale_on=False, title="Drag to pan, Wheel to zoom"
    )
    plt.show()


if __name__ == "__main__":
    demo()
