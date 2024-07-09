from .mesh import compute_uv_map

def get_target_renders(mesh, renderer, texture_image, azim, elev, radius, uvs=None):
    """ Get target renders for the optimization

    Args:
        mesh (Mesh): Mesh object
        renderer (Renderer): Renderer object
        texture_image (torch.tensor): texture image
        azim (torch.tensor): tensor of azimuth angles
        elev (torch.tensor): tensor of elevation angles
        radius (torch.tensor): tensor of radius values for the camera
        uvs (torch.Tensor): UV coordinates

    Returns:
        target_renders (torch.Tensor): Target renders
    """   
    # Compute the UVs using XAtlas is not provided
    if uvs is None:
        uvs, vt, ft = compute_uv_map(mesh)
    
    # Render the target images
    target_renders = renderer.render_texture(
        mesh.vertices,
        mesh.faces,
        uvs,
        texture_image,
        azim=azim,
        elev=elev,
        radius=radius
    )

    return target_renders