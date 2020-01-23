from __future__ import annotations

import functools
import typing as t


class Morphy:
    def __init__(self,
                 upstream: t.Optional[Morphy] = None,
                 upstreams: t.Optional[t.Iterable[Morphy]] = None,
                 stream_name: str = None):
        self.stream_name = stream_name
        self.upstreams = list(upstreams) if upstreams is not None else [upstream]
        self.downstreams: list = []

        self.add_self_to_previous_nodes()

    def add_self_to_previous_nodes(self):
        for upstream in self.upstreams:
            if upstream:
                upstream.downstreams.append(self)

    @classmethod
    def register_node_type(cls):
        """
        Adds initializer of a decorated class as a 'cls' (Morphy) method.
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
