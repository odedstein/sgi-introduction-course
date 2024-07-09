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


    # Rescale triangles


    return triangles