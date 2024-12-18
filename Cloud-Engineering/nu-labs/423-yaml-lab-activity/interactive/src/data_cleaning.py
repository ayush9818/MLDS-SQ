import logging

import pandas as pd

logger = logging.getLogger()


def subset_data(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Subset the data to a list of column names"""
    df_result = df[columns]
    return df_result


def clean_missing(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """Take columns defined in configs from dataframe df."""
    logging.info("------------Printing out kwargs given to clean_missing------------")
    logging.info(kwargs)
    df_result = df.fillna(**kwargs)
    return df_result


def reorder(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """Sort the dataframe values"""
    logging.info("------------Printing out kwargs given to reorder------------")
    logging.info(kwargs)
    df_result = df.sort_values(**kwargs)
    return df_result
