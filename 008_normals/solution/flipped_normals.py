import gpytoolbox as gpy, numpy as np

def flipped_normals(V,F):
    """
    Compute the flipped per-face normals of a triangle mesh.
    """

    N = gpy.per_face_normals(V,F)
    return -N

