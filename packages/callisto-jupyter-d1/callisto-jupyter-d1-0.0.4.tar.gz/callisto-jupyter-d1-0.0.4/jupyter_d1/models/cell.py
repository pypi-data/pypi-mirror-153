from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .JSONType import JSONType
from .kernel_message import KernelMessageWrapper


class CellType(str, Enum):
    code = "code"
    markdown = "markdown"
    raw = "raw"


class CellWrapper(BaseModel):
    cell: JSONType


class CellKernelMessageWrapper(CellWrapper, KernelMessageWrapper):
    pass


class CellsWrapper(BaseModel):
    cells: List[JSONType]


class CellUpdate(BaseModel):
    source: Optional[str] = None
    cell_type: Optional[CellType] = None


class CellAdd(BaseModel):
    source: str = ""
    cell_type: CellType = CellType.code
    before: Optional[UUID] = None
