from .next import next
from .twin import twin
from .global_variables import GHOST_HALF_EDGE, INVALID_HALF_EDGE
import numpy as np

def is_boundary_vertex_from_half_edge(twins, he):
    """
    Check whether the tail vertex v of a half edge is on the boundary

    Inputs:
        twins: (nHe) twin info
        he: (1,) half edge index
    
    Outputs:
        True/False
    """
    he_start = he
    while True:
        # get counter clockwise half edge
        he = twin(twins, next(next(he)))
        if he == he_start:
            return False
        if he == GHOST_HALF_EDGE: # hit boundary
            return True

            
