import sys
sys.path.append('../../')
import matplotlib.pyplot as plt
import polyscope as ps
import numpy as np

from src.read_obj import read_obj
from src.decimate_ssp import decimate_ssp
from src.decimate_random_ssp import decimate_random_ssp
from src.ssp_query_coarse_to_fine import ssp_query_coarse_to_fine
from src.loop_upsample_barycentric import loop_upsample_barycentric

def main():
    V,F = read_obj('./data/spot.obj')

    ssp_maps = []
    Vc,Fc,Fc2F = decimate_ssp(V,F,200, ssp_maps)

    # generate random barycentric coordinates on the coarse mesh
    BC = np.zeros((Vc.shape[0],3), dtype=np.float64)
    BF = -np.ones(Vc.shape[0], dtype=np.int32)
    for f in range(Fc.shape[0]):
        for s in range(Fc.shape[1]):
            v = Fc[f,s]
            if BF[v] < 0: # not inserted
                BC[v, s] = 1.0
                BF[v] = f
    BC = np.array(BC)
    BF = np.array(BF)

    # query coarse to fine
    BC, BF = ssp_query_coarse_to_fine(BC, BF, ssp_maps, Fc2F)
    P = BC[:,0:1] * V[F[BF,0],:] + BC[:,1:2] * V[F[BF,1],:] + BC[:,2:3] * V[F[BF,2],:]

    ps.init()
    ps.register_surface_mesh("fine mesh", V, F, edge_width=1.5)
    ps.register_point_cloud("coarse points", P)
    ps.show()

if __name__ == '__main__':
    main()
