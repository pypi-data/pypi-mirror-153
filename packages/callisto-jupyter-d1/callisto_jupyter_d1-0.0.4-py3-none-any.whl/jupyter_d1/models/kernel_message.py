from typing import List

from pydantic import BaseModel

from .base_wrapper import BaseWrapper


class KernelMessage(BaseModel):
    message_id: str


class KernelMessageWrapper(BaseWrapper):
    kernel_message: KernelMessage


class KernelMessagesWrapper(BaseWrapper):
    kernel_messages: List[KernelMessage]
