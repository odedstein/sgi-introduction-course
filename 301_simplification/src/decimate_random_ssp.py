import numpy as np
import heapq
import polyscope as ps

from .global_variables import GHOST_HALF_EDGE, INVALID_HALF_EDGE, INVALID_VERTEX_INDEX, INF_COST, INF, HAS_BEEN_COLLAPSED, INVALID_EDGE, INVALID_FACE_INDEX, QEM, PROBABILITY_QEM, UNIFORM_QEM, MID_POINT

from .next import next
from .twin import twin
from .tip_vertex import tip_vertex
from .tail_vertex import tail_vertex

from .build_implicit_half_edges import build_implicit_half_edges
from .vertex_quadrics import vertex_quadrics
from .is_boundary_half_edge import is_boundary_half_edge
from .vertex_one_ring_half_edges_from_half_edge import vertex_one_ring_half_edges_from_half_edge
from .vertex_one_ring_faces_from_half_edge import vertex_one_ring_faces_from_half_edge
from .is_boundary_vertex_from_half_edge import is_boundary_vertex_from_half_edge
from .is_collapse_valid import is_collapse_valid
from .remove_unreferenced import remove_unreferenced
from .joint_lscm import joint_lscm
from .ssp_map import ssp_map

def decimate_random_ssp(Vo,Fo,num_target_vertices,ssp_maps,
                   triangle_quality_threshold = 0.1, 
                   edge_quadric_weight = 1.0,
                   verbose = False, 
                   print_every_iterations = 500, 
                   random_perturbation = 0.0, # whether to randomly perturn the cost, the amount will be max_cost * random_perturbation
                   decimation_method = UNIFORM_QEM,
                   boundary_quadric_weight = 1.0, 
                   uniform_quadric_weight = 1e-3,
                   probability_quadric_sq_std_n = 1e-2,
                   probability_quadric_sq_std_p = 1e-2):
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

    TODO: add UV QEM
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
    Kv = vertex_quadrics(V,F, twins, tips, 
                         decimation_method = decimation_method,
                         boundary_quadric_weight = boundary_quadric_weight,
                         uniform_quadric_weight = uniform_quadric_weight,
                         probability_quadric_sq_std_n = probability_quadric_sq_std_n,
                         probability_quadric_sq_std_p = probability_quadric_sq_std_p)

    # =========
    # Initialization
    # =========
    # decimation parameters
    total_collapses = nV - num_target_vertices
    cur_collapses = 0

    # for DEBUG
    # P = []
    # PN = []

    # compute initial edge quadric errors, min head, he2e map, E_time_stamps
    he_processed = np.zeros(nF*3, dtype=bool)
    he2e = -np.ones(nHe, dtype=np.int32)
    eIdx = 0
    min_heap = [] # (cost, cur_collapses, he, i, j, v_opt)
    max_cost = 0.0
    for he in range(nHe):
        if he_processed[he] == False:
            i = tail_vertex(tips, he)
            j = tip_vertex(tips, he)
            Ki = Kv[i,:,:]
            Kj = Kv[j,:,:]
            vi = V[i,:]
            vj = V[j,:]

            # TODO: debug the optimal vertex computation
            v_opt, cost = optimal_location_and_cost(Ki+Kj, vi, vj, decimation_method)
            heapq.heappush(min_heap, (cost, cur_collapses, he, i, j, v_opt))
            # P.append(v_opt) # for DEBUG

            if max_cost < cost: # for random perturbation
                max_cost = cost

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
        # if np.linalg.norm(V[i,:] - GHOST_VERTEX_LOCATION) < 1e-6 or np.linalg.norm(V[j,:] - GHOST_VERTEX_LOCATION) < 1e-6:
        #     print("encounter invalid vertex, this shouldn't happen")
        #     continue
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

        # CHECK is lscm is valid
        is_valid, UV, FUV_pre, FUV_post, fIdx_pre, fIdx_post, ij_indices = joint_lscm(V, F, twins, tips, he, v_opt)
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

        # update face list
        for f_ in fIdx_pre:
            F[f_, F[f_,:]==j] = i
            if F[f_,0] == F[f_,1] or F[f_,1] == F[f_,2] or F[f_,2] == F[f_,0]:
                F[f_,:] = INVALID_VERTEX_INDEX

        # update vertex quadrics
        Kv[i,:,:] = Kv[i,:,:] + Kv[j,:,:]
        Kv[j,:,:] = INF

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

        # store ssp map information
        ssp_maps.append(ssp_map(ij_indices, UV, FUV_pre, FUV_post, fIdx_pre, fIdx_post))

        # =====
        # update costs for edge one-ring half-edges
        he_new = np.min([hennt, hetnnt, next(hent)]) # the next(hent) is important to deal with ear vertex
        assert(tail_vertex(tips, he_new) == i)
        he_list_new = vertex_one_ring_half_edges_from_half_edge(twins, he_new, around_tail=True)
        Ki_ = Kv[i,:,:]
        vi_ = v_opt
        for he_ in he_list_new:
            j_ = tip_vertex(tips, he_)
            Kj_ = Kv[j_,:,:]
            vj_ = V[j_,:]
            v_opt_, cost_ = optimal_location_and_cost(Ki_+Kj_, vi_, vj_, decimation_method, random_perturbation, max_cost)
            heapq.heappush(min_heap, (cost_, cur_collapses, he_, i, j_, v_opt_))

            e_ = he2e[he_]
            E_time_stamps[e_] = cur_collapses

        # if i is a boundary vertex, then we need to update one more edge
        if is_boundary_vertex_from_half_edge(twins, he_list_new[-1]):
            he_ = next(next(he_list_new[-1]))
            j_ = tail_vertex(tips, he_)

            Kj_ = Kv[j_,:,:]
            vj_ = V[j_,:]
            v_opt_, cost_ = optimal_location_and_cost(Ki_+Kj_, vi_, vj_, decimation_method, random_perturbation, max_cost)
            # heapq.heappush(min_heap, (cost_, cur_collapses, he_, i, j_, v_opt_))
            heapq.heappush(min_heap, (cost_, cur_collapses, he_, j_, i, v_opt_)) # make sure (j_, i) is swapped here because the half edge is in the opposite direction

            e_ = he2e[he_]
            E_time_stamps[e_] = cur_collapses
        # =====

    # ps.init()
    # ps.register_surface_mesh("pre", Vo, Fo)
    # ps.register_surface_mesh("post", V, F)
    # ps.show()

    Fc2F = []
    for f in range(F.shape[0]):
        if F[f,0] != INVALID_VERTEX_INDEX:
            Fc2F.append(f)
    Fc2F = np.array(Fc2F, dtype=np.int32)

    # Extract faces from half edge data structure
    # F = faces_from_half_edge_data(tips)
    V,F,IMV,vIdx = remove_unreferenced(V,F[Fc2F,:])
    return V,F,Fc2F

# =====
# Utility functions for qslim
# =====
def optimal_location_and_cost(Ke, v0, v1, decimation_method, random_perturbation=0.0, max_cost=0.0):
    if decimation_method == QEM or decimation_method == UNIFORM_QEM or decimation_method == PROBABILITY_QEM:
        # v'Kv = v'Av + 2b'v + c 
        A = Ke[:3,:3]
        b = Ke[:3,3]
        c = Ke[3,3]

        # get some candidate vertex locations
        LHS = np.vstack((Ke[:3, :], np.array([[0,0,0,1]])))
        v_solve = np.linalg.solve(LHS+np.eye(4)*1e-6, np.array([0,0,0,1]))
        v_solve = v_solve[:3]
        # v_solve = np.linalg.solve(A + 1e-6 * np.eye(3), -b)
        # v_solve = np.linalg.solve(A, -b)
        v_mid = (v0 + v1) / 2.0

        # compute the costs
        cost_v_solve = (v_solve @ A).dot(v_solve) + 2 * b.dot(v_solve) + c
        cost_v_mid = (v_mid @ A).dot(v_mid) + 2 * b.dot(v_mid) + c
        cost_v0 = (v0 @ A).dot(v0) + 2 * b.dot(v0) + c
        cost_v1 = (v1 @ A).dot(v1) + 2 * b.dot(v1) + c

        min_idx = np.argmin([cost_v_solve, cost_v_mid, cost_v0, cost_v1])
        if min_idx == 0: # v_solve is the best
            return v_solve, cost_v_solve + random_perturbation * np.random.rand() * max_cost
        elif min_idx == 1: # v_mid is the best
            return v_mid, cost_v_mid + random_perturbation * np.random.rand() * max_cost
        elif min_idx == 2: # v0 is the best
            return v0, cost_v0 + random_perturbation * np.random.rand() * max_cost
        elif min_idx == 3: # v1 is the best
            return v1, cost_v1 + random_perturbation * np.random.rand() * max_cost
        else:
            raise ValueError("this should be impossible to happen")
    elif decimation_method == MID_POINT:
        cost = np.linalg.norm(v0 - v1) + random_perturbation * np.random.rand() * max_cost
        v_mid = (v0 + v1) / 2.
        return v_mid, cost
    else:
        raise ValueError("decimation method is not defined")

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
