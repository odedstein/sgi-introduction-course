import sys
sys.path.append('../../')
import matplotlib.pyplot as plt
import polyscope as ps
import numpy as np

from src.read_obj import read_obj
from src.decimate_qem import decimate_qem

def main():
    V,F = read_obj('./data/spot.obj')

    Vc,Fc = decimate_qem(V,F,200,
                         boundary_quadric_weight=1.0,
                         boundary_quadric_regularization=1e-6)

    ps.init()
    ps.register_surface_mesh("input mesh", V, F)
    ps.register_surface_mesh("coarse mesh", Vc, Fc)
    ps.show()

if __name__ == '__main__':
    main()
