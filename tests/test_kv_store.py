import os
import tempfile

import pytest

from kv_server.key_value_store import KeyValueStore


@pytest.fixture
def key_value_store():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write("key1 value1\nkey2 value2\nkey3 value3\n")
        f.flush()
        yield KeyValueStore(f.name)


def test_load_from_file(key_value_store):
    assert len(key_value_store) == 3
    assert key_value_store.get("key1") == "value1"
    assert key_value_store.get("key2") == "value2"
    assert key_value_store.get("key3") == "value3"


def test_verify_key(key_value_store):
    assert key_value_store.verify_key("key1")
    assert not key_value_store.verify_key("non-existent-key")


def test_get(key_value_store):
    assert key_value_store.get("key1") == "value1"
    assert key_value_store.get("non-existent-key") is None


def test_set(key_value_store):
    key_value_store.set("key4", "value4")
    assert len(key_value_store) == 4
    assert key_value_store.get("key4") == "value4"


def test_flush(key_value_store):
    key_value_store.flush()
    assert len(key_value_store) == 0
