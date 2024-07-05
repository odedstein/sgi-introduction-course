import numpy as np

def face_areas(V, F):
    """
    Compute triangle area per face

    Inputs:
        V: |V|x3 numpy array of vertex positions
        F: |F|x3 numpy array of face indices
    Outputs:
        FA: |F| numpy array of face areas
    """

    vec1 = V[F[:,1],:] - V[F[:,0],:]
    vec2 = V[F[:,2],:] - V[F[:,0],:]
    FN = np.cross(vec1, vec2) / 2
    FA = np.sqrt(np.sum(FN**2,1))
    
    return FA