import json

from fastapi import Depends, Header, HTTPException, WebSocket, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
from pydantic import ValidationError

from .models.permission import Permission
from .models.token import TokenPayload
from .settings import settings

ALGORITHM = "HS256"

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=settings.OAUTH_TOKEN_URL)


def extract_permission(token: str) -> Permission:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    token_data = TokenPayload(**payload)
    permission_dict = json.loads(token_data.sub)
    return Permission(**permission_dict)


def get_current_permission(
    token: str = Depends(reusable_oauth2),
) -> Permission:
    try:
        return extract_permission(token)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


def read_access(
    permission: Permission = Depends(get_current_permission),
) -> bool:
    if (
        permission.read_access is not True
        and permission.write_access is not True
    ):
        raise HTTPException(status_code=403, detail="Inadequeate permissions")
    return True


def write_access(
    permission: Permission = Depends(get_current_permission),
) -> bool:
    if permission.write_access is not True:
        raise HTTPException(status_code=403, detail="Inadequeate permissions")
    return True


# Browser cant connect with this method. Javascript doesn't
# allow headers (like Authorization) to be customized when connecting to a
# websocket. If browser support is needed in the future, may consider a
# ticket-based approach like the one detailed here:
# https://devcenter.heroku.com/articles/websocket-security#authentication-authorization  # noqa
async def get_current_permission_websocket(
    websocket: WebSocket, authorization: str = Header(None)
) -> Permission:
    try:
        assert authorization is not None
        splits = authorization.split(" ")
        assert len(splits) > 1
        token = splits[1]
        return extract_permission(token)
    except (jwt.JWTError, ValidationError, AssertionError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=403, detail="Inadequeate permissions")


async def read_access_websocket(
    websocket: WebSocket,
    permission: Permission = Depends(get_current_permission_websocket),
) -> bool:
    if (
        permission.read_access is not True
        and permission.write_access is not True
    ):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=403, detail="Inadequeate permissions")
    return True


async def write_access_websocket(
    websocket: WebSocket,
    permission: Permission = Depends(get_current_permission_websocket),
) -> bool:
    if permission.write_access is not True:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=403, detail="Inadequeate permissions")
    return True
