"""
This module implements a simple key-value store.
It loads values from a data file and stores them in memory.
"""
from typing import Union


class KeyValueStore:
    """
    Loads values from file and stores them in memory into a dict.
    Writing is not supported
    """

    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path
        self.key_value_pairs = {}
        self.load_from_file()

    def __len__(self):
        """
        Return KeyValueStore key count.
        """
        return len(self.key_value_pairs)

    def load_from_file(self):
        """
        Load the key-value pairs from the data file into memory.
        Assumes that the data file has one key-value pair per line, in the format "<key> <value>".
        <key> is expected to be string without whitespace.
        <value> is expected to be string that can include whitespace.
        """
        with open(self.data_file_path, encoding="utf-8") as file:
            for line in file:
                key, value = line.strip().split(" ", 1)
                self.set(key, value)

    def verify_key(self, key: str) -> bool:
        """
        Verify if key is present in KeyValueStore
        """
        return key in self.key_value_pairs

    def get(self, key: str) -> Union[None, str]:
        """
        Get the value for the given key.
        Returns None, if key is not found.
        """
        return self.key_value_pairs.get(key)

    def set(self, key: str, value: str):
        """
        Set the value for the given key. If dublicate exists, latest is persisted.
        """
        self.key_value_pairs[key] = value

    def flush(self):
        """
        Clear in memory key-value store.
        """
        self.key_value_pairs.clear()
