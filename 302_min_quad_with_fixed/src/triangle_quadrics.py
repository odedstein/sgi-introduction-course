import numpy as np
from src.compute_triangle_planes import compute_triangle_planes

def triangle_quadrics(V,F):
    """
    Compute triangle quadrics for all the triangle faces in F

    Inputs:
        V: |V|x3 vertex list
        F: |F|x3 face list

    Outputs:
        Qf: (nF,4,4) triangle quadrics
    """
    
    # compute initial quadric error 
    v0_index = F[:,0]
    v1_index = F[:,1]
    v2_index = F[:,2]
    v0 = V[v0_index,:]
    v1 = V[v1_index,:]
    v2 = V[v2_index,:]
    v01 = v1 - v0
    v02 = v2 - v0
    n = np.cross(v01, v02)
    n = n / np.sqrt(np.sum(n**2,1)+1e-12)[:,None]
    d = -np.sum(n*v0, 1)
    p = np.hstack((n,d[:,None]))

    # compute face quadrics
    Qf = np.einsum("fi,fj->fij", p, p) # face quadrics (nF,4,4)

    return Qf