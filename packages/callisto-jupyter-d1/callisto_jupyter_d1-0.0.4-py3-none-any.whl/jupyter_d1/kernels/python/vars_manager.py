import json
from typing import List, Optional

from fastapi.logger import logger

from ...models.kernel_variable import KernelVariable
from ...settings import settings
from ...utils import NotebookNode
from ..vars_manager import VarsManager

# Prints list of current vars to stdout.
# Strange var names used to avoid affecting users
# variables.
raw_get_vars_code = """
try:
    from callisto import format_vars as __d1_format_vars
    print(__d1_format_vars(vars(), abbrev_len={abbrev_len}))
except Exception as e:
    print(e)
"""  # noqa

raw_get_single_var_code = """
try:
    from callisto import format_var as __d1_format_var
    print(__d1_format_var({var_name}, "{var_name}", abbrev_len=None))
except Exception as e:
    print(e)
"""  # noqa


class PythonVarsManager(VarsManager):
    def get_vars_code(self) -> str:
        return raw_get_vars_code.format(abbrev_len=settings.VAR_ABBREV_LEN)

    def get_single_var_code(self, var_name: str) -> str:
        return raw_get_single_var_code.format(var_name=var_name)

    def parse_vars_response(
        self, vars_response: NotebookNode
    ) -> List[KernelVariable]:
        vars: List[KernelVariable] = []
        if "text" not in vars_response:
            return vars
        try:
            json_vars = json.loads(vars_response.text)
            for json_var in json_vars:
                vars.append(
                    KernelVariable(
                        name=json_var.get("name"),
                        type=json_var.get("type"),
                        abbreviated=json_var.get("abbreviated"),
                        value=json_var.get("value"),
                        summary=json_var.get("summary"),
                    )
                )
        except Exception as e:
            logger.debug(
                f"Exception parsing vars for python kernel: {e}, "
                f"{vars_response.text}"
            )
        return vars

    def parse_single_var_response(
        self, var_response: NotebookNode
    ) -> Optional[KernelVariable]:
        var = None
        if "text" not in var_response:
            return var
        try:
            json_var = json.loads(var_response.text)
            var = KernelVariable(
                name=json_var.get("name"),
                type=json_var.get("type"),
                abbreviated=json_var.get("abbreviated"),
                value=json_var.get("value"),
                summary=json_var.get("summary"),
            )
        except Exception as e:
            logger.debug(
                f"Exception parsing var for python kernel: {e}, "
                f"{var_response.text}"
            )
        return var
