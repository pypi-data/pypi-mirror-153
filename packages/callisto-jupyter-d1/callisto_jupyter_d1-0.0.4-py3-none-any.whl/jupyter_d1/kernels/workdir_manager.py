from abc import ABC, abstractmethod

from ..utils import NotebookNode


class WorkDirManager(ABC):
    def __init__(self, workdir: str):
        self._workdir = workdir

    @property
    def workdir(self) -> str:
        return self._workdir

    @abstractmethod
    def get_chdir_code(self, directory: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_cwd_code(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_chdir_response(self, response: NotebookNode) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_cwd_response(self, response: NotebookNode) -> str:
        raise NotImplementedError

    def parse_chdir_output(self, output: NotebookNode) -> str:
        self._workdir = self.parse_chdir_response(output)
        return self._workdir

    def parse_cwd_output(self, output: NotebookNode) -> str:
        self._workdir = self.parse_cwd_response(output)
        return self._workdir
