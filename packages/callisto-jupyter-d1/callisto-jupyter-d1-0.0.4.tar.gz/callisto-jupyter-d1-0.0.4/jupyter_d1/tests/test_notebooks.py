import json
import os
import pathlib
from typing import Dict, Tuple

import pytest  # type: ignore
from fastapi.testclient import TestClient

from jupyter_d1.settings import settings


def upload_notebook(
    client: TestClient,
    token_headers: Dict[str, str],
    filename: str = "simple.ipynb",
) -> str:
    nb_filename = f"jupyter_d1/tests/notebooks/{filename}"
    nb_json = open(nb_filename).read()
    response = client.post(
        "/notebooks/upload",
        params={"filename": filename},
        data=nb_json,
        headers=token_headers,
    )
    assert response.status_code == 201
    path = response.json()["path"]

    response = client.get(
        f"/notebooks/open/?filepath={path}", headers=token_headers
    )
    assert response.status_code == 201
    resp_json = response.json()["notebook"]
    uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]
    return uuid


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestNotebook:
    def test_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers)
        response = client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 200
        nb = response.json()["notebook"]
        assert "cells" in nb.keys()
        assert "metadata" in nb.keys()
        assert "nbformat" in nb.keys()
        assert "nbformat_minor" in nb.keys()
        assert nb["metadata"]["jupyter_d1"]["uuid"] == uuid

    def test_notebooks(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        uuid2 = upload_notebook(
            client, superuser_token_headers, "other_simple.ipynb"
        )
        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 2

        ret_uuid = notebooks[0]["metadata"]["jupyter_d1"]["uuid"]
        ret_uuid2 = notebooks[1]["metadata"]["jupyter_d1"]["uuid"]
        assert uuid != uuid2
        assert set([uuid, uuid2]) == set([ret_uuid, ret_uuid2])

    def test_delete_notebooks(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        upload_notebook(client, superuser_token_headers, "simple.ipynb")
        upload_notebook(client, superuser_token_headers, "other_simple.ipynb")
        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()["notebooks"]
        assert len(resp_json) == 2

        response = client.delete("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 204

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()["notebooks"]
        assert len(resp_json) == 0

    def test_delete_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        uuid2 = upload_notebook(
            client, superuser_token_headers, "other_simple.ipynb"
        )
        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()["notebooks"]
        assert len(resp_json) == 2
        ret_uuid = resp_json[0]["metadata"]["jupyter_d1"]["uuid"]
        ret_uuid2 = resp_json[1]["metadata"]["jupyter_d1"]["uuid"]
        assert set([uuid, uuid2]) == set([ret_uuid, ret_uuid2])

        # delete the first one
        response = client.delete(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()["notebooks"]
        assert len(resp_json) == 1
        # remaining notebook should have uuid2
        assert resp_json[0]["metadata"]["jupyter_d1"]["uuid"] == uuid2

    def test_cells(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4

        for cell in cells:
            uuid = cell["metadata"]["jupyter_d1"]["uuid"]
            assert len(uuid) == 36
            uuid = cell["metadata"]["jupyter_d1"]["notebook_uuid"] == uuid

        cell0 = cells[0]
        assert cell0["cell_type"] == "markdown"
        assert cell0["source"] == "## Simple Test Notebook"

        cell1 = cells[1]
        assert cell1["cell_type"] == "code"
        assert cell1["source"] == 'print("Larry the Llama")'

    def test_one_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell1 = cells[1]
        cell1_uuid = cell1["metadata"]["jupyter_d1"]["uuid"]

        response = client.get(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        cell = response.json()["cell"]
        uuid = cell["metadata"]["jupyter_d1"]["uuid"]
        assert uuid == cell1_uuid
        assert cell["cell_type"] == "code"
        assert cell["source"] == 'print("Larry the Llama")'

    def test_patch_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell1 = cells[1]
        cell1_uuid = cell1["metadata"]["jupyter_d1"]["uuid"]

        new_source = 'hello = "world"'
        response = client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=superuser_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 200
        # check that the returned cell has the new source
        cell = response.json()["cell"]
        assert cell["source"] == new_source

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert (
            file_nb["cells"][1]["metadata"]["jupyter_d1"]["uuid"]
            == cell["metadata"]["jupyter_d1"]["uuid"]
        )
        assert file_nb["cells"][1]["source"][0] == new_source

        # check that retrieving the cell has has the new source
        response = client.get(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        cell = response.json()["cell"]
        assert cell["source"] == new_source

    def test_create_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        # get the existing cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        orig_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], cells)
        )

        assert len(orig_uuids) == 4
        before_uuid = orig_uuids[1]  # place the new cell before position 1

        # add a new cell before index 1
        src = "__**Hello Callist**__"
        params = {
            "before": before_uuid,
            "cell_type": "markdown",
            "source": src,
        }
        response = client.post(
            f"/notebooks/{uuid}/cells",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        new_cell = response.json()["cell"]
        assert new_cell["cell_type"] == "markdown"
        assert new_cell["source"] == src

        new_cell_uuid = new_cell["metadata"]["jupyter_d1"]["uuid"]
        assert len(new_cell_uuid) == 36

        # insert the new uuid into the original list
        orig_uuids.insert(1, new_cell_uuid)

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert (
            file_nb["cells"][1]["metadata"]["jupyter_d1"]["uuid"]
            == new_cell["metadata"]["jupyter_d1"]["uuid"]
        )

        # get the new list of cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        new_cells = response.json()["cells"]
        new_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], new_cells)
        )
        assert len(new_uuids) == 5

        # assert the new list of uuids is the old list with the new uuid
        assert new_uuids == orig_uuids

        # add a new cell at the end (omit position parameter)
        response = client.post(
            f"/notebooks/{uuid}/cells",
            json={},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        new_cell = response.json()["cell"]

        new_cell_uuid = new_cell["metadata"]["jupyter_d1"]["uuid"]
        assert len(new_cell_uuid) == 36

        # insert the new uuid into the original list
        orig_uuids.append(new_cell_uuid)

        # get the new list of cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        new_cells = response.json()["cells"]
        new_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], new_cells)
        )

        # assert the new list of uuids is the old list with the new uuid
        assert new_uuids == orig_uuids

    def test_move_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        # get the existing cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        orig_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], cells)
        )

        assert len(orig_uuids) == 4
        # move the third cell 'before' the second cell (swap positions)
        move_uuid = orig_uuids[2]  # place the new cell before position 1
        before_uuid = orig_uuids[1]  # place the new cell before position 1

        params = {"before": before_uuid}
        response = client.get(
            f"/notebooks/{uuid}/cells/{move_uuid}/move",
            params=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

        # This is the expected reordering
        reordered_uuids = [
            orig_uuids[0],
            orig_uuids[2],  # swap indecies 1, 2
            orig_uuids[1],
            orig_uuids[3],
        ]

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        file_uuids = list(
            map(
                lambda x: x["metadata"]["jupyter_d1"]["uuid"], file_nb["cells"]
            )
        )
        assert file_uuids == reordered_uuids

        # get the new list of cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        new_cells = response.json()["cells"]
        new_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], new_cells)
        )
        assert len(new_uuids) == 4

        # assert the new list of uuids is the old list with the new uuid
        assert new_uuids == reordered_uuids

        move_uuid = reordered_uuids[0]
        # move the first cell to the end (omit position parameter)
        response = client.get(
            f"/notebooks/{uuid}/cells/{move_uuid}/move",
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

        # final list just has the first cell moved to the end
        final_uuids = [
            reordered_uuids[1],
            reordered_uuids[2],
            reordered_uuids[3],
            reordered_uuids[0],
        ]

        # get the new list of cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        new_cells = response.json()["cells"]
        new_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], new_cells)
        )

        # assert the new list of uuids is the old list with the new uuid
        assert new_uuids == final_uuids

    def _test_merge_cells(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        uuid: str,
        position: int,
        above: bool,
        cell_types: Tuple[str, str],
    ):
        if above:
            position_1 = position - 1
            position_2 = position
        else:
            position_1 = position
            position_2 = position + 1

        # get the existing cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4
        cell_uuid = cells[position]["metadata"]["jupyter_d1"]["uuid"]
        cell_1_source = cells[position_1]["source"]
        assert cells[position_1]["cell_type"] == cell_types[0]
        cell_2_source = cells[position_2]["source"]
        assert cells[position_2]["cell_type"] == cell_types[1]

        params = {}
        if above:
            params["above"] = True
        response = client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/merge",
            params=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 3
        cell = cells[position_1]
        assert cell["source"] == f"{cell_1_source}\n{cell_2_source}"
        assert cell["cell_type"] == cell_types[1 if above else 0]
        assert cell["metadata"]["jupyter_d1"]["uuid"] == cell_uuid

        response = client.get(
            f"/notebooks/{uuid}/undo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4
        assert cells[position]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid
        assert cells[position_1]["source"] == cell_1_source
        assert cells[position_1]["cell_type"] == cell_types[0]
        assert cells[position_2]["source"] == cell_2_source
        assert cells[position_2]["cell_type"] == cell_types[1]

        response = client.get(
            f"/notebooks/{uuid}/redo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 3
        cell = cells[position_1]
        assert cell["source"] == f"{cell_1_source}\n{cell_2_source}"
        assert cell["cell_type"] == cell_types[1 if above else 0]
        assert cell["metadata"]["jupyter_d1"]["uuid"] == cell_uuid

    def test_merge_cells(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        self._test_merge_cells(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=1,
            above=False,
            cell_types=("code", "code"),
        )

    def test_merge_cells_above(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        self._test_merge_cells(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=1,
            above=True,
            cell_types=("markdown", "code"),
        )

    def test_merge_first_2_cells(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        self._test_merge_cells(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=0,
            above=False,
            cell_types=("markdown", "code"),
        )

    def test_merge_last_2_cells(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        self._test_merge_cells(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=3,
            above=True,
            cell_types=("code", "code"),
        )

    def _test_split_cell(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        uuid: str,
        position: int,
        split_location: int,
        expected_sources: Tuple[str, str],
        cell_type: str,
    ):
        # get the existing cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4
        cell_uuid = cells[position]["metadata"]["jupyter_d1"]["uuid"]
        original_source = cells[position]["source"]
        assert cells[position]["cell_type"] == cell_type

        response = client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/split",
            params={"split_location": split_location},
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 5
        assert cells[position]["source"] == expected_sources[0]
        assert cells[position]["cell_type"] == cell_type
        assert cells[position + 1]["source"] == expected_sources[1]
        assert cells[position + 1]["cell_type"] == cell_type
        assert cells[position]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid

        response = client.get(
            f"/notebooks/{uuid}/undo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4
        assert cells[position]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid
        assert cells[position]["source"] == original_source
        assert cells[position]["cell_type"] == cell_type

        response = client.get(
            f"/notebooks/{uuid}/redo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 5
        assert cells[position]["source"] == expected_sources[0]
        assert cells[position]["cell_type"] == cell_type
        assert cells[position + 1]["source"] == expected_sources[1]
        assert cells[position + 1]["cell_type"] == cell_type
        assert cells[position]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid

    def test_split_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        self._test_split_cell(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=2,
            split_location=2,
            expected_sources=("2+", "5"),
            cell_type="code",
        )

    def test_split_first_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        self._test_split_cell(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=0,
            split_location=11,
            expected_sources=("## Simple T", "est Notebook"),
            cell_type="markdown",
        )

    def test_split_last_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        self._test_split_cell(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=3,
            split_location=0,
            expected_sources=("", ""),
            cell_type="code",
        )

    def test_round_trip(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Check that when a notebook is uploaded, it gets a UUID.
        Then when it is download, uploaded and downloaded again,
        the UUID is different.
        """
        # initial upload
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        # download the notebook, now with uuid
        response = client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 200
        notebook = response.json()["notebook"]
        data = json.dumps(notebook)
        dl1_uuid = notebook["metadata"]["jupyter_d1"]["uuid"]
        assert uuid == dl1_uuid
        assert (
            notebook["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/simple.ipynb"
        )
        assert notebook["metadata"]["jupyter_d1"]["name"] == "simple"

        # delete the notebook on the server
        response = client.delete(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 204

        # upload the downloaded notebook, fail because file exists
        response = client.post(
            "/notebooks/upload",
            params={"filename": "simple.ipynb"},
            data=data,
            headers=superuser_token_headers,
        )
        assert response.status_code == 400
        path = response.json()["detail"] == "File alreaady exists"

        # upload the downloaded notebook with different name,
        # complete with uuid
        response = client.post(
            "/notebooks/upload",
            params={"filename": "isimple.ipynb"},
            data=data,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        path = response.json()["path"]

        # Check that remote file has a different uuid after upload
        with open(f"{settings.ROOT_DIR}/{path}", "r") as f:
            nb = json.loads(f.read())
        file_uuid = nb["metadata"]["jupyter_d1"]["uuid"]
        assert uuid != file_uuid
        assert (
            nb["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/isimple.ipynb"
        )
        assert nb["metadata"]["jupyter_d1"]["name"] == "isimple"

        # Open notebook, check that uuid changes again
        response = client.get(
            f"/notebooks/open/?filepath={path}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        notebook = response.json()["notebook"]
        open_uuid = notebook["metadata"]["jupyter_d1"]["uuid"]
        assert uuid != open_uuid
        assert file_uuid != open_uuid
        assert (
            notebook["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/isimple.ipynb"
        )
        assert notebook["metadata"]["jupyter_d1"]["name"] == "isimple"

        # Check that new uuid was written to disk after opening the notebook
        with open(f"{settings.ROOT_DIR}/{path}", "r") as f:
            nb = json.loads(f.read())
        new_file_uuid = nb["metadata"]["jupyter_d1"]["uuid"]
        assert new_file_uuid == open_uuid
        assert (
            nb["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/isimple.ipynb"
        )
        assert nb["metadata"]["jupyter_d1"]["name"] == "isimple"

        # finally, get the notebook again and make sure the
        # uuid is the same as when opened
        response = client.get(
            f"/notebooks/{open_uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 200
        notebook = response.json()["notebook"]
        dl2_uuid = notebook["metadata"]["jupyter_d1"]["uuid"]
        assert open_uuid == dl2_uuid

    def test_cell_state_reset(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Check that when a notebook is uploaded, cells states get reset to
        idle and execution counts are reset
        """
        # initial upload
        uuid = upload_notebook(
            client, superuser_token_headers, "stateful_simple.ipynb"
        )

        # download the notebook
        response = client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 200
        notebook = response.json()["notebook"]
        dl1_uuid = notebook["metadata"]["jupyter_d1"]["uuid"]
        assert uuid == dl1_uuid
        assert (
            notebook["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/stateful_simple.ipynb"
        )
        assert notebook["metadata"]["jupyter_d1"]["name"] == "stateful_simple"

        for cell in notebook["cells"]:
            if "jupyter_d1" in cell["metadata"]:
                d1_data = cell["metadata"]["jupyter_d1"]
                if "execution_state" in d1_data:
                    assert d1_data["execution_state"] == "idle"
            if "execution_count" in cell:
                assert cell["execution_count"] is None

    def test_get_bogus_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        "Test error condition when downloading an non-existent notebook."
        from uuid import uuid4

        uuid = uuid4()
        response = client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 404
        resp_json = response.json()
        assert resp_json["error"] == "NOTEBOOK_NOT_FOUND"
        assert resp_json["reason"] == f"Notebook not found with uuid: {uuid}"
        assert resp_json["detail"] is None

    def test_get_bogus_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        "Test error condition when downloading an non-existent cell."
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        from uuid import uuid4

        cell_uuid = uuid4()
        response = client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 404
        resp_json = response.json()
        assert resp_json["error"] == "CELL_NOT_FOUND"
        assert resp_json["reason"] == f"Cell not found with uuid: {cell_uuid}"
        assert resp_json["detail"] is None

    def test_bogus_kernel(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        "Test notebook upload that has an unsupported kernel."
        upload_notebook(client, superuser_token_headers, "weird_kernel.ipynb")

    def test_upload_to_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        os.mkdir(f"{settings.ROOT_DIR}/aproject")
        with open(f"jupyter_d1/tests/notebooks/simple.ipynb", "r") as f:
            nb_raw = f.read()
        response = client.post(
            "/notebooks/upload",
            params={"directory": "aproject", "filename": "koy"},
            data=nb_raw,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        path = response.json()["path"]
        assert path == f"aproject/koy.ipynb"

        with open(f"{settings.ROOT_DIR}/{path}", "r") as f:
            nb = json.loads(f.read())
        file_uuid = nb["metadata"]["jupyter_d1"]["uuid"]
        assert file_uuid is not None
        assert (
            nb["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/{path}"
        )
        assert nb["metadata"]["jupyter_d1"]["name"] == "koy"

        response = client.get(
            f"/notebooks/open/?filepath={path}",
            headers=superuser_token_headers,
        )

        assert response.status_code == 201
        nb = response.json()["notebook"]
        uuid = nb["metadata"]["jupyter_d1"]["uuid"]
        assert uuid != file_uuid
        assert (
            nb["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/{path}"
        )
        assert nb["metadata"]["jupyter_d1"]["name"] == "koy"

    def test_upload_to_directory_fail(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        with open(f"jupyter_d1/tests/notebooks/simple.ipynb", "r") as f:
            nb = json.loads(f.read())
        response = client.post(
            "/notebooks/upload",
            params={"directory": "aproject", "filename": "koy"},
            data=nb,
            headers=superuser_token_headers,
        )
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == f"Directory does not exist {settings.ROOT_DIR}/aproject"
        )

    def test_working_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = client.post(
            "/notebooks/upload",
            params={"filename": "name.ipynb"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        assert response.json()["path"] == "name.ipynb"
        response = client.get(
            "/notebooks/open/?filepath=name.ipynb",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]
        response = client.delete(
            f"/notebooks/{uuid}", data=nb_json, headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = client.get(
            "/notebooks/open/?filepath=name.ipynb",
            headers=superuser_token_headers,
            params={"working_directory": "/tmp"},
        )
        assert response.json()["notebook"]["metadata"]["jupyter_d1"][
            "working_directory"
        ] == str(pathlib.Path("/tmp").resolve())

    def test_upload_and_open_in_memory_no_working_dir_specified(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should default to root dir, 
        notebook should not be saved on disk.
        """
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = client.post(
            "/notebooks/upload_and_open",
            params={"filename": "name.ipynb", "autosave": False},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        # Do an action that would save the notebook if autosave was true
        cell1_uuid = resp_json["notebook"]["cells"][1]["metadata"][
            "jupyter_d1"
        ]["uuid"]
        new_source = 'hello = "world"'
        response = client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=superuser_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 200

        assert not os.path.exists(f"{settings.ROOT_DIR}/name.ipynb")

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == settings.ROOT_DIR
        )

    def test_upload_and_open_in_memory_file_exists_but_its_fine(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Opening notebook in memory when file exists should work fine.
        """
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        with open(f"{settings.ROOT_DIR}/name.ipynb", "w") as f:
            f.write(nb_json)
        response = client.post(
            "/notebooks/upload_and_open",
            params={"filename": "name.ipynb", "autosave": False},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert os.path.exists(f"{settings.ROOT_DIR}/name.ipynb")

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == settings.ROOT_DIR
        )

    def test_upload_and_open_in_memory_working_dir_specified(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should be set to specified directory, 
        notebook should not be saved on disk.
        """
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = client.post(
            "/notebooks/upload_and_open",
            params={
                "filename": "name.ipynb",
                "autosave": False,
                "working_directory": f"{os.getcwd()}/jupyter_d1"
                "/tests/notebooks",
            },
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert not os.path.exists(f"{settings.ROOT_DIR}/name.ipynb")
        # This should be impossible, but might as well check it
        assert not os.path.exists(
            f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb"
        )

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )

    def test_upload_and_open_no_working_dir_specified(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should default to root dir, 
        notebook should be saved on disk.
        """
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = client.post(
            "/notebooks/upload_and_open",
            params={"filename": "name.ipynb"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert os.path.exists(f"{settings.ROOT_DIR}/name.ipynb")

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == settings.ROOT_DIR
        )

    def test_upload_and_open_working_dir_defaults_to_root_dir(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should default to root dir, 
        notebook should be saved on disk.
        """
        try:
            os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")
        except Exception:
            pass
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = client.post(
            "/notebooks/upload_and_open",
            params={
                "filename": "name.ipynb",
                "directory": f"{os.getcwd()}/jupyter_d1/tests/notebooks",
            },
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert os.path.exists(
            f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb"
        )

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )
        os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")

    def test_upload_and_open_working_dir_defaults_to_dir(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should default to directory provided (where notebook
        is also saved), notebook should be saved on disk.
        """
        try:
            os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")
        except Exception:
            pass
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = client.post(
            "/notebooks/upload_and_open",
            params={
                "filename": "name.ipynb",
                "directory": f"{os.getcwd()}/jupyter_d1/tests/notebooks",
            },
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert os.path.exists(
            f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb"
        )

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )
        os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")

    def test_upload_and_open_working_directory_specified(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should be set to provided working dir, 
        notebook should be saved on disk.
        """
        try:
            os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")
        except Exception:
            pass
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = client.post(
            "/notebooks/upload_and_open",
            params={
                "filename": "name.ipynb",
                "directory": f"{os.getcwd()}/jupyter_d1/tests/notebooks",
                "working_directory": "/tmp",
            },
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert resp_json["notebook"]["metadata"]["jupyter_d1"][
            "working_directory"
        ] == str(pathlib.Path("/tmp").resolve())
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert os.path.exists(
            f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb"
        )

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert notebooks[0]["metadata"]["jupyter_d1"][
            "working_directory"
        ] == str(pathlib.Path("/tmp").resolve())
        os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")

    def test_open_notebook_file_twice_returns_same_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """Opening a notebook twice returns an error"""
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = client.post(
            "/notebooks/upload",
            params={"filename": "name.ipynb"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        assert response.json()["path"] == "name.ipynb"
        response = client.get(
            "/notebooks/open/?filepath=name.ipynb",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        metadata = response.json()["notebook"]["metadata"]["jupyter_d1"]
        assert metadata["working_directory"] == settings.ROOT_DIR
        uuid = metadata["uuid"]

        response = client.get(
            "/notebooks/open/?filepath=name.ipynb",
            headers=superuser_token_headers,
            params={"working_directory": "/tmp"},
        )
        assert response.status_code == 201
        metadata = response.json()["notebook"]["metadata"]["jupyter_d1"]
        assert metadata["working_directory"] == settings.ROOT_DIR
        assert metadata["uuid"] == uuid

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == settings.ROOT_DIR
        )

    def test_upload_and_open_notebook_twice_returns_same_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = client.post(
            "/notebooks/upload_and_open",
            params={"autosave": False},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert not os.path.exists(f"{settings.ROOT_DIR}/name.ipynb")

        response = client.post(
            "/notebooks/upload_and_open",
            params={"autosave": False, "working_directory": "/tmp"},
            data=json.dumps(resp_json["notebook"]),
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        assert resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"] == uuid

        response = client.get("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == settings.ROOT_DIR
        )


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestNotebookPermissions:
    def test_notebooks(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
    ):
        upload_notebook(client, superuser_token_headers, "simple.ipynb")
        upload_notebook(client, superuser_token_headers, "other_simple.ipynb")
        response = client.get(
            "/notebooks", headers=permissionless_token_headers
        )
        assert response.status_code == 403
        response = client.get("/notebooks", headers=readonly_token_headers)
        assert response.status_code == 200

    def test_notebook(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = upload_notebook(client, superuser_token_headers)
        response = client.get(
            f"/notebooks/{uuid}", headers=permissionless_token_headers
        )
        assert response.status_code == 403
        response = client.get(
            f"/notebooks/{uuid}", headers=readonly_token_headers
        )
        assert response.status_code == 200

    def test_delete_notebooks(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        upload_notebook(client, superuser_token_headers, "simple.ipynb")
        upload_notebook(client, superuser_token_headers, "other_simple.ipynb")
        response = client.delete("/notebooks", headers=readonly_token_headers)
        assert response.status_code == 403
        response = client.delete("/notebooks", headers=superuser_token_headers)
        assert response.status_code == 204

    def test_delete_notebook(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")
        response = client.delete(
            f"/notebooks/{uuid}", headers=readonly_token_headers
        )
        assert response.status_code == 403
        response = client.delete(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 204

    def test_cells(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=permissionless_token_headers
        )
        assert response.status_code == 403
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=readonly_token_headers
        )
        assert response.status_code == 200

    def test_one_cell(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=readonly_token_headers
        )
        assert response.status_code == 200
        cell1_uuid = response.json()["cells"][1]["metadata"]["jupyter_d1"][
            "uuid"
        ]

        response = client.get(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=permissionless_token_headers,
        )
        assert response.status_code == 403
        response = client.get(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=readonly_token_headers,
        )
        assert response.status_code == 200

    def test_patch_cell(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cell1_uuid = response.json()["cells"][1]["metadata"]["jupyter_d1"][
            "uuid"
        ]

        new_source = 'hello = "world"'
        response = client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=readonly_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 403
        response = client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=superuser_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 200

    def test_patch_and_execute_cell(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cell1_uuid = response.json()["cells"][1]["metadata"]["jupyter_d1"][
            "uuid"
        ]

        new_source = 'hello = "world"'
        response = client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}/execute",
            headers=readonly_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 403
        response = client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}/execute",
            headers=superuser_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 200

        uuid = response.json()["cell"]["metadata"]["jupyter_d1"]["uuid"]
        assert len(uuid) == 36
        message_id = response.json()["kernel_message"]["message_id"]
        assert len(message_id) == 35

    def test_create_cell(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        # add a new cell
        src = "__**Hello Callist**__"
        params = {"cell_type": "markdown", "source": src}
        response = client.post(
            f"/notebooks/{uuid}/cells",
            json=params,
            headers=readonly_token_headers,
        )
        assert response.status_code == 403
        response = client.post(
            f"/notebooks/{uuid}/cells",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201

    def test_move_cell(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = upload_notebook(client, superuser_token_headers, "simple.ipynb")

        # get the existing cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        move_uuid = response.json()["cells"][2]["metadata"]["jupyter_d1"][
            "uuid"
        ]

        response = client.get(
            f"/notebooks/{uuid}/cells/{move_uuid}/move",
            headers=readonly_token_headers,
        )
        assert response.status_code == 403
        response = client.get(
            f"/notebooks/{uuid}/cells/{move_uuid}/move",
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

    def test_upload_notebook(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = client.post(
            "/notebooks/upload", data=nb_json, headers=readonly_token_headers
        )
        assert response.status_code == 403
        response = client.post(
            "/notebooks/upload",
            params={"filename": "name.ipynb"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        assert response.json()["path"] == "name.ipynb"
        response = client.get(
            "/notebooks/open/?filepath=name.ipynb",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
