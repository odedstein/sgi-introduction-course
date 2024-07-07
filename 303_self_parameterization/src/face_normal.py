from .next import next
from .tip_vertex import tip_vertex
import numpy as np

def face_normal(V, tips, f):
    """
    compute the face normal of a give triangle

    Inputs
        tips: (|he|,) array of twin half edge indices
        V: (|V|,) array of vertex locations
        f: (1,) face index

    Outputs
        n: (3,) normal of the face
    """
    he = f * 3 
    v0 = V[tip_vertex(tips, he),:]
    v1 = V[tip_vertex(tips, next(he)),:]
    v2 = V[tip_vertex(tips, next(next(he))),:]
    n = np.cross(v1 - v0, v2 - v0)
    n = n / (np.linalg.norm(n)+1e-6)
    return n