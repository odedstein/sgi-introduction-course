import torch

def transform_triangles(triangles):
    """
    Translate the triangles so that they are in the first quadrant and then rescale them
    to make them as large as possible while still fitting within the unit square. Make
    sure to scale all triangles by the same factor so that our parameteriztion is
    area-preserving up to some global scaler.

    Args:
        triangles (torch.tensor): F x 3 x 2 array of triangle coordinates
    
    Returns:
        triangles (torch.tensor): F x 3 x 2 array of transformed triangle coordinates
    """
    # Translate the triangles so that all coordinates are non-negative
    min_coords = torch.min(triangles, dim=1).values.unsqueeze(1)
    triangles -= min_coords

    # Rescale triangles
    # Find the global max x and y coordinates over all triangles
    max_coordinate = torch.max(triangles)
    # Divide all coordinates by the max coordinate to rescale the triangles
    triangles = triangles / max_coordinate

    return triangles