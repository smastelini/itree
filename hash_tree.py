import functools
import itertools
import typing


class Node:
    __slots__ = 'nid', 'fid', 'theta', 'index', 'depth'

    def __init__(self, nid: int, fid=None, theta: float = None, depth: int = 0):
        self.fid = fid
        self.theta = theta
        self.depth = depth
        self.index: typing.Tuple[int, int]  = (nid, nid)


class HashTree:
    def __init__(self):
        self._data = []
        self._index = {}
        self._depth = None

    def plant(self):
        self._depth = 0

        self._data.append(Node(0, depth=0))
        self._index[0] = self.n_nodes - 1
        self._depth = 0

        return 0

    def split_node(self, leaf: int, fid, theta: float):
        l_child = 2 * leaf + 1
        r_child = 2 * leaf + 2

        inner = self._data[self._index[leaf]]
        inner.index = (l_child, r_child)
        inner.fid = fid
        inner.theta = theta

        depth = inner.depth + 1

        if depth > self._depth:
            self._depth = depth

        self._data.append(Node(l_child, depth=depth))
        self._index[l_child] = self.n_nodes - 1

        self._data.append(Node(r_child, depth=depth))
        self._index[r_child] = self.n_nodes - 1

        return l_child, r_child

    def _eval(self, x):


        nid = 0
        yield nid
        for _ in range(self._depth - 1):
            try:
                node = self._data[self._index[nid]]
                nid = node.index[int(x[node.fid] > node.theta)]
                yield nid
            except KeyError:
                break

    # def walk(self, x):
    #     yield from filter(functools.partial(self._eval, x=x), itertools.repeat(1, self._depth))

    def sort(self, x):
        def fun(nid, _):
            try:
                node = self._data[self._index[nid]]
                return node.index[int(x[node.fid] > node.theta)]
            except KeyError:
                return nid

        nid = functools.reduce(fun, range(self._depth), 0)
        return self._data[self._index[nid]]

    @property
    def n_nodes(self):
        return len(self._data)

    @property
    def depth(self):
        return self._depth
