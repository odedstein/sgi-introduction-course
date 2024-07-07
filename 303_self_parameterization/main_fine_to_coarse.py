import sys
sys.path.append('../../')
import matplotlib.pyplot as plt
import polyscope as ps
import numpy as np

from src.read_obj import read_obj
from src.decimate_ssp import decimate_ssp
from src.decimate_random_ssp import decimate_random_ssp
from src.ssp_query_fine_to_coarse import ssp_query_fine_to_coarse
from src.loop_upsample_barycentric import loop_upsample_barycentric

from src.ssp_query_coarse_to_fine import ssp_query_coarse_to_fine


def main():
    V,F = read_obj('./data/spot.obj')

    ssp_maps = []
    Vc,Fc,Fc2F = decimate_ssp(V,F,200, ssp_maps)

    # fine vertices as barycentric coordinates
    BC = np.zeros((V.shape[0],3), dtype=np.float64)
    BF = -np.ones(V.shape[0], dtype=np.int32)
    for f in range(F.shape[0]):
        for s in range(F.shape[1]):
            v = F[f,s]
            if BF[v] < 0: # not inserted
                BC[v, s] = 1.0
                BF[v] = f
    BC = np.array(BC)
    BF = np.array(BF)

    # query fine and coarse
    BC, BF = ssp_query_fine_to_coarse(BC, BF, ssp_maps, Fc2F)
    P_coarse = BC[:,0:1] * Vc[Fc[BF,0],:] + BC[:,1:2] * Vc[Fc[BF,1],:] + BC[:,2:3] * Vc[Fc[BF,2],:]

    ps.init()
    ps.register_surface_mesh("coarse mesh", Vc, Fc, edge_width=1.5)
    ps.register_point_cloud("fine points", P_coarse)
    ps.show()

if __name__ == '__main__':
    main()