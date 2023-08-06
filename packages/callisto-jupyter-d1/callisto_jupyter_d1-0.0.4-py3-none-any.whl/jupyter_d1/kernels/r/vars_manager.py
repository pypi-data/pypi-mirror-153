import json
from typing import List, Optional

from fastapi.logger import logger

from ...models.kernel_variable import KernelVariable
from ...settings import settings
from ...utils import NotebookNode
from ..vars_manager import VarsManager

raw_install_callistor_github_code = """
        if (!("remotes" %in% (.packages()))) {{
            if (length(find.package("remotes", quiet=TRUE)) < 1) {{
                install.packages("remotes")
            }}
        }}
        remotes::install_github("OakCityLabs/callisto-r@{branch}", upgrade="never", quiet=TRUE)
"""  # noqa

raw_install_callistor_cran_code = """
        install.packages("callistor")
"""  # noqa

raw_load_callistor_code = """
if (!("callistor" %in% (.packages()))) {{
    if (length(find.package("callistor", quiet=TRUE)) < 1) {{
        {install_callistor_code}
    }}
    library("callistor")
}}
"""  # noqa

raw_get_vars_code = """
{load_callistor_code}

cat(callistor::format_vars(environment(), {abbrev_len}))
"""  # noqa

# Note: we try to access the var first so it throws if it doesn't exist
raw_get_single_var_code = """
{load_callistor_code}

cat(callistor::format_var(environment(), "{var_name}", NULL))
"""  # noqa


def get_load_callistor_code(from_github=True) -> str:
    return raw_load_callistor_code.format(
        install_callistor_code=raw_install_callistor_github_code.format(
            branch=settings.CALLISTOR_GITHUB_BRANCH
        )
        if from_github
        else raw_install_callistor_cran_code
    )


class RVarsManager(VarsManager):
    def get_vars_code(self) -> str:
        return raw_get_vars_code.format(
            load_callistor_code=get_load_callistor_code(
                settings.LOAD_CALLISTOR_FROM_GITHUB
            ),
            abbrev_len=settings.VAR_ABBREV_LEN,
        )

    def get_single_var_code(self, var_name: str) -> str:
        return raw_get_single_var_code.format(
            load_callistor_code=get_load_callistor_code(
                settings.LOAD_CALLISTOR_FROM_GITHUB
            ),
            var_name=var_name,
        )

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
                        summary=str(json_var.get("summary")),
                        value=json_var.get("value"),
                    )
                )
        except Exception as e:
            print(e)
            logger.debug(
                f"Exception parsing vars for R kernel: {e}, "
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
                f"Exception parsing var for R kernel: {e}, "
                f"{var_response.text}"
            )
        return var
