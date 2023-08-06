import re
import pandas as pd
import numpy as np
from itertools import chain
from typing import List, Any
from .checker import check_column_align


def normalize_col_name(lst_col_name, pattern=r"(\d){2}.(\d){2}.(\d){4}"):
    lst_space_norm = [
        re.sub("\s\s+", " ", col_name).strip().lower() for col_name in lst_col_name
    ]
    lst_pattern_norm = [
        re.sub(pattern, "", col_name).strip() for col_name in lst_space_norm
    ]
    return lst_pattern_norm


def normalize_df(lst_df, dct_ctk, decimal, **kwargs):
    for df in lst_df:
        df.columns = normalize_col_name(
            df.columns, pattern=kwargs.get("remove_name_pattern", "")
        )
    print("Normalized column name.")
    lst_ctk = list(chain.from_iterable(dct_ctk.values()))
    check_column_align(lst_df, lst_ctk)

    lst_df_date_norm = [
        normalize_date_column(
            df[lst_ctk],
            lst_date_col=dct_ctk.get("date", []),
            parse_format=kwargs.get("parse_date_format"),
        )
        for df in lst_df
    ]
    print("Normalized date column.")
    lst_df_price_normalized = [
        normalize_price_column(
            df, lst_price_col=dct_ctk.get("price", []), decimal=decimal
        )
        for df in lst_df_date_norm
    ]
    print("Normalized price column.")
    return lst_df_price_normalized


def normalize_date_column(
    df: pd.DataFrame,
    lst_date_col: List,
    parse_format: str = None,
    display_format="%Y-%m-%d",
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Function normalize_date_column.
    Parse all date text column into certain format.

    Parameters:
          df (pd.DataFrame): The pandas dataframe that you want to convert to json files.
          lst_date_col (List): The list of date text column names.
          parse_format (str, default None): The fixed date format to parse, auto parse by default.
          display_format (str): The fixed date format to display.

    Examples:
        >>> from rcd_dev_kit import file_manager
        >>> file_manager.write_df_to_json_parallel(df=my_dataframe, json_path="my_path")
    """
    df_copy = df.copy()
    for col in lst_date_col:
        try:
            if np.issubdtype(df_copy[col].dtype, np.datetime64):
                df_copy[col] = df_copy[col].dt.strftime(display_format)
            elif np.issubdtype(df_copy[col].dtype, object):
                df_copy[col] = pd.to_datetime(
                    df_copy[col].str.strip("-"), format=parse_format, **kwargs
                ).dt.strftime(display_format)
            else:
                raise TypeError(
                    f"❌Unrecognised column type: {df_copy[col].dtype} for date!"
                )
        except KeyError:
            continue
    return df_copy


def normalize_decimal(df, lst_col, decimal="."):
    df_copy = df.copy()
    for col in lst_col:
        if decimal == ",":
            df_copy[col] = df_copy[col].str.replace(".", "", regex=True)
            df_copy[col] = df_copy[col].str.replace(",", ".", regex=True)
            print(f"✅ Converted decimal from , to . in column {col}")
        elif decimal == ".":
            print(f"✅ Decimal is set to . in column {col}")
        else:
            raise ValueError(f"❓Unrecognized decimal: {decimal} in column {col}")
    return df_copy


def normalize_price_column(df, lst_price_col, decimal=".", **args):
    df_copy = df.copy()
    for col in lst_price_col:
        # Try to convert
        try:
            # Remove text symbols
            if np.issubdtype(df_copy[col].dtype, object):
                df_copy[col] = df_copy[col].str.strip(" —-�€£/m³")
                # Normalize decimal
                if decimal == ",":
                    df_copy[col] = df_copy[col].str.replace(".", "", regex=True)
                    df_copy[col] = df_copy[col].str.replace(",", ".", regex=True)
                df_copy[col] = pd.to_numeric(df_copy[col].str.strip("-€ "), **args)
            elif np.issubdtype(df_copy[col].dtype, float):
                pass
            else:
                raise TypeError(
                    f"❌Unrecognised column type: {df_copy[col].dtype} for price!"
                )
        except KeyError:
            continue
    return df_copy


def normalize_percentage_column(df, lst_percentage_col, parse_format="%", decimal="."):
    df_copy = df.copy()
    for col in lst_percentage_col:
        # Try to convert
        try:
            if parse_format == "%":
                df_copy[col] = df_copy[col].str.strip(" %-—")
            # Normalize decimal
            if decimal == ",":
                df_copy[col] = df_copy[col].str.replace(".", "", regex=True)
                df_copy[col] = df_copy[col].str.replace(",", ".", regex=True)
            df_copy[col] = pd.to_numeric(df_copy[col]) / 100
        except KeyError:
            continue
    return df_copy
