from ..kernel_definition import KernelDefinition
from .vars_manager import RVarsManager, VarsManager
from .workdir_manager import RWorkDirManager, WorkDirManager


class RKernelDefinition(KernelDefinition):
    def create_vars_manager(self) -> VarsManager:
        return RVarsManager()

    def create_workdir_manager(self, workdir: str) -> WorkDirManager:
        return RWorkDirManager(workdir)


kernel_definition = RKernelDefinition()
