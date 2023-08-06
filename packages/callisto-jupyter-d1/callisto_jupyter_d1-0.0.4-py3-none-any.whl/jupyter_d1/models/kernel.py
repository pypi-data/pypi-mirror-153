from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class JupyterD1Metadata(BaseModel):
    cell_uuid: str


class KernelPayload(BaseModel):
    pass


class KernelHeader(BaseModel):
    # date: DateTime
    msg_id: str
    msg_type: str
    session: str
    username: str
    version: str


class KernelMetadata(BaseModel):
    dependencies_met: bool
    engine: str
    jupyter_d1: JupyterD1Metadata
    # started: DateTime
    status: str


class KernelContent(BaseModel):
    execution_count: int
    payload: List[KernelPayload]
    status: str
    # user_expression: str


class KernelMessage(BaseModel):
    msg_id: str
    msg_type: str
    channel: str
    header: KernelHeader
    parent_header: KernelHeader
    metadata: KernelMetadata
    content: KernelContent
    # buffers: [KernelBuffer]


class KernelIsAlive(BaseModel):
    kernel_id: UUID
    kernel_is_alive: bool


class KernelsIdle(BaseModel):
    idle: bool
    last_idle: datetime
