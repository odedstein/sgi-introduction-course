import gpytoolbox as gpy, numpy as np

def critical_points(V,F,u,tol):
    """
    This function computes the critical points of the function u on the mesh
    V,F by finding the indices of the faces where the gradient of the function
    u is smaller than tol.
    """

    G = gpy.grad(V,F)
    pts = ...

    return pts

