from ..kernel_definition import KernelDefinition
from .vars_manager import PythonVarsManager, VarsManager
from .workdir_manager import PythonWorkDirManager, WorkDirManager


class PythonKernelDefinition(KernelDefinition):
    def create_vars_manager(self) -> VarsManager:
        return PythonVarsManager()

    def create_workdir_manager(self, workdir: str) -> WorkDirManager:
        return PythonWorkDirManager(workdir)


kernel_definition = PythonKernelDefinition()
