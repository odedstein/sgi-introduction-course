# from .vertex_one_ring_half_edges import vertex_one_ring_half_edges
from .next import next
from .twin import twin
from .global_variables import GHOST_HALF_EDGE
from .tip_vertex import tip_vertex
from .vertex_one_ring_half_edges_from_half_edge import vertex_one_ring_half_edges_from_half_edge
import numpy as np

def vertex_one_ring_vertices_from_half_edge(twins,tips,he):
    """
    get the vertex one-ring vertices from a half edge whose tail is that vertex

    Inputs
    twins: (he,) array of twin half edges
    tips: (he,) array of tip vertex indices
    he: half edge index

    Outputs
    one_ring: np array of one ring vertex indices
    """
    one_ring_he = vertex_one_ring_half_edges_from_half_edge(twins, he, around_tail=True)

    one_ring_v = []
    for he in one_ring_he:
        v = tip_vertex(tips, he)
        one_ring_v.append(v)

        # if v is on the boundary
        if twin(twins, next(next(he))) == GHOST_HALF_EDGE: 
            v = tip_vertex(tips, next(he))
            one_ring_v.append(v)
    return np.array(one_ring_v)