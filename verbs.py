import typing as t

from main import Morphy


@Morphy.register_node_type()
class map(Morphy):
    def __init__(self, parent_node: Morphy, func: callable):
        self.func = func
        super().__init__(parent_node)

    def execute_node(self, data_to_process, called_by=None):
        result = self.func(data_to_process)
        return self._emit(result)


@Morphy.register_node_type()
class filter(Morphy):
    def __init__(self, parent_node: Morphy, predicate: callable, func: callable, ):
        self.predicate = predicate
        self.func = func
        super().__init__(parent_node)

    def execute_node(self, data_to_process, called_by=None):
        if self.predicate(data_to_process):
            result = self.func(data_to_process)
            return self._emit(result)


@Morphy.register_node_type()
class union(Morphy):
    def __init__(self, parent_node: Morphy, parent_nodes: t.Iterable[Morphy]):
        super().__init__(parent_node, parent_nodes)

    def execute_node(self, data_to_process, called_by=None):
        return self._emit(data_to_process)


@Morphy.register_node_type()
class union_map(Morphy):
    def __init__(self, parent_node: Morphy, parent_nodes: t.Iterable[Morphy], func: callable):
        super().__init__(parent_node, parent_nodes)
        self.func = func

    def execute_node(self, data_to_process, called_by=None):
        result = self.func(data_to_process)
        return self._emit(result)
