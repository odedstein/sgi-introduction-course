from .global_variables import INVALID_VERTEX_INDEX
from .next import next
from .tip_vertex import tip_vertex
import numpy as np

def faces_from_half_edge_data(tips):
    """
    construct face list from half edge data 

    Inputs:
        tips: (nHe,) list of tip vertices
    Outputs:
        F: |F|x3 face list
    """
    nHe = len(tips)
    F = []
    for he in range(0, nHe, 3):
        if tip_vertex(tips, he) != INVALID_VERTEX_INDEX:
            v1 = tip_vertex(tips, he)
            v2 = tip_vertex(tips, next(he))
            v0 = tip_vertex(tips, next(next(he)))
            if v0 == v1 or v1 == v2 or v0 == v2:
                print(v0, v1, v2)
            F.append([v0, v1, v2])
        else:
            continue
    return np.array(F)