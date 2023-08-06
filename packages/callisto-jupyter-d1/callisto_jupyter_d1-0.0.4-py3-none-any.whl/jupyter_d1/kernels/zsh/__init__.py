from ..kernel_definition import KernelDefinition
from .vars_manager import VarsManager, ZshVarsManager
from .workdir_manager import WorkDirManager, ZshWorkDirManager


class ZshKernelDefinition(KernelDefinition):
    def create_vars_manager(self) -> VarsManager:
        return ZshVarsManager()

    def create_workdir_manager(self, workdir: str) -> WorkDirManager:
        return ZshWorkDirManager(workdir)


kernel_definition = ZshKernelDefinition()
