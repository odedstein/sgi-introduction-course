import gpytoolbox as gpy, scipy as sp

def reverse_subdivision(V, F, uu, k):
    """Given a function uu on a mesh which has been subdivided k times from the
    coarse V,F, reconstruct a function u on the coarse meth V,F.
    """

    _,_,S = gpy.subdivide(V,F, iters=k, method='loop', return_matrix=True)
    u = sp.sparse.linalg.spsolve(S.T * S, S.T * uu)

    return u
