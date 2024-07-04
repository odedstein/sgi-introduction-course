def closed_cylinder(nx,nz):
    """Returns a **closed** cylinder mesh.

    Parameters
    ----------
    nx : int
         number of vertices along the equator of the cylinder (at least 3)
    nz : int
         number of vertices on the z-axis of the cylinder (at least 2)

    Returns
    -------
    V : (n,3) numpy array
        vertex positions of the cylinder
    F : (m,3) numpy array
        face positions of the cylinder
    """