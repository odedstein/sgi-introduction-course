import torch

def trivial_parameterization(triangles):
    # Local basis origin is the first vertex in each triangle
    origins = triangles[:, 0]

    # Get the normal of the plane defined by the triangle
    e1 = triangles[:, 1] - origins
    e2 = triangles[:, 2] - origins
    normal = torch.cross(e1, e2, dim=1)
    normal /= torch.linalg.norm(normal, dim=1).unsqueeze(1)

    # We will use e1 as the first basis. Second basis will be cross between e1 and the normal
    basis1 = e1 / torch.linalg.norm(e1, dim=1).unsqueeze(1)
    basis2 = torch.cross(normal, basis1, dim=1)
    basis2 /= torch.linalg.norm(basis2, dim=1).unsqueeze(1)

    # First vertex is the origin. Project the other two vertices onto the local bases.
    # Note that in PyTorch `torch.dot()` only works with 1D tensors so we instead use
    # einsum notation to compute the dot product.
    uv0 = torch.zeros(triangles.shape[0], 2).to(triangles.device)
    uv1 = torch.stack((
        torch.einsum('bi,bi->b', e1, basis1),
        torch.einsum('bi,bi->b', e1, basis2)
    ), dim=1)
    uv2 = torch.stack((
        torch.einsum('bi,bi->b', e2, basis1),
        torch.einsum('bi,bi->b', e2, basis2)
    ), dim=1)
    uvs = torch.stack((uv0, uv1, uv2), dim=1)

    return uvs, origins, basis1, basis2