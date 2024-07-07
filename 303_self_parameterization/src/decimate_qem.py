import numpy as np
import heapq
import polyscope as ps

from .global_variables import GHOST_HALF_EDGE, INVALID_HALF_EDGE, INVALID_VERTEX_INDEX, INF_COST, INF, HAS_BEEN_COLLAPSED, INVALID_EDGE, INVALID_FACE_INDEX, QEM, PROBABILITY_QEM, UNIFORM_QEM, MID_POINT

from .next import next
from .twin import twin
from .tip_vertex import tip_vertex
from .tail_vertex import tail_vertex

from .build_implicit_half_edges import build_implicit_half_edges
from .is_boundary_half_edge import is_boundary_half_edge
from .vertex_one_ring_half_edges_from_half_edge import vertex_one_ring_half_edges_from_half_edge
from .vertex_one_ring_faces_from_half_edge import vertex_one_ring_faces_from_half_edge
from .is_boundary_vertex_from_half_edge import is_boundary_vertex_from_half_edge
from .is_collapse_valid import is_collapse_valid
from .remove_unreferenced import remove_unreferenced
from .faces_from_half_edge_data import faces_from_half_edge_data

from exercise.optimal_location_and_cost import optimal_location_and_cost
from exercise.triangle_quadrics import triangle_quadrics
from exercise.face_areas import face_areas
from src.compute_triangle_planes import compute_triangle_planes


def decimate_qem(Vo,Fo,num_target_vertices,
                   triangle_quality_threshold = 0.1, 
                   verbose = False, 
                   print_every_iterations = 500, 
                   boundary_quadric_weight = 1.0,
                   boundary_quadric_regularization = 1e-6):
    """
    Perform quadric error mesh simplification

    Inputs
        Vo: |V|x3 vertex list
        Fo: |F|x3 face list
        num_target_vertices: number of vertices in the coarsened mesh

    Optional inputs:
        triangle_quality_threshold: (1,) scalar between 0 (degenerated) and 1 (equilateral triangle) indicating threshold of output triangle quality. Close to 0 may produce sliver triangles. Close 1 may cause the decimation unable to reach target vertex count
        edge_quadric_weight: weights on preserving boundary of the mesh
        verbose: True/False whether to print out warning
        print_every_iterations: how many iterations to print out the progress

    Outputs:
        V,F decimated triangle mesh
        Fc2F: index map for faces, such that f_index = Fc2F[fc_index]

    Note: we are using the implicit half edge data sturcutre where
        Triangle-index       = edge-index // 3
        Sub-edge-index       = edge-index % 3
        Next-edge-index      = (triangle-index * 3) + ((edge-index     + 1) % 3)
        Previous-edge-index  = (triangle-index * 3) + ((edge-index + 3 - 1) % 3)
    """
    V = Vo.copy()
    F = Fo.copy()

    # basic geometric quantities
    nHe = F.shape[0] * 3
    nV = V.shape[0]
    nF = F.shape[0]
    GHOST_VERTEX_LOCATION = V.mean(0)

    # twins, tips, v2he = build_implicit_half_edges(F, return_v2he=True)
    twins, tips = build_implicit_half_edges(F, return_v2he=False)
    Qv = vertex_quadrics(V,F,twins,tips,boundary_quadric_weight,boundary_quadric_regularization)

    # =========
    # Initialization
    # =========
    # decimation parameters
    total_collapses = nV - num_target_vertices
    cur_collapses = 0

    # compute initial edge quadric errors, min head, he2e map, E_time_stamps
    he_processed = np.zeros(nF*3, dtype=bool)
    he2e = -np.ones(nHe, dtype=np.int32)
    eIdx = 0
    min_heap = [] # (cost, cur_collapses, he, i, j, v_opt)
    for he in range(nHe):
        if he_processed[he] == False:
            i = tail_vertex(tips, he)
            j = tip_vertex(tips, he)
            Qi = Qv[i,:,:]
            Qj = Qv[j,:,:]

            Qeij = Qi + Qj
            v_opt, cost = optimal_location_and_cost(Qeij)
            heapq.heappush(min_heap, (cost, cur_collapses, he, i, j, v_opt))

            # add processed half edges
            he_processed[he] = True
            if not is_boundary_half_edge(twins, he): # if not boundary he
                he_twin = twin(twins, he)
                he_processed[he_twin] = True

            # construct he2e
            he2e[he] = eIdx
            eIdx += 1
        else: # if this he has been processed before
            he_twin = twin(twins, he)
            he2e[he] = he2e[he_twin]

    # initialize time stamps
    nE = eIdx
    E_time_stamps = np.zeros(nE, dtype=np.int32)

    # start decimation
    while True:
        if cur_collapses == total_collapses:
            break

        # get the edge with min cost
        cost, time_stamp, he, i, j, v_opt = heapq.heappop(min_heap)
        # =====
        # CHECK if this edge information is up-to-date 
        e = he2e[he] # edge index
        if e == INVALID_EDGE: # if edge has been removed
            continue
        if time_stamp != E_time_stamps[e]: # if cost is obsolete
            continue 
        if np.abs(cost-INF_COST) < 1e-6:
            print("encounter INF cost, cannot be decimated further")
            break
        # =====

        # =====
        # CHECK is collapse valid
        is_valid = is_collapse_valid(V, twins, tips, he, v_opt, triangle_quality_threshold=triangle_quality_threshold, verbose=verbose)
        if not is_valid:
            E_time_stamps[e] = cur_collapses
            heapq.heappush(min_heap, (INF_COST, cur_collapses, he, i, j, v_opt))
            continue
        # =====
        
        # Notation
        #          k            
        #         /  \         
        #        /    \     
        #  hennt/henn  \     
        #      /     hen\hent     
        #     /    he    \  
        #    i ---------  j 
        #     \    het   /   
        # hetnt\hetn    /     
        #       \ hetnn/hetnnt       
        #        \    /         
        #         \  /       
        #          l    
        hen = next(he)
        henn = next(hen)
        hent = twin(twins, hen) # could be GHOST_HALF_EDGE
        hennt = twin(twins, henn) # could be GHOST_HALF_EDGE
        het = twin(twins,he) # could be GHOST_HALF_EDGE
        if het == GHOST_HALF_EDGE: 
            # if he is boundary half edge
            hetn = GHOST_HALF_EDGE
            hetnn = GHOST_HALF_EDGE
            hetnt = GHOST_HALF_EDGE
            hetnnt = GHOST_HALF_EDGE
        else:
            hetn = next(het)
            hetnn = next(hetn)
            hetnt = twin(twins, hetn)  # could be GHOST_HALF_EDGE
            hetnnt = twin(twins, hetnn)  # could be GHOST_HALF_EDGE    
        
        # =====
        # start post edge collapse
        cur_collapses += 1

        # print progress
        if cur_collapses % print_every_iterations == 0:
            print("decimation progress:", cur_collapses, "/", total_collapses)

        # topo update tips (we always keep vertex i)
        he_list_tip_i = vertex_one_ring_half_edges_from_half_edge(twins, next(next(he)), around_tail=False)
        he_list_tip_j = vertex_one_ring_half_edges_from_half_edge(twins, he, around_tail=False)
        for he_ in he_list_tip_j:
            tips[he_] = i
        for he_ in he_list_tip_i:
            tips[he_] = i
            
        # topo update twins 
        update_twin(twins, hennt, hent)
        update_twin(twins, hetnt, hetnnt)

        # move vertex
        V[i,:] = v_opt
        V[j,:] = GHOST_VERTEX_LOCATION

        # update vertex quadrics
        Qv[i,:,:] = Qv[i,:,:] + Qv[j,:,:]
        Qv[j,:,:] = INF

        # remove info from tips and twins
        for he_ in [he, hen, henn, het, hetn, hetnn]:
            update_tip(tips, he_, INVALID_VERTEX_INDEX)
            update_twin(twins, he_, INVALID_HALF_EDGE)

        # update he2e list 
        update_he2e(he2e, hent, he2e[henn])
        if hetn != GHOST_HALF_EDGE:
            update_he2e(he2e, hetnnt, he2e[hetn])
        for he_ in [he, hen, henn, het, hetn, hetnn]:
            update_he2e(he2e, he_, INVALID_EDGE)

        # =====
        # update costs for edge one-ring half-edges
        he_new = np.min([hennt, hetnnt, next(hent)]) # the next(hent) is important to deal with ear vertex
        assert(tail_vertex(tips, he_new) == i)
        he_list_new = vertex_one_ring_half_edges_from_half_edge(twins, he_new, around_tail=True)
        Qi_ = Qv[i,:,:]
        for he_ in he_list_new:
            j_ = tip_vertex(tips, he_)
            Qj_ = Qv[j_,:,:]
            Qeij_ = Qi_ + Qj_
            v_opt_, cost_ = optimal_location_and_cost(Qeij_)
            heapq.heappush(min_heap, (cost_, cur_collapses, he_, i, j_, v_opt_))

            e_ = he2e[he_]
            E_time_stamps[e_] = cur_collapses

        # if i is a boundary vertex, then we need to update one more edge
        if is_boundary_vertex_from_half_edge(twins, he_list_new[-1]):
            he_ = next(next(he_list_new[-1]))
            j_ = tail_vertex(tips, he_)

            Qj_ = Qv[j_,:,:]
            Qeij_ = Qi_ + Qj_
            v_opt_, cost_ = optimal_location_and_cost(Qeij_)
            heapq.heappush(min_heap, (cost_, cur_collapses, he_, j_, i, v_opt_)) # make sure (j_, i) is swapped here because the half edge is in the opposite direction

            e_ = he2e[he_]
            E_time_stamps[e_] = cur_collapses
        # =====

    F = faces_from_half_edge_data(tips)
    V,F,IMV,vIdx = remove_unreferenced(V,F)
    return V,F

# =====
# Utility functions for qslim
# =====
# def optimal_location_and_cost(Qe):
#     # v'Qv = v'Av + 2b'v + c 
#     A = Qe[:3,:3]
#     b = Qe[:3,3]
#     c = Qe[3,3]

#     # get some candidate vertex locations
#     v_optimal = np.linalg.solve(A, -b)
#     quadric_error = (v_optimal @ A).dot(v_optimal) + 2 * b.dot(v_optimal) + c
#     return v_optimal, quadric_error

def update_tip(tips, he_, he_tip_):
    if he_ != GHOST_HALF_EDGE: # if not ghost
        tips[he_] = he_tip_

def update_twin(twins, he_, he_twin_):
    if he_ != GHOST_HALF_EDGE and he_ != INVALID_HALF_EDGE: # if not ghost
        twins[he_] = he_twin_
    if he_twin_ != GHOST_HALF_EDGE and he_twin_ != INVALID_HALF_EDGE:
        twins[he_twin_] = he_

def update_he2e(he2e, he_, e_):
    if he_ != GHOST_HALF_EDGE:
        he2e[he_] = e_

def update_time_stamp(E_time_stamps, he2e, he_, new_time_stamp):
    if he_ != GHOST_HALF_EDGE:
        E_time_stamps[he2e[he_]] = new_time_stamp

# def triangle_quadrics(V,F):
#     """
#     Compute triangle quadrics 

#     Inputs:
#         V: |V|x3 vertex list
#         F: |F|x3 face list

#     Outputs:
#         Qf: (nF,4,4) triangle quadrics
#     """
#     # compute initial quadric error 
#     p = compute_triangle_planes(V, F)

#     # compute face quadrics
#     Qf = np.einsum("fi,fj->fij",p, p) # face quadrics (nF,4,4)
#     return Qf

def vertex_quadrics(V,F, twins=None, tips=None, boundary_quadric_weight=1.0, boundary_quadric_regularization=1e-6):
    """
    Compute vertex quadrics 

    Inputs:
        V: |V|x3 vertex list
        F: |F|x3 face list
        twins: |he| twin info of half edges
        tips: |he| tip vertices of half edges
        boundary_quadric_weight: scalar weight on how well you want to preserve boundaries

    Outputs:
        Qv: (nV,4,4) vertex quadrics
    """
    # compute half edge data structure information if not provided
    if twins is None or tips is None:
        twins, tips = build_implicit_half_edges(F)

    # some useful mesh quantities
    nHe = F.shape[0] * 3
    nV = V.shape[0]
    nF = F.shape[0]

    # compute triangle quadrics
    Qf = triangle_quadrics(V,F) # triangle quadrics (nF,4,4)

    # make face quadric weighted by 1/3 of the face area (see Sec 3.4 in https://www.cs.cmu.edu/~garland/thesis/thesis-onscreen.pdf)
    FA = face_areas(V,F)

    # compute vertex quadrics 
    Qv = np.zeros((nV,4,4))
    for f in range(nF):
        v0,v1,v2 = F[f,:]
        one_third_face_area = FA[f] / 3.0
        Qv[v0,:,:] += Qf[f,:,:] * one_third_face_area
        Qv[v1,:,:] += Qf[f,:,:] * one_third_face_area
        Qv[v2,:,:] += Qf[f,:,:] * one_third_face_area

    # include boundary quadrics 
    for he in range(nHe):
        # extract vertex indices
        v_tip_index = tip_vertex(tips, he)
        v_tail_index = tail_vertex(tips, he)
        v_opp_index = tip_vertex(tips, next(he))

        # extract vertex locations
        v_tip = V[v_tip_index,:]
        v_tail = V[v_tail_index,:]
        v_opp = V[v_opp_index,:]

        # compute face normal
        fn = np.cross(v_tip - v_tail, v_opp - v_tail)
        fn = fn / np.linalg.norm(fn)

        # compute half edge normal
        he_n = np.cross(v_tip - v_tail, fn)
        he_n = he_n / np.linalg.norm(he_n)

        # compute half edge plane equation
        he_d = -he_n.dot(v_tail)
        he_p = np.append(he_n,he_d)

        # compute half edge quadric
        he_K = np.outer(he_p, he_p)

        # edge length 
        el = np.linalg.norm(v_tip - v_tail)
            
        # add to vertex quadrics
        if is_boundary_half_edge(twins, he): # if this is boundary half edge
            Qv[v_tail_index,:,:] += boundary_quadric_weight * el**2 * he_K
            Qv[v_tip_index,:,:] += boundary_quadric_weight * el**2 * he_K
        else:
            Qv[v_tail_index,:,:] += boundary_quadric_regularization * el**2 * he_K
            Qv[v_tip_index,:,:] += boundary_quadric_regularization * el**2 * he_K

    return Qv