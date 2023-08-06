import asyncio
from datetime import datetime
from typing import AsyncGenerator, Dict

import pytest  # type: ignore
from async_asgi_testclient import TestClient  # type: ignore
from pytest_mock import MockFixture  # type: ignore

from jupyter_d1 import app
from jupyter_d1.models.server_stats import (CPUStats, DiskStats, GPUStats,
                                            MemoryStats, ServerStats)
from jupyter_d1.settings import settings

from .utils import wait_for_event


@pytest.fixture()
async def client() -> AsyncGenerator:
    async with TestClient(app) as c:
        yield c


@pytest.fixture()
async def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    r = await client.get(
        "/login/access-token", headers={"Authorization": "test9token_4"}
    )
    token = r.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


class TestStats:
    @pytest.mark.asyncio
    async def test_get_stats(
        self, client: TestClient, superuser_token_headers: Dict[str, str],
    ):
        await asyncio.sleep(1)
        response = await client.get(
            f"/server/stats", headers=superuser_token_headers
        )
        assert response.status_code == 200
        stats = response.json()["server_stats"]
        assert len(stats) >= 1
        assert stats[0]["timestamp"] is not None
        assert stats[0]["disk"]["free"] is not None
        assert stats[0]["disk"]["percent"] is not None
        assert stats[0]["memory"]["available"] is not None
        assert stats[0]["memory"]["total"] is not None
        assert stats[0]["cpu"]["percent"] is not None
        assert stats[0]["cpu"]["load_percent"] is not None
        assert stats[0]["gpu"] == []

    @pytest.mark.asyncio
    async def test_get_latest_stats(
        self, client: TestClient, superuser_token_headers: Dict[str, str],
    ):
        await asyncio.sleep(1)
        response = await client.get(
            f"/server/latest_stats", headers=superuser_token_headers
        )
        assert response.status_code == 200
        stats = response.json()["server_stats"]
        assert stats["timestamp"] is not None
        assert stats["disk"]["free"] is not None
        assert stats["disk"]["percent"] is not None
        assert stats["memory"]["available"] is not None
        assert stats["memory"]["total"] is not None
        assert stats["cpu"]["percent"] is not None
        assert stats["cpu"]["load_percent"] is not None
        assert stats["gpu"] == []

    @pytest.mark.asyncio
    async def test_stats_response(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
    ):
        stats_manager = mocker.patch("jupyter_d1.routers.server.stats_manager")
        stats_manager.get_stats.return_value = [
            ServerStats(
                timestamp=datetime(1994, 5, 3, 4, 3, 4),
                disk=DiskStats(free=5, percent=9.3, total=300),
                memory=MemoryStats(available=400, total=953),
                cpu=CPUStats(percent=8.73, load_percent=44.3),
                gpu=[
                    GPUStats(
                        name="rrr30 d",
                        gpu_usage_percent=44.43,
                        memory_usage_percent=8.1,
                        memory_free=4420,
                        memory_used=999,
                        memory_total=1009,
                    )
                ],
            )
        ]
        response = await client.get(
            f"/server/stats", headers=superuser_token_headers
        )
        assert response.status_code == 200
        stats = response.json()["server_stats"]
        assert len(stats) == 1
        assert stats[0]["timestamp"] == "1994-05-03T04:03:04"
        assert stats[0]["disk"]["free"] == 5
        assert stats[0]["disk"]["percent"] == 9.3
        assert stats[0]["disk"]["total"] == 300
        assert stats[0]["memory"]["available"] == 400
        assert stats[0]["memory"]["total"] == 953
        assert stats[0]["cpu"]["percent"] == 8.73
        assert stats[0]["cpu"]["load_percent"] == 44.3
        assert len(stats[0]["gpu"]) == 1
        assert stats[0]["gpu"][0]["name"] == "rrr30 d"
        assert stats[0]["gpu"][0]["gpu_usage_percent"] == 44.43
        assert stats[0]["gpu"][0]["memory_usage_percent"] == 8.1
        assert stats[0]["gpu"][0]["memory_free"] == 4420
        assert stats[0]["gpu"][0]["memory_used"] == 999
        assert stats[0]["gpu"][0]["memory_total"] == 1009

    @pytest.mark.asyncio
    async def test_get_environment(
        self, client: TestClient, superuser_token_headers: Dict[str, str],
    ):
        await asyncio.sleep(1)
        response = await client.get(
            f"/server/environment", headers=superuser_token_headers
        )
        assert response.status_code == 200
        environment = response.json()["environment_info"]
        assert environment["os"]["platform"] is not None
        assert environment["os"]["name"] is not None
        assert environment["os"]["raw_name"] is not None
        assert environment["os"]["uname"] is not None
        assert environment["python"]["version"] is not None
        assert environment["python"]["executable"] is not None
        assert environment["python"]["pythonpath"] is not None
        assert environment["python"]["version_info"] is not None
        assert environment["python"]["packages"] is not None
        assert environment["python"]["version_info"]["major"] is not None
        assert environment["python"]["version_info"]["minor"] is not None
        assert environment["python"]["version_info"]["micro"] is not None
        assert (
            environment["python"]["version_info"]["releaselevel"] is not None
        )
        assert environment["python"]["version_info"]["serial"] is not None
        assert environment["process"]["argv"] is not None
        assert environment["process"]["cwd"] is not None
        assert environment["process"]["user"] is not None
        assert environment["process"]["pid"] is not None
        assert environment["process"]["environ"] is not None
        assert environment["config"] is not None
        if environment.get("conda", None) is not None:
            assert environment["conda"]["version"] is not None
        assert environment["cores"] is not None
        assert environment["version"] == settings.VERSION

    @pytest.mark.asyncio
    async def test_get_version(
        self, client: TestClient, superuser_token_headers: Dict[str, str],
    ):
        response = await client.get(
            f"/server/version", headers=superuser_token_headers
        )
        assert response.json()["version"] == settings.VERSION


class TestStatsWebSocket:
    @pytest.mark.asyncio
    async def test_stats_websocket(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):

        async with client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:

            stats = await wait_for_event(websocket, "server_stats")
            assert stats["server_stats"]["timestamp"] is not None
            assert stats["server_stats"]["disk"]["free"] is not None
            assert stats["server_stats"]["disk"]["percent"] is not None
            assert stats["server_stats"]["disk"]["total"] is not None
            assert stats["server_stats"]["memory"]["available"] is not None
            assert stats["server_stats"]["memory"]["total"] is not None
            assert stats["server_stats"]["cpu"]["percent"] is not None
            assert stats["server_stats"]["cpu"]["load_percent"] is not None
            assert stats["server_stats"]["gpu"] == []


class TestLogWebSocket:
    @pytest.mark.asyncio
    async def test_log_websocket(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):

        async with client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:

            from jupyter_d1.main import logger

            logger.debug("hi hello jjkolq")

            log = await wait_for_event(websocket, "log")
            assert "hi hello jjkolq" in log["log"]
            assert "DEBUG" in log["log"]
