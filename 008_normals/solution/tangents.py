def tangents(V,F):
    """
    Computes two orthogonal, oriented tangent vectors for each face in a
    triangle mesh.
    """

    # Extract the first edge of each face and normalize it.
    E1 = V[F[:,2],:] - V[F[:,1],:]
    T1 = E1 / np.linalg.norm(E1, axis=-1)[:, None]

    # Extract the second edges and project onto the orthogonal complement of E1.
    E2 = V[F[:,0],:] - V[F[:,2],:]
    E2 = E2 - np.sum(E2*T1, axis=-1)[:,None]*T1

    # Normalize to get unit vectors
    T2 = E2 / np.linalg.norm(E2, axis=-1)[:,None]

    return T1,T2
