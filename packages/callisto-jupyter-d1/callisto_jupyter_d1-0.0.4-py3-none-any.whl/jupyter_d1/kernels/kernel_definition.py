from abc import ABC, abstractmethod

from .vars_manager import VarsManager
from .workdir_manager import WorkDirManager


class KernelDefinition(ABC):
    @abstractmethod
    def create_vars_manager(self) -> VarsManager:
        raise NotImplementedError

    @abstractmethod
    def create_workdir_manager(self, workdir: str) -> WorkDirManager:
        raise NotImplementedError
