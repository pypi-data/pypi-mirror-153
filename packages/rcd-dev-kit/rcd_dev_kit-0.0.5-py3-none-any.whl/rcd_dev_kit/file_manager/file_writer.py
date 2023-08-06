import os
import json
import pandas as pd
from typing import Tuple
from functools import partial
from rcd_dev_kit import decorator_manager
from concurrent.futures import ThreadPoolExecutor


def write_json(tpl_json_data: Tuple, output_path: str) -> None:
    json_id, json_content = tpl_json_data
    print(f"Generating {json_id}...")
    with open(os.path.join(output_path, f"{json_id}.json"), "w", encoding="utf8") as f:
        json.dump(json_content, f, ensure_ascii=False)


@decorator_manager.timeit(program_name="Parallel Writing pd.DataFrame to json")
def write_df_to_json_parallel(df: pd.DataFrame, json_path: str) -> None:
    """
    Function write_df_to_json_parallel.
    Write pandas dataframe into json file with multithreading, one row per json with index as file name.

    Parameters:
          df (pd.DataFrame): The pandas dataframe that you want to convert to json files.
          json_path (str): The folder path which hold your json files.

    Examples:
        >>> from rcd_dev_kit import file_manager
        >>> file_manager.write_df_to_json_parallel(df=my_dataframe, json_path="my_path")
    """
    str_json = df.to_json(orient="records", force_ascii=False)
    lst_json = json.loads(str_json)

    work_func = partial(write_json, output_path=json_path)
    with ThreadPoolExecutor() as executor:
        list(executor.map(work_func, zip(df.index, lst_json)))
