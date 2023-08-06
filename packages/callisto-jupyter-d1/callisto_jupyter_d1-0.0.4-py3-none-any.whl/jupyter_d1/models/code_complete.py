from typing import Optional

from pydantic import BaseModel


class CodeComplete(BaseModel):
    code: str
    cursor_position: Optional[int] = None
