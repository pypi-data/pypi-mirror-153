from datetime import datetime, timedelta
from typing import Dict

import pytest  # type: ignore
from async_asgi_testclient import (  # type: ignore
    TestClient as WebSocketTestClient
)
from fastapi.testclient import TestClient
from pytest_mock import MockFixture  # type: ignore

from .utils import wait_for_event


def test_rclone(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    mocker: MockFixture,
):
    mock_requests = mocker.patch("jupyter_d1.routers.rclone.requests")
    mock_requests.post().json.return_value = {"pldefe": "fj39499"}
    response = client.post(
        "/rclone/config/dump", headers=superuser_token_headers
    )
    assert response.status_code == 200
    # print(response.json())
    assert response.json() == {"pldefe": "fj39499"}
    assert (
        mock_requests.post.call_args[0][0]
        == "http://127.0.0.1:5572/config/dump"
    )


def test_rclone_query_params(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    mocker: MockFixture,
):
    mock_requests = mocker.patch("jupyter_d1.routers.rclone.requests")
    mock_requests.post().json.return_value = {"gg": "754d"}
    response = client.post(
        "/rclone/config/get",
        headers=superuser_token_headers,
        params={"name": "gdrive"},
    )
    assert response.status_code == 200
    # print(response.json())
    assert response.json() == {"gg": "754d"}
    assert (
        mock_requests.post.call_args[0][0]
        == "http://127.0.0.1:5572/config/get"
    )
    assert dict(mock_requests.post.call_args[1]["params"]) == {
        "name": "gdrive"
    }


def test_rclone_post_data(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    mocker: MockFixture,
):
    mock_requests = mocker.patch("jupyter_d1.routers.rclone.requests")
    mock_requests.post().json.return_value = {"polnd": "logkj"}
    superuser_token_headers["Content-Type"] = "application/json"
    response = client.post(
        "/rclone/options/set",
        headers=superuser_token_headers,
        data='{"vfs": {"CacheMaxSize": 100}}',
    )
    assert response.status_code == 200
    # print(response.json())
    assert response.json() == {"polnd": "logkj"}
    # mock_requests.post.assert_called_once()
    # print(mock_requests.post.calls)
    assert (
        mock_requests.post.call_args[0][0]
        == "http://127.0.0.1:5572/options/set"
    )
    assert (
        mock_requests.post.call_args[1]["data"]
        == b'{"vfs": {"CacheMaxSize": 100}}'
    )


@pytest.fixture()
async def superuser_token_headers(
    websocket_client: WebSocketTestClient,
) -> Dict[str, str]:
    r = await websocket_client.get(
        "/login/access-token", headers={"Authorization": "test9token_4"}
    )
    token = r.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


@pytest.mark.asyncio
async def test_rclone_websocket(
    websocket_client: WebSocketTestClient,
    superuser_token_headers: Dict[str, str],
    mocker: MockFixture,
):
    mock_requests = mocker.patch("jupyter_d1.routers.rclone.requests")
    mock_requests.post().json.return_value = {"polnd": "logkj"}

    async with websocket_client.websocket_connect(
        f"/server/ws", headers=superuser_token_headers
    ) as websocket:
        time = datetime.now()

        async def assert_stats():
            resp = await wait_for_event(websocket, "rclone_stats")
            assert resp == {"rclone_stats": {"polnd": "logkj"}}
            assert (
                time - datetime.now() - timedelta(seconds=3)
            ).microseconds < 1e6

        for i in range(3):
            await assert_stats()
