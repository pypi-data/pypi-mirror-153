import os
import pickle
from typing import Generator

from galleries import files_utils
from galleries.data_read_write.ifile_data_reader_writer import IFileDataReaderWriter


class PickleDataReaderWriter(IFileDataReaderWriter):

    def __init__(self):
        self._file = None

    def read_data(self, file_path: str) -> Generator:
        self.release()
        self._file = open(file_path, "rb")
        end_reached = False
        try:
            while not end_reached:
                try:
                    row_data = pickle.load(self._file)
                    yield row_data
                except EOFError:
                    end_reached = True
        finally:
            self.release()

    def write_data(self, data: Generator, file_path: str, append: bool = False):
        if not os.path.exists(file_path):
            files_utils.create_dir_of_file(file_path)
        write_mode = "ab" if append else "wb"
        file = open(file_path, write_mode)
        try:
            for d in data:
                pickle.dump(d, file)
        finally:
            file.close()

    def release(self):
        if self._file is not None:
            self._file.close()
            self._file = None
