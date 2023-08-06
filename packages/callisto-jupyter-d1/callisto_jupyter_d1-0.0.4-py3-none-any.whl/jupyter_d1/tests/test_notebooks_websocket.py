import asyncio
import base64
import os
import pathlib
import shutil
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, List, Optional
from unittest.mock import call

# from fastapi.testclient import TestClient
import pytest  # type: ignore
from async_asgi_testclient import TestClient  # type: ignore
from pytest_mock import MockFixture  # type: ignore

from jupyter_d1 import app
from jupyter_d1.settings import settings

from .utils import (collect_websocket_messages, filter_websocket_collection,
                    get_superuser_token, receive_json, wait_for_event,
                    workdir_1)

# All test coroutines will be treated as marked.
# pytestmark = pytest.mark.asyncio

WEBSOCKET_SLEEP_TIME = 10.1


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


@pytest.fixture(scope="function")
async def clear_notebooks(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> AsyncGenerator:
    yield
    response = await client.delete(
        "/notebooks", headers=superuser_token_headers
    )
    assert response.status_code == 204
    response = await client.get("/notebooks", headers=superuser_token_headers)
    assert response.status_code == 200


async def upload_notebook(
    client: TestClient,
    token_headers: Dict[str, str],
    filename: str = "simple.ipynb",
) -> str:
    nb_filename = f"jupyter_d1/tests/notebooks/{filename}"
    nb_json = open(nb_filename).read()
    response = await client.post(
        "/notebooks/upload",
        query_string={"filename": filename},
        data=nb_json,
        headers=token_headers,
    )
    assert response.status_code == 201
    path = response.json()["path"]

    response = await client.get(
        f"/notebooks/open/?filepath={path}", headers=token_headers
    )
    assert response.status_code == 201
    resp_json = response.json()["notebook"]
    uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

    # Give kernel time to fully start, kernel messages can get
    # dropped otherwise
    await asyncio.sleep(2)
    return uuid


def assert_cell_positions(cells: List[Dict[str, Any]]):
    assert [c["metadata"]["jupyter_d1"]["position"] for c in cells] == list(
        range(0, len(cells))
    )


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestNotebookWebSocket:
    @pytest.mark.asyncio
    async def test_notebook_cell_execute(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            # first two chunks received should be a execution count update and
            # cell_update with an execution_state of 'busy' when processing
            # starts. Order is variable, so here we handle either order.
            def assert_json_content(data, execution_count=None):
                if "cell_update" in data:
                    cell_data = data["cell_update"][0]
                    d1_metadata = cell_data["metadata"]["jupyter_d1"]
                    assert d1_metadata["execution_state"] == "busy"
                    assert d1_metadata["uuid"] == cell_uuid
                    assert cell_data["execution_count"] == execution_count
                    return None
                elif "cell_execution_reply" in data:
                    assert data["cell_execution_reply"]["execution_count"] == 1
                    assert data["cell_execution_reply"]["cell_id"] == cell_uuid
                    assert data["cell_execution_reply"]["parent_id"] == msg_id
                    return 1
                else:
                    raise AssertionError(f"unexpected cell type: {data}")

            data = await receive_json(
                websocket, msg_types=["cell_update", "cell_execution_reply"]
            )
            exec_count = assert_json_content(data)
            data = await receive_json(
                websocket, msg_types=["cell_update", "cell_execution_reply"]
            )
            assert_json_content(data, exec_count)

            # third chunk received should be a cell_update with
            # the new output, and an execution_state of 'busy'
            # since it is still processing
            data = await receive_json(websocket, msg_types=["cell_update"])
            expected = {
                "cell_update": [
                    {
                        "cell_type": "code",
                        "execution_count": 1,
                        "metadata": {
                            "jupyter_d1": {
                                "position": 2,
                                "uuid": cell_uuid,
                                "notebook_uuid": uuid,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [
                            {
                                "data": {"text/plain": "7"},
                                "execution_count": 1,
                                "metadata": {},
                                "output_type": "execute_result",
                            }
                        ],
                        "source": "2+5",
                    }
                ]
            }

            # from pprint import pprint
            # print("data")
            # pprint(data)
            # print("expected")
            # pprint(expected)
            assert data == expected

            # third chunk received should be a cell_update with
            # an execution_state of 'idle' becuase it's all done
            data = await receive_json(websocket, msg_types=["cell_update"])
            d1_metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "idle"

            data = await receive_json(websocket, msg_types=["vars"])
            assert len(data["vars"]) == 14

    @pytest.mark.asyncio
    async def test_notebook_sequential_execute(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell_uuid1 = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid2 = cells[2]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid3 = cells[3]["metadata"]["jupyter_d1"]["uuid"]

        code1 = """import time; time.sleep(1.1); print("checkpoint1")"""
        code2 = """import time; time.sleep(1.2); print("checkpoint2")"""
        code3 = """import time; time.sleep(1.3); print("checkpoint3")"""

        params1 = {"source": code1}
        params2 = {"source": code2}
        params3 = {"source": code3}

        resp1 = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid1}",
            json=params1,
            headers=superuser_token_headers,
        )
        assert resp1.status_code == 200

        resp2 = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid2}",
            json=params2,
            headers=superuser_token_headers,
        )
        assert resp2.status_code == 200

        resp3 = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid3}",
            json=params3,
            headers=superuser_token_headers,
        )
        assert resp3.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            pass

            # await asyncio.sleep(WEBSOCKET_SLEEP_TIME)
            await asyncio.sleep(3.5)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid1}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid2}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid3}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Messages on the web socket can arrive in a slightly different
            # order from run to run.  The 'cell_update' messages arrive arround
            # the same time as some of the cell_execution messages.  It doesn't
            # really matter, but it makes testing tricky.  For a stable test,
            # gather all the responses and split them into two lists, one for
            # cell_update messages and one for all the others.

            # The most important thing for this test is that all the
            # "cell_execution_request" messages arrive first as the cells are
            # queued for execution and the "cell_execution_input",
            # "cell_execution_reply", etc messages show up later as the cells
            # are processed.

            cell_update_msgs = []
            non_cell_update_msgs = []
            for i in range(19):
                data = await receive_json(websocket)
                if "cell_update" in data.keys():
                    cell_update_msgs.append(data)
                else:
                    non_cell_update_msgs.append(data)

            # should get three execution requests
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_request" in data.keys()
            msg_id1 = data["cell_execution_request"]["message_id"]
            assert len(msg_id1) == 35

            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_request" in data.keys()
            msg_id2 = data["cell_execution_request"]["message_id"]
            assert len(msg_id2) == 35

            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_request" in data.keys()
            msg_id3 = data["cell_execution_request"]["message_id"]
            assert len(msg_id3) == 35

            # cell update for the first executing cell
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid1
            )

            # cell_execution_input for the first cell's code being executed
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_input" in data
            assert (
                data["cell_execution_input"]["content"]["code"] == code1
            ), f'Failed to find "{code1}" in cell_stream data: {data}'
            assert (
                data["cell_execution_input"]["parent_id"] == msg_id1
            ), f"Failed to find expected parent_id"

            # stream output for the first cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_stream" in data.keys()
            assert (
                data["cell_stream"]["output"]["text"] == "checkpoint1\n"
            ), f"Failed to find checkpoint1 in cell_stream data: {data}"

            # execution_reply for the end of the first cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_reply" in data.keys()
            assert data["cell_execution_reply"]["parent_id"] == msg_id1

            # cell update with the results of the first cell's execution
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid1
            )

            # cell update for the begining of the second cell's execution
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid2
            )

            # cell_input update with the second cell's code being executed
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_input" in data
            assert (
                data["cell_execution_input"]["content"]["code"] == code2
            ), f'Failed to find "{code2}" in cell_stream data: {data}'
            assert (
                data["cell_execution_input"]["parent_id"] == msg_id2
            ), f"Failed to find expected parent_id"

            # stream output of the second cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_stream" in data.keys()
            assert (
                data["cell_stream"]["output"]["text"] == "checkpoint2\n"
            ), f"Failed to find checkpoint2 in cell_stream data: {data}"

            # exectuion_reply for the end of the second cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_reply" in data.keys()
            assert data["cell_execution_reply"]["parent_id"] == msg_id2

            # cell_update with the results of the second cell
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid2
            )

            # cell_update as the third cell begins execution
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid3
            )

            # cell_execution_input with third cell code about to be executed
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_input" in data
            assert (
                data["cell_execution_input"]["content"]["code"] == code3
            ), f'Failed to find "{code3}" in cell_stream data: {data}'
            assert (
                data["cell_execution_input"]["parent_id"] == msg_id3
            ), f"Failed to find expected parent_id"

            # stream output of the third cell
            data = non_cell_update_msgs.pop(0)
            assert "cell_stream" in data.keys()
            assert (
                data["cell_stream"]["output"]["text"] == "checkpoint3\n"
            ), f"Failed to find checkpoint3 in cell_stream data: {data}"

            # execution reply for finishing the third cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_reply" in data.keys()
            assert data["cell_execution_reply"]["parent_id"] == msg_id3

            # cell_update for cell three with the output
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid3
            )

            # var update
            data = non_cell_update_msgs.pop(0)
            assert "vars" in data.keys()

    @pytest.mark.asyncio
    async def test_cell_patch_and_execute(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "7-9"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            expected = {
                "cell_update": [
                    {
                        "cell_type": "code",
                        "execution_count": 1,
                        "metadata": {
                            "jupyter_d1": {
                                "position": 1,
                                "uuid": cell_uuid,
                                "notebook_uuid": uuid,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [
                            {
                                "data": {"text/plain": "-2"},
                                "execution_count": 1,
                                "metadata": {},
                                "output_type": "execute_result",
                            }
                        ],
                        "source": "7-9",
                    }
                ]
            }

            patch_json = response.json()
            # response should contain both the 'cell','kernel_message' wrappers
            assert "cell" in patch_json.keys()
            msg_id = response.json()["kernel_message"]["message_id"]
            assert len(msg_id) == 35

            exec_reply = await receive_json(
                websocket, msg_types=["cell_execution_reply"]
            )
            assert exec_reply["cell_execution_reply"]["cell_id"] == cell_uuid
            assert exec_reply["cell_execution_reply"]["parent_id"] == msg_id

            data = await receive_json(websocket, msg_types=["cell_update"])
            assert data == expected

    @pytest.mark.asyncio
    async def test_notebook_cell_add(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)
            params = {
                "cell_type": "markdown",
                "source": "__**Hello Callisto!**__",
            }
            response = await client.post(
                f"/notebooks/{uuid}/cells",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 201

            data = await receive_json(websocket, msg_types=["cell_add"])
            cells = data["cell_add"]
            assert len(cells) == 5  # should dump all the cells
            cell = cells[-1]
            cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

            expected = {
                "cell_type": "markdown",
                "metadata": {
                    "jupyter_d1": {
                        "position": 4,
                        "uuid": cell_uuid,
                        "notebook_uuid": uuid,
                    }
                },
                "source": "__**Hello Callisto!**__",
            }

            # from pprint import pprint
            # print("data")
            # pprint(data)
            # print("expected")
            # pprint(expected)
            assert cell == expected

    @pytest.mark.asyncio
    async def test_notebook_cell_patch(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get an existing cell
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[1]["source"] == 'print("Larry the Llama")'

            cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
            params = {"source": "__Banana Rama!__"}
            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(websocket)
            cells = data["cell_update"]
            assert len(cells) == 1
            cell = cells[0]

            expected = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {
                    "jupyter_d1": {
                        "execution_state": "idle",
                        "position": 1,
                        "notebook_uuid": uuid,
                        "uuid": cell_uuid,
                    }
                },
                "outputs": [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": "Larry the Llama\n",
                    }
                ],
                "source": "__Banana Rama!__",
            }

            assert cell == expected

    @pytest.mark.asyncio
    async def test_notebook_cell_delete(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        assert cells[3]["metadata"]["jupyter_d1"]["position"] == 3

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.delete(
                f"/notebooks/{uuid}/cells/{cell_uuid}",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await receive_json(websocket)

            del cells[2]
            cells[2]["metadata"]["jupyter_d1"]["position"] = 2
            expected = {"cell_delete": cells}

            assert data == expected

    @pytest.mark.asyncio
    async def test_notebook_cell_move(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get the existing cells
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            orig_uuids = list(
                map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], cells)
            )

            # move the last cell to before the first cell
            before_uuid = orig_uuids[1]
            move_uuid = orig_uuids[3]

            params = {"before": before_uuid}
            response = await client.get(
                f"/notebooks/{uuid}/cells/{move_uuid}/move",
                query_string=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await receive_json(websocket)
            cells = data["cell_update"]
            assert len(cells) == 4  # should dump all the cells

            new_uuids = []
            for cell in cells:
                uuid = cell["metadata"]["jupyter_d1"]["uuid"]
                new_uuids.append(uuid)

            expected_uuids = [
                orig_uuids[0],
                orig_uuids[3],
                orig_uuids[1],
                orig_uuids[2],
            ]
            assert new_uuids == expected_uuids

            # Check cell positions
            assert_cell_positions(cells)

    @pytest.mark.asyncio
    async def test_notebook_cells_merge(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get the existing cells
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
            cells[2]["metadata"]["jupyter_d1"]["uuid"]
            next_cell_uuid = cells[3]["metadata"]["jupyter_d1"]["uuid"]
            assert cells[1]["source"] == 'print("Larry the Llama")'
            assert cells[2]["source"] == "2+5"

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/merge",
                query_string={"above": False},
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await receive_json(websocket)
            cells = data["cell_delete"]
            assert len(cells) == 3
            assert cells[1]["source"] == 'print("Larry the Llama")\n2+5'
            assert cells[1]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid
            assert cells[2]["source"] == ""
            assert cells[2]["metadata"]["jupyter_d1"]["uuid"] == next_cell_uuid
            # Check cell positions
            assert_cell_positions(cells)

    @pytest.mark.asyncio
    async def test_notebook_cell_split(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get the existing cells
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
            next_cell_uuid = cells[2]["metadata"]["jupyter_d1"]["uuid"]
            assert cells[1]["source"] == 'print("Larry the Llama")'

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/split",
                query_string={"split_location": 2},
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await receive_json(websocket)
            cells = data["cell_update"]
            assert len(cells) == 5
            assert cells[1]["source"] == "pr"
            assert cells[1]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid
            assert cells[2]["source"] == 'int("Larry the Llama")'
            assert cells[2]["metadata"]["jupyter_d1"]["uuid"] is not None
            assert cells[3]["metadata"]["jupyter_d1"]["uuid"] == next_cell_uuid

            # Check cell positions
            assert_cell_positions(cells)

    @pytest.mark.asyncio
    async def test_cell_stream(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        assert cells[1]["execution_count"] is None

        params = {
            "source": "import time\nfor i in ('heres', 'a', "
            "'streamofdata'):\n    print(i)\n    time.sleep(0.9)"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            outputs = ["heres", "a", "streamofdata"]
            cell_streams: List[Dict[str, Any]] = []
            received_info = {
                "received_cell_stream_count": 0,
                "received_cell_update_count": 0,
                "received_cell_execution": False,
                "received_vars": False,
            }

            # Receive cell stream output
            async def receive_cell_stream(data):
                cell_stream = data["cell_stream"]
                expected_output = {
                    "name": "stdout",
                    "text": f"{outputs.pop(0)}\n",
                    "output_type": "stream",
                }
                assert cell_stream["output"] == expected_output
                assert cell_stream["cell_id"] == cell_uuid
                received_info["received_cell_stream_count"] += 1
                return expected_output

            async def receive_cell_update(data):
                cell_update = data["cell_update"]
                assert len(cell_update) == 1
                cell_d1_data = cell_update[0]["metadata"]["jupyter_d1"]
                assert cell_d1_data["uuid"] == cell_uuid
                if received_info["received_cell_update_count"] == 0:
                    assert cell_d1_data["execution_state"] == "busy"
                else:
                    assert cell_d1_data["execution_state"] == "idle"
                    assert cell_update[0]["outputs"] == cell_streams
                assert (
                    cell_update[0]["execution_count"] is None
                    or cell_update[0]["execution_count"] == 1
                )
                received_info["received_cell_update_count"] += 1

            async def receive_cell_execution(data):
                cell_exec = data["cell_execution_reply"]
                assert cell_exec["cell_id"] == cell_uuid
                assert cell_exec["execution_count"] == 1
                assert len(cell_exec["parent_id"]) == 35
                received_info["received_cell_execution"] = True

            msg_types = [
                "cell_stream",
                "cell_update",
                "cell_execution_reply",
                "vars",
            ]
            for i in range(7):
                data = await receive_json(websocket, msg_types=msg_types)
                if "cell_stream" in data:
                    cell_streams.append(await receive_cell_stream(data))
                if "cell_update" in data:
                    await receive_cell_update(data)
                if "cell_execution_reply" in data:
                    await receive_cell_execution(data)
                if "vars" in data:
                    received_info["received_vars"] = True

            assert received_info["received_cell_update_count"] == 2
            assert received_info["received_cell_execution"]
            assert received_info["received_vars"]
            assert received_info["received_cell_stream_count"] == 3

    @pytest.mark.asyncio
    async def test_idle_status(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        async def is_idle_status():
            response = await client.get(
                f"/kernels/idle", headers=superuser_token_headers
            )
            assert response.status_code == 200
            json = response.json()
            return (
                json["idle"],
                datetime.strptime(json["last_idle"], "%Y-%m-%dT%H:%M:%S.%f"),
            )

        # Kernel is idle
        is_idle, last_idle_1 = await is_idle_status()
        assert is_idle is True

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # Kernel is still idle
        is_idle, last_idle_2 = await is_idle_status()
        assert is_idle is True
        assert last_idle_1 == last_idle_2

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        busy_cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        quick_cell_uuid = cells[2]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "from time import sleep\nwhile True:\n    sleep(5)"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{busy_cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{quick_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(websocket, msg_types=["vars"])
            assert "vars" in data

            # Need to wait for the UPDATE_WORKDIR_REQUEST to finish
            # (and we won't see it through the websocket)
            await asyncio.sleep(1)

            # Kernel is still idle (no code running)
            is_idle, last_idle_3 = await is_idle_status()
            assert is_idle is True
            assert last_idle_3 > last_idle_2

            response = await client.get(
                f"/notebooks/{uuid}/cells/{busy_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # first chunk received should be a cell_update with
            # an execution_state of 'busy' when processing starts
            data = await wait_for_event(websocket, "cell_update")
            d1_metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "busy"

            # Kernel should not be idle now
            is_idle, last_idle_4 = await is_idle_status()
            assert is_idle is False
            assert last_idle_4 == last_idle_3

    @pytest.mark.asyncio
    async def test_kernel_interrupt(
        self, client: TestClient, superuser_token_headers: Dict[str, str],
    ):
        async def is_idle_status():
            response = await client.get(
                f"/kernels/idle", headers=superuser_token_headers
            )
            assert response.status_code == 200
            json = response.json()
            return (
                json["idle"],
                datetime.strptime(json["last_idle"], "%Y-%m-%dT%H:%M:%S.%f"),
            )

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # Kernel is idle
        is_idle, last_idle_1 = await is_idle_status()
        assert is_idle is True

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        busy_cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "from time import sleep\nwhile True:\n    sleep(5)"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{busy_cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{busy_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a cell_update with
            # an execution_state of 'busy' when processing starts
            data = await wait_for_event(websocket, "cell_update")
            d1_metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "busy"
            assert d1_metadata["uuid"] == busy_cell_uuid

            # Kernel should not be idle now
            is_idle, last_idle_2 = await is_idle_status()
            assert is_idle is False
            assert last_idle_2 == last_idle_1

            response = await client.get(
                f"/notebooks/{uuid}/interrupt_kernel",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await wait_for_event(websocket, "kernel_interrupted")
            assert data["kernel_interrupted"]["interrupted"] is True

            # Receive cell error output
            data = await wait_for_event(websocket, "cell_update")
            d1_metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "busy"
            assert data["cell_update"][0]["execution_count"] is None
            assert d1_metadata["position"] == 1
            assert d1_metadata["uuid"] == busy_cell_uuid
            cell = data["cell_update"][0]
            assert cell["cell_type"] == "code"
            assert len(cell["outputs"]) == 1
            assert cell["outputs"][0]["ename"] == "KeyboardInterrupt"
            assert "KeyboardInterrupt" in cell["outputs"][0]["traceback"][1]

            def assert_json_content(data, execution_count=None):
                if "cell_update" in data:
                    cell_data = data["cell_update"][0]
                    d1_metadata = cell_data["metadata"]["jupyter_d1"]
                    assert d1_metadata["execution_state"] == "idle"
                    assert d1_metadata["uuid"] == busy_cell_uuid
                    assert cell_data["execution_count"] == execution_count
                    return None
                elif "cell_execution_reply" in data:
                    assert data["cell_execution_reply"]["execution_count"] == 1
                    assert (
                        data["cell_execution_reply"]["cell_id"]
                        == busy_cell_uuid
                    )
                    assert len(data["cell_execution_reply"]["parent_id"]) == 35
                    assert data["cell_execution_reply"]["parent_id"] == msg_id
                    return 1
                else:
                    raise AssertionError(f"unexpected cell type: {data}")

            # Execution count update
            data = await wait_for_event(websocket, "cell_execution_reply")
            exec_count = assert_json_content(data)
            data = await wait_for_event(websocket, "cell_update")
            assert_json_content(data, exec_count)

            # Kernel should be idle now
            is_idle, last_idle_3 = await is_idle_status()
            assert is_idle is True
            assert last_idle_3 > last_idle_2

    @pytest.mark.asyncio
    async def test_bogus_code_error(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "this isnt code"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            # execution_count update and busy status update,
            # in uncertain order
            def assert_json_content(data, execution_count=None):
                if "cell_update" in data:
                    cell_data = data["cell_update"][0]
                    d1_metadata = cell_data["metadata"]["jupyter_d1"]
                    assert d1_metadata["execution_state"] == "busy"
                    assert d1_metadata["uuid"] == cell_uuid
                    assert d1_metadata["position"] == 1
                    assert cell_data["execution_count"] == execution_count
                    cell = data["cell_update"][0]
                    assert cell["cell_type"] == "code"
                    assert len(cell["outputs"]) == 0
                    return None
                elif "cell_execution_reply" in data:
                    assert data["cell_execution_reply"]["execution_count"] == 1
                    assert data["cell_execution_reply"]["cell_id"] == cell_uuid
                    assert len(data["cell_execution_reply"]["parent_id"]) == 35
                    assert data["cell_execution_reply"]["parent_id"] == msg_id
                    return 1
                else:
                    raise AssertionError(f"unexpected cell type: {data}")

            msg_types = [
                "cell_update",
                "cell_execution_reply",
            ]

            data = await receive_json(websocket, msg_types=msg_types)
            exec_count = assert_json_content(data)
            data = await receive_json(websocket, msg_types=msg_types)
            assert_json_content(data, exec_count)

            # Still busy with output, error output received
            data = await receive_json(websocket, msg_types=["cell_update"])
            d1_metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "busy"
            assert data["cell_update"][0]["execution_count"] == 1
            assert d1_metadata["position"] == 1
            assert d1_metadata["uuid"] == cell_uuid
            cell = data["cell_update"][0]
            assert cell["cell_type"] == "code"
            assert len(cell["outputs"]) == 1
            assert cell["outputs"][0]["ename"] == "SyntaxError"
            assert "SyntaxError" in cell["outputs"][0]["traceback"][0]

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            assert "vars" in data

    @pytest.mark.asyncio
    async def test_scratch_execute(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "4*5"},
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a scratch_update with
            # an execution_state of 'busy' when processing starts
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Receive scratch execution output
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            expected_output = {
                "data": {"text/plain": "20"},
                "execution_count": 1,
                "metadata": {},
                "output_type": "execute_result",
            }
            assert scratch_update["output"] == expected_output

            # Scratch execution state set to idle
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "idle"

    @pytest.mark.asyncio
    async def test_scratch_code_idle_status(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        async def is_idle_status():
            response = await client.get(
                f"/kernels/idle", headers=superuser_token_headers
            )
            assert response.status_code == 200
            json = response.json()
            return (
                json["idle"],
                datetime.strptime(json["last_idle"], "%Y-%m-%dT%H:%M:%S.%f"),
            )

        # Kernel is idle
        is_idle, last_idle_1 = await is_idle_status()
        assert is_idle is True

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # Kernel is still idle
        is_idle, last_idle_2 = await is_idle_status()
        assert is_idle is True
        assert last_idle_1 == last_idle_2

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "4+9"},
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # Execution state busy
            await receive_json(websocket, msg_types=["scratch_update"])
            # Execution output
            await receive_json(websocket, msg_types=["scratch_update"])
            # Execution state idle
            await receive_json(websocket, msg_types=["scratch_update"])

            # Kernel is still idle (no code running)
            is_idle, last_idle_3 = await is_idle_status()
            assert is_idle is True
            assert last_idle_3 > last_idle_2

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            assert "vars" in data

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={
                    "code": "from time import sleep\n"
                    "while True:\n    sleep(1)"
                },
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a cell_update with
            # an execution_state of 'busy' when processing starts
            data = await wait_for_event(websocket, "scratch_update")
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Kernel should not be idle now
            is_idle, last_idle_4 = await is_idle_status()
            assert is_idle is False
            assert last_idle_4 > last_idle_3

    @pytest.mark.asyncio
    async def test_scratch_stream(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={
                    "code": "import time\nfor i in ('heres', 'a', "
                    "'streamofdata'):\n    print(i)\n    "
                    "time.sleep(0.3)"
                },
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a scratch_update with
            # an execution_state of 'busy' when processing starts
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Receive scratch execution output
            async def receive_text(text):
                data = await receive_json(
                    websocket, msg_types=["scratch_update"]
                )
                scratch_update = data["scratch_update"]
                expected_output = {
                    "name": "stdout",
                    "text": f"{text}\n",
                    "output_type": "stream",
                }
                assert scratch_update["output"] == expected_output

            await receive_text("heres")
            await receive_text("a")
            await receive_text("streamofdata")

            # Scratch execution state set to idle
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "idle"

    @pytest.mark.asyncio
    async def test_vars_update_cell_execute(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "x = 7-9"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {
                var["name"]: {
                    "type": var["type"],
                    "value": var["value"],
                    "summary": var["summary"],
                }
                for var in data["vars"]
            }

            assert vars["x"]["type"] == "int"
            assert vars["x"]["value"]["single_value"] == "-2"
            assert vars["x"]["summary"] == "-2"

            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

    @pytest.mark.asyncio
    async def test_vars_update_scratch_execute(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "x_u = 27/10"},
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {
                var["name"]: {
                    "type": var["type"],
                    "value": var["value"],
                    "summary": var["summary"],
                }
                for var in data["vars"]
            }

            assert vars["x_u"]["type"] == "float"
            assert vars["x_u"]["value"]["single_value"] == "2.7"
            assert vars["x_u"]["summary"] == "2.7"

            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

    @pytest.mark.asyncio
    async def test_notebook_write_permission(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        readonly_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        with pytest.raises(AssertionError):
            async with client.websocket_connect(
                f"/notebooks/{uuid}/ws/notebook",
                headers=readonly_token_headers,
            ):
                pass

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ):
            pass

    @pytest.mark.asyncio
    async def test_notebook_stream_permission(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        with pytest.raises(AssertionError):
            async with client.websocket_connect(
                f"/notebooks/{uuid}/ws/stream",
                headers=permissionless_token_headers,
            ):
                pass

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/stream", headers=readonly_token_headers
        ):
            pass

    @pytest.mark.asyncio
    async def test_vars_update_bash(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "bash", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        vars_list = response.json()["vars"]
        assert len(vars_list) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "export D1_VAR_TEST=p903s"},
            )
            assert response.status_code == 200

            data = await receive_json(
                websocket, timeout=60, msg_types=["vars"]
            )
            vars = {
                var["name"]: {
                    "type": var["type"],
                    "value": var["value"],
                    "summary": var["summary"],
                }
                for var in data["vars"]
            }
            assert vars["D1_VAR_TEST"]["type"] is None
            assert vars["D1_VAR_TEST"]["value"]["single_value"] == "p903s"
            assert vars["D1_VAR_TEST"]["summary"] == "p903s"

    @pytest.mark.asyncio
    async def test_vars_update_r_kernel(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "ir", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        vars_list = response.json()["vars"]
        assert len(vars_list) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={
                    "code": "ffo <- 9\n"
                    'k = data.frame(col1=c("t", 5), '
                    'col2=c("4", 6), col3=c("h", 8))'
                },
            )
            assert response.status_code == 200

            # Give it time to install callistor
            await asyncio.sleep(10)

            data = await receive_json(
                websocket, timeout=60, msg_types=["vars"]
            )
            vars = {var["name"]: var for var in data["vars"]}

            assert vars["ffo"]["type"] == "numeric"
            assert vars["ffo"]["abbreviated"] is False
            assert vars["ffo"]["summary"] == "9"
            assert vars["ffo"]["value"]["single_value"] == "9"
            assert vars["k"]["type"] == "data.frame"
            assert vars["k"]["abbreviated"] is False
            assert "Size: 2x3 Memory: " in vars["k"]["summary"]
            assert vars["k"]["value"]["multi_value"]["column_count"] == 3
            assert vars["k"]["value"]["multi_value"]["row_count"] == 2
            assert vars["k"]["value"]["multi_value"]["column_names"] == [
                "col1 (factor)",
                "col2 (factor)",
                "col3 (factor)",
            ]
            assert vars["k"]["value"]["multi_value"]["row_names"] == ["1", "2"]
            assert vars["k"]["value"]["multi_value"]["data"] == [
                ["t", "4", "h"],
                ["5", "6", "8"],
            ]

    @pytest.mark.asyncio
    async def test_page_payload(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "python", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        response = await client.post(
            f"/notebooks/{uuid}/cells",
            headers=superuser_token_headers,
            json={"cell_type": "code", "source": "?str"},
        )
        cell_uuid = response.json()["cell"]["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await receive_json(websocket, msg_types=["payload_page"])
            assert "text/plain" in data["payload_page"]["data"]
            assert data["payload_page"]["message_id"] == msg_id
            assert data["payload_page"]["start"] == 0

    @pytest.mark.asyncio
    async def test_code_completion(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "python", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/complete",
                json={"code": "s"},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await receive_json(websocket)
            assert len(data["complete_reply"]["matches"]) > 0
            assert data["complete_reply"]["message_id"] == msg_id
            assert data["complete_reply"]["cursor_start"] == 0
            assert data["complete_reply"]["cursor_end"] == 1

    @pytest.mark.asyncio
    async def test_code_completion_cursor_position(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "python", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/complete",
                json={"code": "5 + prin + 6", "cursor_position": 7},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await receive_json(websocket)
            assert data["complete_reply"]["matches"] == ["print"]
            assert data["complete_reply"]["message_id"] == msg_id
            assert data["complete_reply"]["cursor_start"] == 4
            assert data["complete_reply"]["cursor_end"] == 7

    @pytest.mark.asyncio
    async def test_history(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            await receive_json(websocket)
            await receive_json(websocket)
            await receive_json(websocket)
            await receive_json(websocket)
            await receive_json(websocket)

            response = await client.post(
                f"/notebooks/{uuid}/history", headers=superuser_token_headers
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await wait_for_event(websocket, "history_reply")

            assert data["history_reply"]["message_id"] == msg_id
            history = data["history_reply"]["history"]
            assert history[0]["line_number"] == 0
            assert history[0]["input"] == ""
            assert history[0]["output"] is None
            assert history[1]["line_number"] == 1
            assert history[1]["input"] == "2+5"
            assert history[1]["output"] == "7"

    @pytest.mark.asyncio
    async def test_restart_kernel(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/restart_kernel",
                headers=superuser_token_headers,
            )

            assert response.status_code == 204

            data = await wait_for_event(websocket, "kernel_restarted")

            assert data["kernel_restarted"]["run_all_cells"] is False
            cells = data["kernel_restarted"]["cells"]
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"
            assert cells[2]["execution_count"] == 1

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        for cell in cells:
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"
            assert cells[2]["execution_count"] == 1

    @pytest.mark.asyncio
    async def test_restart_kernel_and_clear_output(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/restart_kernel_and_clear_output",
                headers=superuser_token_headers,
            )

            assert response.status_code == 204

            data = await wait_for_event(websocket, "kernel_restarted")

            assert data["kernel_restarted"]["run_all_cells"] is False
            cells = data["kernel_restarted"]["cells"]
            for cell in cells:
                assert (
                    ("outputs" not in cell or len(cell["outputs"]) == 0)
                    and "execution_count" not in cell
                    or cell["execution_count"] is None
                )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        for cell in cells:
            assert (
                ("outputs" not in cell or len(cell["outputs"]) == 0)
                and "execution_count" not in cell
                or cell["execution_count"] is None
            )

    @pytest.mark.asyncio
    async def test_restart_kernel_and_run_all_cells(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert "outputs" not in cells[0]
        assert cells[1]["outputs"][0]["text"] == "Larry the Llama\n"
        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/restart_kernel_and_execute_all",
                headers=superuser_token_headers,
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            kernel_restarted_msgs = filter_websocket_collection(
                msgs, "kernel_restarted"
            )
            cell_update_msgs = filter_websocket_collection(msgs, "cell_update")

            data = kernel_restarted_msgs.pop(0)
            assert data["kernel_restarted"]["run_all_cells"] is True
            cells = data["kernel_restarted"]["cells"]
            for cell in cells:
                assert (
                    ("outputs" not in cell or len(cell["outputs"]) == 0)
                    and "execution_count" not in cell
                    or cell["execution_count"] is None
                )

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert len(cell["outputs"]) == 0
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "busy"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["outputs"][0]["text"] == "Larry the Llama\n"
            assert cell["execution_count"] == 1
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert len(cell["outputs"]) == 0
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "busy"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["outputs"][0]["data"]["text/plain"] == "7"
            assert cell["execution_count"] == 2
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "busy"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["outputs"][0]["data"]["text/plain"] == "7"
            assert cell["execution_count"] == 2
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestKernelVarsManager:
    @pytest.mark.asyncio
    async def test_get_single_var_detail(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Large dataframe is abbreviated in summary, not in variable
        details request.
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import pandas as pd\ndf3 = "
            "pd.DataFrame([{str(i): i + j for i in range(5)} for j in "
            "range(150)])"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {
                var["name"]: {
                    "type": var["type"],
                    "value": var["value"],
                    "summary": var["summary"],
                    "abbreviated": var["abbreviated"],
                }
                for var in data["vars"]
            }

            assert vars["df3"]["type"] == "DataFrame"
            assert vars["df3"]["value"]["multi_value"]["column_count"] == 5
            assert vars["df3"]["value"]["multi_value"]["row_count"] == 150
            assert vars["df3"]["value"]["multi_value"]["column_names"] == [
                str(i) for i in range(5)
            ]
            assert vars["df3"]["value"]["multi_value"]["data"] == [
                [str(i + j) for i in range(5)] for j in range(10)
            ]
            assert vars["df3"]["summary"] == "Size: 150x5 Memory: 5.98 KB"
            assert vars["df3"]["abbreviated"] is True

            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

            response = await client.get(
                f"/notebooks/{uuid}/vars/df3", headers=superuser_token_headers
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "df3"
            assert single_var["type"] == "DataFrame"
            assert single_var["value"]["multi_value"]["column_count"] == 5
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                str(i) for i in range(5)
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                [str(i + j) for i in range(5)] for j in range(150)
            ]
            assert single_var["summary"] == "Size: 150x5 Memory: 5.98 KB"
            assert single_var["abbreviated"] is False

            # Shouldn't have changed anything in the current vars
            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

            # Var that doesn't exist
            response = await client.get(
                f"/notebooks/{uuid}/vars/df2", headers=superuser_token_headers
            )
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_single_var_detail_r_kernel(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        R Kernel large dataframe is abbreviated in summary, not in variable
        details request.
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple_r.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == "f <- 543"

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "kool = data.frame(col1=c(1:150), col2=c(150:1))"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {var["name"]: var for var in data["vars"]}

            assert vars["kool"]["type"] == "data.frame"
            assert vars["kool"]["value"]["multi_value"]["column_count"] == 2
            assert vars["kool"]["value"]["multi_value"]["row_count"] == 150
            assert vars["kool"]["value"]["multi_value"]["column_names"] == [
                "col1 (integer)",
                "col2 (integer)",
            ]
            assert vars["kool"]["value"]["multi_value"]["data"] == [
                [str(i + 1), str(150 - i)] for i in range(25)
            ]
            assert "Size: 150x2 Memory:" in vars["kool"]["summary"]
            assert vars["kool"]["abbreviated"] is True

            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            assert list(current_vars) == data["vars"]

            response = await client.get(
                f"/notebooks/{uuid}/vars/kool", headers=superuser_token_headers
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "kool"
            assert single_var["type"] == "data.frame"
            assert single_var["value"]["multi_value"]["column_count"] == 2
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                "col1 (integer)",
                "col2 (integer)",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                [str(i + 1), str(150 - i)] for i in range(150)
            ]
            assert "Size: 150x2 Memory:" in single_var["summary"]
            assert single_var["abbreviated"] is False

            # Shouldn't have changed anything in the current vars
            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            assert list(current_vars) == data["vars"]

            # Var that doesn't exist
            response = await client.get(
                f"/notebooks/{uuid}/vars/df2", headers=superuser_token_headers
            )
            assert response.status_code == 404


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestWorkingDirectory:
    async def assert_python_working_directory(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        open_path: str,
        working_directory: str,
        query_string: Optional[Dict[str, Any]] = None,
    ):
        """Test that python kernel is started in correct directory."""
        if query_string is None:
            query_string = {}
        query_string["filepath"] = open_path
        response = await client.get(
            f"/notebooks/open/",
            headers=superuser_token_headers,
            query_string=query_string,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        # /tmp symlinks to /private/tmp on mac, so we resolve
        resolved_work_dir = str(pathlib.Path(working_directory).resolve())

        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == resolved_work_dir
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "import os\nos.getcwd()"},
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a scratch_update with
            # an execution_state of 'busy' when processing starts
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Receive scratch execution output
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]

            expected_output = {
                "data": {"text/plain": f"'{resolved_work_dir}'"},
                "execution_count": 1,
                "metadata": {},
                "output_type": "execute_result",
            }
            assert scratch_update["output"] == expected_output

            # Scratch execution state set to idle
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "idle"

            token = get_superuser_token()
            auth = base64.b64encode(f"{token}:".encode("utf-8"))
            response = await client.get(
                f"/dav{resolved_work_dir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_working_directory_passed_in(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        If notebook is opened with working directory specified, make sure
        the kernel is running in that directory.
        """
        filename = "simple.ipynb"
        nb_filename = f"jupyter_d1/tests/notebooks/{filename}"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload",
            query_string={"filename": filename},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        await self.assert_python_working_directory(
            client,
            superuser_token_headers,
            open_path=filename,
            working_directory=f"{os.getcwd()}/jupyter_d1/tests/notebooks",
            query_string={
                "working_directory": f"{os.getcwd()}/jupyter_d1"
                "/tests/notebooks"
            },
        )

    @pytest.mark.asyncio
    async def test_file_in_different_working_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        If notebook in a different directory is opened, make sure
        the kernel is running in that directory.
        """
        shutil.copyfile(
            "jupyter_d1/tests/notebooks/simple.ipynb",
            "jupyter_d1/tests/notebooks/simple_copy.ipynb",
        )
        await self.assert_python_working_directory(
            client,
            superuser_token_headers,
            open_path=f"{os.getcwd()}/jupyter_d1/tests/"
            "notebooks/simple_copy.ipynb",
            working_directory=f"{os.getcwd()}/jupyter_d1/tests/notebooks",
        )
        os.remove("jupyter_d1/tests/notebooks/simple_copy.ipynb")

    @pytest.mark.asyncio
    async def test_file_in_parent_directory_of_working_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        If notebook in the parent directory of the server's working directory 
        is opened, make sure the kernel is running in that parent directory.
        """
        shutil.copyfile(
            "jupyter_d1/tests/notebooks/simple.ipynb",
            f"/tmp/simple_copy.ipynb",
        )
        await self.assert_python_working_directory(
            client,
            superuser_token_headers,
            open_path=f"/tmp/simple_copy.ipynb",
            working_directory=f"/tmp",
        )
        os.remove("/tmp/simple_copy.ipynb")

    @pytest.mark.asyncio
    async def test_file_in_sub_directory_of_working_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        If notebook in a sub directory of the server's working directory 
        is opened, make sure the kernel is running in that sub directory.
        """
        pathlib.Path("/tmp/jupyter_d1_test/some_nbs").mkdir(exist_ok=True)
        shutil.copyfile(
            "jupyter_d1/tests/notebooks/simple.ipynb",
            f"/tmp/jupyter_d1_test/some_nbs//simple_copy.ipynb",
        )
        await self.assert_python_working_directory(
            client,
            superuser_token_headers,
            open_path=f"/tmp/jupyter_d1_test/some_nbs/simple_copy.ipynb",
            working_directory=f"/tmp/jupyter_d1_test/some_nbs",
        )
        shutil.rmtree("/tmp/jupyter_d1_test/some_nbs")

    @pytest.mark.asyncio
    async def test_r_kernel_working_directory_passed_in(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        working_directory = "/tmp"
        response = await client.post(
            "/notebooks/create",
            query_string={
                "kspec_name": "ir",
                "filename": "heyp",
                "working_directory": working_directory,
            },
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "getwd()"},
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a scratch_update with
            # an execution_state of 'busy' when processing starts
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Receive scratch execution output
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            # /tmp symlinks to /private/tmp on mac, so we resolve
            resolved_work_dir = pathlib.Path(working_directory).resolve()
            expected_output = {
                "data": {
                    "text/html": f"'{resolved_work_dir}'",
                    "text/latex": f"'{resolved_work_dir}'",
                    "text/markdown": f"'{resolved_work_dir}'",
                    "text/plain": f'[1] "{resolved_work_dir}"',
                },
                "metadata": {},
                "output_type": "display_data",
            }
            assert scratch_update["output"] == expected_output

            # Scratch execution state set to idle
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "idle"

            token = get_superuser_token()
            auth = base64.b64encode(f"{token}:".encode("utf-8"))
            response = await client.get(
                f"/dav{resolved_work_dir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 200


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestChangeWorkingDirectory:
    async def do_test_change_working_directory(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        kspec_name: str,
    ):
        working_directory = "/tmp"
        resolved_work_dir = str(pathlib.Path(working_directory).resolve())
        response = await client.post(
            "/notebooks/create",
            query_string={
                "kspec_name": kspec_name,
                "filename": "heyp",
                "working_directory": working_directory,
            },
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        token = get_superuser_token()
        auth = base64.b64encode(f"{token}:".encode("utf-8"))
        response = await client.get(
            f"/dav{resolved_work_dir}",
            headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            new_workdir = f"{os.getcwd()}/jupyter_d1/tests/notebooks"
            response = await client.patch(
                f"/notebooks/{uuid}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": new_workdir},
            )
            assert response.status_code == 200

            data = await receive_json(websocket, msg_types=["metadata"])

            metadata = data["metadata"]
            assert metadata["jupyter_d1"]["working_directory"] == new_workdir

            response = await client.get(
                f"/dav{new_workdir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 200

            response = await client.get(
                f"/dav{resolved_work_dir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 404

        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        resp_json = response.json()["notebook"]
        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == new_workdir
        )

    async def do_test_change_working_directory_in_code(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        kspec_name: str,
        chdir_code: str,
    ):
        working_directory = "/tmp"
        resolved_work_dir = str(pathlib.Path(working_directory).resolve())
        response = await client.post(
            "/notebooks/create",
            query_string={
                "kspec_name": kspec_name,
                "filename": "heyp",
                "working_directory": working_directory,
            },
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        token = get_superuser_token()
        auth = base64.b64encode(f"{token}:".encode("utf-8"))
        response = await client.get(
            f"/dav{resolved_work_dir}",
            headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            new_workdir = f"{os.getcwd()}/jupyter_d1/tests/notebooks"
            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": chdir_code.format(new_workdir=new_workdir)},
            )
            assert response.status_code == 200

            data = await wait_for_event(websocket, "metadata", timeout=10)

            metadata = data["metadata"]
            assert metadata["jupyter_d1"]["working_directory"] == new_workdir

            response = await client.get(
                f"/dav{new_workdir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 200

            response = await client.get(
                f"/dav{resolved_work_dir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 404

        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        resp_json = response.json()["notebook"]
        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == new_workdir
        )

    @pytest.mark.asyncio
    async def test_python_change_working_directory_endpoint(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory(
            client, superuser_token_headers, "python"
        )

    @pytest.mark.asyncio
    async def test_python_change_working_directory_in_code(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory_in_code(
            client,
            superuser_token_headers,
            "python",
            'import os\nos.chdir("{new_workdir}")',
        )

    @pytest.mark.asyncio
    async def test_r_change_working_directory_endpoint(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory(
            client, superuser_token_headers, "ir"
        )

    @pytest.mark.asyncio
    async def test_r_change_working_directory_in_code(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory_in_code(
            client, superuser_token_headers, "ir", 'setwd("{new_workdir}")'
        )

    @pytest.mark.asyncio
    async def test_bash_change_working_directory_endpoint(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory(
            client, superuser_token_headers, "bash"
        )

    @pytest.mark.asyncio
    async def test_bash_change_working_directory_in_code(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory_in_code(
            client, superuser_token_headers, "bash", "cd {new_workdir}"
        )

    @pytest.mark.asyncio
    async def test_change_working_directory_fail_invalid_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        working_directory = "/tmp"
        resolved_work_dir = str(pathlib.Path(working_directory).resolve())
        response = await client.post(
            "/notebooks/create",
            query_string={
                "kspec_name": "python",
                "filename": "heyp",
                "working_directory": working_directory,
            },
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        token = get_superuser_token()
        auth = base64.b64encode(f"{token}:".encode("utf-8"))
        response = await client.get(
            f"/dav{resolved_work_dir}",
            headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
        )
        assert response.status_code == 200

        await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

        new_workdir = f"{os.getcwd()}/tests/notrealdir"
        response = await client.patch(
            f"/notebooks/{uuid}/change_working_directory",
            headers=superuser_token_headers,
            query_string={"directory": new_workdir},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Directory does not exist"

        await asyncio.sleep(2)

        response = await client.get(
            f"/dav{new_workdir}",
            headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
        )
        assert response.status_code == 404

        response = await client.get(
            f"/dav{resolved_work_dir}",
            headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        resp_json = response.json()["notebook"]
        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == resolved_work_dir
        )


@pytest.mark.usefixtures(
    "clear_notebooks", "clear_notebook_directory", "clear_notebook_directory_2"
)
class TestSaveAs:
    @pytest.mark.asyncio
    async def test_rename(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert not os.path.exists(f"{settings.ROOT_DIR}/awholenewname.ipynb")

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/rename",
                query_string={"filename": "awholenewname"},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"{settings.ROOT_DIR}/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["path"]
                == f"{settings.ROOT_DIR}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert os.path.exists(f"{settings.ROOT_DIR}/awholenewname.ipynb")
            assert not os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

    @pytest.mark.asyncio
    async def test_rename_different_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert not os.path.exists(f"{workdir_1}/awholenewname.ipynb")

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/rename",
                query_string={
                    "filename": "awholenewname",
                    "directory": "/tmp/test_nb_2/",
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"/tmp/test_nb_2/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["path"]
                == f"{workdir_1}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert os.path.exists(f"{workdir_1}/awholenewname.ipynb")
            assert not os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

    @pytest.mark.asyncio
    async def test_rename_file_exists(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """Fail if file exists unless overwrite param is set to true"""
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        with open(f"{workdir_1}/awholenewname.ipynb", "w") as f:
            f.write("some text here")

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert os.path.exists(f"{workdir_1}/awholenewname.ipynb")

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/rename",
                query_string={
                    "filename": "awholenewname",
                    "directory": "/tmp/test_nb_2/",
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 400
            assert response.json()["detail"] == f"File already exists"

            response = await client.patch(
                f"/notebooks/{uuid}/rename",
                query_string={
                    "filename": "awholenewname",
                    "directory": "/tmp/test_nb_2/",
                    "overwrite": True,
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"/tmp/test_nb_2/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["path"]
                == f"{workdir_1}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert os.path.exists(f"{workdir_1}/awholenewname.ipynb")
            assert not os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

        with open(f"{workdir_1}/awholenewname.ipynb", "r") as f:
            assert f.read() != "some text here"

    @pytest.mark.asyncio
    async def test_save_as(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert not os.path.exists(f"{settings.ROOT_DIR}/awholenewname.ipynb")

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/save_as",
                query_string={"filename": "awholenewname"},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"{settings.ROOT_DIR}/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["path"]
                == f"{settings.ROOT_DIR}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"
            assert metadata["jupyter_d1"]["uuid"] == uuid

            assert os.path.exists(f"{settings.ROOT_DIR}/awholenewname.ipynb")
            assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

            response = await client.get(
                f"/notebooks/{uuid}", headers=superuser_token_headers
            )
            resp_json = response.json()["notebook"]
            assert (
                resp_json["metadata"]["jupyter_d1"]["name"] == "awholenewname"
            )
            assert resp_json["metadata"]["jupyter_d1"]["uuid"] == uuid

    @pytest.mark.asyncio
    async def test_save_as_different_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert not os.path.exists(f"{workdir_1}/awholenewname.ipynb")

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/save_as",
                query_string={
                    "filename": "awholenewname",
                    "directory": "/tmp/test_nb_2/",
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"/tmp/test_nb_2/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["path"]
                == f"{workdir_1}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert os.path.exists(f"{workdir_1}/awholenewname.ipynb")
            assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

    @pytest.mark.asyncio
    async def test_save_as_file_exists(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """Fail if file exists unless overwrite param is set to true"""
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        with open(f"{workdir_1}/awholenewname.ipynb", "w") as f:
            f.write("some text here")

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert os.path.exists(f"{workdir_1}/awholenewname.ipynb")

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/save_as",
                query_string={
                    "filename": "awholenewname",
                    "directory": "/tmp/test_nb_2/",
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 400
            assert response.json()["detail"] == f"File already exists"

            response = await client.patch(
                f"/notebooks/{uuid}/save_as",
                query_string={
                    "filename": "awholenewname",
                    "directory": "/tmp/test_nb_2/",
                    "overwrite": True,
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"/tmp/test_nb_2/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["path"]
                == f"{workdir_1}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert os.path.exists(f"{workdir_1}/awholenewname.ipynb")
            assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

        with open(f"{workdir_1}/awholenewname.ipynb", "r") as f:
            assert f.read() != "some text here"


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestD1Commands:
    async def do_test_d1_notify(
        self,
        cell_content: str,
        notifications: List[str],
        remaining_stdout: str,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
    ):
        execute_d1_command = mocker.patch(
            "jupyter_d1.storage.notebook_manager.execute_d1_command"
        )

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        assert cells[1]["execution_count"] is None

        body = {"source": cell_content}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=body,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            cell_streams: List[Dict[str, Any]] = []
            received_info = {
                "received_cell_stream_count": 0,
                "received_cell_update_count": 0,
                "received_cell_execution": False,
                "received_vars": False,
            }

            # Receive cell stream output
            async def receive_cell_stream(data):
                cell_stream = data["cell_stream"]
                expected_output = {
                    "name": "stdout",
                    "text": remaining_stdout,
                    "output_type": "stream",
                }
                assert cell_stream["output"] == expected_output
                assert cell_stream["cell_id"] == cell_uuid
                received_info["received_cell_stream_count"] += 1
                return expected_output

            async def receive_cell_update(data):
                cell_update = data["cell_update"]
                assert len(cell_update) == 1
                cell_d1_data = cell_update[0]["metadata"]["jupyter_d1"]
                assert cell_d1_data["uuid"] == cell_uuid
                if received_info["received_cell_update_count"] == 0:
                    assert cell_d1_data["execution_state"] == "busy"
                    assert (
                        cell_update[0]["execution_count"] is None
                        or cell_update[0]["execution_count"] == 1
                    )
                else:
                    assert cell_d1_data["execution_state"] == "idle"
                    assert cell_update[0]["outputs"] == cell_streams
                    assert cell_update[0]["execution_count"] == 1
                received_info["received_cell_update_count"] += 1

            async def receive_cell_execution(data):
                cell_exec = data["cell_execution_reply"]
                assert cell_exec["cell_id"] == cell_uuid
                assert cell_exec["execution_count"] == 1
                assert len(cell_exec["parent_id"]) == 35
                received_info["received_cell_execution"] = True

            msg_types = [
                "cell_stream",
                "cell_update",
                "cell_execution_reply",
                "vars",
            ]
            for i in range(5):
                data = await receive_json(websocket, 20, msg_types=msg_types)
                if "cell_stream" in data:
                    cell_streams.append(await receive_cell_stream(data))
                if "cell_update" in data:
                    await receive_cell_update(data)
                if "cell_execution_reply" in data:
                    await receive_cell_execution(data)
                if "vars" in data:
                    received_info["received_vars"] = True

            assert received_info["received_cell_update_count"] == 2
            assert received_info["received_cell_execution"]
            assert received_info["received_vars"]
            assert received_info["received_cell_stream_count"] == 1

            execute_d1_command.assert_has_calls(
                [call(note) for note in notifications]
            )

    @pytest.mark.asyncio
    async def test_d1_notify(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
    ):
        cell_content = (
            'print("___callisto_d1_command___{'
            '\\"command_type\\":\\"notify\\",'
            '\\"title\\":\\"atitle\\",'
            '\\"message\\":\\"test6e4\\"}___callisto_d1_command___", '
            ' end="")'
        )
        notifications = [
            '{"command_type":"notify",'
            '"title":"atitle",'
            '"message":"test6e4"}'
        ]
        await self.do_test_d1_notify(
            cell_content,
            notifications,
            "",
            client,
            superuser_token_headers,
            mocker,
        )

    @pytest.mark.asyncio
    async def test_d1_notify_incomplete(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
    ):
        cell_content = (
            'print("ruh___callisto_d1_command___{'
            '\\"command_type\\":\\"notify\\",'
            '\\"title\\":\\"atitle\\",'
            '\\"message\\":\\"test6e4\\"}___callisto_d1_command___mori'
            '___callisto_d1_command___jjuo", '
            ' end="")'
        )
        notifications = [
            '{"command_type":"notify",'
            '"title":"atitle",'
            '"message":"test6e4"}'
        ]
        await self.do_test_d1_notify(
            cell_content,
            notifications,
            "ruhmorijjuo",
            client,
            superuser_token_headers,
            mocker,
        )

    @pytest.mark.asyncio
    async def test_d1_notify_invalid_command(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
    ):
        cell_content = (
            'print("___callisto_d1_command___{'
            '\\"command_type\\":\\"notify\\",'
            '\\"title\\":\\"atitle\\",'
            '\\"message\\":\\"test6e4\\"}___callisto_d1_command___mori'
            "___callisto_d1_command___{jjuo}___callisto_d1_command___"
            'whey", '
            ' end="")'
        )
        notifications = [
            '{"command_type":"notify",'
            '"title":"atitle",'
            '"message":"test6e4"}',
            "{jjuo}",
        ]
        await self.do_test_d1_notify(
            cell_content,
            notifications,
            "moriwhey",
            client,
            superuser_token_headers,
            mocker,
        )


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestNotebooksWebSocket:
    async def get_notebooks_event(self, websocket):
        for i in range(5):
            data = await receive_json(websocket)
            if "notebooks" in data:
                break
        return data

    @pytest.mark.asyncio
    async def test_notebooks_updates(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):

        async with client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            uuid = await upload_notebook(client, superuser_token_headers)

            data = await wait_for_event(websocket, "notebooks", tries=100)
            assert len(data["notebooks"]) == 1
            assert data["notebooks"][0]["uuid"] == uuid
            assert data["notebooks"][0]["name"] == "simple"

            uuid2 = await upload_notebook(
                client,
                superuser_token_headers,
                filename="stateful_simple.ipynb",
            )
            data = await wait_for_event(websocket, "notebooks", tries=100)
            assert len(data["notebooks"]) == 2
            assert data["notebooks"][0]["uuid"] == uuid
            assert data["notebooks"][0]["name"] == "simple"
            assert data["notebooks"][1]["uuid"] == uuid2
            assert data["notebooks"][1]["name"] == "stateful_simple"

            response = await client.delete(
                f"/notebooks/{uuid}", headers=superuser_token_headers
            )
            assert response.status_code == 204
            data = await wait_for_event(websocket, "notebooks", tries=100)
            assert len(data["notebooks"]) == 1
            assert data["notebooks"][0]["uuid"] == uuid2
            assert data["notebooks"][0]["name"] == "stateful_simple"

            response = await client.delete(
                "/notebooks", headers=superuser_token_headers
            )
            assert response.status_code == 204
            data = await wait_for_event(websocket, "notebooks", tries=100)
            assert len(data["notebooks"]) == 0
