import numpy as np, scipy as sp
def four_corners(m,n):
    """This function constructs an m x n sparse matrix with ones in each of its
    four corners.
    """

    i = ?
    j = ?
    k = ?
    A = sp.sparse.csr_matrix((k,(i,j)), shape=(m,n))

    return A


