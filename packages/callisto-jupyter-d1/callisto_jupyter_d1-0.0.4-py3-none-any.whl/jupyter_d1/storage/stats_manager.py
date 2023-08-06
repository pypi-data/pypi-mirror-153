from collections import deque
from datetime import datetime
from threading import RLock
from typing import Deque, List, Optional

from asyncblink import signal  # type: ignore
from fastapi.logger import logger

try:
    import psutil  # type: ignore

    has_psutil = True
    logger.debug("Successfully loaded psutil.")
except ImportError:
    has_psutil = False
    logger.debug("Failed to load psutil.  Disabling.")
import asyncio
from itertools import islice

try:
    from pynvml import NVMLError  # type: ignore
    from pynvml import (nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex,
                        nvmlDeviceGetMemoryInfo, nvmlDeviceGetName,
                        nvmlDeviceGetUtilizationRates, nvmlInit)

    nvml_support = True
except ImportError:
    nvml_support = False

from ..models.server_stats import (CPUStats, DiskStats, GPUStats, MemoryStats,
                                   ServerStats)
from ..settings import settings
from ..signals import SERVER_STATS_UPDATE

if nvml_support:
    try:
        nvmlInit()
        device_count = nvmlDeviceGetCount()
    except NVMLError as err:
        print(f"Error with init NVML: {err}")
        nvml_support = False


class StatsManager:
    def __init__(self, max_cache_length: int):
        self.max_cache_length = max_cache_length
        self.cache: Deque[ServerStats] = deque(maxlen=max_cache_length)
        self.cache_lock = RLock()

    def get_stats(self, start, end) -> List[ServerStats]:
        return list(islice(self.cache, start, end))

    def get_latest(self) -> Optional[ServerStats]:
        return self.cache[0] if len(self.cache) > 0 else None

    def put(self, stats: ServerStats):
        with self.cache_lock:
            self.cache.appendleft(stats)

    def get_gpu_stats(self) -> List[GPUStats]:
        if not nvml_support or device_count == 0:
            return []
        gpu_stats_list: List[GPUStats] = []
        for i in range(device_count):
            handle = nvmlDeviceGetHandleByIndex(i)

            gpu_stats = GPUStats()
            try:
                gpu_stats.name = nvmlDeviceGetName(handle)
                util = nvmlDeviceGetUtilizationRates(handle)
                gpu_stats.gpu_usage_percent = util.gpu
                gpu_stats.memory_usage_percent = util.memory
                memory_info = nvmlDeviceGetMemoryInfo(handle)
                gpu_stats.memory_free = memory_info.free
                gpu_stats.memory_used = memory_info.used
                gpu_stats.memory_total = memory_info.total
            except NVMLError as err:
                print(f"Error getting gpu stats: {err}")
            gpu_stats_list.append(gpu_stats)
        return gpu_stats_list

    def collect_server_stats(self) -> ServerStats:
        if has_psutil:
            disk_usage = psutil.disk_usage(settings.ROOT_DIR)
            memory_usage = psutil.virtual_memory()
            cpu_usage = psutil.cpu_percent()
            cpu_load_percent = psutil.getloadavg()[0] / psutil.cpu_count()
        else:
            disk_usage = 0
            memory_usage = 0
            cpu_usage = 0
            cpu_load_percent = 0
        gpu_stat_list = self.get_gpu_stats()
        server_stats = ServerStats(
            timestamp=datetime.now(),
            cpu=CPUStats(percent=cpu_usage, load_percent=cpu_load_percent),
            disk=DiskStats(
                free=disk_usage.free,
                percent=disk_usage.percent,
                total=disk_usage.total,
            ),
            memory=MemoryStats(
                available=memory_usage.available, total=memory_usage.total
            ),
            gpu=gpu_stat_list,
        )
        self.put(server_stats)
        return server_stats

    def dispatch_server_stats(self):
        server_stats = None
        try:
            server_stats = self.collect_server_stats()
        except Exception:
            pass
        if server_stats is not None:
            signal(SERVER_STATS_UPDATE).send(server_stats=server_stats)

    async def server_stats_periodic(self):
        while True:
            self.dispatch_server_stats()
            await asyncio.sleep(settings.SERVER_STATS_POLLING_INTERVAL)
