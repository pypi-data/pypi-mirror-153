import json
from typing import Dict

import pytest  # type: ignore
from fastapi.testclient import TestClient

from jupyter_d1.settings import settings

from .test_notebooks import upload_notebook


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestUndo:
    def get_uuids(self, cells):
        def uuid(cell):
            return cell["metadata"]["jupyter_d1"]["uuid"]

        return list(map(uuid, cells))

    def test_undo_delete(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers)

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        # Start with 4 cells
        assert len(cells) == 4
        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        # Delete a cell
        response = client.delete(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert len(file_nb["cells"]) == 3

        # Now 3 cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 3

        # Undo deletion
        response = client.get(
            f"/notebooks/{uuid}/undo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert len(file_nb["cells"]) == 4

        # Back to original, 4 cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4

        # Redo the deletion
        response = client.get(
            f"/notebooks/{uuid}/redo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert len(file_nb["cells"]) == 3

        # Back to 3 cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 3

    def test_undo_create(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers)

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        # Start with 4 cells
        assert len(cells) == 4
        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        # Add a cell
        src = "__**Hello Callisto**__"
        params = {"before": cell_uuid, "cell_type": "markdown", "source": src}
        response = client.post(
            f"/notebooks/{uuid}/cells",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        new_cell = response.json()["cell"]
        assert new_cell["cell_type"] == "markdown"
        assert new_cell["source"] == "__**Hello Callisto**__"

        # Now 5 cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 5

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert len(file_nb["cells"]) == 5

        # Undo creation
        response = client.get(
            f"/notebooks/{uuid}/undo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert len(file_nb["cells"]) == 4

        # Back to original, 4 cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4

        # Redo the addition
        response = client.get(
            f"/notebooks/{uuid}/redo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert len(file_nb["cells"]) == 5

        # Back to 5 cells
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 5

        # check the contents of the new cell are correct
        cell = cells[2]
        assert cell["cell_type"] == "markdown"
        assert cell["source"] == "__**Hello Callisto**__"
        # Same for file on disk
        assert file_nb["cells"][2]["cell_type"] == "markdown"
        assert file_nb["cells"][2]["source"] == ["__**Hello Callisto**__"]

    def test_undo_update(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers)

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        # Start with 4 cells
        assert len(cells) == 4
        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]
        assert cell["cell_type"] == "code"
        assert cell["source"] == "2+5"

        # Update a cell
        src = "__**Hello Callisto**__"
        params = {"cell_type": "markdown", "source": src}
        response = client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        cell = response.json()["cell"]
        assert cell["cell_type"] == "markdown"
        assert cell["source"] == src

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert file_nb["cells"][2]["source"] == [src]
        assert file_nb["cells"][2]["cell_type"] == "markdown"

        # Undo update
        response = client.get(
            f"/notebooks/{uuid}/undo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert file_nb["cells"][2]["source"] == ["2+5"]
        assert file_nb["cells"][2]["cell_type"] == "code"

        # Back to original content
        response = client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            headers=superuser_token_headers,
        )
        cell = response.json()["cell"]
        assert response.status_code == 200
        assert cell["cell_type"] == "code"
        assert cell["source"] == "2+5"

        # Redo update
        response = client.get(
            f"/notebooks/{uuid}/redo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert file_nb["cells"][2]["source"] == [src]
        assert file_nb["cells"][2]["cell_type"] == "markdown"

        # Now updated content
        response = client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            headers=superuser_token_headers,
        )
        cell = response.json()["cell"]
        assert response.status_code == 200
        assert cell["cell_type"] == "markdown"
        assert cell["source"] == src

    def test_undo_move(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = upload_notebook(client, superuser_token_headers)

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        uuids = self.get_uuids(cells)
        assert len(uuids) == 4

        uuid_a = uuids[0]
        uuid_b = uuids[1]
        uuid_c = uuids[2]
        uuid_d = uuids[3]

        # 'move' with no query param should move uuid_b
        # to the end of the list
        response = client.get(
            f"/notebooks/{uuid}/cells/{uuid_b}/move",
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert self.get_uuids(file_nb["cells"]) == [
            uuid_a,
            uuid_c,
            uuid_d,
            uuid_b,
        ]

        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        uuids = self.get_uuids(response.json()["cells"])
        assert uuids == [uuid_a, uuid_c, uuid_d, uuid_b]

        # Undo move
        response = client.get(
            f"/notebooks/{uuid}/undo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert self.get_uuids(file_nb["cells"]) == [
            uuid_a,
            uuid_b,
            uuid_c,
            uuid_d,
        ]

        # Back to original order
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        uuids = self.get_uuids(response.json()["cells"])
        assert uuids == [uuid_a, uuid_b, uuid_c, uuid_d]

        # Redo the move
        response = client.get(
            f"/notebooks/{uuid}/redo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert self.get_uuids(file_nb["cells"]) == [
            uuid_a,
            uuid_c,
            uuid_d,
            uuid_b,
        ]

        # Back to altered order
        response = client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        uuids = self.get_uuids(response.json()["cells"])
        assert uuids == [uuid_a, uuid_c, uuid_d, uuid_b]


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestUndoPermissions:
    def get_uuids(self, cells):
        def uuid(cell):
            return cell["metadata"]["jupyter_d1"]["uuid"]

        return list(map(uuid, cells))

    def test_undo_permission(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = upload_notebook(client, superuser_token_headers)

        response = client.get(
            f"/notebooks/{uuid}/undo", headers=readonly_token_headers
        )
        assert response.status_code == 403
        response = client.get(
            f"/notebooks/{uuid}/undo", headers=superuser_token_headers
        )
        assert response.status_code == 204

    def test_redo_permission(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = upload_notebook(client, superuser_token_headers)

        response = client.get(
            f"/notebooks/{uuid}/redo", headers=readonly_token_headers
        )
        assert response.status_code == 403
        response = client.get(
            f"/notebooks/{uuid}/redo", headers=superuser_token_headers
        )
        assert response.status_code == 204
