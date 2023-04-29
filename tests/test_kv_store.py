import os
import tempfile
from kv_server.key_value_store import KeyValueStore

def test_load_from_file():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write("key1 value1\nkey2 value2\nkey3 value3\n")
        f.flush()
        key_value_store = KeyValueStore(f.name)
        assert len(key_value_store) == 3
        assert key_value_store.get("key1") == "value1"
        assert key_value_store.get("key2") == "value2"
        assert key_value_store.get("key3") == "value3"

def test_verify_key():
    key_value_store = KeyValueStore(os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "example.data")))
    assert key_value_store.verify_key("key1")
    assert not key_value_store.verify_key("non-existent-key")

def test_get():
    key_value_store = KeyValueStore(os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "example.data")))
    assert key_value_store.get("key1") == "value1"
    assert key_value_store.get("non-existent-key") is None

def test_set():
    key_value_store = KeyValueStore(os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "example.data")))
    key_value_store.set("key4", "value4")
    assert len(key_value_store) == 4
    assert key_value_store.get("key4") == "value4"

def test_flush():
    key_value_store = KeyValueStore(os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "example.data")))
    key_value_store.flush()
    assert len(key_value_store) == 0
