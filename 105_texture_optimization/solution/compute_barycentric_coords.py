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
    a, b, c = triangles[:, 0, :], triangles[:, 1, :], triangles[:, 2, :]
    v0, v1 = b - a, c - a

    v2 = points[:, None, :] - a[None, :, :]
    
    d00 = torch.sum(v0 * v0, dim=-1)
    d01 = torch.sum(v0 * v1, dim=-1)
    d11 = torch.sum(v1 * v1, dim=-1)
    d20 = torch.sum(v2 * v0, dim=-1)
    d21 = torch.sum(v2 * v1, dim=-1)
    
    denom = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1 - (v + w)
    
    return torch.stack([u, v, w], dim=-1)