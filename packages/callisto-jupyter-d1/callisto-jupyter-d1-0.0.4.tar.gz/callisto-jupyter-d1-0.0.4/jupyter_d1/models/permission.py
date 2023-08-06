from typing import Optional

from pydantic import BaseModel

from .base_wrapper import BaseWrapper


class Permission(BaseModel):
    id: int
    user_id: int
    work_node_id: int
    read_access: Optional[bool]
    write_access: Optional[bool]


class PermissionWrapper(BaseWrapper):
    permission: Permission
