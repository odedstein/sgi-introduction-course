import numpy as np

def cotmatrix_dense(V,F):
    '''
    COTMATRIX computes the cotangent laplace matrix of a triangle mesh

    Inputs:
    V: |V|-by-3 numpy ndarray of vertex positions
    F: |F|-by-3 numpy ndarray of face indices

    Output:
    L: |V|-by-|V| matrix
    '''
    V = np.array(V)
    F = np.array(F)
    numVert = V.shape[0]
    numFace = F.shape[0]

    temp1 = np.zeros((numFace, 3))
    temp2 = np.zeros((numFace, 3))
    angles = np.zeros((numFace, 3))

    # compute angle
    for i in range(3):
        i1 = (i  ) % 3
        i2 = (i+1) % 3
        i3 = (i+2) % 3
        temp1 = V[F[:,i2],:] - V[F[:,i1],:]
        temp2 = V[F[:,i3],:] - V[F[:,i1],:]

        # normalize the vectors
        norm_temp1 = np.sqrt(np.power(temp1,2).sum(axis = 1))
        norm_temp2 = np.sqrt(np.power(temp2,2).sum(axis = 1))
        temp1 = np.divide(temp1, np.repeat([norm_temp1], 3, axis=0).transpose())
        temp2 = np.divide(temp2, np.repeat([norm_temp2], 3, axis=0).transpose())

        # compute angles
        dotProd = np.multiply(temp1, temp2).sum(axis = 1)
        angles[:,i1] = np.arccos(dotProd)

    # compute cotan laplace
    L = np.zeros((numVert,numVert), dtype=np.float64)
    for i in range(3):
        i1 = (i  ) % 3
        i2 = (i+1) % 3
        i3 = (i+2) % 3
        L[F[:,i1],F[:,i2]] += -1 / (np.tan(angles[:,i3])+1e-6)    
    L = (L + L.transpose()) / 2
    temp = np.array(L.sum(axis=1)).reshape((numVert))
    L -= np.diag(temp)
    return -L