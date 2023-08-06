import asyncio
from typing import Any

import requests
from asyncblink import signal  # type: ignore
from fastapi import APIRouter, Depends, Request

from jupyter_d1.signals import RCLONE_UPDATE

from ..d1_response import D1Response
from ..deps import write_access
from ..settings import settings

router = APIRouter(default_response_class=D1Response)


@router.post("/{api_path:path}", dependencies=[Depends(write_access)])
async def rclone_api(api_path: str, request: Request) -> Any:
    body = await request.body()
    r = requests.post(
        f"http://127.0.0.1:5572/{api_path}",
        params=request.query_params,
        headers=request.headers,
        data=body,
    )
    return r.json()


def dispatch_rclone_stats():
    r = None
    try:
        r = requests.post(f"http://127.0.0.1:5572/core/stats", timeout=3)
    except Exception:
        pass
    if r is not None:
        signal(RCLONE_UPDATE).send(stats=r.json())


async def stats_periodic():
    while True:
        dispatch_rclone_stats()
        await asyncio.sleep(settings.RCLONE_STATS_POLLING_INTERVAL)
