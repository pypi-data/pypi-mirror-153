#!/usr/bin/env python

"""
TODO
"""

from pathlib import Path
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import typer

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
    df: pd.DataFrame, column_list: List[str]
) -> List[Tuple[str, str]]:
    """TODO"""

    if not column_list:
        columns = df.columns.tolist()
        x_column = columns[0]
        y_columns = columns[1:]
        column_pairs = [(x_column, y_column) for y_column in y_columns]

    else:
        column_list_items = [len(value.split(",")) for value in column_list]
        if all((item == 1 for item in column_list_items)):
            # X Y1 Y2 ... YN
            column_list = [convert_to_label(df, value) for value in column_list]
            x_column = column_list[0]
            y_columns = column_list[1:]
            column_pairs = [(x_column, y_column) for y_column in y_columns]

        elif all((item == 2 for item in column_list_items)):
            # X1,Y1 X2,Y2 ... XN,YN
            column_pairs = []
            for pair in column_list:
                x_value, y_value = pair.split(",")
                x_column = convert_to_label(df, x_value)
                y_column = convert_to_label(df, y_value)
                column_pairs.append((x_column, y_column))

        else:
            exit_cli("ERROR")

    # Verify all column indices are valid
    for x_column, y_column in column_pairs:
        if x_column not in df:
            exit_cli(f"Invalid column: {x_column}")
        if y_column not in df:
            exit_cli(f"Invalid column: {y_column}")

    return column_pairs


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
        Series(df, x_column, y_column,
            marker="o", color=next(cycle).get("color"))
        for x_column, y_column in column_pairs
    ]

    return series


def run(
    data_file_path: Path = typer.Argument(default=None, exists=True, dir_okay=False),
    columns: List[str] = typer.Argument(default=None),
    data: Optional[List[Path]] = typer.Option(default=None, dir_okay=False),
    x: Optional[List[str]] = typer.Option(default=None),
    y: Optional[List[str]] = typer.Option(default=None),
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    context: Context = typer.Option(Context.notebook),
    head: bool = typer.Option(None, help="Display head of data file."),
    demo: bool = typer.Option(None, help="Generate demo.png and use it."),
    version: bool = version_option(),
) -> None:
    """
        Plot will read the DATA_FILE_PATH and plot the data specified by COLUMNS.

        COLUMNS must be of the form
          X Y1 Y2 ... Yn
        or
          X1,Y1 X2,Y2 ... Xn,Yn

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

    \b
        Holding the left mouse button down and moving the mouse will pan the plot.
        Rolling the mouse wheel up and down will zoom out and in where the mouse is.
    """

    df_list = []

    if data_file_path:
        df_list.append(load_data(data_file_path))
        title = title or data_file_path.stem.replace("_", " ")

    df_list.extend(load_data(data_file_path) for data_file_path in data)
    if not title:
        title = ", ".join(d.stem.replace("_", " ") for d in data)

    if demo:
        df_list = demo_df("demo.dat")
        title = title or "Demo"

    if not df_list:
        exit_cli("Must specify data file path(s) or use --demo")

    if head:
        exit_cli(df_list[0].head(10))  # FIXME - assumes one df

    setup(context)

    if x and y:
        columns = x + y

    column_pairs = make_column_pairs(df_list[0], columns)  # FIXME - assumes one df

    series = []
    for df in df_list:
        series += load_series(df, column_pairs)

    if len(column_pairs) == 1:
        xlabel, ylabel = column_pairs[0]

    plot1 = Plot(title=title, xlabel=xlabel, ylabel=ylabel)
    plot1.add(series)
    plot1.draw()
    plt.show()


def main() -> None:
    """Call the app command run"""

    app = typer.Typer(add_completion=False)
    app.command()(run)
    app()


if __name__ == "__main__":
    main()
