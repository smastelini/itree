cimport cython
from libc.stdlib cimport malloc, realloc
from libc.stdint cimport SIZE_MAX


cdef struct s_node:
    long fid
    float theta
    size_t index[2]

ctypedef s_node node


cdef class Tree
    # TODO
    # - handle memory deallocation
    # - check pickling/unplickling actions: for instance, compress tree before persisting it
    # (remove unnecessary over-allocated memory)
    cdef:
        readonly long max_depth
        readonly size_t n_nodes
        readonly size_t capacity

        node *_data
        dict _feat_map
        size_t _next_feat

    def __cinit__(self, long max_depth=-1):
        if max_depth < 0:
            max_depth = SIZE_MAX

        self.max_depth = max_depth
        self.capacity = 0

        # Map longs to the feature name
        self._feat_map = {}
        self._next_feat = 0

    cdef void _init_node(self, size_t position, unsigned int depth):
        cdef node* n = &self._data[position]

        n.fid = -1

        # Self loops
        n.index[0] = position
        n.index[1] = position

    cpdef size_t plant(self) nogil except -1:
        """Allocate the initial capacity of the tree and defines the root node.

        Returns
        -------
            The position of the root node in the tree.

        Raises
        ------
        MemoryError
            In case the initial memory requirements are not met.
        """
        cdef size_t init_capacity

        # TODO: check indexing
        if self.max_depth <= 10:
            init_capacity = <size_t>(2 ** (self.max_depth + 1) - 1)
        else:
            init_capacity = 2047

        self._resize(init_capacity)

        # Prepare root
        self._init_node(0)

        return 0

    cpdef long walk(self, dict x):
        pass

    cpdef long sort(self, dict x):
        pass

    cpdef (size_t, size_t) split_node(self, size_t parent, fid, double theta):
        if fid not in self._feat_map:
            self._feat_map[self._next_feat] = fid
            self._next_feat += 1

        return self._split_node(parent, self._feat_map[fid], theta)

    cdef (size_t, size_t) _split_node(self, long parent, long fid, double theta):
        cdef size_t l_child = 2 * parent + 1
        cdef size_t r_child = 2 * parent + 2
        cdef node* p_node = &self._data[parent]

        p_node.fid = fid
        p_node.theta = theta

        p_node.index[0] = l_child
        p_node.index[1] = r_child

        # Reset leaves to their default state
        self._init_node(l_child)
        self._init_node(r_child)

        self.n_nodes += 2

        # Ensure we have enough memory to work with
        if self.n_nodes > 0.7 * self.capacity:
            self._resize()

        return (l_child, r_child)

    cdef int _resize(self, size_t capacity=SIZE_MAX) nogil except -1:
        # There is no need to reallocate memory
        if capacity == self.capacity and self._data != NULL:
            return 0

        # If capacity is not specificed, allocate memory using pre-defined actions
        if capacity == SIZE_MAX:
            if self.capacity == 0:
                # Decision stump
                capacity = 3
            else:
                # TODO revisit that
                # Doubles the existing size
                capacity = 2 * self.capacity

        # Allocate memory for the nodes
        self.__safe_realloc(&self._data, capacity)
        # Update the current capacity
        self.capacity = capacity

        return 0

    @staticmethod
    cdef realloc_ptr __safe_realloc(realloc_ptr* p, size_t n_elems) nogil except *:
        """Helper method to safely realloc memory for the internal tree structure."""
        cdef size_t n_bytes = n_elems * sizeof(p[0][0])

        if n_bytes / sizeof(p[0][0]) != n_elems:
            # Overflow in the multiplication
            with gil:
                raise MemoryError(f"Could not allocate {n_elems * sizeof(p[0][0]} bytes.")

        cdef realloc_ptr tmp = <realloc_ptr>realloc(p[0], n_bytes)
        if tmp == NULL:
            with gil:
                raise MemoryError("Could not allocate {n_bytes} bytes.")

        p[0] = tmp  # Change the pointer

        return tmp

    @property
    def root(self):
        if self.n_nodes > 0:
            return self._data[0]

    @property
    def depth(self):
        pass
