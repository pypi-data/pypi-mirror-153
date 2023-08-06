import numpy as np
import pandas as pd
from typing import Type, Union, Dict
from sqlalchemy import Integer, SmallInteger, BigInteger, String, Float, Boolean, Date
from ..decorator_manager import timeit


@timeit(program_name="Detect AWS length and type for each column")
def detect_aws_type(df: pd.DataFrame) -> Dict:
    """
    Function detect_aws_type.
    Parse each column in a dataframe to calculate AWS type.

    Parameters:
        df (pd.DataFrame): The pandas dataframe that you want to convert to json files.

    Returns:
        Dict: Column name as key, AWS type as value.

    Examples:
        >>> from rcd_dev_kit.pandas_manager import detect_aws_type
        >>> detect_aws_type(df=my_dataframe)
        ✅'Detect AWS length and type for each column' end in 0:00:02.485355 s.⏰
    """
    print("🧮Calculating the best AWS type and length for each column...")
    dct_aws_type = {col: get_ser_aws_type(ser=df[col]) for col in df.columns}
    return dct_aws_type


# @timeit(program_name="detection")
def get_ser_aws_type(
    ser: pd.Series,
) -> Union[
    Type[SmallInteger],
    Type[Integer],
    Type[BigInteger],
    Type[Float],
    Type[Date],
    Type[Boolean],
    String,
]:
    # print(f"Parsing {ser.name} with pandas type: {ser.dtype}...")
    dct_pd_type = {
        pd.Int64Dtype: "get_int_type(ser.abs().max())",
        pd.Float64Dtype: "Float",
        pd.BooleanDtype: "Boolean",
        pd.StringDtype: "String(shift_bit_length(int(ser.map(get_char_length).max())))",
    }
    for k, v in dct_pd_type.items():
        if isinstance(ser.dtype, k):
            return eval(v)

    dct_np_type = {
        int: "get_int_type(ser.abs().max())",
        float: "Float",
        np.bool_: "Boolean",
        np.object_: "String(shift_bit_length(int(ser.map(get_char_length).max())))",
        np.datetime64: "Date",
    }
    for k, v in dct_np_type.items():
        if np.issubdtype(ser.dtype, k):
            return eval(v)

    raise ValueError(f"❌Unrecognized type: {ser.dtype}")

    # if isinstance(ser.dtype, pd.Int64Dtype) | np.issubdtype(ser.dtype, int):
    #     return get_int_type(ser.abs().max())
    # elif isinstance(ser.dtype, pd.Float64Dtype) | np.issubdtype(ser.dtype, float):
    #     return Float
    # elif isinstance(ser.dtype, pd.BooleanDtype) | np.issubdtype(ser.dtype, np.bool_):
    #     return Boolean
    # elif isinstance(ser.dtype, pd.StringDtype) | np.issubdtype(ser.dtype, np.object_):
    #     char_max_len = ser.map(get_char_length).max()
    #     return String(shift_bit_length(int(char_max_len)))
    # elif np.issubdtype(ser.dtype, np.datetime64):
    #     return Date
    # else:
    #     raise ValueError(f"❌Unrecognized type: {ser.dtype}")


def get_int_type(integer: int) -> Type[Union[SmallInteger, Integer, BigInteger]]:
    if int(integer) in range(-32768, 32767):
        return SmallInteger
    elif int(integer) in range(-2147483648, 2147483647):
        return Integer
    elif int(integer) in range(-9223372036854775808, 9223372036854775807):
        return BigInteger
    else:
        raise ValueError(f"❌Unrecognized integer type: {integer}")


def get_char_length(string: str) -> int:
    return len(str(string).encode("utf8"))


def shift_bit_length(x: int) -> int:
    return 1 << (x - 1).bit_length() if x != 1 else 2
