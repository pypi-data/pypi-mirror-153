import asyncio
import os

from fastapi.logger import logger
from jupyter_client import AsyncMultiKernelManager  # type: ignore
from jupyter_client import kernelspec
from jupyter_core.paths import jupyter_runtime_dir  # type: ignore

from .kernel_listener import KernelListener


class KernelManager:
    def __init__(self):
        self._kmanager = AsyncMultiKernelManager()
        self._kmanager.connection_dir = jupyter_runtime_dir()
        if not os.path.exists(self._kmanager.connection_dir):
            os.makedirs(
                self._kmanager.connection_dir, mode=0o700, exist_ok=True
            )
        self._specManager = kernelspec.KernelSpecManager()
        self.clients = {}  # map of notebook uuid to client objects
        self.listeners = {}

    async def shutdown_all(self):
        # make a copy so we don't change the array during iteration
        uuids = list(self.clients.keys())

        for uuid in uuids:
            await self.shutdown_kernel(uuid)

    async def shutdown_kernel(self, uuid):
        listener = self.listeners.get(uuid)
        if listener is not None:
            await listener.shutdown_listener()
        del self.clients[uuid]
        await self._kmanager.shutdown_kernel(str(uuid))

    async def restart_kernel(self, uuid):
        await self._kmanager.restart_kernel(str(uuid))

    async def interrupt_kernel(self, uuid):
        await self._kmanager.interrupt_kernel(str(uuid))

    async def kernel_is_alive(self, uuid) -> bool:
        return await self._kmanager.is_alive(str(uuid))

    async def start_kernel(self, kernel_name, uuid, directory):
        if uuid in self.clients.keys():
            logger.info(f"replacing kernel for {uuid}")
            await self.shutdown_kernel(uuid)
        else:
            logger.info(f"starting kernel for {uuid}")
        await self._kmanager.start_kernel(
            kernel_name=kernel_name, kernel_id=str(uuid), cwd=directory
        )
        kernel = self._kmanager.get_kernel(str(uuid))

        client = kernel.client()
        client.start_channels()
        self.clients[uuid] = client

        # start the event listener
        listener = KernelListener(client, uuid)
        self.listeners[uuid] = listener
        asyncio.create_task(listener.listen())

    async def execute(
        self,
        uuid: str,
        code: str,
        silent: bool = False,
        store_history: bool = True,
    ):
        client = self.clients[uuid]
        msg_id = client.execute(
            code, silent=silent, store_history=store_history,
        )
        return msg_id

    async def complete(self, uuid: str, code: str, cursor_pos: int = None):
        client = self.clients[uuid]
        msg_id = client.complete(code, cursor_pos=cursor_pos)
        return msg_id

    async def get_history(self, uuid: str):
        client = self.clients[uuid]
        msg_id = client.history(output=True)
        return msg_id

    def kernel_names(self):
        kspecs = self._specManager.get_all_specs()
        return list(kspecs.keys())

    def get_kernelspec(self, uuid):
        return self._kmanager.get_kernel(str(uuid)).kernel_spec
