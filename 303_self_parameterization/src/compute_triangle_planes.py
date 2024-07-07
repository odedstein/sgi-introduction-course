import numpy as np

def compute_triangle_planes(V, F):
    """
    Compute plane equations for all triangles

    Inputs:
        V: (|V|,3) vertex list
        F: (|F|,3) face list

    Outputs:
        nd: (|F|,4) plane coefficients where norm(nd[idx,:3]) = 1
    """
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
    nd = np.hstack((n,d[:,None]))
    
    return nd