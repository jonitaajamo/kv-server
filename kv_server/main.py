import os
from pathlib import Path
from logging import Logger, getLogger

from kv_server.key_value_store import KeyValueStore

from fastapi import FastAPI, HTTPException

from contextlib import asynccontextmanager

def read_environment_or_return_default() -> str:
    default = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'example.data'))
    return os.environ.get('KV_DATA_FILE_PATH', default)

kv_data_file_path: str = read_environment_or_return_default()

logger: Logger  = getLogger(__name__)

key_value_store: KeyValueStore = KeyValueStore(kv_data_file_path)

app: FastAPI = FastAPI()

@app.get("/key/{key}")
async def get_key(key: str) -> dict:
    """
    HTTP GET router to handle key requests.
    Return HTTP exception 404, if key is not found.
    """
    if value := key_value_store.get(key):
        return {"key": value}

    raise HTTPException(status_code=404, detail="Key not found")
