import numpy as np

# Reference: https://github.com/nmwsharp/intrinsic-triangulations-tutorial/blob/master/tutorial_skeleton.py
def sort_rows(A):
    """
    Sorts rows lexicographically, i.e., comparing the first column first, then
    using subsequent columns to break ties.

    :param A: A 2D array
    :returns: A sorted array with the same dimensions as A
    """
    return A[np.lexsort(np.rot90(A))]