import traceback
from typing import Any, Callable, Dict, List

from fastapi.logger import logger


class Action:
    def __init__(
        self,
        func: Callable,
        args: List[Any] = [],
        kwargs: Dict[str, Any] = {},
        name: str = "",
    ):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.name = name

    def do(self):
        self.func(*self.args, **self.kwargs)

    def __repr__(self):
        return (
            f"Action(func={self.func}, args={self.args}, "
            + f"kwargs={self.kwargs}, name={self.name})"
        )


class UndoManager:
    def __init__(self, logging: bool = False):
        self.logging = logging
        self.logging = True
        self.reset()
        self._undo_in_progress = False
        self._redo_in_progress = False
        self._pause = False
        self._undo_in_progress_name = ""
        self._redo_in_progress_name = ""

    def debug_log(self, msg: str, force: bool = False):
        if self.logging or force:
            logger.debug(msg)

    def pause(self):
        self._pause = True

    def unpause(self):
        self._pause = False

    def reset(self):
        "Clear both the undo and redo stacks"
        self.debug_log(f"Resetting undo/redo stacks")
        self.undo_actions: List[Action] = []
        self.redo_actions: List[Action] = []

    def add_action(
        self,
        func: Callable,
        args: List[Any] = [],
        kwargs: Dict[str, Any] = {},
        name: str = "",
    ):
        "Push a new action onto the undo stack."

        if self._pause:
            return

        action = Action(func, args=args, kwargs=kwargs, name=name)

        if self._undo_in_progress and self._redo_in_progress:
            self.debug_log(
                f"Undo action and Redo action in progress,"
                + f" ignoring new action: {name}"
            )
            return

        if self._undo_in_progress:
            action.name = self._undo_in_progress_name
            self.debug_log(
                f"Undo action in progress, adding new action to redo: {name}"
            )
            self.redo_actions.append(action)
            return

        if self._redo_in_progress:
            action.name = self._redo_in_progress_name
            self.debug_log(
                f"Redo action in progress, adding new action to undo: {name}"
            )
            self.undo_actions.append(action)
            return

        self.undo_actions.append(action)

    @property
    def can_undo(self) -> bool:
        "Is there an undo action in the stack"
        return len(self.undo_actions) > 0

    @property
    def can_redo(self) -> bool:
        "Is there an redo action in the stack"
        return len(self.redo_actions) > 0

    def undo(self):
        """
        Perform the next action in the undo stack and move it to
        the redo stack.
        """
        if self.can_undo:
            self.debug_log(f"Attempting undo for {self.next_undo_name}")
            action = self.undo_actions.pop()
            try:
                self._undo_in_progress = True
                self._undo_in_progress_name = action.name
                action.do()
                self._undo_in_progress = False
                self.debug_log(f"Undo complete")
            except Exception as e:  # noqa
                tb = traceback.format_exc()
                self.debug_log(f"Undo failed: {e}\n{tb}", force=True)
                self.reset()
                return
        else:
            self.debug_log(f"Unable to undo. Undo stack is empty!")

    def redo(self):
        """
        Perform the next action in the redo stack and move it to
        the undo stack.
        """
        if self.can_redo:
            self.debug_log(f"Attempting redo for {self.next_redo_name}")
            action = self.redo_actions.pop()
            try:
                self._redo_in_progress = True
                self._redo_in_progress_name = action.name
                action.do()
                self._redo_in_progress = False
                self.debug_log(f"Redo complete")
            except Exception as e:  # noqa
                tb = traceback.format_exc()
                self.debug_log(f"Redo failed: {e}\n{tb}", force=True)
                self.reset()
                return
        else:
            self.debug_log(f"Unable to redo. Redo stack is empty!")

    @property
    def undo_count(self) -> int:
        "Number of actions in the undo stack."
        return len(self.undo_actions)

    @property
    def redo_count(self) -> int:
        "Number of actions in the redo stack."
        return len(self.redo_actions)

    @property
    def next_undo_name(self) -> str:
        "Name of the next action in the undo stack"
        if self.can_undo:
            return self.undo_actions[-1].name
        else:
            return ""

    @property
    def next_redo_name(self) -> str:
        "Name of the next action in the redo stack"
        if self.can_redo:
            return self.redo_actions[-1].name
        else:
            return ""
