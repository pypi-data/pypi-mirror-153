from galleries.data_read_write.pickle_data_reader_writer import PickleDataReaderWriter
from galleries.data_read_write.sqlite_data_reader_writer import SqliteDataReaderWriter


def default_reader_writer():
    return PickleDataReaderWriter()
    # return SqliteDataReaderWriter()
