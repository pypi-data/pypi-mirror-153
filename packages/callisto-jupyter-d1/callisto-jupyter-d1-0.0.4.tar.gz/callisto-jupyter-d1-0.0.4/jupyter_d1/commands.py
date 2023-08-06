import json
from enum import Enum

import requests

from jupyter_d1.settings import settings


class D1CommandType(str, Enum):
    NOTIFY = "notify"


def execute_d1_notify(title: str, message: str):
    requests.post(
        f"{settings.MOTHERSHIP_URL}/work_nodes/{settings.WORK_NODE_ID}/push",
        json={
            "secret": settings.PUSH_NOTE_SECRET_KEY,
            "title": title,
            "message": message,
        },
        timeout=30,
    )


def execute_d1_command(command: str):
    try:
        command_dict = json.loads(command)
        command_type = D1CommandType(command_dict.get("command_type"))
        if command_type == D1CommandType.NOTIFY:
            execute_d1_notify(command_dict["title"], command_dict["message"])
    except Exception:
        pass
