from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base_wrapper import BaseWrapper


class OSInfo(BaseModel):
    platform: str
    name: str
    raw_name: str
    uname: Dict[str, Any]


class PythonVersionInfo(BaseModel):
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


class PythonInfo(BaseModel):
    version: str
    executable: str
    pythonpath: List[str]
    version_info: PythonVersionInfo
    packages: Optional[Dict[str, str]]


class ProcessInfo(BaseModel):
    argv: List[str]
    cwd: str
    user: str
    pid: int
    environ: Dict[str, Any]


class CondaInfo(BaseModel):
    version: str


class EnvironmentInfo(BaseModel):
    os: OSInfo
    python: PythonInfo
    config: Dict[str, Any]
    process: ProcessInfo
    conda: Optional[CondaInfo]
    cores: int
    version: int


class EnvironmentInfoWrapper(BaseWrapper):
    environment_info: EnvironmentInfo


class Version(BaseModel):
    version: int
