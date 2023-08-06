#!/usr/bin/env python

"""
TODO
"""

import sys
from collections import namedtuple
from itertools import count
from pathlib import Path
from typing import Any, List, Optional, Union

import typer

__version__ = "0.0.1"

PlotInfo = namedtuple("PlotInfo", "xlabel ylabel series")


def next_item(ring: List, item: Any) -> Any:
    """Find item in ring, and then
    return the next item or the first if `item` is the last in ring.
    Assumes `item` in `ring`; otherwise will throw ValueError

    :param ring: A list of items representing a ring buffer
    :param item: Item in the ring buffer
    :returns: the next item in ring buffer.
    """
    index = (ring.index(item) + 1) % len(ring)
    return ring[index]


def unique_filename(filename: Union[str, Path]) -> Path:
    """Given a filename, return a filename for a path that does not already exist.
    If the given filename does not exist it will be returned,
    otherwise a filename with
    the same stem followed by an integer and then the same suffix is returned.

    :param filename: Desired filename that the result is based on.
    :returns: a unique filename
    """
    path = Path(filename)
    if path.exists():
        stem = path.stem
        suffix = path.suffix
        for n in count(2):
            path = Path(f"{stem}{n}{suffix}")
            if not path.exists():
                break
    return path


def exit_cli(comment: Optional[str] = None) -> None:
    """Exit using typer, echoing comment if provided

    :param comment: String to print before exiting
    """
    if comment:
        typer.echo(comment)
    sys.exit(0)


def version_option() -> bool:
    """
    :returns: the typer Option that handles --version
    """

    def version_callback(_ctxt: typer.Context, value: bool):
        if value:
            exit_cli(f"plot version: {__version__}")

    return typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    )
