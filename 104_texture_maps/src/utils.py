import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
import numpy as np
from igl import grad

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

def get_jacobian(vs, fs, uvmap):
    """ Get jacobian of mesh given an input UV map

    Args:
        vs (np.ndarray): V x 3 array of vertex positions
        fs (np.ndarray): F x 3 integer array of face indices
        uvmap (np.ndarray): V x 2 array of UV coordinates

    Returns:
        J (np.array): F x 3 x 2 array of jacobians
    """
    # Visualize distortion
    G = np.array(grad(vs, fs).todense())

    # NOTE: currently gradient is organized as X1, X2, X3, ... Y1, Y2, Y3, ... Z1, Z2, Z3 ... reshape to X1, Y1, Z1, ...
    splitind = G.shape[0]//3
    newG = np.zeros_like(G) # F*3 x V
    newG[::3] = G[:splitind]
    newG[1::3] = G[splitind:2*splitind]
    newG[2::3] = G[2*splitind:]

    J = (newG @ uvmap).reshape(-1, 3, 2) # F x 3 x 2
    return J

def compute_distortion(vertices, faces, uvs):
    """ Compute the distortion of the parameterization

    Args:
        vertices (np.array): V x 3 array of vertex positions
        faces (np.array): F x 3 integer array of face indices
        uvs (np.array): F*3 x 2 array of UV coordinates
    
    Returns:
        S (np.array): the singular values of the jacobian

    """
    corner_vertices = vertices[faces].reshape(-1, 3)
    corner_faces = np.arange(faces.shape[0]*3).reshape(-1, 3)
    J = get_jacobian(corner_vertices, corner_faces, uvs)
    _, S, _ = np.linalg.svd(J)
    return S