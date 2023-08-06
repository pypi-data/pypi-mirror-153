import os
from pathlib import Path
from typing import Optional
from uuid import UUID, uuid4

from fastapi.logger import logger
from nbformat.notebooknode import NotebookNode  # type: ignore


class NotebookValidator:
    def _validate_jupyter_metadata_node(self, node):
        """
        Create the jupyter_d1 section in the node's metadata if it
        doesn't exist.
        """
        if "jupyter_d1" not in node.metadata.keys():
            node.metadata.jupyter_d1 = NotebookNode()

    def _validate_jupyter_metadata(self, notebook_node: NotebookNode):
        "Ensure all the notebook nodes have jupyter_d1 section"
        self._validate_jupyter_metadata_node(notebook_node)
        for cell in notebook_node.cells:
            self._validate_jupyter_metadata_node(cell)

    def _validate_uuid_node(
        self, node, force_new: bool = False, reset_state: bool = False
    ) -> UUID:
        "Return the uuid from a node's metadata.  Create one if it is missing."
        if "uuid" not in node.metadata.jupyter_d1.keys() or force_new:
            node.metadata.jupyter_d1.uuid = uuid4()
        if reset_state:
            node.metadata.jupyter_d1.execution_state = "idle"
            if "execution_count" in node:
                node.execution_count = None
        return node.metadata.jupyter_d1.uuid

    def _validate_uuids(
        self,
        notebook_node: NotebookNode,
        new_notebook_uuid: bool = False,
        reset_state: bool = False,
    ) -> UUID:
        "Ensure all the notebook nodes have uuids & return the notebook uuid."
        nb_uuid = self._validate_uuid_node(notebook_node, new_notebook_uuid)
        uuids = [nb_uuid]
        for cell in notebook_node.cells:
            cell_uuid = self._validate_uuid_node(cell, reset_state=reset_state)
            cell.metadata.jupyter_d1.notebook_uuid = nb_uuid
            uuids.append(cell_uuid)

        # Check for uniqueness in UUIDs
        uuid_set = set(uuids)
        if len(uuids) != len(uuid_set):
            for uuid in uuid_set:
                uuids.remove(uuid)
            logger.error(f"Duplicate UUID(s) found in validation. {uuids}")
            raise IndexError(f"Duplicate uuids in notebook: {uuids}")
        return nb_uuid

    def _validate_positions(self, notebook_node: NotebookNode):
        "Renumber all the cells according to their current position"
        for (idx, cell) in enumerate(notebook_node.cells):
            cell.metadata.jupyter_d1.position = idx

    def _validate_path(
        self,
        notebook_node: NotebookNode,
        directory: Optional[str],
        filename: str,
    ):
        "Set name and path attribute in metadata"
        notebook_node.metadata.jupyter_d1.name = filename
        path = f"{filename}.ipynb"
        if directory is not None:
            try:
                directory = str(Path(directory).resolve())
            except Exception as e:
                logger.error(e)
            path = f"{directory}/{path}"
        notebook_node.metadata.jupyter_d1.path = path

    def _validate_working_dir(
        self,
        notebook_node: NotebookNode,
        working_directory: Optional[str],
        directory: Optional[str],
    ):
        """
        Set working_directory attribute in metadata.

        Priority is working_directory parameter, existing metadata
        working_directory, and then defaults to directory
        """
        d1_meta = notebook_node.metadata.jupyter_d1
        if working_directory is None:
            working_directory = d1_meta.get("working_directory", None)
        if working_directory is None or not os.path.exists(working_directory):
            working_directory = directory
        if working_directory is not None:
            try:
                working_directory = str(Path(working_directory).resolve())
            except Exception as e:
                logger.error(e)
        d1_meta.working_directory = working_directory

    def validate(
        self,
        notebook_node: NotebookNode,
        directory: Optional[str] = None,
        filename: Optional[str] = None,
        working_directory: Optional[str] = None,
        new_notebook_uuid: bool = False,
        reset_state: bool = False,
    ):
        """
        Ensure all the notebook nodes have positions and uuids
        """
        self._validate_jupyter_metadata(notebook_node)
        self._validate_positions(notebook_node)
        self._validate_uuids(
            notebook_node, new_notebook_uuid, reset_state=reset_state
        )
        if filename is not None:
            self._validate_path(notebook_node, directory, filename)
        if directory is not None or working_directory is not None:
            self._validate_working_dir(
                notebook_node, working_directory, directory
            )
