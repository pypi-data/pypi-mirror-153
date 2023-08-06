#!/usr/bin/env python

"""
TODO
"""

from pathlib import Path
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from typer import Typer, Argument, Option

from .functions import demo_df
from .series import Context, Plot, Series, setup
from .util import exit_cli, version_option

__version__ = "0.0.1"


def load_data(
    data_file_path: Path,
    header=0,  # int = typer.Option(0, help="Number of rows in data_file header"),
    delimiter=None,
) -> pd.DataFrame:
    """TODO"""

    df = pd.read_csv(
        data_file_path,
        header=header,
        engine="python",
        sep=delimiter,
    )
    return df


def convert_to_label(df: pd.DataFrame, value: str) -> str:
    """Return the appropriate label for dataframe, df.
    Assumes value is either the column number (first=1)
    or is already the appropriate label.

    :param df: A pandas dataframe.
    :param value: Either a label or index for a dataframe column
    :returns: dataframe label
    """

    try:
        index = int(value) - 1
    except ValueError:
        return value

    columns = df.columns.tolist()
    if not 0 <= index < len(columns):
        exit_cli(f"Invalid column: {value}")

    return columns[index]


def make_column_pairs(
    df: pd.DataFrame, column_string: Optional[str]
) -> List[Tuple[str, str]]:
    """TODO"""

    if not column_string:
        columns = df.columns.tolist()
        x_column = columns[0]
        y_columns = columns[1:]
        column_pairs = [(x_column, y_column) for y_column in y_columns]
        return column_pairs

    column_pairs = []
    for column_substring in column_string.split(":"):
        column_list = column_substring.split(",")
        if len(column_list) < 2:
            exit_cli(
                f"Does not support series without x column yet ({column_substring})"
            )

        column_list = [convert_to_label(df, value) for value in column_list]
        x_column = column_list[0]
        y_columns = column_list[1:]
        column_pairs += [(x_column, y_column) for y_column in y_columns]

    return column_pairs


def verify_column_pairs(df: pd.DataFrame, column_pairs: List[Tuple[str, str]]):
    """TODO"""
    # Verify all column indices are valid
    for x_column, y_column in column_pairs:
        if x_column not in df:
            exit_cli(f"Invalid column: {x_column}")
        if y_column not in df:
            exit_cli(f"Invalid column: {y_column}")


def load_series(
    df: pd.DataFrame,
    column_pairs: List[Tuple[str, str]],
) -> List[Series]:
    """Load dataframe into series using the columns specified by column list

    :param df: The dataframe to load from
    :param column_pairs: A list of x/y pairs of columns to load
    :returns: the xlabel, ylabel and series in a namedtuple
    """

    # assert column_list, "invalid column_list (len==0)"
    # assert len(column_list) > 1, "invalid column_list (len<=1)"
    # assert type(column_list[0]) == int, "invalid column_list (type != int)"

    cycle = plt.rcParams["axes.prop_cycle"]()

    series = [
        Series(df, x_column, y_column, marker="o", color=next(cycle).get("color"))
        for x_column, y_column in column_pairs
    ]

    return series


def run(
    data_file_path: Path = Argument(
        None, exists=True, dir_okay=False, help="File to parse for new series"
    ),
    column_string: str = Argument(
        None, help="Columns of file to parse.  See above for series format."
    ),
    files: List[Path] = Option(
        None,
        "--file",
        exists=True,
        dir_okay=False,
        help="Additional file(s) to parse for new series",
    ),
    columns: List[str] = Option(
        None,
        "--col",
        help="Columns of files to parse for new series.  There should be one --file for each --coll.",
    ),
    title: str = Option("", help="Title of plot."),
    xlabel: str = Option("", help="Label for X Axis."),
    ylabel: str = Option("", help="Label for Y Axis."),
    x: Optional[Tuple[float, float]] = Option(None, "-x", help="Range for X Axis."),
    y: Optional[Tuple[float, float]] = Option(None, "-y", help="Range for Y Axis."),
    head: bool = Option(None, help="Display head of data file."),
    demo: bool = Option(None, help="Generate a set of sample series."),
    context: Context = Option(Context.notebook),
    version: bool = version_option(),
) -> None:
    """
        Plot will read the DATA_FILE_PATH and plot the data specified by COLUMNS.

        COLUMNS must be of the form
          X,Y1,Y2,...,Yn
        or
          X1,Y1:X2,Y2:...:Xn,Yn

        The column value must either be the index of the column (1...N),
        or the name of the column.


        User Interface

    \b
        Key    | Result
        -------|------------------------
        g      | Toggle Grid
        l      | Cycle Line Width
        m      | Cycle Marker Size
        1-9    | Toggle Series 1-9 Display
        enter  | Save Plot to png Image
        escape | Exit
        left   | Pan left
        right  | Pan right
        up     | Pan up
        down   | Pan down

    \b
        Holding the left mouse button down and moving the mouse will pan the plot.
        Rolling the mouse wheel up and down will zoom out and in where the mouse is.
    """
    df_list = []

    if data_file_path:
        df_list.append(load_data(data_file_path))
        title = title or data_file_path.stem.replace("_", " ")

    df_list.extend(load_data(data_file_path) for data_file_path in files)
    if not title:
        title = ", ".join(f.stem.replace("_", " ") for f in files)

    if demo:
        df_list = [demo_df("demo.dat")]
        title = title or "Demo"

    if not df_list:
        exit_cli("Must specify data file path(s) or use --demo")

    if head:
        exit_cli(df_list[0].head(10))  # FIXME - assumes one df

    column_list = [column_string] if column_string else []
    column_list.extend(iter(columns))

    setup(context)

    series = []
    if len(column_list) in {0, 1}:
        df = df_list[0]
        column_pairs = make_column_pairs(df, column_list[0])
        verify_column_pairs(df, column_pairs)
        for df in df_list:
            series += load_series(df, column_pairs)
    elif len(column_list) == len(df_list):
        for df, column_string in zip(df_list, column_list):
            column_pairs = make_column_pairs(df, column_string)
            verify_column_pairs(df, column_pairs)
            series += load_series(df, column_pairs)
    else:
        exit_cli("Invalid number of columns")

    if len(column_pairs) == 1:
        xlabel, ylabel = column_pairs[0]

    plot1 = Plot(title=title, xlabel=xlabel, ylabel=ylabel)
    plot1.add(series)
    plot1.draw()
    if x:
        plot1.ax.set_xlim(x[0], x[1])
    if y:
        plot1.ax.set_ylim(y[0], y[1])
    plt.show()


def main() -> None:
    """Call the app command run"""

    app = Typer(add_completion=False)
    app.command()(run)
    app()


if __name__ == "__main__":
    main()
