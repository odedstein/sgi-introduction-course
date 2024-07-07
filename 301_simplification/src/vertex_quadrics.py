import numpy as np
from .is_boundary_half_edge import is_boundary_half_edge
from .tip_vertex import tip_vertex
from .tail_vertex import tail_vertex
from .build_implicit_half_edges import build_implicit_half_edges
from .next import next
from .face_normals import face_normals
from .face import face
from .global_variables import QEM, PROBABILITY_QEM, UNIFORM_QEM

from exercise.face_areas import face_areas
from src.compute_triangle_planes import compute_triangle_planes

def vertex_quadrics(V,F,
                    twins=None,
                    tips=None, 
                    decimation_method=UNIFORM_QEM,
                    boundary_quadric_weight = 1.0,
                    uniform_quadric_weight = 1e-3,
                    probability_quadric_sq_std_n = 1e-2,
                    probability_quadric_sq_std_p = 1e-2):
    """
    Compute vertex quadrics 

    Inputs:
        V: |V|x3 vertex list
        F: |F|x3 face list
        twins: |he| twin info of half edges
        tips: |he| tip vertices of half edges
        edge_quadric_weight: scalar weight on how well you want to preserve boundaries

    Outputs:
        Kv: (nV,4,4) vertex quadrics
    
    TODO: each vertex quadric is symmetric, we can make it (nV,10) to save storage cost
    """
    # compute half edge data structure information if not provided
    if twins is None or tips is None:
        twins, tips = build_implicit_half_edges(F)

    # some useful mesh quantities
    nHe = F.shape[0] * 3
    nV = V.shape[0]
    nF = F.shape[0]

    # compute initial quadric error 
    p = compute_triangle_planes(V, F)

    # compute face quadrics
    if decimation_method == QEM:
        Kf = np.einsum("fi,fj->fij",p, p) # face quadrics (nF,4,4)
    elif decimation_method == PROBABILITY_QEM:
        # probabilistic quadric error from "Fast and Robust QEF Minimization using Probabilistic Quadrics"
        unit_Nf = face_normals(V,F)
        Kf = np.zeros((nF,4,4))
        for f in range(nF):
            n = unit_Nf[f]
            ijk = F[f,:]
            p = V[ijk,:].mean(0)

            d = p.dot(n)

            A = np.outer(n,n) + np.eye(3)*probability_quadric_sq_std_n
            b = d * n + probability_quadric_sq_std_n * p
            c = d*d + probability_quadric_sq_std_n * p.dot(p) + probability_quadric_sq_std_p * n.dot(n) + 3*probability_quadric_sq_std_p*probability_quadric_sq_std_n
            Kf[f,:3,:3] = A
            Kf[f,3,:3] = -b
            Kf[f,:3,3] = -b
            Kf[f,3,3] = c
    elif decimation_method == UNIFORM_QEM:
        Kf = np.einsum("fi,fj->fij",p, p) # face quadrics (nF,4,4)

        # add interior half-edge boundary quadrics
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
            
            # add to face quadrics
            fIdx = face(he)
            Kf[fIdx,:,:] += uniform_quadric_weight * he_K

    # make face quadric weighted by 1/3 of the face area (see Sec 3.4 in https://www.cs.cmu.edu/~garland/thesis/thesis-onscreen.pdf)
    FA = face_areas(V,F)
    FA = FA / FA.mean() # normalize FA so that its mean is 1, just to improve numerics
    Kf = Kf * FA[:,None,None] / 3

    # compute vertex quadrics 
    Kv = np.zeros((nV,4,4))
    for f in range(nF):
        kf = Kf[f,:,:]     
        v0,v1,v2 = F[f,:]
        Kv[v0,:,:] += kf
        Kv[v1,:,:] += kf
        Kv[v2,:,:] += kf

    # include boundary half edge quadrics 
    for he in range(nHe):
        if is_boundary_half_edge(twins, he): # if this is boundary half edge

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
            
            # add to vertex quadrics
            Kv[v_tail_index,:,:] += boundary_quadric_weight * he_K
            Kv[v_tip_index,:,:] += boundary_quadric_weight * he_K

    return Kv
