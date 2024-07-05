import numpy as np
# from .global_variables import EPS
epsilon = 1e-7

def barycentric_coordinates_skala(p, a, b, c, return_info = False):
    """
    Givne a 2d point "p" and the vertex locations of a triangle (a,b,c), this function outputs the barycentric coordinates

    Inputs:
    p,a,b,c: numpy array with size 2

    Outputs:
    b: barycentric coordinates

    Optional outputs:
    is_degenerated: whether triangle is degenerated
    is_inside: whether p is inside the triangle
    distance_to_valid: distance of the raw b to a valid barycentric coordinate

    Reference:
    "Barycentric coordinates computation in homogeneous coordinates" by Vaclav Skala
    """
    
    # assemble system matrix
    A = np.array([a,b,c], dtype=np.float64)
    A = np.concatenate((A, p[None,:]), axis = 0)
    A = np.insert(A, 2, 1, axis=1).T

    # # compute barycentric coordinate in the homo coord
    raw_b = np.zeros(4,dtype=np.float64)
    idx0 = np.array([1,2,3])
    idx1 = np.array([0,2,3])
    idx2 = np.array([0,1,3])
    idx3 = np.array([0,1,2])
    raw_b[0] = np.linalg.det(A[:,idx0])
    raw_b[1] = -np.linalg.det(A[:,idx1])
    raw_b[2] = np.linalg.det(A[:,idx2])
    raw_b[3] = -np.linalg.det(A[:,idx3])

    degenerated = is_degenerated(raw_b)
    inside = is_inside(raw_b)

    # compute outputs
    if not degenerated and inside: # valid case
        # normalized bary
        b = -raw_b[:3] / raw_b[3]
        dist_to_valid = distance_to_valid_barycentric(b)

        # clip to a valid barycentric
        b = np.clip(b, 0, 1)
        b = b / b.sum()
    elif not degenerated and not inside: # bary is outside
        b = -raw_b[:3] / raw_b[3]
        dist_to_valid = distance_to_valid_barycentric(b)
    else: # triangle is degenerated
        b = np.array([np.Inf, np.Inf, np.Inf])
        dist_to_valid = np.Inf

    if return_info:
        return b, degenerated, inside, dist_to_valid
    else:
        return b

def is_inside(b_all):
    b = b_all[:3]
    b4 = b_all[3]
    if b4 > 0:
        return np.logical_and(np.all(-epsilon <= -b), np.all(-b <= b4+epsilon))
    else:
        return np.logical_and(np.all(b4-epsilon <= -b), np.all(-b <= epsilon))

def is_degenerated(raw_b):
    return np.abs(raw_b[-1]) < epsilon

def distance_to_valid_barycentric(b):
    distance_to_zero = 0.0 - b
    distance_to_zero[distance_to_zero<0] = 0.0
    distance_to_one = b - 1.0
    distance_to_one[distance_to_one<0] = 0.0
    return np.maximum(distance_to_zero.max(), distance_to_one.max())