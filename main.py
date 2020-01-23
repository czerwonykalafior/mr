from __future__ import annotations

import functools
import typing as t


class Morphy:
    def __init__(self,
                 upstream: t.Optional[Morphy] = None,
                 upstreams: t.Optional[t.Iterable[Morphy]] = None,
                 stream_name: str = None):
        self.stream_name = stream_name
        self.upstreams = upstreams if upstreams is not None else [upstream]
        self.downstreams: list = []

        self.add_self_to_previous_nodes()

    def add_self_to_previous_nodes(self):
        for upstream in self.upstreams:
            if upstream:
                upstream.downstreams.append(self)

    @classmethod
    def register_arrow(cls):
        def _(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                return result

            setattr(cls, func.__name__, func)
            return wrapper()

        return _
