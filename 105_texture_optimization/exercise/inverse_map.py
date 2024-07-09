import torch
from .compute_barycentric_coords import compute_barycentric_coords

def inverse_map(vertices, faces, uv_triangles, texels, tolerance=1e-6):
   """ Compute the inverse map from texels to surface points.

   Recommended approach:
   1. Scale triangles to the scale of the texels (0-1 --> 0-texture_image_size)
   2. Determine which texels are covered by which triangles
      (can do this using barycentric coordinates)
   3. Compute the barycentric coordinates for each covered texel with respect to the
      triangle that covers it
   4. For each covered texel, compute its 3D coordinate on the surface by using
      barycentric interpolation (use the barycentric coordinates of the triangle that
      covers it and the 3D vertices of that triangle)

   Args:
      vertices (torch.tensor): V x 3 array of vertex coordinates
      faces (torch.tensor): F x 3 array of triangle vertex indices
      uv_triangles (torch.tensor): F x 3 x 2 array of triangle coordinates in UV space
      texels (torch.tensor): N x 2 array of texel coordinates
      tolerance (float): Tolerance for barycentric coordinates validity. Use this when
                        checking if a texel is covered by a triangle.

   Returns:
      surface_points (torch.tensor): N x 3 array of surface points
      texel_indices (torch.tensor): N x 1 array of texel indices
   """
   # scale triangles to texel coordinates


   # Compute the barycentric coordinates for each texel with respect to each triangle


   # For each texel, for each triangle, determine if the texel lies inside the triangle


   # Get indices of valid texels and corresponding triangles


   # Select valid barycentric coordinates


   # Select corresponding triangle vertices for each valid point


   # Compute 3D coordinates for valid points
   # Hint: Use the barycentric coordinates of the texel and the vertices of the triangle


   # Return the surface points and texel indices

   ...
