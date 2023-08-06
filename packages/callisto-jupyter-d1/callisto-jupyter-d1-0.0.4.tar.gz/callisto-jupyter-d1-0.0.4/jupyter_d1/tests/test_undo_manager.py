from jupyter_d1.undo_manager import UndoManager

logging = False


class Seq:
    def __init__(self, seq, undo_manager):
        "Wraps a list of int"
        self._seq = seq
        self.undo_manager = undo_manager

    def add(self, value=1):
        "Add 'value' to the end of the list."
        self._seq.append(value)
        self.undo_manager.add_action(self.remove, name=f"Add {value}")

    def remove(self):
        "Removes the last item from the list"
        value = self._seq.pop()
        kwargs = {"value": value}
        self.undo_manager.add_action(
            self.add, kwargs=kwargs, name=f"Remove {value}"
        )
        return value

    def bulk_add(self, values=[]):
        "Add values to the end of the list"
        count = len(values)
        self.undo_manager.pause()
        for value in values:
            self.add(value)
        self.undo_manager.unpause()

        kwargs = {"count": count}
        self.undo_manager.add_action(
            self.bulk_remove, kwargs=kwargs, name=f"Bulk add {len(values)}"
        )

    def bulk_remove(self, count):
        "Remove 'count' values from the list"
        self.undo_manager.pause()
        values = []
        for i in range(count):
            value = self.remove()
            values.append(value)
        self.undo_manager.unpause()

        values.reverse()  # for undo, need reverse order
        kwargs = {"values": values}
        self.undo_manager.add_action(
            self.bulk_add, kwargs=kwargs, name=f"Bulk remove {len(values)}"
        )

    @property
    def seq(self):
        return self._seq


class TestUndoManager:
    def test_undo_bulk(self):
        um = UndoManager(logging=logging)
        assert um.undo_count == 0
        assert um.redo_count == 0

        seq = Seq([11, 12], um)
        assert seq.seq == [11, 12]

        seq.bulk_add([25, 26, 27])
        assert seq.seq == [11, 12, 25, 26, 27]
        assert um.undo_count == 1
        assert um.redo_count == 0
        assert um.next_undo_name == "Bulk add 3"

        um.undo()
        assert seq.seq == [11, 12]
        assert um.undo_count == 0
        assert um.redo_count == 1
        assert um.next_redo_name == "Bulk add 3"

        um.redo()
        assert seq.seq == [11, 12, 25, 26, 27]
        assert um.undo_count == 1
        assert um.redo_count == 0
        assert um.next_undo_name == "Bulk add 3"

        seq.bulk_remove(2)
        assert seq.seq == [11, 12, 25]
        assert um.undo_count == 2
        assert um.redo_count == 0
        assert um.next_undo_name == "Bulk remove 2"

        um.undo()
        assert seq.seq == [11, 12, 25, 26, 27]
        assert um.undo_count == 1
        assert um.redo_count == 1
        assert um.next_redo_name == "Bulk remove 2"

        um.redo()
        assert seq.seq == [11, 12, 25]
        assert um.undo_count == 2
        assert um.redo_count == 0
        assert um.next_undo_name == "Bulk remove 2"

    def test_undo(self):
        um = UndoManager(logging=logging)
        assert um.undo_count == 0
        assert um.redo_count == 0

        seq = Seq([1, 2], um)
        assert seq.seq == [1, 2]

        seq.add(3)
        assert seq.seq == [1, 2, 3]
        assert um.undo_count == 1
        assert um.next_undo_name == "Add 3"
        assert um.redo_count == 0

        um.undo()
        assert seq.seq == [1, 2]
        assert um.undo_count == 0
        assert um.redo_count == 1
        assert um.next_redo_name == "Add 3"

        # extra undo() calls shouldn't do anything
        um.undo()
        um.undo()
        um.undo()
        assert seq.seq == [1, 2]
        assert um.undo_count == 0
        assert um.redo_count == 1
        assert um.next_redo_name == "Add 3"

        um.redo()
        assert seq.seq == [1, 2, 3]
        assert um.undo_count == 1
        assert um.next_undo_name == "Add 3"
        assert um.redo_count == 0

        # more redo() calls shouldn't do anything.
        um.redo()
        um.redo()
        um.redo()
        assert seq.seq == [1, 2, 3]
        assert um.undo_count == 1
        assert um.next_undo_name == "Add 3"
        assert um.redo_count == 0

        seq.remove()
        assert seq.seq == [1, 2]
        assert um.undo_count == 2
        assert um.next_undo_name == "Remove 3"
        assert um.redo_count == 0

        um.undo()
        assert seq.seq == [1, 2, 3]
        assert um.undo_count == 1
        assert um.next_undo_name == "Add 3"
        assert um.redo_count == 1
        assert um.next_redo_name == "Remove 3"

        um.redo()
        assert seq.seq == [1, 2]
        assert um.undo_count == 2
        assert um.next_undo_name == "Remove 3"
        assert um.redo_count == 0
