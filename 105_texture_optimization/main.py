import torch
import torchvision
import random
import os
import numpy as np
from src.render import Renderer
from src.mesh import Mesh, compute_uv_map
from src.get_target_renders import get_target_renders
from src.utils import get_texels, load_texture_image
from src.optimize_texture import optimize_texture
from solution.inverse_map import inverse_map


# Set up some global variables
RENDER_SIZE = 256 # Dimentions of the output rendered image
DEVICE = "cuda" # Either "cuda" or "cpu"; determines whether the code runs on GPU or CPU
MESH_PATH = "data/spot.obj" # Path to the mesh file
TEXTURE_IMAGE_PATH = "data/spot_texture.png" # The target texture image path
# (can be either "data/uv_grid.png" or "data/spot_texture.png")
RENDERS_PATH = "rendered_images.png" # Path of the output rendered images
SEED = 42
OPTIM_ITERATIONS = 1000
TEXTURE_IMAGE_SIZE = 256
NUM_RENDERS = 3
TARGET_UVS = "load" # Either "load" or None
VIZ_UVS = True
TOLERANCE = 0.5 # How strict to be about texels lying inside triangles. Lower is more
# strict and will make the optimization faster, but might introduce seam artifacts due
# to anti-aliasing. The correct way to handle this would be to include anti-aliasing in
# our inverse_mapping() function, but this is beyond the scope of this tutorial.
# Recommended values: 1e-6 for cube.obj, 0.5 for spot.obj

# Set seed for reproducibility
random.seed(SEED)
os.environ['PYTHONHASHSEED'] = str(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)

# Setup
# Initialize renderer
renderer = Renderer(
    DEVICE,
    dim=(RENDER_SIZE, RENDER_SIZE)
)

# Load in mesh
mesh = Mesh(MESH_PATH, device=DEVICE)

# Initialize a texture image
texture_image = torch.ones(1, 3, TEXTURE_IMAGE_SIZE, TEXTURE_IMAGE_SIZE).to(DEVICE)


# Computing a UV parameterization with XAtlas
uvs, vt, ft = compute_uv_map(mesh)
uvs = uvs[0]

# Target setup
# Load the target texture image
target_texture_image = load_texture_image(TEXTURE_IMAGE_PATH, renderer.device)

# UV parameterization for the target images
# If no UVs are provided, we can use the same ones we computed for our optimization
if TARGET_UVS == "load":
    from src.utils import load_uvs
    print(MESH_PATH, "MESH_PATH")
    target_uvs, _ = load_uvs(MESH_PATH)
    target_uvs = target_uvs.to(DEVICE)
else:
    target_uvs = uvs

# Optionally, we can visualze the UV parameterization like we did in module 104
if VIZ_UVS:
    from src.utils import plot_uvs
    from PIL import Image
    test_texture_image = Image.open("data/uv_grid.png")
    # normalize the texture map values to be between 0 and 1
    test_texture_image = np.asarray(test_texture_image)[:, :, :3] / 255
    plot_uvs("test_plot_uvs.png", vt.cpu().numpy(), ft.cpu().numpy(), test_texture_image, "UVs")

# Visualize the target renders
target_renders = get_target_renders(
    mesh,
    renderer,
    target_texture_image,
    azim=torch.deg2rad(torch.tensor([-90, 0, 90], device=DEVICE)),
    elev=torch.deg2rad(torch.tensor([30, 30, 30], device=DEVICE)),
    radius=torch.tensor([2], device=DEVICE),
    uvs=target_uvs
)
torchvision.utils.save_image(target_renders, "target_renders.png")

# Get the surface points and texel indices
texels = get_texels(TEXTURE_IMAGE_SIZE, device=DEVICE)
surface_points, texel_indices = inverse_map(
    mesh.vertices,
    mesh.faces,
    uvs,
    texels,
    tolerance=TOLERANCE
)

# Optimize the texture map
mlp, texture_image = optimize_texture(
    mesh,
    surface_points,
    texel_indices,
    uvs,
    texture_image,
    renderer,
    num_renders=NUM_RENDERS,
    iterations=OPTIM_ITERATIONS,
    lr=1e-4,
    device=DEVICE,
    target_texture=target_texture_image,
    target_uvs=target_uvs
)

# Save the final texture image
torchvision.utils.save_image(texture_image, "final_texture.png")

# Render and save the final textured mesh
final_renders = renderer.render_texture(
    mesh.vertices,
    mesh.faces,
    uvs,
    texture_image,
    azim=torch.deg2rad(torch.tensor([-90, 0, 90], device=DEVICE)),
    elev=torch.deg2rad(torch.tensor([30, 30, 30], device=DEVICE)),
    radius=torch.tensor([2], device=DEVICE)
)
torchvision.utils.save_image(final_renders, "final_mesh_renders.png")