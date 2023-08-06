import pandas as pd
from typing import List
import re


def check_quality_table_names(table_name: str, df: pd.DataFrame):
    string_check = re.compile("[\s@\-!#$%^&*+()<>?/\|}{~:]")
    # Check if the table name agrees with the SQL standards. It must not have accented letters or any special character.
    if not table_name.isascii() or (string_check.search(table_name) is not None):
        raise SyntaxError(
            f"❌Table name '{table_name}' does not agree with the SQL standards. "
            f"Please remove accents, spaces or any special characters."
        )

    for col_name in df.columns:
        if not col_name.isascii() or (string_check.search(col_name) is not None):
            raise SyntaxError(
                f"❌Column name '{col_name}' does not agree with the SQL standards. "
                f"Please remove accents, spaces or any special characters."
            )


def check_na(df: pd.DataFrame, raise_error: bool = False) -> None:
    """
    Function check_na.
    Use this function to check %na in a pandas dataframe, optional: raise Error if any.

    Args:
        df(pd.DataFrame): The pandas dataframe to check NA.
        raise_error(bool): True to raise Error when there is any NA, by default: True.
    Returns:
        None
    Examples:
        >>> from rcd_dev_kit.pandas_manager import check_duplication
        >>> check_na(df=my_dataframe, raise_error=False)
    """
    print("Checking na by column...")
    df_na_count = (
        df.isna()
        .sum()
        .reset_index()
        .rename(columns={"index": "variable", 0: "na_count"})
    )
    df_na_count["n_row"] = df.shape[0]
    df_na_count["na%"] = (
        round(100 * df_na_count["na_count"] / df_na_count["n_row"], 2)
        .astype(str)
        .apply(lambda x: f"{x}%")
    )
    print(df_na_count)
    if raise_error:
        assert (
            len(df_na_count["na_count"].unique().tolist()) == 1
        ), f"There is NA in dataframe."
        print("️⭕️No NA detected!")


def check_duplication(
    df: pd.DataFrame, lst_col: List, raise_error: bool = False
) -> pd.DataFrame:
    """
    Function check_duplication.
    Use this function to check %duplicates in a pandas dataframe, optional: raise Error if any.

    Args:
        df(pd.DataFrame): The pandas dataframe to check duplicates.
        lst_col(list): List of columns name to verify the duplicates.
        raise_error(bool): True to raise Error when there is any duplicates, by default: True.
    Returns:
        None
    Examples:
        >>> from rcd_dev_kit.pandas_manager import check_duplication
        >>> check_duplication(df=my_dataframe, lst_col=["col1", "col2"], raise_error=True)
    """
    print(f"Checking duplication at level {lst_col}...")
    df_copy = df.copy()
    df_dup = df_copy[df_copy.duplicated(subset=lst_col, keep=False)].sort_values(
        by=lst_col
    )
    sentence = f"There are {df_dup.shape} duplications which is {round(100 * df_dup.shape[0] / df_copy.shape[0], 2)}% of the whole data."
    if raise_error:
        assert df_dup.shape[0] == 0, sentence
        print("️⭕️No duplication detected!")
    else:
        print(sentence)
    return df_dup


# def check_column_type(lst_df, lst_price_col, lst_code_col):
#     print("🔬Checking column type...")
#     for df in lst_df:
#         for col in lst_price_col:
#             assert np.issubdtype(df[col].dtype,
#                                  np.number), f"Price Column {col} is not type np.number but {df[col].dtype}."
#         for col in lst_code_col:
#             assert np.issubdtype(df[col].dtype,
#                                  np.object_), f"Code Column {col} is not type np.object but {df[col].dtype}."
#     print("Price columns are all numeric!")
#     print("Code columns are all object!")


def check_column_align(lst_df, lst_standard_col):
    print("🔬Checking column consistency...")
    for df in lst_df:
        difference = set(lst_standard_col) - set(df.columns)
        assert len(difference) == 0, f"Cannot find columns {difference}."
    print("⭕️Columns are all aligned!")
