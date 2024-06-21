import gpytoolbox as gpy, numpy as np

def boundary_triangles(F):
    """Return a list of boundary triangle indices for an input triangulation F.
    """

    # Compute boundary edges.
    bdry_edges = gpy.boundary_edges(F)

    # Find all triangles that contain both vertices of a boundary edge.
    # HINT: Look at the documentation of the `where` or `nonzero` function in
    # NumPy.
    bdry_tri_list = []
    for ei in range(bdry_edges.shape[0]):
        e = bdry_edges[ei,:]
        for fi in range(F.shape[0]):
            f = F[fi,:]
            if np.nonzero(e[0]==f)[0].shape[0]>0 and np.nonzero(e[1]==f)[0].shape[0]>0:
                bdry_tri_list.append(fi)

    return np.array(bdry_tri_list)


