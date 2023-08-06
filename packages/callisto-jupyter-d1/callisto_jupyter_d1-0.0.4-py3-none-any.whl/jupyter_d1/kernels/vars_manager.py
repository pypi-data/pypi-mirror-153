from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.kernel_variable import KernelVariable
from ..utils import NotebookNode

# TODO: Send updates as diffs


class VarsManager(ABC):
    def __init__(self):
        self._vars = []
        self._tmp_vars = []

    @abstractmethod
    def get_vars_code(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_single_var_code(self, var_name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_vars_response(
        self, vars_response: NotebookNode
    ) -> List[KernelVariable]:
        raise NotImplementedError

    @abstractmethod
    def parse_single_var_response(
        self, var_response: NotebookNode
    ) -> Optional[KernelVariable]:
        return None

    @property
    def vars(self) -> List[KernelVariable]:
        return self._vars

    def parse_output(self, vars_output: NotebookNode):
        vars = self.parse_vars_response(vars_output)
        self._tmp_vars += vars

    def on_request_start(self):
        self._tmp_vars = []

    def on_request_end(self) -> List[KernelVariable]:
        self._vars = self._tmp_vars
        return self._vars
