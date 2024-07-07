import numpy as np
from .outline import outline

def vector_area_matrix_dense(F, nV=None):
    """
    this function computes the vector area matrix (see LSCM) for conformal flattening

    Inputs
    F: |F|x3 numpy array of the face indices
    nV: number of vertices

    Outputs
    A: nV*2 x nV*2 DENSE atrix (it is actually a sparse matrix)
    """
    if nV is None:
        nV = F.max() + 1
    E = outline(F)
    A = np.zeros((nV*2, nV*2), dtype=np.float64)
    for e in range(E.shape[0]):
        i = E[e,0]
        j = E[e,1]

        A[i+nV, j] -= 0.25
        A[j, i+nV] -= 0.25
        A[i, j+nV] += 0.25
        A[j+nV, i] += 0.25
    return A