import os
import pytest
from fastapi.testclient import TestClient

from main import app, read_environment_or_return_default

client = TestClient(app)


def test_read_environment_or_return_default_env_variable():
    os.environ["KV_DATA_FILE_PATH"] = "/path/to/example.data"
    assert read_environment_or_return_default() == "/path/to/example.data"


def test_read_environment_or_return_default_no_env_variable():
    os.environ.pop("KV_DATA_FILE_PATH", None)
    assert read_environment_or_return_default() == os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "example.data")
    )


@pytest.fixture(scope="module")
def mock_key_value_store(tmp_path_factory):
    data_file = tmp_path_factory.mktemp("data").joinpath("example.data")
    data_file.write_text("foo bar\nbaz qux\n")

    return KeyValueStore(str(data_file))


def test_get_key_exists(mock_key_value_store):
    response = client.get("/key/foo")
    assert response.status_code == 200
    assert response.json() == {"key": "bar"}


def test_get_key_does_not_exist(mock_key_value_store):
    response = client.get("/key/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Key not found"}
