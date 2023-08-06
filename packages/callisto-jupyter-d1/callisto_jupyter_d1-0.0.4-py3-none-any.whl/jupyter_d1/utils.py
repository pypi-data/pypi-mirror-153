import asyncio
from typing import List, Type

import nbformat  # type: ignore
from asyncblink import signal  # type: ignore
from fastapi import WebSocket
from fastapi.logger import logger
from websockets.exceptions import ConnectionClosedError

from .signals import APP_SHUTDOWN

NotebookNode = Type[nbformat.notebooknode.NotebookNode]


def add_to_node_metadata(node: NotebookNode, **kwargs):
    if node.metadata.hasattr("jupyter_d1") is False:
        node.metadata.jupyter_d1 = {}
    node.metadata.jupyter_d1.update(kwargs)


def add_to_dict_metadata(someDict, **kwargs):
    if someDict.get("metadata") is None:
        someDict["metadata"] = {}
    metadata = someDict["metadata"]

    if metadata.get("jupyter_d1") is None:
        metadata["jupyter_d1"] = {}
    jupyter_d1 = metadata["jupyter_d1"]

    jupyter_d1.update(kwargs)


class BoolObject:
    def __init__(self, value=False):
        self.value = value

    def __bool__(self):
        return self.value


async def websocket_poll(websocket: WebSocket, msgs: List[str]):
    # use an object to communicate across coroutines
    connected = BoolObject(value=True)

    async def shutdown_listener(*args, **kwargs):
        connected.value = False

    signal(APP_SHUTDOWN).connect(shutdown_listener)

    while connected:
        await asyncio.sleep(0.1)
        if len(msgs) != 0:
            msg = msgs.pop(0)
            try:
                await websocket.send_text(msg)
            except ConnectionClosedError:
                logger.debug("client closed connection to websocket service")
                connected.value = False

    await websocket.close()
