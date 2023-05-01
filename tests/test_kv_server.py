import os

import pytest
from fastapi.testclient import TestClient

from kv_server.key_value_store import KeyValueStore
from kv_server.main import app, read_environment_or_return_default

client = TestClient(app)


def test_read_environment_or_return_default_env_variable():
    os.environ["KV_DATA_FILE_PATH"] = "/path/to/example.data"
    assert read_environment_or_return_default() == "/path/to/example.data"


def test_read_environment_or_return_default_no_env_variable():
    os.environ.pop("KV_DATA_FILE_PATH", None)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    expected_path = os.path.join(base_dir, "data", "example.data")
    assert read_environment_or_return_default() == expected_path


@pytest.fixture(scope="module")
def mock_key_value_store(tmp_path_factory):
    data_file = tmp_path_factory.mktemp("data").joinpath("example.data")
    data_file.write_text("foo bar\nbaz qux\n")
    return KeyValueStore(str(data_file))


def test_get_key_exists(monkeypatch, mock_key_value_store):
    monkeypatch.setattr("kv_server.main.key_value_store", mock_key_value_store)
    response = client.get("/key/foo")
    assert response.status_code == 200
    assert response.json() == {"foo": "bar"}


def test_get_key_does_not_exist(monkeypatch, mock_key_value_store):
    monkeypatch.setattr("kv_server.main.key_value_store", mock_key_value_store)
    response = client.get("/key/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Key not found"}
