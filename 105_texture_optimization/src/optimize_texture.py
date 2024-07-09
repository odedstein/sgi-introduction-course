import torch
import torchvision
from tqdm import tqdm
from pathlib import Path

from .mlp import MLP
from .get_target_renders import get_target_renders
from .bake_texture_map import bake_texture_map

def optimize_texture(
    mesh,
    surface_points,
    texel_indices,
    uvs,
    texture_image,
    renderer,
    num_renders=3,
    iterations=2000,
    lr=1e-4,
    target_texture="uv_grid",
    target_uvs=None,
    device="cuda"
):
    """ Optimize the texture map of a mesh

    Args:
        mesh (Mesh): Mesh object
        surface_points (torch.Tensor): Surface points
        texel_indices (torch.Tensor): Indices of the texels
        uvs (torch.Tensor): UV coordinates
        texture_image (torch.Tensor): Texture image
        renderer (Renderer): Renderer object
        num_renders (int): Number of renders to use for optimization
        iterations (int): Number of optimization iterations
        lr (float): Learning rate
        target_texture (str): Which texture to use for the target renders
        target_uvs (torch.Tensor): UV coordinates of the target mesh
        device (str): Device to run the optimization on
    
    Returns:
        mlp (MLP): Trained MLP used to predict RGB values over the mesh surface
        texture_image (torch.Tensor): Updated texture image
    """
    # Initialize directories to save results
    Path("results/renders").mkdir(parents=True, exist_ok=True)
    Path("results/textures").mkdir(parents=True, exist_ok=True)

    # Initialize our coordinate network mapping surface points to RGB colors
    mlp = MLP(depth=4, width=256, out_dim=3, input_dim=3).to(device)

    # Initialize our optimizer
    optim = torch.optim.Adam(mlp.parameters(), lr)

    # Optimize our texture map
    for iteration in tqdm(range(iterations)):
        # Reset gradients
        optim.zero_grad()

        # Get MLP predictions for the RGB values
        pred_rgbs = mlp(surface_points)

        # Bake the predicted RGBs into the texture map
        baked_texture_image = torch.zeros_like(texture_image)
        for channel in range(3):
            baked_texture_image[:, channel] = bake_texture_map(
                                                    pred_rgbs[:, channel],
                                                    texel_indices,
                                                    texture_image[0, channel, :, :].clone().detach()
                                                )
        texture_map = baked_texture_image.transpose(2, 3).flip(2)

        # Randomly sample camera parameters (angles in radians)
        azim = torch.deg2rad(torch.rand((num_renders,), device=device) * 360)
        elev = torch.deg2rad(torch.rand((num_renders,), device=device) * 180 - 90)
        radius = torch.rand((num_renders,), device=device) + 1 # range is [1, 2]

        # Render the mesh with the new texture map
        renders = renderer.render_texture(
            mesh.vertices,
            mesh.faces,
            uvs,
            texture_map,
            azim=azim,
            elev=elev,
            radius=radius
        )

        # Compute the loss between the rendered image and the target image
        target_renders = get_target_renders(
            mesh,
            renderer,
            target_texture,
            azim=azim,
            elev=elev,
            radius=radius,
            uvs=target_uvs
        )
        loss = torch.nn.functional.mse_loss(renders, target_renders)

        # Backpropagate gradients to parameters
        loss.backward()

        # Update parameters by taking a step in the direction indicated by the gradients
        optim.step()

        # Log results
        if iteration % 100 == 0:
            # Log the loss
            print(f"Iteration: {iteration}, Loss: {loss.item()}")
        if iteration % 25 == 0:
            # Save the rendered image
            torchvision.utils.save_image(renders, f"results/renders/iter_{iteration}.png")
            # Save the texture map
            torchvision.utils.save_image(texture_map, f"results/textures/texture_map_{iteration}.png")
            # Save the target renders
            # torchvision.utils.save_image(target_renders, f"results/target_renders_{iteration}.png")

    return mlp, texture_map