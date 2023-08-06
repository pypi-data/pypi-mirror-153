from typing import Dict, List

from pydantic import BaseModel

from .base_wrapper import BaseWrapper
from .JSONType import JSONType


class KernelSpecDetail(BaseModel):
    display_name: str
    language: str
    interrupt_mode: str
    metadata: JSONType
    argv: List[str]
    env: Dict[str, str]


class KernelSpec(BaseModel):
    resource_dir: str
    spec: KernelSpecDetail
    kernel_name: str


class KernelSpecsWrapper(BaseWrapper):
    kernel_specs: List[KernelSpec]
