import numpy as np, scipy as sp

def triangles_matrix(n):
    """This function constructs an n x n sparse matrix with a triangular pattern
    of ones, as by the following pattern:
    0 1 1 1 1 1 1 1 1 1 1
    1 0 1 0 0 0 0 0 0 0 1
    1 1 0 1 0 0 0 0 0 0 1
    1 0 1 0 1 0 0 0 0 0 1
    1 0 0 1 0 1 0 0 0 0 1
    1 0 0 0 1 0 1 0 0 0 1
    1 0 0 0 0 1 0 1 0 0 1
    1 0 0 0 0 0 1 0 1 0 1
    1 0 0 0 0 0 0 1 0 1 1
    1 0 0 0 0 0 0 0 1 0 1
    1 1 1 1 1 1 1 1 1 1 0
    """

    i = ?
    j = ?
    k = ?
    A = sp.sparse.csr_matrix((k,(i,j)), shape=(n,n))

    return A


