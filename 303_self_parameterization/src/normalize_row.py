import numpy as np

def normalize_row(X):
    """
    normalizes the l2-norm of each row in a np array 

    Input:
        X: (n,m) numpy array
    Output:
        X_normalized: (n,m) row normalized numpy array
    """
    norm_row = np.sqrt(np.sum(X * X, axis = 1))
    X_normalized = X / (norm_row.reshape(X.shape[0],1) + 1e-10)
    return X_normalized