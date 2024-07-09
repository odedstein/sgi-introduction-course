def bake_texture_map(features, texel_indices, texture_image):
    """ Bake features into the texture map

    Args:
        features (torch.Tensor): features to bake of shape (N,)
        texel_indices (torch.Tensor): Indices of the texels to bake of shape (N,)
        texture_image (torch.Tensor): Texture image of shape (H, W)
    
    Returns:
        torch.Tensor: Updated texture image of shape (H, W)
    """
    flat_texture = texture_image.flatten()
    flat_texture[texel_indices] = features
    texture = flat_texture.reshape(texture_image.shape[0], texture_image.shape[1])
    return texture
