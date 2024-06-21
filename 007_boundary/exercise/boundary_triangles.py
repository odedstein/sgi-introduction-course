import gpytoolbox as gpy, numpy as np

def boundary_triangles(F):
    """Return a list of boundary triangle indices for an input triangulation F.
    """

    # Compute boundary edges.
    bdry_edges = ?

    # Find all triangles that contain both vertices of a boundary edge.
    # HINT: Look at the documentation of the `where` or `nonzero` function in
    # NumPy.
    bdry_tri_list = ?

    return np.array(bdry_tri_list)
