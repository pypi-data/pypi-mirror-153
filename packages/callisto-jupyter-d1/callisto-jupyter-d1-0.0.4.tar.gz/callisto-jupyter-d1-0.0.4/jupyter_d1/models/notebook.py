from typing import List

from .base_wrapper import BaseWrapper
from .JSONType import JSONType


class NotebookWrapper(BaseWrapper):
    notebook: JSONType


class NotebooksWrapper(BaseWrapper):
    notebooks: List[JSONType]


class NotebookPath(BaseWrapper):
    path: str
