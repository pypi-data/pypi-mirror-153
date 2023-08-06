from enum import Enum


class ExecutionState(str, Enum):
    busy = "busy"
    idle = "idle"
    starting = "starting"
    unknown = "unknown"
