import torch
import torchvision
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation

def load_texture_image(path, device):
    # Load image
    image = torchvision.io.read_image(path).to(device).float() / 255.0
    # Remove alpha channel if it exists
    image = image[:3]
    return image

def get_texels(n, device):
    # Create a grid of pixel coordinates
    x = torch.linspace(0, n-1, steps=n).to(device)
    y = torch.linspace(0, n-1, steps=n).to(device)
    px, py = torch.meshgrid(x, y)

    # Create pixel point tensor
    p = torch.stack((px.flatten(), py.flatten()), dim=1)

    return p

def plot_uvs(savefile, vt, ft, img,
                 name, linewidth=1,
                 xmin=0, xmax=1, ymin=0, ymax=1,
            ):
    """ Plot UV overlaid on a texture image

    Args:
        savefile (str): the path to save the image
        vt (torch.tensor): V x 2 array of UV coordinates
        ft (torch.tensor): F x 3 integer array of face indices
        img (torch.tensor): a texture image
        name (str): the title of the plot
        linewidth (float): the width of the triangle edges
        xmin (float): the minimum x value of the plot
        xmax (float): the maximum x value of the plot
        ymin (float): the minimum y value of the plot
        ymax (float): the maximum y value of the plot
    
    Returns:
        None
    """
    # First center the predicted vertices
    tris = Triangulation(vt[:, 0], vt[:, 1], triangles=ft)
    fig, axs = plt.subplots(figsize=(10, 10))

    # Plot image
    axs.imshow(img, origin='upper', extent=[xmin, xmax, ymin, ymax])

    # plot ours
    axs.set_title(name, fontsize=24)
    axs.triplot(tris, 'k-', linewidth=linewidth)

    plt.axis('off')
    axs.axis('equal')
    plt.savefig(savefile)

def load_uvs(path):
    vt = []
    uv = []
    with open(path, "r") as f:
        content = f.readlines()
        if ".obj" in path:
            for line in content:
                elems = line.split(" ")
                if elems[0] == "vt":
                        vt.append([float(uv) for uv in elems[1:]])
            for line in content:
                elems = line.split(" ")
                if elems[0] == "f":
                    if "//" in elems[1]:
                        pass
                    elif "/" in elems[1]:
                        for vert in elems[1:]:
                            uv.append(vt[int(vert.split("/")[1]) - 1])
    vt = torch.tensor(vt)
    uvs = torch.tensor(uv)
    return uvs, vt