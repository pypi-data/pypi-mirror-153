import asyncio

from asyncblink import signal  # type: ignore

from jupyter_d1.signals import (APP_SHUTDOWN, CONTROL_CHANNEL, HB_CHANNEL,
                                IOPUB_CHANNEL, SHELL_CHANNEL, STDIN_CHANNEL)


class KernelListener:
    def __init__(self, client, kernel_id):
        self.client = client
        self.kernel_id = kernel_id
        self.should_listen = True
        self.iopub_signal = signal(IOPUB_CHANNEL)
        self.shell_signal = signal(SHELL_CHANNEL)
        self.stdin_signal = signal(STDIN_CHANNEL)
        self.hb_signal = signal(HB_CHANNEL)
        self.control_signal = signal(CONTROL_CHANNEL)

        # stop listening if the fastapi app shuts down
        signal(APP_SHUTDOWN).connect(self.shutdown_listener)

    async def shutdown_listener(self, *args, **kwargs):
        self.should_listen = False

    async def listen(self):
        while self.should_listen:
            if await self.client.iopub_channel.msg_ready():
                iopub_msg = await self.client.get_iopub_msg()
                self.iopub_signal.send(
                    msg=iopub_msg, kernel_id=self.kernel_id, channel="iopub"
                )

            if await self.client.shell_channel.msg_ready():
                shell_msg = await self.client.get_shell_msg()
                self.shell_signal.send(
                    msg=shell_msg, kernel_id=self.kernel_id, channel="shell"
                )

            if await self.client.stdin_channel.msg_ready():
                stdin_msg = await self.client.get_stdin_msg()
                self.stdin_signal.send(
                    msg=stdin_msg, kernel_id=self.kernel_id, channel="stdin"
                )

            if await self.client.control_channel.msg_ready():
                control_msg = await self.client.get_control_msg()
                self.control_signal.send(
                    msg=control_msg,
                    kernel_id=self.kernel_id,
                    channel="control",
                )

            if await self.client.control_channel.msg_ready():
                control_msg = await self.client.get_hb_msg()
                self.control_signal.send(
                    msg=control_msg, kernel_id=self.kernel_id, channel="hb"
                )

            await asyncio.sleep(0.1)
