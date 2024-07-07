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

    i = np.concatenate((np.arange(1,n), np.arange(0,n-1),
                        np.zeros(n-2), (n-1)*np.ones(n-2),
                        np.arange(2,n-1), np.arange(1,n-2)))
    j = np.concatenate((np.zeros(n-1), (n-1)*np.ones(n-1),
                        np.arange(1,n-1), np.arange(1,n-1),
                        np.arange(1,n-2), np.arange(2,n-1)))
    k = np.ones(i.shape[0])
    A = sp.sparse.csr_matrix((k,(i,j)), shape=(n,n))

    return A


