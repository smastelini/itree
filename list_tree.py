import abc


class ListTree(abc.ABC):
    
    def __init__(self):
        self.children = []
        self.depth = []
        self.parent = []
        
    @property
    def n_nodes(self):
        return len(self.depth)
    
    @property
    def height(self):
        return max(self.depth)
        
    def add_node(self, parent: int = None) -> int:
        """Add a node to the tree."""
        self.children.append([])
        self.depth.append(self.depth[parent] if parent is not None else 0)
        self.parent.append(parent)
        node_index = self.n_nodes - 1
        
        # Update the parent
        if parent is not None:
            self.children[parent].append(node_index)
        
        return node_index
    
    def _iter_dfs(self, node: int):
        yield node
        for child in self.children[node]:
            yield from self._iter_dfs(child)
    
    def iter_dfs(self):
        """Iterate over nodes in depth-first order."""
        yield from self._iter_dfs(0)
        
    def iter_branches(self):
        """Iterate over branches in depth-first order."""
        yield from (node for node in self.iter_dfs() if self.children[node])
        
    def iter_leaves(self):
        """Iterate over leaves in depth-first order."""
        yield from (node for node in self.iter_dfs() if not self.children[node])
        
    @abc.abstractmethod
    def determine_next_step(self, branch: int, x: dict) -> int:
        """Decide down which child to walk."""
        
    def walk(self, x):
        """Walk down the tree according to the split decisions made along the way."""
        node = 0
        yield node
        while self.children[node]:
            step = self.determine_next_step(node, x)
            node = self.children[node][step]
            yield node


class LTNode:
    __slots__ = 'feature', 'threshold'

    def __init__(self, feature, threshold):
        self.feature = feature
        self.threshold = threshold


class BinaryListTree(ListTree):

    def __init__(self):
        super().__init__()
        self.nodes = []

    def determine_next_step(self, branch, x):
        branch = self.nodes[branch]
        if x[branch.feature] < branch.threshold:
            return 0
        return 1

    def sort(self, x):
        try:
            node = self.nodes[0]
        except IndexError:
            return None

        for node in self.walk(x):
            pass

        return self.nodes[node]
