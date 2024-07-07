import numpy as np
def norm_row(X):
    """
    compute the norm of each row
    """
    return np.sqrt(np.power(X,2).sum(1))
