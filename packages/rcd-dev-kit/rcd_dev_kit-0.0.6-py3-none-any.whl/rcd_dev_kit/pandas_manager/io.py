import os
import itertools
import multiprocessing
from ..decorator_manager import timeit


def collect_file(path, file_name, suffix, **kwargs):
    lst_files = sorted((file for file in os.listdir(path) if (file.endswith(suffix))
                        and (not file.startswith("~$")) and (file_name.lower() in file.lower())))
    tpl_iterable = (lst_files, [path] * len(lst_files), )
    for value in kwargs.values():
        lst_arg = [value] * len(lst_files)
        tpl_iterable += (lst_arg, )
    lst_iterable = list(zip(*tpl_iterable))
    return lst_iterable


@timeit(program_name="Read Non-empty files")
def read_parallelized(file_path, work_func, file_name, suffix, **kwargs):
    lst_iterable = collect_file(file_path, file_name, suffix, **kwargs)
    print(f"There are {len(lst_iterable)} files in path: {file_path}.")

    print(f"Start reading files...")
    nb_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(nb_processes)
    lst_df_raw = pool.starmap(work_func, lst_iterable)
    pool.close()

    lst_df_non_empty = [df for df in lst_df_raw if not df.empty]
    return lst_df_non_empty