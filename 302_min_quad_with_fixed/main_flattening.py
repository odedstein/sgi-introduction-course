import sys
sys.path.append('../../')
import matplotlib.pyplot as plt
import polyscope as ps
import numpy as np
import igl

from src.read_obj import read_obj
from src.decimate_qem import decimate_qem

from src.cotmatrix_dense import cotmatrix_dense
from exercise.mqwf_dense import mqwf_dense

def main():
    V,F = read_obj('./data/ogre_sim.obj')

    # construct the laplacian
    L = cotmatrix_dense(V, F)

    # extract the boundary
    bnd = igl.boundary_loop(F)
    # map to a unit disk
    uvb = igl.map_vertices_to_circle(V, bnd)

    Bo = np.zeros((np.shape(V)[0],2))

    # solve the constrained linear system
    UV2 = mqwf_dense(L, Bo, bnd, uvb)
    zeros_column = np.zeros((np.shape(V)[0], 1))
    UV = np.hstack((UV2, zeros_column))
    UV[:, [0, 1, 2]] = UV[:, [0, 2, 1]]

    ps.init()
    ps.register_surface_mesh("input mesh", V, F)
    ps.register_surface_mesh("2D parameterization mesh", UV, F)
    ps.show()

if __name__ == '__main__':
    main()