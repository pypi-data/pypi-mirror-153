import json
import os
import platform
import secrets
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, validator

callisto_env = os.getenv("CALLISTO_ENV", "dev").lower()
dotenv_file = f"{callisto_env}.env"


class Settings(BaseSettings):
    pretty_name: str = "Jupyter D1"
    VERSION: int = 1
    OAUTH_TOKEN_URL: str = "/login/access-token"
    META_INFO_FILE: Optional[str] = None
    META_INFO: Dict[str, Any] = {}

    @validator("META_INFO", pre=True)
    def get_meta_info(
        cls, v: Dict[str, Any], values: Dict[str, Any]
    ) -> Dict[str, Any]:
        if len(v.keys()) > 0:
            return v
        meta_info_file = values.get("META_INFO_FILE", None)
        if meta_info_file is not None:
            with open(meta_info_file, "r") as f:
                return json.loads(f.read().rstrip())
        else:
            return {}

    WORK_NODE_ID: Optional[int] = None
    SECRET_KEY: str = ""
    PUSH_NOTE_SECRET_KEY: Optional[str] = None
    MOTHERSHIP_URL: Optional[str] = None

    @validator("WORK_NODE_ID", pre=True)
    def get_work_node_id(
        cls, v: Optional[int], values: Dict[str, Any]
    ) -> Optional[int]:
        meta_info = values.get("META_INFO", None)
        if meta_info is not None and "work_node_id" in meta_info:
            return meta_info["work_node_id"]
        return None

    @validator("SECRET_KEY", pre=True)
    def get_secret_key(cls, v: str, values: Dict[str, Any]) -> str:
        if len(v) > 0:
            return v
        if callisto_env in ("dev", "local"):
            return secrets.token_urlsafe(32)
        meta_info = values.get("META_INFO", None)
        if meta_info is not None and "auth_secret" in meta_info:
            return meta_info["auth_secret"]
        raise ValueError(v)

    @validator("PUSH_NOTE_SECRET_KEY", pre=True)
    def get_push_note_secret_key(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Optional[str]:
        if v is not None and len(v) > 0:
            return v
        meta_info = values.get("META_INFO", None)
        if meta_info is not None and "push_note_secret" in meta_info:
            return meta_info["push_note_secret"]
        return None

    @validator("MOTHERSHIP_URL", pre=True)
    def get_mothership_url(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Optional[str]:
        meta_info = values.get("META_INFO", None)
        if meta_info is not None and "env" in meta_info:
            if meta_info["env"] == "prod":
                return "https://app.callistoapp.com/api/v1"
            else:
                return "https://staging.callistoapp.com/api/v1"
        return None

    # Login enabled for local environment
    LOGIN_ENABLED: bool = callisto_env == "dev"
    LOGIN_TOKEN: Optional[str] = None
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # This is the root directory exposed via WebDAV
    ROOT_DIR: str = os.getcwd()

    @validator("ROOT_DIR")
    def absolute_root_dir(cls, v: str, values: Dict[str, Any]) -> str:
        return str(Path(v).resolve())

    # Rclone settings
    RCLONE_STATS_POLL = True
    RCLONE_STATS_POLLING_INTERVAL = 20  # seconds

    # Server stats
    SERVER_STATS_POLLING_INTERVAL = 5  # seconds
    SERVER_STATS_TTL = 24  # hours

    DAV_SETTINGS: Dict[str, Any] = {}

    @validator("DAV_SETTINGS", pre=True)
    def get_dav_settings(
        cls, v: Dict[str, Any], values: Dict[str, Any]
    ) -> Dict[str, Any]:
        root_dir = values.get("ROOT_DIR", None)
        if root_dir is None:
            raise ValueError(v)
        Path(root_dir).mkdir(parents=True, exist_ok=True)

        return {
            "host": "0.0.0.0",
            "port": 8080,
            "mount_path": "/dav",
            "provider_mapping": {root_dir.lower(): root_dir},
            "verbose": 3,
            "http_authenticator": {
                "domain_controller": "jupyter_d1.dav_auth.JWTDomainController",
                "accept_basic": True,
                "accept_digest": False,
                "default_to_digest": False,
            },
            # Taken from default config
            # (https://wsgidav.readthedocs.io/en/latest/user_guide_configure.html)  # noqa
            "dir_browser": {
                # Render HTML listing for GET requests on collections
                "enable": True,
                # List of fnmatch patterns:
                "ignore": [
                    ".DS_Store",  # macOS folder meta data
                    "._*",  # macOS hidden data files
                    "Thumbs.db",  # Windows image previews
                ],
                "icon": True,
                # Raw HTML code, appended as footer (True: use a default)
                "response_trailer": True,
                "show_user": True,  # Show authenticated user an realm
                # Send <dm:mount> response if request URL contains '?davmount'
                "davmount": False,
                # Invoke MS Offce documents for editing using WebDAV
                "ms_sharepoint_support": True,
                # The path to the directory that contains template.html and
                # associated assets.
                # The default is the htdocs directory within the dir_browser
                # directory.
                "htdocs_path": None,
            },
        }

    WATCHDOG_IGNORE_PATTERNS: List[str] = [".DS_Store", "._*"]
    WATCHDOG_ENABLED: bool = False

    @validator("WATCHDOG_ENABLED")
    def get_watchdog_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        if v is True:
            return True
        meta_info = values.get("META_INFO", None)
        if meta_info is not None and "env" in meta_info:
            if meta_info["env"] == "test":
                return True
        if platform.system().startswith("Darwin"):
            return False
        return True

    # Number of elements (approximately) at which to abbreviate variables
    # in the variable explorer
    VAR_ABBREV_LEN: int = 50

    LOAD_CALLISTOR_FROM_GITHUB: bool = True
    CALLISTOR_GITHUB_BRANCH: str = "dev"

    @validator("CALLISTOR_GITHUB_BRANCH", pre=True)
    def get_callistor_branch(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Optional[str]:
        meta_info = values.get("META_INFO", None)
        if meta_info is not None and "env" in meta_info:
            if meta_info["env"] == "prod":
                return "master"
        return "dev"

    class Config:
        case_sensitive = True
        env_prefix = "CALLISTO_"
        env_file = dotenv_file


settings = Settings()
