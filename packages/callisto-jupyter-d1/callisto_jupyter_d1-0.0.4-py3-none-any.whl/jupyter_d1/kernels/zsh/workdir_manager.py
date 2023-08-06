from ...utils import NotebookNode
from ..workdir_manager import WorkDirManager

raw_chdir_code = "cd {directory}"
raw_cwd_code = "pwd"


class ZshWorkDirManager(WorkDirManager):
    def get_chdir_code(self, directory: str) -> str:
        return f"{raw_chdir_code.format(directory=directory)}\n{raw_cwd_code}"

    def get_cwd_code(self) -> str:
        return raw_cwd_code

    def extract_cwd(self, response: NotebookNode) -> str:
        return response.text.strip()

    def parse_chdir_response(self, response: NotebookNode) -> str:
        return self.extract_cwd(response)

    def parse_cwd_response(self, response: NotebookNode) -> str:
        return self.extract_cwd(response)
