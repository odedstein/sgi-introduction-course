import polyscope as ps
import numpy as np
from src.mesh import Mesh
from PIL import Image

ps.init()
mesh = Mesh("data/spot.obj")
ps_mesh = ps.register_surface_mesh(
    "mesh",
    mesh.vertices,
    mesh.faces,
    edge_width=1,
    material='clay',
)

# Add the parameterization
ps_mesh.add_parameterization_quantity("param", mesh.uv, defined_on='corners')

# Add the texture map
texture_map = Image.open("data/spot_texture.png")
# normalize the texture map values to be between 0 and 1
texture_map = np.asarray(texture_map) / 255
ps_mesh.add_color_quantity("spot_texture", texture_map, 
                           defined_on='texture', param_name="param", 
                           enabled=True)
ps.show()
