from typing import Optional

from . import python, r, zsh
from .kernel_definition import KernelDefinition
from .vars_manager import VarsManager  # noqa
from .workdir_manager import WorkDirManager  # noqa


def get_kernel_definition(language: str) -> Optional[KernelDefinition]:
    if language == "python":
        return python.kernel_definition
    elif language in ("zsh", "bash"):
        return zsh.kernel_definition
    elif language == "R":
        return r.kernel_definition
    else:
        return None
