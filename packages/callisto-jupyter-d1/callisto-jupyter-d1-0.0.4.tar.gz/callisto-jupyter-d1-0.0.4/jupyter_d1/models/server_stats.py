from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .base_wrapper import BaseWrapper


class DiskStats(BaseModel):
    free: int
    percent: float
    total: int


class MemoryStats(BaseModel):
    available: int
    total: int


class CPUStats(BaseModel):
    percent: float
    load_percent: float


class GPUStats(BaseModel):
    name: Optional[str]
    gpu_usage_percent: Optional[float]
    memory_usage_percent: Optional[float]
    memory_free: Optional[int]
    memory_used: Optional[int]
    memory_total: Optional[int]


class ServerStats(BaseModel):
    timestamp: datetime
    disk: DiskStats
    memory: MemoryStats
    cpu: CPUStats
    gpu: List[GPUStats]


class ServerStatsWrapper(BaseWrapper):
    server_stats: Optional[ServerStats]


class ServerStatsListWrapper(BaseWrapper):
    server_stats: List[ServerStats]
