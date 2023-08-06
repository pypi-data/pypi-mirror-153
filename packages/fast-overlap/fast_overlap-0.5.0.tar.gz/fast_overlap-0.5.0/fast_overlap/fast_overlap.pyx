# distutils: language=c++

import numpy as np

cimport cython
cimport numpy as np

__all__ = [
    "overlap",
    "overlap_parallel",
]
cimport numpy as np


cdef extern from "parallel_overlap.cpp":
    cdef void overlap_parallel_cpp(int *, int *, Py_ssize_t[2], int *, Py_ssize_t) nogil

@cython.wraparound(False)
@cython.nonecheck(False)
cpdef overlap_parallel(int [:,::1] prev, int[:,::1] curr, shape=None):
    """
    Calculate the pairwise overlap the labels for two arrays in
    parallel using openmp. This may not work on non-linux OSes.

    Currently limited to only accept `int` type arrays.

    Parameters
    ----------
    prev, curr : 2D array-like of int
        curr will have at least as many unique labels as prev
    shape : tuple of int, optional
        The shape of the output array. This should reflect the maximum
        value of labels.

    Returns
    -------
    arr : (N, M) array of int
        N is the number of unique labels in prev and M the number of unique in curr.
        The ijth entry in the array gives the number of pixels for which label *i* in prev
        overlaps with *j* in curr.
    """
    prev = np.ascontiguousarray(prev)
    curr = np.ascontiguousarray(curr)

    if shape is None:
        shape = (prev.max(), curr.max())

    cdef np.ndarray[int, ndim=2, mode="c"] output = np.zeros(shape, dtype=np.dtype("i"))
    cdef Py_ssize_t ncols = shape[1]

    with nogil:
        overlap_parallel_cpp(&prev[0,0], &curr[0,0], prev.shape, &output[0,0], ncols)
    return output



from libc cimport stdint

ctypedef fused ints:
    stdint.uint8_t
    stdint.uint16_t
    stdint.uint32_t
    stdint.uint64_t
    stdint.int8_t
    stdint.int16_t
    stdint.int32_t
    stdint.int64_t

# @cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cpdef overlap(ints[:, :] prev, ints[:,:] curr, shape=None):
    """
    Calculate the pairwise overlap the labels for two arrays.

    Parameters
    ----------
    prev, curr : 2D array-like of int
        curr will have at least as many unique labels as prev
    shape : tuple of int, optional
        The shape of the output array. This should reflect the maximum
        value of labels.

    Returns
    -------
    arr : (N, M) array of int
        N is the number of unique labels in prev and M the number of unique in curr.
        The ijth entry in the array gives the number of pixels for which label *i* in prev
        overlaps with *j* in curr.
    """
    prev = np.ascontiguousarray(prev)
    curr = np.ascontiguousarray(curr)

    if shape is None:
        shape = (np.max(prev)+1, np.max(curr)+1)

    cdef int [:, :] arr
    arr = np.zeros(shape, dtype=np.dtype("i"))
    cdef size_t I, J, i, j
    for i in range(prev.shape[0]):
        for j in range(prev.shape[1]):
            p = prev[i,j]
            c = curr[i,j]
            if p and c:
                arr[p, c] += 1
    return np.asarray(arr)
