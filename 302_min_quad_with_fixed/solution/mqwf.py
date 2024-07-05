import numpy as np
import scipy

def mqwf(A, B, known, known_val):
    """
    This function solves the following problem 

    minimize_x 0.5 * x' * A * x - x' * B 
    such that x[known] = known_val

    Inputs
        A: n x n scipy sparse array 
        B: n x dim np array
        known: 1D np array of indices of constrained vertices
        known_val: constrained values at "known"

    Outputs
        u: n x dim of output solution
    """

    # determin problem dimension
    if len(B.shape) == 1:
        dim = 1
    else:
        dim = B.shape[1]
    
    # reshape B and known_val to be (n,1) if their shapes are (n,)
    n = A.shape[0]
    if dim == 1:
        known_val = np.reshape(known_val, (len(known_val),1))
        B = np.reshape(B, (n,1))
    
    unknown = np.arange(n)
    unknown = np.delete(unknown, known)

    # construct new linear system for symmetric matrix A
    # Auu * x_unknown = RHS[unknown] - Auk @ known_values
    Auu = A[:,unknown]
    Auu = Auu[unknown,:]
    preF = scipy.sparse.linalg.factorized(Auu) # prefactorization, a key to make linear solve A LOT faster for consecutive solves if having the same system matrix A

    # get RHS    
    Auk = A[unknown,:]
    Auk = Auk[:,known]
    RHS = B[unknown] - Auk @ known_val

    # solve 
    unknown_val = preF(RHS)

    # assemble solution
    out = np.zeros((n,B.shape[1]))
    out[unknown] = unknown_val
    out[known] = known_val
    if dim == 1:
        out = out.flatten()
    return out