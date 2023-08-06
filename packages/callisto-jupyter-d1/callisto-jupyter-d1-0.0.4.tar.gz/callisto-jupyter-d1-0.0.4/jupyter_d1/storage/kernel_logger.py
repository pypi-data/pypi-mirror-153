from pprint import pformat

from asyncblink import signal  # type: ignore
from fastapi.logger import logger

from jupyter_d1.signals import (CONTROL_CHANNEL, HB_CHANNEL, IOPUB_CHANNEL,
                                SHELL_CHANNEL, STDIN_CHANNEL)

log_to_file = False
log_to_logger = False


class KernelLogger:
    def __init__(self):
        signal(IOPUB_CHANNEL).connect(self.log_iopub)
        signal(SHELL_CHANNEL).connect(self.log_shell)
        signal(STDIN_CHANNEL).connect(self.log_stdin)
        signal(HB_CHANNEL).connect(self.log_hb)
        signal(CONTROL_CHANNEL).connect(self.log_control)
        if log_to_file:
            self.file = open("/tmp/kernel_msg.log", "w")

    def log(self, channel, msg):
        if log_to_file:
            self.file.write(
                f"\n>>>>>>>>>>>>>>>> kernel >>>>>>>>>>>>>>>>>>>>\n"
            )
            self.file.write(f">>> {channel}: {pformat(msg)}\n")
        if log_to_logger:
            logger.debug(f"{channel}: {pformat(msg)}")

    async def log_iopub(self, sender, msg, **kwargs):
        self.log("iopub", msg)

    async def log_shell(self, sender, msg, **kwargs):
        self.log("shell", msg)

    async def log_stdin(self, sender, msg, **kwargs):
        self.log("stdin", msg)

    async def log_hb(self, sender, msg, **kwargs):
        self.log("hb", msg)

    async def log_control(self, sender, msg, **kwargs):
        self.log("control", msg)
