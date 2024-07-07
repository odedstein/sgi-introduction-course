import numpy as np
import scipy
from . loop_upsample_connectivity import loop_upsample_connectivity

def loop_upsample_barycentric(V,F,num_subdiv_iters=1):
    '''
    computes the mid-point loop subdivision with new points represented as barycentric coordinates and the new face list

    Inputs:
    nV: number of vertices
    F: |F|-by-3 numpy ndarray of face indices

    Output:
    BC: (n, 3) barycentric coordinates
    BF: (n) barycentric face indices on the mesh V,F
    Fs: (m, 3) new face list after loop subdivision

    Note: This function perfoms mid point upsampling with loop subdivision connecivity. This function has consistent vertices/faces with https://github.com/HTDerekLiu/neuralSubdiv/blob/master/utils_matlab/midPointUpsample.m. In order to be consistent, this is slower than usual

    '''
    NF = F.copy()
    for ii in range(num_subdiv_iters):
        if ii == 0:
            S, NF = loop_upsample_connectivity(V.shape[0], NF)
        else:
            SS, NF = loop_upsample_connectivity(S.shape[0], NF)
            S = SS @ S

        
    BC = np.zeros((S.shape[0],3), dtype=np.float64)
    BF = np.zeros((S.shape[0]), dtype=np.int32)
    for r in range(S.shape[0]):
        indices = S[[r],:].indices
        values = S[[r],:].data

        per_face_sum = np.zeros(F.shape[0], dtype=np.int32)
        for idx in indices:
            per_face_sum += np.sum(F == idx, 1)
        
        fIdx = np.where(per_face_sum == len(indices))[0][0]
        for ii in range(len(indices)):
            v = indices[ii]
            idx_in_f = np.where(F[fIdx,:] == v)[0][0]
            BC[r, idx_in_f] = values[ii]
        BF[r] = fIdx
    return BC, BF, NF