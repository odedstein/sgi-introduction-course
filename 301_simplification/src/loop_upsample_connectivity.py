import numpy as np
import scipy
import scipy.sparse as sparse


def loop_upsample_connectivity(nV, F):
    '''
    computes the mid-point loop subdivision operator (S) and the new face list

    Inputs:
    nV: number of vertices
    F: |F|-by-3 numpy ndarray of face indices

    Output:
    S: mid-point subdivision matrix such that S@V = Vs
    Fs: |F|*4-by-3 new face list after loop subdivision

    Note: This function perfoms mid point upsampling with loop subdivision connecivity. This function has consistent vertices/faces with https://github.com/HTDerekLiu/neuralSubdiv/blob/master/utils_matlab/midPointUpsample.m. In order to be consistent, this is slower than usual

    '''
    # assemble half edge indices
    nF = F.shape[0]
    hE = np.zeros((nF*3,2),dtype=np.int32)
    for ii in range(3):
        for f in range(nF):
            v0 = F[f,ii]
            v1 = F[f,(ii+1) % 3]
            if v0 < v1:
                hE[ii*nF + f,:] = v0, v1
            elif v1 < v0:
                hE[ii*nF + f,:] = v1, v0
            else:
                raise ValueError("degenerated face with two corners being the same vertex")
            
    E, reverse_indices = np.unique(hE, axis=0, return_inverse=True)

    # construct the new face list
    Fs = np.zeros((nF*4, 3), dtype=np.int32)
    hEF = np.zeros((nF*4, 3), dtype=np.int32)
    fIdx = 0
    for f in range(nF):
        hEF[fIdx,:] = F[f,0], nV+f, nV+2*nF+f # f0, i2, i1
        fIdx += 1
    for f in range(nF):
        hEF[fIdx,:] = F[f,1], nV+nF+f, nV+f # f1, i0, i2
        fIdx += 1
    for f in range(nF):
        hEF[fIdx,:] = F[f,2], nV+2*nF+f, nV+nF+f # f2, i1, i0
        fIdx += 1
    for f in range(nF):
        hEF[fIdx,:] = nV+nF+f, nV+2*nF+f, nV+f # i0, i1, i2
        fIdx += 1

    # build hE2E
    hE2E = np.concatenate((np.arange(nV),reverse_indices+nV))
    for r in range(4 * nF):
        for c in range(3):
            Fs[r,c] = hE2E[hEF[r,c]]

    # build subdiv operator such that Vs = S @ V
    nE = E.shape[0]
    row = []
    col = []
    val = []
    # even verts
    for e in range(nE):
        for c in range(E.shape[1]):
            row.append(e + nV)
            col.append(E[e,c])
            val.append(0.5)
    # odd verts
    for v in range(nV):
        row.append(v)
        col.append(v)
        val.append(1.0)
    S = scipy.sparse.csr_array((val, (row, col)), shape=(nE+nV, nV))

    return S, Fs
