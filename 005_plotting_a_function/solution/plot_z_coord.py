import gpytoolbox as gpy, polyscope as ps, numpy as np

def plot_z_coord(V,F):
    """This method plots the z-cordinate on the input mesh V,F
    """

    f = V[:,2]
    ps.init()
    ps_surface = ps.register_surface_mesh("surface", V, F)
    ps_surface.add_scalar_quantity("z coordinate", f, enabled=True)
    ps.show()


