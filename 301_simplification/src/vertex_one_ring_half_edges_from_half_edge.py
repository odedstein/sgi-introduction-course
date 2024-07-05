from .next import next
from .twin import twin
from .global_variables import GHOST_HALF_EDGE
import numpy as np

def vertex_one_ring_half_edges_from_half_edge(twins,he,around_tail=True):
    """
    get the vertex one-ring half-edges from a half edge. If "around_tail=True", the vertex will be the tail vertex of the input half-edge. If "around_tail=False",the vertex will be the tip vertex of the input half-edge

    Inputs
    twins: (he,) array of twin half edges
    he: (1,) half edge index
    around_tail: True/False to determine whether to rotate around the tail or the tip vertex

    Outputs
    one_ring: np array of one ring half-edges 
    
    Note:
    if the tip/tail vertex is a boundary vertex, this will only return the valid half-edges in the ccw order (thus missing one half edge whose tip is the vertex).
    """
    if around_tail: # rotate around the tail of the half edge
        he_start = he
        one_ring = [he]
        while True:
            # get counter clockwise half edge
            he = twin(twins, next(next(he)))
            if he == he_start:
                # this is an interior vertex, so it reaches the starting he
                break
            if he == GHOST_HALF_EDGE: # hit boundary, then go clock wise
                he = he_start
                while True:
                    if twin(twins, he) == GHOST_HALF_EDGE:
                        break
                    he = next(twin(twins, he))
                    one_ring.insert(0,he)
                break
            one_ring.append(he)
        return np.array(one_ring)
    else:  # rotate around the tips of the half edge
        he_start = he
        one_ring = [he]
        while True:
            # if hit boundary, then go clock wise
            if twin(twins, he) == GHOST_HALF_EDGE: 
                he = he_start
                while True:
                    he = twin(twins, next(he))
                    if he == GHOST_HALF_EDGE:
                        return np.array(one_ring)
                    one_ring.insert(0,he)

            # get counter clockwise half edge
            he = next(next( twin(twins, he)))
            if he == he_start:
                # this is an interior vertex, so it reaches the starting he
                return np.array(one_ring)
            one_ring.append(he)