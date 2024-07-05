import numpy as np
def shuffle_by_1(A):
    """
    Shuffles the columns of a matrix to the right by one.

    This function returns the matrix A with columns shuffled to the right by 1,
    such that the new ith col is the old i-1th col, and the new 1st col 
    is the old last col.
    """
    B = A.copy()
    tempCol = B[:, -1].copy()
    B[:, 1:] = B[:, :-1]
    B[:, 0] = tempCol
    return B

