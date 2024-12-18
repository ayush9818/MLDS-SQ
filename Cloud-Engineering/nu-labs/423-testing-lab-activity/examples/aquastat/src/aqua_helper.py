import pandas as pd
import logging


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def slice_by_time(df: pd.DataFrame, time_period: str) -> pd.DataFrame:
    """For a `time_period`, creates a dataframe with a row for each country and
    a column for each AQUASTAT variable.

    Args:
        df (:obj:`pandas.DataFrame`):  with the columns, `country`, `variable`,
            `value`, and `time period`
        time_period (`str): time period for filtering the data set and pivoting

    Returns:
        df (:obj:`pandas.DataFrame`): Pivoted dataframe

    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Provided argument `df` is not a Panda's DataFrame object")

    # Only take data for time period of interest
    df = df[df.time_period == time_period]

    # Pivot table
    df = df.pivot(index="country", columns="variable", values="value")

    df.columns.name = time_period

    return df
