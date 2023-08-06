from pydantic import BaseModel

from .base_wrapper import BaseWrapper


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str


class TokenWrapper(BaseWrapper):
    token: Token
