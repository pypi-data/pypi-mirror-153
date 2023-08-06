from ...utils import NotebookNode
from ..workdir_manager import WorkDirManager

raw_import_line = "import os as ___d1os"
raw_chdir_line = "___d1os.chdir('{directory}')"
raw_cwd_line = "print(___d1os.getcwd())"

raw_chdir_code = f"""
{raw_import_line}
{raw_chdir_line}
{raw_cwd_line}
"""
raw_cwd_code = f"""
{raw_import_line}
{raw_cwd_line}"""


class PythonWorkDirManager(WorkDirManager):
    def get_chdir_code(self, directory: str) -> str:
        return raw_chdir_code.format(directory=directory)

    def get_cwd_code(self) -> str:
        return raw_cwd_code

    def parse_chdir_response(self, response: NotebookNode) -> str:
        return response.text.strip()

    def parse_cwd_response(self, response: NotebookNode) -> str:
        return response.text.strip()
