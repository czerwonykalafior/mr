import typing as t

from main import Morphy


@Morphy.register_node_type()
class map(Morphy):
    def __init__(self, parent_node: Morphy):
        super().__init__(parent_node)

    def execute_node(self, data_to_process, called_by=None):
        print(data_to_process)
        return self._emit(data_to_process + 1)


@Morphy.register_node_type()
class filter(Morphy):
    def __init__(self, parent_node, predicate):
        self.predicate = predicate
        super(filter, self).__init__(parent_node)

    def execute_node(self, data_to_process, called_by=None):
        if self.predicate:
            data_to_process += data_to_process + 1
        return self._emit(data_to_process)


@Morphy.register_node_type()
class union(Morphy):
    def __init__(self, parent_node: Morphy, parent_nodes: t.Iterable[Morphy]):
        super(union, self).__init__(parent_node, parent_nodes)

    def execute_node(self, data_to_process, called_by=None):
        return self._emit(data_to_process)
