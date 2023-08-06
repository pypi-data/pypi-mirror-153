from typing import List, Optional

from pydantic import BaseModel

from .base_wrapper import BaseWrapper
from .JSONType import JSONType


class KernelVariable(BaseModel):
    name: str
    type: Optional[str]
    abbreviated: Optional[bool] = False
    value: JSONType
    summary: Optional[str]


class KernelVariableWrapper(BaseWrapper):
    single_var: KernelVariable


class KernelVariablesWrapper(BaseWrapper):
    vars: List[KernelVariable]
