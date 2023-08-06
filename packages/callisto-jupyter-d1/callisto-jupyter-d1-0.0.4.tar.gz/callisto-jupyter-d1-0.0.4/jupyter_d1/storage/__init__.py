from ..settings import settings
from .environment_dump import EnvironmentDump
from .kernel_logger import KernelLogger
from .kernel_manager import KernelManager
from .notebook_manager import NBMException  # noqa
from .notebook_manager import NotebookManager
from .stats_manager import StatsManager

kmanager = KernelManager()
manager = NotebookManager(kmanager)
stats_manager = StatsManager(
    settings.SERVER_STATS_POLLING_INTERVAL * settings.SERVER_STATS_TTL * 60
)
environment_dump = EnvironmentDump()

# Instantiate a logger to echo out the messages from the kernels
klogger = KernelLogger()
