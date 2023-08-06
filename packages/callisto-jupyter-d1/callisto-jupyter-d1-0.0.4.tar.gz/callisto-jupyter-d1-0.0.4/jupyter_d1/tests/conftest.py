import logging
import os
import shutil
import unittest
from pathlib import Path
from typing import AsyncGenerator, Dict, Generator

import pytest  # type: ignore
from async_asgi_testclient import (  # type: ignore
    TestClient as WebSocketTestClient
)
from fastapi.logger import logger
from fastapi.testclient import TestClient

from jupyter_d1 import app
from jupyter_d1.settings import settings

from .utils import (get_permissionless_token_headers,
                    get_readonly_token_headers, get_superuser_token_headers)

enable_logger_output = False
# enable_logger_output = True


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture()
def readonly_token_headers(client: TestClient) -> Dict[str, str]:
    return get_readonly_token_headers()


@pytest.fixture()
def permissionless_token_headers(client: TestClient) -> Dict[str, str]:
    return get_permissionless_token_headers()


@pytest.fixture(scope="function")
def clear_notebooks(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> Generator:
    yield
    response = client.delete("/notebooks", headers=superuser_token_headers)
    assert response.status_code == 204
    response = client.get("/notebooks", headers=superuser_token_headers)
    assert response.status_code == 200


@pytest.fixture(scope="function")
def clear_notebook_directory(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> Generator:
    root_path = Path(settings.ROOT_DIR)
    root_path.mkdir(parents=True, exist_ok=True)
    yield
    if "/tmp" in str(root_path.absolute()):
        for filename in os.listdir(root_path):
            file_path = os.path.join(root_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))


@pytest.fixture(scope="function")
def clear_notebook_directory_2() -> Generator:
    workdir = Path("/tmp/test_nb_2/")
    workdir.mkdir(parents=True, exist_ok=True)
    yield
    for filename in os.listdir(workdir):
        file_path = os.path.join(workdir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


@pytest.fixture()
async def websocket_client() -> AsyncGenerator:
    async with WebSocketTestClient(app) as c:
        yield c


@pytest.fixture()
def ututils() -> unittest.TestCase:
    """Unittest TestCase so we can use useful things like assertCountEquals"""
    return unittest.TestCase()


def pytest_sessionstart(session):

    if enable_logger_output:
        # Print out logging (visible with `pytest -s`)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
