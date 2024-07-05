import numpy as np

from .global_variables import GHOST_HALF_EDGE, INVALID_HALF_EDGE, INVALID_VERTEX_INDEX, INF_COST, INF, HAS_BEEN_COLLAPSED, INVALID_EDGE
from .is_boundary_vertex_from_half_edge import is_boundary_vertex_from_half_edge
from .vertex_one_ring_vertices_from_half_edge import vertex_one_ring_vertices_from_half_edge
from .vertex_one_ring_half_edges_from_half_edge import vertex_one_ring_half_edges_from_half_edge
from .is_boundary_half_edge import is_boundary_half_edge
from .face_normal import face_normal
from .face import face
from .twin import twin
from .next import next
from .tail_vertex import tail_vertex
from .tip_vertex import tip_vertex

def is_collapse_valid(V, twins, tips, he, v_opt,
                      triangle_quality_threshold = 0.1, 
                      verbose=True,):
    """
    This is used to detemine whether a half edge can be collapsed by checking all the conditions

    Inputs:
        V: |V|x3 vertex list
        twins: |he| list of half edge twins
        tips: |he| list of half edge tip vertex indices
        he: (1,) half edge index
        v_opt: (1,) the optimal vertex location after contracting he
        triangle_quality_threshold: (1,) scalar between 0 and 1 (perfectly equilateral lateral triangle), indicating the threshold of triangle quality
        verbose: True/Fase to print out warning messages
    Outputs:
        True/Fase whether this edge can be collapsed
    """

    # 1. Topological check: Boundary constraint to avoid non manifold vertices
    # see Sec 3.2 of https://www.merlin.uzh.ch/contributionDocument/download/14550#:~:text=A%20vertex%20split%20involves%20removing,operator%20adds%20detail%20to%20it.

    is_i_boundary_vertex = is_boundary_vertex_from_half_edge(twins, he)
    is_j_boundary_vertex = is_boundary_vertex_from_half_edge(twins, next(he))
    is_he_boundary_half_edge = is_boundary_half_edge(twins, he)
    if is_i_boundary_vertex and is_j_boundary_vertex and not is_he_boundary_half_edge:
        # if i,j are boundary vertices, but he is not a boundary half edge, then skip
        if verbose:
            print("decimation violates the boundary topological constraint, skip it")
        return False

    # 2. link conditions (see App.C https://arxiv.org/pdf/2005.01819.pdf)
    one_ring_v_i = vertex_one_ring_vertices_from_half_edge(twins, tips, he)
    one_ring_v_j = vertex_one_ring_vertices_from_half_edge(twins, tips, next(he))
    num_intersected_v = len(np.intersect1d(one_ring_v_i, one_ring_v_j))
    if not is_he_boundary_half_edge and (num_intersected_v != 2): 
        # for interior he, the number of intersected v should be exactly 2 
        if verbose:
            print("decimation violates internal link condition, skip it")
        return False
    
    if is_he_boundary_half_edge and (num_intersected_v != 1): 
        # for boundary he, the number of intersected v should be exactly 1
        if verbose:
            print("decimation violates boundary link condition, skip it")
        return False
    
    # TODO: 3. empty constraint (see Sec 3.2 of https://www.merlin.uzh.ch/contributionDocument/download/14550#:~:text=A%20vertex%20split%20involves%20removing,operator%20adds%20detail%20to%20it.)


    # 4. Flipover and triangle quality checks  (see Sec 3.7 of https://www.cs.cmu.edu/~garland/thesis/thesis-onscreen.pdf)
    f_to_be_removed = [face(he)]
    if twin(twins, he) != GHOST_HALF_EDGE:
        f_to_be_removed.append(face(twin(twins, he)))

    # Check one ring triangles, except the ones that are going to be removed
    he_list_tip_i = vertex_one_ring_half_edges_from_half_edge(twins, next(next(he)), around_tail=False)
    he_list_tip_j = vertex_one_ring_half_edges_from_half_edge(twins, he, around_tail=False)
    he_list = np.concatenate((he_list_tip_i, he_list_tip_j))
    for he_ in he_list:
        f_ = face(he_)
        if not f_ in f_to_be_removed: # if f_ would remain
            he_nn = next(next(he_))
            
            # do flipover check
            v_tail = tail_vertex(tips, he_nn)
            v_tip = tip_vertex(tips, he_nn)
            fn_ = face_normal(V, tips, f_)
            inward_edge_normal_he_nn = np.cross(fn_, V[v_tip,:] - V[v_tail,:])
            d = -inward_edge_normal_he_nn.dot(V[v_tip,:])

            # if np.sign(inward_edge_normal_he_nn.dot(vi)+d) != np.sign(inward_edge_normal_he_nn.dot(v_opt)+d): # the paper says this, but I feel the version below is sufficient
            if np.sign(inward_edge_normal_he_nn.dot(v_opt)+d) < 0:
                if verbose:
                    print("decimation will cause foldover, skip it")
                return False
            
            # do triangle quality check
            l_tail_tip = np.linalg.norm(V[v_tip,:] - V[v_tail,:])
            l_tip_opt = np.linalg.norm(v_opt - V[v_tip,:])
            l_opt_tail = np.linalg.norm(V[v_tail,:] - v_opt)
            s = (l_tail_tip + l_tip_opt + l_opt_tail) / 2.0
            area = np.sqrt(s * (s - l_tail_tip) * (s - l_tip_opt) *  (s - l_opt_tail) + 1e-6) # area from Heron's rule
            quality = 4 * np.sqrt(3) * area / (l_tail_tip**2 + l_tip_opt**2 + l_opt_tail**2 + 1e-6)
            if quality < triangle_quality_threshold:
                if verbose:
                    print("triangle quality below threshold, skip it")
                return False
            
    # if it passes all the checks, then return true
    return True



# def is_collapse_valid(V, twins, tips, he, v_opt, S=None, s_opt=None,
#                       triangle_quality_threshold = 0.1, 
#                       uv_triangle_quality_threshold = 0.0,
#                       verbose=True,):
#     """
#     This is used to detemine whether a half edge can be collapsed by checking all the conditions

#     Inputs:
#         V: |V|x3 vertex list
#         twins: |he| list of half edge twins
#         tips: |he| list of half edge tip vertex indices
#         he: (1,) half edge index
#         v_opt: (1,) the optimal vertex location after contracting he
#         triangle_quality_threshold: (1,) scalar between 0 and 1 (perfectly equilateral lateral triangle), indicating the threshold of triangle quality
#         verbose: True/Fase to print out warning messages
#     Outputs:
#         True/Fase whether this edge can be collapsed
#     """

#     # 1. Topological check: Boundary constraint to avoid non manifold vertices
#     # see Sec 3.2 of https://www.merlin.uzh.ch/contributionDocument/download/14550#:~:text=A%20vertex%20split%20involves%20removing,operator%20adds%20detail%20to%20it.

#     is_i_boundary_vertex = is_boundary_vertex_from_half_edge(twins, he)
#     is_j_boundary_vertex = is_boundary_vertex_from_half_edge(twins, next(he))
#     is_he_boundary_half_edge = is_boundary_half_edge(twins, he)
#     if is_i_boundary_vertex and is_j_boundary_vertex and not is_he_boundary_half_edge:
#         # if i,j are boundary vertices, but he is not a boundary half edge, then skip
#         if verbose:
#             print("decimation violates the boundary topological constraint, skip it")
#         return False

#     # 2. link conditions (see App.C https://arxiv.org/pdf/2005.01819.pdf)
#     one_ring_v_i = vertex_one_ring_vertices_from_half_edge(twins, tips, he)
#     one_ring_v_j = vertex_one_ring_vertices_from_half_edge(twins, tips, next(he))
#     num_intersected_v = len(np.intersect1d(one_ring_v_i, one_ring_v_j))
#     if not is_he_boundary_half_edge and (num_intersected_v != 2): 
#         # for interior he, the number of intersected v should be exactly 2 
#         if verbose:
#             print("decimation violates internal link condition, skip it")
#         return False
    
#     if is_he_boundary_half_edge and (num_intersected_v != 1): 
#         # for boundary he, the number of intersected v should be exactly 1
#         if verbose:
#             print("decimation violates boundary link condition, skip it")
#         return False
    
#     # TODO: 3. empty constraint (see Sec 3.2 of https://www.merlin.uzh.ch/contributionDocument/download/14550#:~:text=A%20vertex%20split%20involves%20removing,operator%20adds%20detail%20to%20it.)


#     # 4. Flipover and triangle quality checks  (see Sec 3.7 of https://www.cs.cmu.edu/~garland/thesis/thesis-onscreen.pdf)
#     f_to_be_removed = [face(he)]
#     if twin(twins, he) != GHOST_HALF_EDGE:
#         f_to_be_removed.append(face(twin(twins, he)))

#     # Check one ring triangles, except the ones that are going to be removed
#     he_list_tip_i = vertex_one_ring_half_edges_from_half_edge(twins, next(next(he)), around_tail=False)
#     he_list_tip_j = vertex_one_ring_half_edges_from_half_edge(twins, he, around_tail=False)
#     he_list = np.concatenate((he_list_tip_i, he_list_tip_j))
#     for he_ in he_list:
#         f_ = face(he_)
#         if not f_ in f_to_be_removed: # if f_ would remain
#             he_nn = next(next(he_))
            
#             # do flipover check
#             v_tail = tail_vertex(tips, he_nn)
#             v_tip = tip_vertex(tips, he_nn)
#             fn_ = face_normal(V, tips, f_)
#             inward_edge_normal_he_nn = np.cross(fn_, V[v_tip,:] - V[v_tail,:])
#             d = -inward_edge_normal_he_nn.dot(V[v_tip,:])

#             # if np.sign(inward_edge_normal_he_nn.dot(vi)+d) != np.sign(inward_edge_normal_he_nn.dot(v_opt)+d): # the paper says this, but I feel the version below is sufficient
#             if np.sign(inward_edge_normal_he_nn.dot(v_opt)+d) < 0:
#                 if verbose:
#                     print("decimation will cause foldover, skip it")
#                 return False
            
#             # do triangle quality check
#             l_tail_tip = np.linalg.norm(V[v_tip,:] - V[v_tail,:])
#             l_tip_opt = np.linalg.norm(v_opt - V[v_tip,:])
#             l_opt_tail = np.linalg.norm(V[v_tail,:] - v_opt)
#             s = (l_tail_tip + l_tip_opt + l_opt_tail) / 2.0
#             area = np.sqrt(s * (s - l_tail_tip) * (s - l_tip_opt) *  (s - l_opt_tail) + 1e-6) # area from Heron's rule
#             quality = 4 * np.sqrt(3) * area / (l_tail_tip**2 + l_tip_opt**2 + l_opt_tail**2 + 1e-6)
#             if quality < triangle_quality_threshold:
#                 if verbose:
#                     print("triangle quality below threshold, skip it")
#                 return False
            
#             # # check UV flipover
#             # if S is not None and s_opt is not None: # has input UV
#             #     s_tail = S[v_tail,:]
#             #     s_tip = S[v_tip,:]
#             #     uv_normal = np.cross(s_tip-s_tail, s_opt-s_tail)
#             #     if uv_normal < 0: # UV flip
#             #         if verbose:
#             #             print("UV triangle flip, skip it")
#             #         return False
                
#             #     sl_tail_tip = np.linalg.norm(S[v_tip,:] - S[v_tail,:])
#             #     sl_tip_opt = np.linalg.norm(s_opt - S[v_tip,:])
#             #     sl_opt_tail = np.linalg.norm(S[v_tail,:] - s_opt)
#             #     ss = (sl_tail_tip + sl_tip_opt + sl_opt_tail) / 2.0
#             #     s_area = np.sqrt(ss * (ss - sl_tail_tip) * (ss - sl_tip_opt) *  (ss - sl_opt_tail) + 1e-6) # area from Heron's rule
#             #     s_quality = 4 * np.sqrt(3) * s_area / (sl_tail_tip**2 + sl_tip_opt**2 + sl_opt_tail**2 + 1e-6)
#             #     if s_quality < uv_triangle_quality_threshold:
#             #         if verbose:
#             #             print("UV triangle quality below threshold, skip it")
#             #         return False

#     # if it passes all the checks, then return true
#     return True
