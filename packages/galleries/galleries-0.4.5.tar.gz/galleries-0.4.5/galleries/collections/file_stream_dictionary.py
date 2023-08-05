import os
import pickle
from typing import Any, Generator

from galleries import files_utils
from mnd_utils.datastructures.circular_generator import CircularGenerator

from galleries.data_read_write import default_reader_writer


class FileStreamDictionary:

    def __init__(self, file_path, batch_size, append_buffer_size=100, data_reader_writer=None):
        self._file_path = file_path
        self._data_reader_writer = data_reader_writer or default_reader_writer()
        self._closed = False
        self._circular_generator = CircularGenerator(self._get_generator)
        self._all_loaded = False
        self._batch_size = batch_size
        self._current_batch: dict = None
        self._append_buffer_size = append_buffer_size
        self._append_buffer = {}

    @property
    def append_buffer_size(self):
        return self._append_buffer_size

    @append_buffer_size.setter
    def append_buffer_size(self, value):
        self._append_buffer_size = value

    @property
    def closed(self):
        return self._closed

    def _get_generator(self):
        yield from self._data_reader_writer.read_data(self._file_path)

    def _get_current_batch_dict(self):
        if self._current_batch is None:
            # initialize batch
            self._load_next_batch()
            if len(self._current_batch) < self._batch_size:
                self._all_loaded = True
        return self._current_batch

    def _load_next_batch(self):
        size = self._batch_size
        gen = self._circular_generator[:size]
        self._current_batch = {}
        for index, value in gen:
            if index in self._current_batch:
                break  # turned around
            self._current_batch[index] = value

    def _append_pushed_data(self):
        # close
        self._data_reader_writer.release()

        # append data
        data = ((index, d) for index, d in self._append_buffer.items())
        self._data_reader_writer.write_data(data, self._file_path, append=True)

        # reset
        self._circular_generator = CircularGenerator(self._get_generator)
        self._all_loaded = False
        self._current_batch: dict = None
        self._append_buffer.clear()

    def try_get_item(self, key) -> (Any, bool):
        try:
            value = self[key]
            return value, True
        except KeyError:
            return None, False

    def __getitem__(self, key):
        if self._closed:
            raise IOError("Error: reading closed stream")

        batch = self._get_current_batch_dict()
        if key in batch:
            return batch[key]
        if key in self._append_buffer:
            return self._append_buffer[key]
        # else
        if self._all_loaded:
            raise KeyError(key)
        first_key = next(iter(batch.keys()))
        while True:
            self._load_next_batch()
            found = key in self._current_batch
            if found:
                return self._current_batch[key]

            first_key_again = first_key in self._current_batch
            if first_key_again:
                raise KeyError(key)

    def __iter__(self):
        if self._closed:
            raise IOError("Error: reading closed stream")
        self._append_pushed_data()
        return self._get_generator()

    def push_data(self, index, data):
        self._append_buffer[index] = data
        length = len(self._append_buffer)
        if length >= self._append_buffer_size:
            self._append_pushed_data()

    def close(self):
        self._append_pushed_data()
        self._closed = True
        self._data_reader_writer.release()
