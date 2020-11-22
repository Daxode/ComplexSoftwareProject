from cpython cimport array
from cython.operator cimport dereference
from cython cimport view

cdef class Node:
    def __init__(self, const float[:] point):
        self.point = point
        self.hashKey = <char*>&self.point[0]

    cdef public GetPoint(self):
        return self.point

    def __hash__(self):
        return <Py_hash_t>self.hashKey

    def __getitem__(self, key):
        return self.point[key]

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return f"({self.point[0]}, {self.point[1]}, {self.point[2]})"

    def __repr__(self):
        return f"({self.point[0]}, {self.point[1]}, {self.point[2]})"

cdef class NodeRef(Node):
    def __init__(self, const float[:] point):
        super().__init__(point)
        self.relativeDist = -1

cdef class NodeKey(Node):
    def __init__(self, const float[:] point):
        super().__init__(point)
        self.weight = 1