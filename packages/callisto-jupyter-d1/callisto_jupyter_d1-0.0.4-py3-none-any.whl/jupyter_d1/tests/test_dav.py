import asyncio
import os
import pathlib
import platform
import shutil
from typing import Dict
from unittest import TestCase

import pytest  # type: ignore
from async_asgi_testclient import (  # type: ignore
    TestClient as WebSocketTestClient
)
from fastapi import WebSocket
from fastapi.testclient import TestClient
from pytest_mock import MockFixture  # type: ignore

from jupyter_d1.settings import settings

from .test_notebooks_websocket import upload_notebook
from .utils import (get_permissionless_token, get_read_only_token,
                    get_superuser_token, wait_for_event, workdir_1)

is_mac = platform.system().startswith("Darwin")


class TestDav:
    def test_dav_auth(
        self, client: TestClient,
    ):
        response = client.get("/dav")
        assert response.status_code == 401

        response = client.get(f"/dav/", auth=(get_permissionless_token(), ""))
        assert response.status_code == 401

        # Alias of / to ROOT_DIR was removed, make sure it doesn't work
        response = client.get(f"/dav/", auth=(get_read_only_token(), ""))
        assert response.status_code == 404

        response = client.get(
            f"/dav{settings.ROOT_DIR}", auth=(get_read_only_token(), "")
        )
        assert response.status_code == 200

        response = client.get(
            f"/dav{settings.ROOT_DIR}", auth=(get_superuser_token(), "")
        )
        assert response.status_code == 200

    def test_dav_provider_added_for_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        shutil.copyfile(
            "jupyter_d1/tests/notebooks/simple.ipynb",
            "jupyter_d1/tests/notebooks/simple_copy.ipynb",
        )
        other_directory = f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        token = get_read_only_token()
        response = client.get(f"/dav{other_directory}", auth=(token, ""))
        assert response.status_code == 404

        path = f"{other_directory}/simple_copy.ipynb"
        response = client.get(
            f"/notebooks/open/?filepath={path}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == other_directory
        )
        response = client.get(f"/dav{other_directory}", auth=(token, ""))
        assert response.status_code == 200

        response = client.delete(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = client.get(f"/dav{other_directory}", auth=(token, ""))
        assert response.status_code == 404

        os.remove("jupyter_d1/tests/notebooks/simple_copy.ipynb")

    def test_dav_provider_added_for_notebook_set_working_dir(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        shutil.copyfile(
            "jupyter_d1/tests/notebooks/simple.ipynb",
            "jupyter_d1/tests/notebooks/simple_copy.ipynb",
        )
        other_directory = f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        working_dir = "/tmp"
        resolved_work_dir = str(pathlib.Path(working_dir).resolve())
        token = get_read_only_token()
        response = client.get(f"/dav{resolved_work_dir}", auth=(token, ""))
        assert response.status_code == 404

        path = f"{other_directory}/simple_copy.ipynb"
        response = client.get(
            f"/notebooks/open/?filepath={path}",
            headers=superuser_token_headers,
            params={"working_directory": working_dir},
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == resolved_work_dir
        )
        response = client.get(f"/dav{resolved_work_dir}", auth=(token, ""))
        assert response.status_code == 200

        response = client.delete(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = client.get(f"/dav{resolved_work_dir}", auth=(token, ""))
        assert response.status_code == 404

        os.remove("jupyter_d1/tests/notebooks/simple_copy.ipynb")

    def test_dav_provider_notebook_in_subdirectory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        If notebook is in subdirectory of d1's working directory, 
        dav should work regardless of whether the notebook is open.
        """
        pathlib.Path(f"{settings.ROOT_DIR}/some_nbs").mkdir(exist_ok=True)
        shutil.copyfile(
            "jupyter_d1/tests/notebooks/simple.ipynb",
            f"{settings.ROOT_DIR}/some_nbs/simple_copy.ipynb",
        )

        nb_dir = f"{settings.ROOT_DIR}/some_nbs"
        working_dir = f"{settings.ROOT_DIR}/some_nbs"
        token = get_read_only_token()
        response = client.get(f"/dav{working_dir}", auth=(token, ""))
        assert response.status_code == 200

        path = f"{nb_dir}/simple_copy.ipynb"
        response = client.get(
            f"/notebooks/open/?filepath={path}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == working_dir
        )
        response = client.get(f"/dav{working_dir}", auth=(token, ""))
        assert response.status_code == 200

        response = client.delete(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = client.get(f"/dav{working_dir}", auth=(token, ""))
        assert response.status_code == 200

        shutil.rmtree(f"{settings.ROOT_DIR}/some_nbs")


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "clear_notebook_directory", "clear_notebook_directory_2"
)
class TestWatchdogWebSocket:
    async def clear_websocket_queue(self, websocket, wait_for=0.3):
        while True:
            try:
                await asyncio.wait_for(websocket.receive_json(), wait_for)
            except Exception:
                break

    async def create_dir(self, websocket: WebSocket, ututils: TestCase):
        os.mkdir(f"{settings.ROOT_DIR}/new_dir")

        resp = await wait_for_event(websocket, "watchdog_event")
        resp2 = await wait_for_event(websocket, "watchdog_event")

        ututils.assertCountEqual(
            [resp, resp2],
            [
                {
                    "watchdog_event": {
                        "event_type": "created",
                        "src_path": f"{settings.ROOT_DIR}/new_dir",
                        "dest_path": None,
                    }
                },
                {
                    "watchdog_event": {
                        "event_type": "modified",
                        "src_path": settings.ROOT_DIR,
                        "dest_path": None,
                    }
                },
            ],
        )

    async def create_file(
        self,
        websocket: WebSocket,
        ututils: TestCase,
        directory: str = settings.ROOT_DIR,
    ):
        with open(f"{directory}/new_file", "w") as f:
            f.write("this is a new file")

        resp1 = await wait_for_event(websocket, "watchdog_event")
        resp2 = await wait_for_event(websocket, "watchdog_event")
        expected = [
            {
                "watchdog_event": {
                    "event_type": "modified",
                    "src_path": f"{directory}",
                    "dest_path": None,
                }
            },
            {
                "watchdog_event": {
                    "event_type": "created",
                    "src_path": f"{directory}/new_file",
                    "dest_path": None,
                }
            },
        ]
        ututils.assertCountEqual([resp1, resp2], expected)

    async def test_create_dir(
        self,
        websocket_client: WebSocketTestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
        mocker: MockFixture,
    ):
        async with websocket_client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:
            # assert False
            await self.create_dir(websocket, ututils)

    async def test_create_file(
        self,
        websocket_client: WebSocketTestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        async with websocket_client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:
            await self.create_file(websocket, ututils)

    async def test_modified_file(
        self,
        websocket_client: WebSocketTestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        async with websocket_client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:
            await self.clear_websocket_queue(websocket)
            await self.create_file(websocket, ututils)

            with open(f"{settings.ROOT_DIR}/new_file", "w") as f:
                f.write("this is an edit")
            expected = [
                {
                    "watchdog_event": {
                        "event_type": "modified",
                        "src_path": f"{settings.ROOT_DIR}/new_file",
                        "dest_path": None,
                    }
                }
            ]
            resps = []
            for _ in expected:
                resps.append(await wait_for_event(websocket, "watchdog_event"))
            for resp in resps:
                assert expected.pop(expected.index(resp)) is not None

    async def test_deleted_file(
        self,
        websocket_client: WebSocketTestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        async with websocket_client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:
            await self.clear_websocket_queue(websocket)
            await self.create_file(websocket, ututils)
            await self.clear_websocket_queue(websocket)

            os.remove(f"{settings.ROOT_DIR}/new_file")

            expected = [
                {
                    "watchdog_event": {
                        "event_type": "modified",
                        "src_path": settings.ROOT_DIR,
                        "dest_path": None,
                    }
                },
                {
                    "watchdog_event": {
                        "event_type": "deleted",
                        "src_path": f"{settings.ROOT_DIR}/new_file",
                        "dest_path": None,
                    }
                },
            ]
            resps = []
            resp1 = await wait_for_event(websocket, "watchdog_event")
            resp2 = await wait_for_event(websocket, "watchdog_event")
            resps = [resp1, resp2]
            # This modified event doesn't appear to happen on linux
            if is_mac:
                resp3 = await wait_for_event(websocket, "watchdog_event")
                resps.append(resp3)
                expected.append(
                    {
                        "watchdog_event": {
                            "event_type": "modified",
                            "src_path": f"{settings.ROOT_DIR}/new_file",
                            "dest_path": None,
                        }
                    }
                )
            ututils.assertCountEqual(resps, expected)

    async def test_nested_updates(
        self,
        websocket_client: WebSocketTestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        async with websocket_client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:
            await self.clear_websocket_queue(websocket)
            await self.create_dir(websocket, ututils)
            await self.create_file(
                websocket, ututils, directory=f"{settings.ROOT_DIR}/new_dir"
            )
            await self.clear_websocket_queue(websocket)
            os.rename(
                f"{settings.ROOT_DIR}/new_dir/new_file",
                f"{settings.ROOT_DIR}/new_file",
            )

            expected = [
                {
                    "watchdog_event": {
                        "event_type": "moved",
                        "src_path": f"{settings.ROOT_DIR}/new_dir/new_file",
                        "dest_path": f"{settings.ROOT_DIR}/new_file",
                    }
                },
                {
                    "watchdog_event": {
                        "event_type": "modified",
                        "src_path": f"{settings.ROOT_DIR}/new_dir",
                        "dest_path": None,
                    }
                },
            ]

            # More differences between mac and linux
            if is_mac:
                expected.append(
                    {
                        "watchdog_event": {
                            "event_type": "modified",
                            "src_path": f"{settings.ROOT_DIR}/"
                            "new_dir/new_file",
                            "dest_path": None,
                        }
                    }
                )
            else:
                expected.append(
                    {
                        "watchdog_event": {
                            "event_type": "modified",
                            "src_path": "/tmp/jupyter_d1_test",
                            "dest_path": None,
                        }
                    }
                )
            resps = []
            for _ in expected:
                resps.append(await wait_for_event(websocket, "watchdog_event"))
            ututils.assertCountEqual(resps, expected)

    async def test_added_for_notebook(
        self,
        websocket_client: WebSocketTestClient,
        superuser_token_headers: Dict[str, str],
    ):
        """
        Monitor new workdir for notebook, and stop monitoring when changed.
        """
        async with websocket_client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:
            new_workdir = workdir_1

            # Should not get notified of directory changes yet
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir")
            with pytest.raises(AssertionError):
                await wait_for_event(websocket, "watchdog_event")

            # Upload notebook, workdir same as root dir
            uuid = await upload_notebook(
                websocket_client, superuser_token_headers,
            )

            # Change nb workdir
            response = await websocket_client.patch(
                f"/notebooks/{uuid}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": new_workdir},
            )
            assert response.status_code == 200

            # Make sure new nb workdir is now monitored for changes
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir2")
            event = await wait_for_event(websocket, "watchdog_event")
            assert event == {
                "watchdog_event": {
                    "event_type": "created",
                    "src_path": f"{new_workdir}/new_dir2",
                    "dest_path": None,
                }
            }

            # Change nb workdir back to root dir
            response = await websocket_client.patch(
                f"/notebooks/{uuid}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": settings.ROOT_DIR},
            )
            assert response.status_code == 200

            # Make sure previous nb workdir is no longer monitored
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir3")
            with pytest.raises(AssertionError):
                await wait_for_event(websocket, "watchdog_event")

    async def test_change_monitored_directory(
        self,
        websocket_client: WebSocketTestClient,
        superuser_token_headers: Dict[str, str],
    ):
        """Monitor more specific directory when possible"""
        async with websocket_client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:
            new_workdir = workdir_1

            # Should not get notified of directory changes yet
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir")
            with pytest.raises(AssertionError):
                await wait_for_event(websocket, "watchdog_event")

            # Upload notebook, workdir same as root dir
            uuid = await upload_notebook(
                websocket_client, superuser_token_headers
            )

            # Change nb workdir
            response = await websocket_client.patch(
                f"/notebooks/{uuid}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": new_workdir},
            )
            assert response.status_code == 200

            # Make sure new nb workdir is now monitored for changes
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir2")
            event = await wait_for_event(websocket, "watchdog_event")
            assert event == {
                "watchdog_event": {
                    "event_type": "created",
                    "src_path": f"{new_workdir}/new_dir2",
                    "dest_path": None,
                }
            }

            # Change nb workdir to sub directory
            response = await websocket_client.patch(
                f"/notebooks/{uuid}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": f"{new_workdir}/new_dir"},
            )
            assert response.status_code == 200

            # Make sure parent dir is no longer monitored
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir3")
            with pytest.raises(AssertionError):
                await wait_for_event(websocket, "watchdog_event")

            # Make sure sub dir is now monitored for changes
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir/newer_dir")
            event = await wait_for_event(websocket, "watchdog_event")
            assert event == {
                "watchdog_event": {
                    "event_type": "created",
                    "src_path": f"{new_workdir}/new_dir/newer_dir",
                    "dest_path": None,
                }
            }

    async def test_multiple_notebooks(
        self,
        websocket_client: WebSocketTestClient,
        superuser_token_headers: Dict[str, str],
    ):
        """
        Multiple notebooks, one with workdir that is parent dir of the other's
        workdir. Then switch the parent workdir to a sub dir, make sure both
        subdirs are still monitored, but not the parent
        """
        async with websocket_client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:
            new_workdir = workdir_1

            # Should not get notified of directory changes yet
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir")
            with pytest.raises(AssertionError):
                await wait_for_event(websocket, "watchdog_event")

            # Upload notebook, workdir same as root dir
            uuid = await upload_notebook(
                websocket_client, superuser_token_headers,
            )
            uuid2 = await upload_notebook(
                websocket_client,
                superuser_token_headers,
                filename="other_simple.ipynb",
            )
            await asyncio.sleep(3.0)

            # Change nb workdir
            response = await websocket_client.patch(
                f"/notebooks/{uuid}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": new_workdir},
            )
            assert response.status_code == 200
            response = await websocket_client.patch(
                f"/notebooks/{uuid2}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": f"{new_workdir}/new_dir"},
            )
            assert response.status_code == 200

            # Make sure new nb workdir is now monitored for changes
            await self.clear_websocket_queue(websocket)
            await asyncio.sleep(10.0)
            os.mkdir(f"{new_workdir}/new_dir2")
            event = await wait_for_event(websocket, "watchdog_event")
            assert event == {
                "watchdog_event": {
                    "event_type": "created",
                    "src_path": f"{new_workdir}/new_dir2",
                    "dest_path": None,
                }
            }

            # Change nb workdir to sub directory
            response = await websocket_client.patch(
                f"/notebooks/{uuid}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": f"{new_workdir}/new_dir2"},
            )
            assert response.status_code == 200

            # Make sure parent dir is no longer monitored
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir3")
            with pytest.raises(AssertionError):
                await wait_for_event(websocket, "watchdog_event")

            # Make sure sub dir is still monitored for changes
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir/newer_dir")
            event = await wait_for_event(websocket, "watchdog_event")
            assert event == {
                "watchdog_event": {
                    "event_type": "created",
                    "src_path": f"{new_workdir}/new_dir/newer_dir",
                    "dest_path": None,
                }
            }

            # Make sure other sub dir is now also monitored for changes
            await self.clear_websocket_queue(websocket)
            os.mkdir(f"{new_workdir}/new_dir2/newer_dir2")
            event = await wait_for_event(websocket, "watchdog_event")
            assert event == {
                "watchdog_event": {
                    "event_type": "created",
                    "src_path": f"{new_workdir}/new_dir2/newer_dir2",
                    "dest_path": None,
                }
            }
