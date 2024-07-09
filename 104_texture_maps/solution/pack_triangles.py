import torch
from .transform_triangles import transform_triangles

def pack_triangles(triangles):
    """
    This function takes an array of triangles in the 2D plane and packs them into the
    unit square in a way such that no triangles overlap.

    See the description below for a suggested way to implement this. The proposed
    approach is by no means the most efficient packing so don't worry if there is unused
    space. Most triangulations won't perfectly fill the square with this triangle soup
    parameterization approach.

    One way to accomplish this is to rescale all triangles and place them on a square
    grid within the unit square. We can do this in the following steps:
        (1) Based on the number of triangles, determine the number of points needed on
            the grid needed to fit all triangles.
        (2) Translate the triangles so that they are in the first quadrant and then
            rescale them by a SINGLE value so that they are as large as possible while
            still fitting in the unit square.
        (3) Rescale the triangles so that they will fit on the grid without overlapping.
        (4) Arrange the triangles on the grid.

    Args:
        triangles (torch.tensor): F x 3 x 2 array of triangle coordinates
    
    Returns:
        packed_triangles (torch.tensor): F x 3 x 2 array of packed triangle coordinates

    """
    # Get the device (either "cpu" or "cuda")
    # Any time we create a PyTorch tensor from scratch, we need to specify the device
    # For example: new_tensor = torch.tensor([1, 2, 3]).to(device)
    device = triangles.device

    # Get the number of triangles
    num_triangles = triangles.shape[0]

    # Calculate number of rows/columns needed for this square grid
    # (based on the number of triangles)
    grid_size = int(torch.ceil(torch.sqrt(torch.tensor(num_triangles, dtype=torch.float))).item())

    # Generate a grid given these row/column sizes (see torch.meshgrid). Get a grid
    # coordinates tensor of shape (grid_rows * grid_columns, 2). Make sure that all
    # points in the grid are still contained within the unit square.
    grid_x, grid_y = torch.meshgrid(
        torch.linspace(0, 1 - (1 / grid_size), grid_size).to(device),
        torch.linspace(0, 1 - (1 / grid_size), grid_size).to(device),
        indexing='ij'
    )
    grid_coords = torch.stack((grid_x.flatten(), grid_y.flatten()), dim=1)

    # Complete and use the helper function "transform_triangles()" to transform the
    # triangles so that that they are as large as possible while still fitting in the
    # unit square.
    transformed_triangles = transform_triangles(triangles)

    # Rescale the triangles so that they fit on the grid without overlapping
    scaled_triangles = transformed_triangles / grid_size

    # Arrange the triangles on the grid
    # Hint: try adding the grid coordinates to the triangle coordinates
    # One way to do this might be using `.flatten()` method in PyTorch
    packed_triangles = scaled_triangles + grid_coords[:num_triangles, None, :]

    # Return the packed triangles
    return packed_triangles