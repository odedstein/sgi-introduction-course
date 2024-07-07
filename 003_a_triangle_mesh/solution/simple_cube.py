import numpy as np

def simple_cube():
    """Construct a triangle mesh for a single cube.

    This function returns two variables, the vertex-list V and the face-list
    F describing a triangle mesh of a single cube.
    """

    V = np.array([[0., 0., 0.],
        [1., 0., 0.],
        [0., 1., 0.],
        [1., 1., 0.],
        [0., 0., 1.],
        [1., 0., 1.],
        [0., 1., 1.],
        [1., 1., 1.]])

    F = np.array([[0, 1, 2],
        [1, 3, 2],
        [0, 1, 4],
        [1, 5, 4],
        [1, 3, 7],
        [1, 7, 5],
        [3, 2, 6],
        [3, 6, 7],
        [2, 0, 6],
        [0, 4, 6],
        [4, 5, 6],
        [5, 7, 6]])

    return V, F

