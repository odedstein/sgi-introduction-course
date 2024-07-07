import gpytoolbox as gpy, numpy as np

def boundary_length(V,F):
    """Compute the length of the input mesh V,F's boundary.
    """

    # Compute the boundary edges
    bdry_edges = ?

    # Compute a matrix whose rows are equal to edgeEnd-edgeStart for each
    BE = ?

    # Compute the total length of all boundary edges
    # HINT: look up the documentation for the NumPy function np.linalg.norm, and
    #   study the `axis` parameter in particular.
    L = ?

    return L
