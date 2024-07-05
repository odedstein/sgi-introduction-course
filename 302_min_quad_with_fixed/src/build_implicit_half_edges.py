import numpy as np
from .sort_rows import sort_rows
from .global_variables import GHOST_HALF_EDGE
from .face_side_to_half_edge_index import face_side_to_half_edge_index
from .glue_half_edges import glue_half_edges
from .tip_vertex import tip_vertex
from .twin import twin
from .is_boundary_half_edge import is_boundary_half_edge

def build_implicit_half_edges(F, return_v2he=False):
    """
    build twin half-edge list and tip vertex list 

    Inputs
        F: |F|x3 face list

    Outputs
        twin_he_all: (|F|*3=He,) array of twin half edge indices
        v_end_all: (|F|*3=He,) array of tip vertex indices
        v2he: (|F|*3=He,) array of half-edges starting from each vertex
    """

    # compute vertex indices
    v_start_all = F.flatten()
    v_end_all = np.roll(F,-1,1).flatten()

    # compute twin half edge indices
    nF = F.shape[0]
    nS = 3 * nF
    S = np.empty([nS,4], dtype=np.int64)

    # Build a temparary list S of all face-sides, given by tuples (vi,vj,f,s),
    # where (vi,vj) are the vertex indices of side s of face f in sorted order (vi<vj).
    for f in range(nF):   
        for s in range(3): # for each side
            # get two vertex indices of the opposite side of F[f,s]
            vi = F[f, s]
            vj = F[f, (s+1)%3]
            S[f*3+s] = (min(vi,vj), max(vi,vj), f, s)

    # Sort the rows so that the sides that are going to be glued are adjacent
    # e.g. S[2*i,:] should be glued with S[2*i+1,:]
    S = sort_rows(S)

    # Build the |F|x3 gluing map G, by linking together pairs of sides with the same vertex indices.
    ii = 0
    twin_he_all = np.full((3*nF), GHOST_HALF_EDGE, dtype=np.int64)
    while True:
        if ii == (S.shape[0] - 1): # last row (must be a boundary face side, so glue to ghost)
            ii += 1
        elif S[ii, 0] != S[ii+1, 0] or S[ii, 1] != S[ii+1, 1]: # boundary face side (glue to ghost)
            ii += 1
        else: # interior face side
            fs0 = (S[ii  , 2], S[ii  , 3])
            fs1 = (S[ii+1, 2], S[ii+1, 3])
            he0 = face_side_to_half_edge_index(fs0)
            he1 = face_side_to_half_edge_index(fs1)
            glue_half_edges(twin_he_all, he0, he1)
            ii += 2
        if ii >= S.shape[0]:
            break

    if return_v2he == True:
        # Build v2he, mapping from a vertex to one of the half-edges whose tail (not tip) is that vertex
        nV = F.max()+1
        v2he = np.zeros(nV, dtype=int)
        v_visited = np.zeros(nV, dtype=bool)
        for he in range(nS):            
            v = tip_vertex(v_end_all, he)
            if v_visited[v] == False: # not visited yet
                if not is_boundary_half_edge(twin_he_all, he): # if it has twin
                    he_twin = twin(twin_he_all, he)
                    v2he[v] = he_twin
                    v_visited[v] = True

        return twin_he_all, v_end_all, v2he
    else:
        return twin_he_all, v_end_all