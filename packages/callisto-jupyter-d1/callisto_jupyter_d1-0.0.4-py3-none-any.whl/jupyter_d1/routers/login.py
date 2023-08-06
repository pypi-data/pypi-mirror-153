import json
from datetime import timedelta
from typing import Any, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.encoders import jsonable_encoder

from .. import deps, security
from ..models.permission import Permission, PermissionWrapper
from ..models.token import TokenWrapper
from ..settings import settings

router = APIRouter()


@router.get("/login/access-token", response_model=TokenWrapper)
def login_access_token(authorization: Optional[str] = Header(None)) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    if settings.LOGIN_ENABLED is not True and settings.LOGIN_TOKEN is None:
        raise HTTPException(
            400, "Login not enabled, login with the Callisto mothership"
        )
    if (
        settings.LOGIN_TOKEN is not None
        and settings.LOGIN_TOKEN != authorization
    ):
        raise HTTPException(401, "Login token does not match")

    permission = Permission(
        id=-1, user_id=-1, work_node_id=-1, write_access=True, read_access=True
    )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = {
        "access_token": security.create_access_token(
            json.dumps(jsonable_encoder(permission)),
            expires_delta=access_token_expires,
        ),
        "token_type": "bearer",
    }
    return TokenWrapper(token=token)


@router.post("/login/test-token", response_model=PermissionWrapper)
def test_token(
    permission: Permission = Depends(deps.get_current_permission),
) -> Any:
    """
    Test access token
    """
    return PermissionWrapper(permission=permission)
