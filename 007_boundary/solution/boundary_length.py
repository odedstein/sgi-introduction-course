import gpytoolbox as gpy, numpy as np

def boundary_length(V,F):
    """Compute the length of the input mesh V,F's boundary.
    """

    # Compute the boundary edges
    bdry_edges = gpy.boundary_edges(F)

    # Compute a matrix whose rows are equal to edgeEnd-edgeStart for each
    BE = V[bdry_edges[:,1],:] - V[bdry_edges[:,0],:]

    # Compute the total length of all boundary edges
    # HINT: look up the documentation for the NumPy function np.linalg.norm, and
    #   study the `axis` parameter in particular.
    L = np.sum(np.linalg.norm(BE, axis=-1))

    return L
