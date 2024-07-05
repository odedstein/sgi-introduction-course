import numpy as np
import multiprocessing
from functools import partial
from .ssp_map import ssp_map
from .barycentric_coordinates_skala import barycentric_coordinates_skala

def ssp_query_coarse_to_fine(BC, BF, ssp_maps, Fc2F):

    ssp_query_coarse_to_fine_single_partial = partial(ssp_query_coarse_to_fine_single, BC=BC,BF=BF,ssp_maps=ssp_maps,Fc2F=Fc2F)

    num_points = BC.shape[0]
    with multiprocessing.Pool() as pool:
        for b, bc, bf in pool.map(ssp_query_coarse_to_fine_single_partial, range(num_points)):
            BC[b,:] = bc
            BF[b] = bf
    return BC, BF

def ssp_query_coarse_to_fine_single(b, BC, BF, ssp_maps, Fc2F):

    bc = BC[b,:]
    bf = Fc2F[BF[b]]

    for ssp_map in reversed(ssp_maps):
        if bf in ssp_map.fIdx_post:
            # if this barycentric point is in the decimation
            UV = ssp_map.UV
            F_pre = ssp_map.F_pre
            F_post = ssp_map.F_post
            fIdx_pre = ssp_map.fIdx_pre
            fIdx_post = ssp_map.fIdx_post

            # compute the query point in UV
            idx = np.where(fIdx_post == bf)[0][0]
            uv0 = UV[F_post[idx, 0],:] 
            uv1 = UV[F_post[idx, 1],:] 
            uv2 = UV[F_post[idx, 2],:] 
            p = uv0*bc[0] + uv1*bc[1] + uv2*bc[2]

            min_barycentric_distance = np.inf
            min_bc = np.ones(3,dtype=np.float64)
            min_bf = -1
            for kk in range(F_pre.shape[0]):
                uv0 = UV[F_pre[kk,0],:]
                uv1 = UV[F_pre[kk,1],:]
                uv2 = UV[F_pre[kk,2],:]

                bc_kk, _, inside, dist_to_valid_kk = barycentric_coordinates_skala(p, uv0, uv1, uv2, return_info=True)
                if inside:
                    min_bc = bc_kk
                    min_bf = fIdx_pre[kk]
                    break
                else:
                    if dist_to_valid_kk < min_barycentric_distance:
                        min_bc = bc_kk
                        min_bf = fIdx_pre[kk]
            bc = min_bc
            bf = min_bf
    return b, bc, bf