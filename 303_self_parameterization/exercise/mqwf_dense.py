import numpy as np
import scipy
# from sksparse.cholmod import cholesky

def mqwf_dense(A, B, known, known_val):
    """
    This function solves the following problem 

    minimize_x 0.5 * x' * A * x - x' * B 
    such that x[known] = known_val

    Inputs:
        A: n x n np array 
        B: n x dim np array
        known: 1D np array of indices of constrained vertices
        known_val: constrained values at "known"

    Outputs:
        u: n x dim of output solution
    """

    #### Fill in the missing part #####


    ###################################


    return u