from typing import Union

import pandas as pd


def capital_case(some_string: str) -> str:
    """For a `some_string`, returns its capitalized format.

    Args:
        some_string (str), any valid string
    Returns:
        some_string.capitalize() (str): Capitalized some_string
    """
    return some_string.capitalize()


def select_dataframe_column(input_df: pd.DataFrame, columns: Union[str, list[str]]):
    """For a `column`, creates a dataframe with selected columns.

    Args:
        input_df (:obj:`pandas.DataFrame`): Dataframe  with the columns, `A`, `B`, and `time C`
        columns (str or a list of strs): column names for slicing the dataframe
    Returns:
        sliced_df (:obj:`pandas.DataFrame`): sliced dataframe
    """
    sliced = input_df[columns]
    sliced_df = pd.DataFrame(sliced)
    return sliced_df
