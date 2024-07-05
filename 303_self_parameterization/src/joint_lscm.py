import numpy as np
import scipy
import polyscope as ps
from .read_obj import read_obj

from .global_variables import GHOST_HALF_EDGE, INVALID_HALF_EDGE, INVALID_VERTEX_INDEX, INF_COST, INF, HAS_BEEN_COLLAPSED, INVALID_EDGE
from .is_boundary_vertex_from_half_edge import is_boundary_vertex_from_half_edge
from .vertex_one_ring_vertices_from_half_edge import vertex_one_ring_vertices_from_half_edge
from .vertex_one_ring_half_edges_from_half_edge import vertex_one_ring_half_edges_from_half_edge
from .vertex_one_ring_faces_from_half_edge import vertex_one_ring_faces_from_half_edge
from .is_boundary_half_edge import is_boundary_half_edge
from .face_normal import face_normal
from .face import face
from .twin import twin
from .next import next
from .tail_vertex import tail_vertex
from .tip_vertex import tip_vertex
from .cotmatrix_dense import cotmatrix_dense
from .vector_area_matrix_dense import vector_area_matrix_dense

from exercise.mqwf_dense import mqwf_dense

def joint_lscm(V, F, twins, tips, he, v_opt):
    # case variables
    INTERIOR = 0
    I_ON_BOUNDARY = 1
    J_ON_BOUNDARY = 2
    BOUNDARY = 3

    # determine which case in joint lscm
    is_i_boundary_vertex = is_boundary_vertex_from_half_edge(twins, he)
    is_j_boundary_vertex = is_boundary_vertex_from_half_edge(twins, next(he))
    is_he_boundary_half_edge = is_boundary_half_edge(twins, he)

    if not is_i_boundary_vertex and not is_j_boundary_vertex and not is_he_boundary_half_edge:
        which_case = INTERIOR # a regular interior edge
    elif is_i_boundary_vertex and not is_j_boundary_vertex and not is_he_boundary_half_edge:
        which_case = I_ON_BOUNDARY # vi on boundary, not vj is not
    elif not is_i_boundary_vertex and is_j_boundary_vertex and not is_he_boundary_half_edge:
        which_case = J_ON_BOUNDARY # vj on boundary, not vi is not
    elif is_i_boundary_vertex and is_j_boundary_vertex and is_he_boundary_half_edge:
        which_case = BOUNDARY # both i,j,he are on boundary
    else:
        # this includes the case where vi,vj are on boundary, but he is not. This collapse cause the mesh to be non-manifold, skip this
        return False

    # start flattening
    if which_case == INTERIOR:
        UV, FUV_pre, FUV_post, fIdx_pre, fIdx_post, ij_indices = joint_lscm_interior(V, F, twins, tips, he, v_opt)
    else:
        raise ValueError("to be implemented")
    
    is_valid = check_valid_UV(UV, FUV_pre, FUV_post)
    return is_valid, UV, FUV_pre, FUV_post, fIdx_pre, fIdx_post, ij_indices

def check_valid_UV(UV, FUV_pre, FUV_post):
    # check NANs
    if np.any(np.isnan(UV)):
        return False
    
    # check fold over
    vec1 = UV[FUV_pre[:,1],:] - UV[FUV_pre[:,0],:]
    vec2 = UV[FUV_pre[:,2],:] - UV[FUV_pre[:,0],:]
    area = np.cross(vec1, vec2)
    if np.any(area < 0):
        return False
    
    vec1 = UV[FUV_post[:,1],:] - UV[FUV_post[:,0],:]
    vec2 = UV[FUV_post[:,2],:] - UV[FUV_post[:,0],:]
    area = np.cross(vec1, vec2)
    if np.any(area < 0):
        return False
    
    return True

def joint_lscm_interior(V, F, twins, tips, he, v_opt):
    """
    Return
    UV: #V_loc x 2 UV location
    """
    # gather topological information
    i = tail_vertex(tips, he)
    j = tip_vertex(tips, he)
    one_ring_i = vertex_one_ring_vertices_from_half_edge(twins, tips, he)
    one_ring_j = vertex_one_ring_vertices_from_half_edge(twins, tips, next(he))
    one_ring_ij = np.setdiff1d(np.union1d(one_ring_i, one_ring_j), np.array([i,j]))

    # construct V_joint
    V_joint = np.concatenate((V[[i,j],:], v_opt[None,:], V[one_ring_ij,:]))
    nV_joint = V_joint.shape[0]

    # create index maps mapping original index to local index to V_joint
    index_map = {}
    index_map[i] = 0
    index_map[j] = 1
    idx = 3 # idx = 2 is for v_opt
    for k in one_ring_ij:
        index_map[k] = idx
        idx += 1

    # assemble local face list
    Nf_i = vertex_one_ring_faces_from_half_edge(twins, he)
    Nf_j = vertex_one_ring_faces_from_half_edge(twins, twin(twins,he))

    Nf_pre = np.concatenate((Nf_i, Nf_j[1:-1]))
    F_joint_pre = np.zeros((len(Nf_pre), 3), dtype=np.int32)
    for ii in range(len(Nf_pre)):
        f_ = Nf_pre[ii]
        for jj in range(3):
            v = F[f_,jj]
            F_joint_pre[ii,jj] = index_map[v]

    Nf_post = np.concatenate((Nf_i[1:-1], Nf_j[1:-1]))
    F_joint_post = np.zeros((len(Nf_post), 3), dtype=np.int32)
    v_opt_index = 2
    for ii in range(len(Nf_post)):
        f_ = Nf_post[ii]
        for jj in range(3):
            v = F[f_,jj]
            if v == i or v == j:
                F_joint_post[ii,jj] = v_opt_index
            else:
                F_joint_post[ii,jj] = index_map[v]

    # assemble cotangent weight before collapse
    L = cotmatrix_dense(V_joint, F_joint_pre) + cotmatrix_dense(V_joint, F_joint_post)

    # assemble vector area matrix
    A = vector_area_matrix_dense(F_joint_pre, nV_joint) + vector_area_matrix_dense(F_joint_post, nV_joint)

    # solve for least square conformal map
    LHS = scipy.linalg.block_diag(L,L) + 2 * A
    RHS = np.zeros(nV_joint*2, dtype=np.float64)
    known = np.array([0, 1, nV_joint, nV_joint+1], dtype=np.int32)
    known_val = np.array([0, 1, 0, 0], dtype=np.float64)
    UV_joint = mqwf_dense(LHS, RHS, known, known_val)
    UV_joint = UV_joint.reshape(2,nV_joint).T

    ij_indices = np.array([0, 1])

    return UV_joint, F_joint_pre, F_joint_post, Nf_pre, Nf_post, ij_indices