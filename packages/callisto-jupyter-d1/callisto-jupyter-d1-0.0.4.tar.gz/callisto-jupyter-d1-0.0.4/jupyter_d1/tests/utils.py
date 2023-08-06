import asyncio
import json
import os
import pathlib
from asyncio.exceptions import TimeoutError
from datetime import timedelta
from typing import Any, Dict, List

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from jupyter_d1 import security
from jupyter_d1.models.permission import Permission
from jupyter_d1.settings import settings

WEBSOCKET_RECEIVE_TIMEOUT = float(
    os.environ.get("TEST_WEBSOCKET_RECEIVE_TIMEOUT", 4.0)
)

# Another directory to use during testing, cleared by a test fixture after
# every test
workdir_1 = str(pathlib.Path("/tmp/test_nb_2").resolve())


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    r = client.get(
        "/login/access-token", headers={"Authorization": "test9token_4"}
    )
    tokens = r.json()["token"]
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def create_auth_headers(token: str) -> Dict[str, str]:
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def create_auth_token(permission: Permission) -> str:
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    a_token = security.create_access_token(
        json.dumps(jsonable_encoder(permission)),
        expires_delta=access_token_expires,
    )
    return a_token


def get_superuser_token() -> str:
    permission = Permission(
        id=-1, user_id=-1, work_node_id=-1, write_access=True, read_access=True
    )

    return create_auth_token(permission)


def get_read_only_token() -> str:
    permission = Permission(
        id=-1,
        user_id=-1,
        work_node_id=-1,
        write_access=False,
        read_access=True,
    )

    return create_auth_token(permission)


def get_permissionless_token() -> str:
    permission = Permission(
        id=-1,
        user_id=-1,
        work_node_id=-1,
        write_access=False,
        read_access=False,
    )

    return create_auth_token(permission)


def get_readonly_token_headers() -> Dict[str, str]:
    return create_auth_headers(get_read_only_token())


def get_permissionless_token_headers() -> Dict[str, str]:
    return create_auth_headers(get_permissionless_token())


async def receive_json(
    websocket: WebSocket,
    timeout: float = WEBSOCKET_RECEIVE_TIMEOUT,
    msg_types: List[str] = [],
    max_retries: int = 20,
) -> Dict[str, Any]:
    """ 
    timeout -- timeout value for waiting on websocket data
    msg_types -- list of messages types to look for in the websocket stream.
        Types not included in the list will be ignored.
        The default value of [] means no filtering -- return all messages
    max_retries -- the max number of messages that can be ignore (that don't 
        match the msg_types list).  Default is 20.
    """
    count = 0
    while True:
        data = await asyncio.wait_for(
            websocket.receive_json(), timeout=timeout
        )

        # early exit if there's no filtering to do
        if len(msg_types) == 0:
            return data

        keys = list(data.keys())
        for msg_type in msg_types:
            if msg_type in keys:
                return data
        assert count < max_retries, "Too many retries in receive_json"
        count += 1


async def wait_for_event(
    websocket: WebSocket,
    event_type: str,
    tries: int = 15,
    timeout: float = WEBSOCKET_RECEIVE_TIMEOUT,
) -> Dict[str, Any]:

    return await receive_json(
        websocket, timeout=timeout, msg_types=[event_type], max_retries=tries
    )


async def collect_websocket_messages(
    websocket: WebSocket, timeout: float = WEBSOCKET_RECEIVE_TIMEOUT
) -> List[Dict[str, Any]]:
    """ 
    Start listening to the websocket and collect all messages until the 
    timeout is exceeded waiting on the next message.  Return all received 
    messages.
    """

    msgs = []
    try:
        while True:
            msg = await receive_json(websocket, timeout)
            msgs.append(msg)
    except TimeoutError:
        pass

    return msgs


def filter_websocket_collection(
    messages: List[Dict[str, Any]], msg_type: str
) -> List[Dict[str, Any]]:
    """ 
    Give a list of websocket messages, strip out and return the messages that
    contain `msg_type` as a top level key.
    """

    def has_key(a_dict: Dict[str, Any]) -> bool:
        return msg_type in a_dict.keys()

    return list(filter(has_key, messages))
