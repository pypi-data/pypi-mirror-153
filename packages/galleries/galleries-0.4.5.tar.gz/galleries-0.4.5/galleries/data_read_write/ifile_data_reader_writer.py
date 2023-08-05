import abc
from typing import Generator


class IFileDataReaderWriter:

    @abc.abstractmethod
    def read_data(self, file_path: str) -> Generator:
        pass

    @abc.abstractmethod
    def write_data(self, data: Generator, file_path: str, append: bool = False):
        pass

    @abc.abstractmethod
    def release(self):
        pass
