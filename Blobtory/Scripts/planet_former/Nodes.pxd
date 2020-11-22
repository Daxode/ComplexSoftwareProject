from cython cimport view
from cpython cimport array

cdef class Node:
    cdef const float[:] point
    cdef char* hashKey
    cdef public GetPoint(self)

cdef class NodeRef(Node):
    cdef public float relativeDist

cdef class NodeKey(Node):
    cdef public float weight
