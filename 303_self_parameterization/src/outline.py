import numpy as np
import scipy 

def outline(F):
    """
    this function extract (unordered) boundary edges of a mesh

    Inputs
    F: |F|x3 numpy array of the face indices

    Outputs
    O: |E|x2 numpy array of unordered boundary edges

    Reference:
    this code is adapted from https://github.com/alecjacobson/gptoolbox/blob/master/mesh/outline.m
    """
    nV = F.max()+1
    row = F.flatten()
    col = F[:,[1,2,0]].flatten()
    data = np.ones(len(row), dtype=np.int32)
    A = scipy.sparse.csr_matrix((data, (row, col)), shape=(nV,nV)) # build directed adj matrix
    AA = A - A.transpose() # figure out edges that only have one half edge
    AA.eliminate_zeros()
    I,J,V = scipy.sparse.find(AA) # get the non-zeros
    O = np.array([I[V>0], J[V>0]]).T # construct the boundary edge list
    return O
