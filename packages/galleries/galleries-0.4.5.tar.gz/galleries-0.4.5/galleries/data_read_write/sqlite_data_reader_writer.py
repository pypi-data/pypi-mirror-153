import io
import pickle

import numpy as np
import os.path
import sqlite3
from sqlite3 import Connection
from typing import Generator, Optional

from galleries import files_utils
from galleries.data_read_write.ifile_data_reader_writer import IFileDataReaderWriter


def adapt_array(arr):
    """
    https://stackoverflow.com/a/18622264/9464297
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)
# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)


class SqliteDataReaderWriter(IFileDataReaderWriter):
    TABLE_NAME = "Data"

    def __init__(self):
        self._connection: Optional[Connection] = None

    def read_data(self, file_path: str) -> Generator:
        self.release()
        self._connect(file_path)
        cur = self._connection.cursor()
        try:
            data = cur.execute("SELECT * FROM Data")
            for d in data:
                yield pickle.loads(d[0])
        except:
            pass
        finally:
            self.release()

    def write_data(self, data: Generator, file_path: str, append: bool = False):
        self.release()
        exists = os.path.exists(file_path)
        if not exists:
            files_utils.create_dir_of_file(file_path)

        try:
            self._connect(file_path)
            cur = self._connection.cursor()
            exists_table = False
            try:
                tables = cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='Data'; """).fetchall()
                exists_table = tables != []
            except sqlite3.OperationalError:
                pass
            if not exists_table:
                cur.execute("CREATE TABLE Data (data BLOB)")

            if not append:
                cur.execute("DELETE FROM Data")

            for d in data:
                bd = pickle.dumps(d)
                cur.execute("INSERT INTO Data (data) VALUES(?)", [bd])

            self._connection.commit()
        finally:
            self.release()

    def release(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def _connect(self, file_path):
        self._connection = sqlite3.connect(file_path, detect_types=sqlite3.PARSE_DECLTYPES)
