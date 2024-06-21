import numpy as np
def top_left_corner(A, r, c):
    """
    Select the top-left corner of a matrix.

    This function returns the r-by-c top-left corner of the matrix A
    """
    return A[:r,:c]

