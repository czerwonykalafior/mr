from __future__ import annotations
import functools
import typing as t


class Morphy:
    """ Base node type in Morphy. Graph is build by subscribing to previous nodes.
     Node keeps references to it's parents and children.
    """

    def __init__(self,
                 parent_node: t.Optional[Morphy] = None,
                 parent_nodes: t.Optional[t.Iterable[Morphy]] = None,
                 node_name: str = None):
        self.node_name = node_name
        self.parent_nodes = list(parent_nodes) if parent_nodes is not None else [parent_node]
        self.child_nodes: list = []

        self.add_self_to_parent_nodes()

    def add_self_to_parent_nodes(self):
        for node in self.parent_nodes:
            if node:
                node.child_nodes.append(self)

    @classmethod
    def register_node_type(cls):
        """
        Add initializer of a decorated class as a 'cls' (Morphy) method.
        New class is a node type with some special powers.
        :return: Same, not changed class that was decorated.
        """

        def _(node_type: t.Type):
            @functools.wraps(node_type)
            def wrapper(*args, **kwargs):
                node = node_type(*args, **kwargs)
                return node

            setattr(cls, node_type.__name__, wrapper)
            return node_type

        return _

    def emit(self, data_to_process):
        self._emit(data_to_process)

    def execute_node(self, data_to_process, called_by=None):
        pass  # interface for child classes, never executed on base class

    def _emit(self, data_to_process):
        for child in self.child_nodes:
            child.execute_node(data_to_process, called_by=self)
