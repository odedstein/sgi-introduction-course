from .global_variables import GHOST_HALF_EDGE
from .twin import twin

def is_boundary_half_edge(twins, he):
    """
    Determine whether a half-edge is a boundary half edge

    Inputs
        twins (|he|,) list of twin indices
        he (1,) scalar of half edge index

    Output
        True/False whether this is a boundary half edge
    """
    return twin(twins, he) == GHOST_HALF_EDGE