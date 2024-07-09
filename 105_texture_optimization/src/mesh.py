import kaolin as kal
import torch
import copy
import xatlas
import numpy as np

class Mesh:
    def __init__(self,obj_path, device):
        if ".obj" in obj_path:
            try:
                mesh = kal.io.obj.import_mesh(obj_path, with_normals=True, with_materials=True)
            except:
                mesh = kal.io.obj.import_mesh(obj_path, with_normals=True, with_materials=False)
        elif ".off" in obj_path:
            mesh = kal.io.off.import_mesh(obj_path)
        else:
            raise ValueError(f"{obj_path} extension not implemented in mesh reader.")

        self.vertices = mesh.vertices.to(device)
        self.faces = mesh.faces.to(device)
        self.ft = mesh.face_uvs_idx
        self.vt = mesh.uvs
        self.normalize_mesh(inplace=True, target_scale=0.6, dy=0.25)

    def normalize_mesh(self,inplace=False, target_scale=1, dy=0):
        mesh = self if inplace else copy.deepcopy(self)

        verts = mesh.vertices
        center = verts.mean(dim=0)
        verts -= center
        scale = torch.max(torch.norm(verts, p=2, dim=1))
        verts /= scale
        verts *= target_scale
        verts[:, 1] += dy
        mesh.vertices = verts
        return mesh

def compute_xatlas_texture_map(mesh):
    device = mesh.vertices.device
    v_np = mesh.vertices.cpu().numpy()
    f_np = mesh.faces.int().cpu().numpy()
    atlas = xatlas.Atlas()
    atlas.add_mesh(v_np, f_np)
    chart_options = xatlas.ChartOptions()
    chart_options.max_iterations = 4
    atlas.generate(chart_options=chart_options)
    vmapping, ft_np, vt_np = atlas[0]  # [N], [M, 3], [N, 2]
    vt = torch.from_numpy(vt_np.astype(np.float32)).float().to(device)
    ft = torch.from_numpy(ft_np.astype(np.int64)).int().to(device)
    return vt, ft

def compute_uv_map(mesh):
    vt, ft = compute_xatlas_texture_map(mesh)
    uvs = kal.ops.mesh.index_vertices_by_faces(
        vt.unsqueeze(0),
        ft.long()
    ).detach()
    return uvs, vt, ft