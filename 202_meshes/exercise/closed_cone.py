def closed_cone(nx,nz):
    """Returns a **closed** cone mesh.

    Parameters
    ----------
    nx : int
         number of vertices along the base of the cone (at least 3)
    nz : int
         number of vertices on the z-axis of the cone (at least 2)

    Returns
    -------
    V : (n,3) numpy array
        vertex positions of the cone
    F : (m,3) numpy array
        face positions of the cone
    """