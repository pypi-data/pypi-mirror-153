import os
import shutil


class FileOperator:
    """
    Class FileOperator.
    Use this class to manupilate directory path or files.

    Parameters:
          path (str): The path of a directory.

    Examples:
        >>> from rcd_dev_kit import file_manager
        >>> fo = file_manager.FileOperator("my_path")
        >>> fo.remove_all()

    """

    def __init__(self, path):
        assert (
            os.path.isfile(path) is False
        ), f"Please enter a directory path instead of a file path!"
        assert os.path.isdir(path), f"Please enter a correct directory path!"
        print(f"Initializing directory path as '{path}'")
        self.path = path
        self.lst_file = os.listdir(path)
        print(f"There are {len(self.lst_file)} files under directory.")

    @staticmethod
    def remove_in_list(path, lst_file):
        for file in lst_file:
            os.remove(os.path.join(path, file))
        print(f"✅{len(lst_file)} files removed.")

    def remove_all(self, keep_dir=True):
        if keep_dir:
            FileOperator.remove_in_list(path=self.path, lst_file=self.lst_file)
        else:
            shutil.rmtree(self.path)

    def remove_keyword(self, keyword):
        lst_file_to_remove = [file for file in self.lst_file if keyword in file]
        FileOperator.remove_in_list(path=self.path, lst_file=lst_file_to_remove)

    def remove_suffix(self, suffix):
        lst_file_to_remove = [
            file for file in self.lst_file if file.endswith(f".{suffix}")
        ]
        FileOperator.remove_in_list(path=self.path, lst_file=lst_file_to_remove)

    @staticmethod
    def read_in_list(path, lst_file, read_func, **kwarg):
        lst_df = [
            read_func(os.path.join(path, file), **kwarg)
            for file in lst_file
            if not file.startswith(("~$", "."))
        ]
        print(f"✅{len(lst_df)} df read.")
        return lst_df

    def read_all(self, read_func, **kwarg):
        lst_df = FileOperator.read_in_list(
            path=self.path, lst_file=self.lst_file, read_func=read_func, **kwarg
        )
        return lst_df
