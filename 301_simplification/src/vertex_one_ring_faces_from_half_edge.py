# from .vertex_one_ring_half_edges import vertex_one_ring_half_edges
from .vertex_one_ring_half_edges_from_half_edge import vertex_one_ring_half_edges_from_half_edge
from .face import face

import numpy as np

def vertex_one_ring_faces_from_half_edge(twins,he):
    """
    get the vertex one-ring faces 

    Inputs
    twins: (he,) array of twin half edges
    v2he: (V,) array of emitting half edge indices
    v: vertex index

    Outputs
    one_ring: np array of one ring faces of vertex v
    """
    one_ring_he = vertex_one_ring_half_edges_from_half_edge(twins, he)
    one_ring_f = []
    for he in one_ring_he:
        one_ring_f.append(face(he))
    return np.array(one_ring_f)