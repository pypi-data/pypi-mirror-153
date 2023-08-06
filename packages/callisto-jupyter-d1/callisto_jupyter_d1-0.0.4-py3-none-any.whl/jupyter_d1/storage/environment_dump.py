import imp
import json
import os
import platform
import subprocess
import sys

from fastapi.logger import logger

try:
    import psutil  # type: ignore

    has_psutil = True
    logger.debug("Successfully loaded psutil.")
except ImportError:
    has_psutil = False
    logger.debug("Failed to load psutil.  Disabling.")
from typing import Any, Dict, Optional

from ..models.environment_info import (CondaInfo, EnvironmentInfo, OSInfo,
                                       ProcessInfo, PythonInfo,
                                       PythonVersionInfo)
from ..settings import settings

# Based on
# https://github.com/Runscope/healthcheck/blob/master/healthcheck/__init__.py


class EnvironmentDump(object):
    def dump_environment(self) -> EnvironmentInfo:
        if has_psutil:
            cpu_count = psutil.cpu_count()
        else:
            cpu_count = 0
        return EnvironmentInfo(
            os=self.get_os(),
            python=self.get_python(),
            config=self.get_config(),
            process=self.get_process(),
            conda=self.get_conda(),
            cores=cpu_count,
            version=settings.VERSION,
        )

    def get_os(self) -> OSInfo:
        raw_name = platform.system()
        name = raw_name
        if raw_name.startswith("Darwin"):
            name = "macOS"
        return OSInfo(
            platform=sys.platform,
            name=name,
            raw_name=raw_name,
            uname=dict(platform.uname()._asdict()),
        )

    def get_config(self) -> Dict[str, Any]:
        return self.safe_dump(settings.dict())

    def get_python(self) -> PythonInfo:
        python_info = PythonInfo(
            version=sys.version,
            executable=sys.executable,
            pythonpath=sys.path,
            version_info=PythonVersionInfo(
                major=sys.version_info.major,
                minor=sys.version_info.minor,
                micro=sys.version_info.micro,
                releaselevel=sys.version_info.releaselevel,
                serial=sys.version_info.serial,
            ),
        )
        if imp.find_module("pkg_resources"):
            import pkg_resources

            packages = dict(
                [
                    (p.project_name, p.version)
                    for p in pkg_resources.working_set
                ]
            )
            python_info.packages = packages

        return python_info

    def get_conda(self) -> Optional[CondaInfo]:
        try:
            process = subprocess.run(
                ["conda", "--version"], stdout=subprocess.PIPE
            )
            version = process.stdout.decode("utf-8")
            return CondaInfo(version=version)
        except Exception:
            return None

    def get_login(self):
        # Based on https://github.com/gitpython-developers/GitPython/pull/43/
        # Fix for 'Inappopropirate ioctl for device' on posix systems.
        if os.name == "posix":
            import pwd

            username = pwd.getpwuid(os.geteuid()).pw_name
        else:
            username = os.environ.get(
                "USER", os.environ.get("USERNAME", "UNKNOWN")
            )
            if username == "UNKNOWN" and hasattr(os, "getlogin"):
                username = os.getlogin()
        return username

    def get_process(self) -> ProcessInfo:
        return ProcessInfo(
            argv=sys.argv,
            cwd=os.getcwd(),
            user=self.get_login(),
            pid=os.getpid(),
            environ=self.safe_dump(os.environ),
        )

    def safe_dump(self, dictionary) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for key in dictionary.keys():
            if (
                key.lower().endswith("key")
                or key.lower().endswith("token")
                or key.lower().endswith("pass")
            ):
                # Try to avoid listing passwords and access tokens or
                # keys in the output
                result[key] = "********"
            else:
                try:
                    json.dumps(dictionary[key])
                    result[key] = dictionary[key]
                except TypeError:
                    pass
        return result
