from pydantic import BaseModel


class ScratchCode(BaseModel):
    code: str
