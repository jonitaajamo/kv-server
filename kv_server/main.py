"""
Main entrypoint for Key-Value Server Application.
Defines basic configuration and FastAPI app.
"""
import logging
import os
import sys

from fastapi import FastAPI, HTTPException

from kv_server.key_value_store import KeyValueStore


def read_environment_or_return_default() -> str:
    """
    Checks os environment variables for KV_DATA_FILE_PATH.
    Return the project's default example data, if none is provided.
    File is always required.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default = os.path.join(base_dir, "data", "example.data")
    return os.environ.get("KV_DATA_FILE_PATH", default)


kv_data_file_path: str = read_environment_or_return_default()

logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(message)s")
logger: logging.Logger = logging.getLogger(__name__)

logger.info("Loading Key-Value pairs from file %s", kv_data_file_path)

try:
    key_value_store: KeyValueStore = KeyValueStore(kv_data_file_path)
except FileNotFoundError:
    logger.error(
        "File not found, please set KV_DATA_FILE_PATH to point to valid data file."
    )
    sys.exit(1)

logger.info("%s Key-Value pairs loaded", str(len(key_value_store)))

app: FastAPI = FastAPI()


@app.get("/key/{key}")
async def get_key(key: str) -> dict:
    """
    HTTP GET router to handle key requests.
    Return HTTP exception 404, if key is not found.
    """
    if value := key_value_store.get(key):
        return {key: value}

    raise HTTPException(status_code=404, detail="Key not found")
