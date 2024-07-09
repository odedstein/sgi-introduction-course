import os
import numpy as np
import gpytoolbox as gpy

def compute_total_curvature(V, F):

    '''
    Computes the sum of the (signed) Gaussian curvature at every vertex of the mesh
    '''

    # [F,3,3] tensor of corner positions for each triangle
    corner_pos = V[F,:]

    # [F,3,3] tensors of the two edge-vectors emanating from each corner
    vecA = np.roll(corner_pos, 1, axis=1) - corner_pos
    vecB = np.roll(corner_pos, 2, axis=1) - corner_pos

    # "cosine rule" to compute corner angles
    # A dot B = |A||B|cos(theta) --> theta = arccos((A dot B) / |A||B|)
    normA = np.linalg.norm(vecA, axis=-1) # [F,3]
    normB = np.linalg.norm(vecB, axis=-1) # [F,3]
    dot_prod = np.sum(vecA * vecB, axis=-1) # [F,3]
    corner_angles = np.arccos(dot_prod / (normA * normB)) # [F,3] tensor of corner angles in radians for each triangle

    # compute the total curvature
    num_verts = V.shape[0]
    total_curvature = num_verts * 2.* np.pi - np.sum(corner_angles)

    return total_curvature

def process_mesh(filename):

    '''
    This function reads a mesh file, computes its total curvature, then uses the 
    Gauss-Bonnet Theorem to determine its genus. Roughly, the genus is how many 
    'handles' the shape has in a topological sense, a sphere has 0, a torus has 1, etc.

    Everything in this function is correct. 
    '''
    
    print(f"\n === Processing mesh {filename}")

    V, F = gpy.read_mesh(filename)
    
    print(f"  {V.shape[0]} verts   {F.shape[0]} faces")

    total_curvature = compute_total_curvature(V,F) #
    euler_characteristic_computed = total_curvature / (2.*np.pi) # total_curvature = 2*pi*chi
    genus_computed = (euler_characteristic_computed - 2.) / -2.  # chi = 2 - 2*genus

    print(f"  total curvature {total_curvature:.2f} = {total_curvature / np.pi:.2f} π")
    print(f"  Gauss-Bonnet Theorem says the genus is {genus_computed:.2f} (valid for closed triangle meshes only)")

# manage paths 
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "..", "data")

# call the function on several meshes
process_mesh(os.path.join(DATA_DIR, "sphere_good.obj"))
process_mesh(os.path.join(DATA_DIR, "spot_good.obj"))
process_mesh(os.path.join(DATA_DIR, "torus_good.obj"))
process_mesh(os.path.join(DATA_DIR, "triple_torus_good.obj"))
process_mesh(os.path.join(DATA_DIR, "sphere_bad.obj"))
