import torch

def compute_barycentric_coords(triangles, points):
    """ Compute the barycentric coordinates for a collection of points with respect to a
    set of triangles.

    Args:
        triangles (torch.tensor): F x 3 x 2 array of faces in UV space
        points (torch.tensor): N x 2 array of texel coordinates
    
    Returns:
        barycentric_coords (torch.tensor): N x F x 3 array of barycentric coordinates
    """
    ...