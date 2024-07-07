import numpy as np

def remove_unreferenced(V,F):
    """
    remove unreferenced indices from V

    Inputs
    V: |V|xn array of vertex locations
    F: |F|xn array of face list

    Outputs
    V,F: new mesh
    IMV: index map for vertices such that IMV[old_vIdx] = new_vIdx
    vIdx: |newV| list of new vertex indices, st Vnew = V[uV,:]
    """
    # removed unreferenced vertices/faces
    nV = V.shape[0]

    # get a list of unique vertex indices from face list
    vIdx = np.unique(F)

    # index map for vertices such that IMV[old_vIdx] = new_vIdx
    IMV = np.zeros(nV, dtype = np.int32)
    IMV[vIdx] = np.arange(len(vIdx))

    # return the new mesh
    V = V[vIdx]
    F = IMV[F]
    return V,F,IMV,vIdx