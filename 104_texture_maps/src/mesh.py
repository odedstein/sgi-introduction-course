import numpy as np

class Mesh:
    def __init__(self, path, torch=False):
        self.load(path, torch=torch)

    def load(self, path, torch):
        vertices = []
        colors = []
        faces = []
        normals = []
        vt = []
        uv = []
        with open(path, "r") as f:
            content = f.readlines()
            if ".obj" in path:
                for line in content:
                    elems = line.split(" ")
                    if elems[0] == "v":
                        vertices.append([float(cord) for cord in elems[1:4]])
                        if len(elems[4:]) > 0:
                            colors.append([int(255 * float(rgb)) for rgb in elems[4:]])
                    if elems[0] == "f":
                        if "//" in elems[1]:
                            faces.append(
                                [int(vert.split("//")[0]) - 1 for vert in elems[1:]]
                            )
                        elif "/" in elems[1]:
                            faces.append(
                                [int(vert.split("/")[0]) - 1 for vert in elems[1:]]
                            )
                        elif "/1/" in elems[1]:
                            faces.append(
                                [int(vert.split("/1/")[0]) - 1 for vert in elems[1:]]
                            )
                        else:
                            faces.append([int(vert) - 1 for vert in elems[1:]])
                    if elems[0] == "vn":
                        normals.append([float(normal) for normal in elems[1:]])
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

        if torch:
            import torch
            self.vertices = torch.FloatTensor(vertices)
            self.faces = torch.Tensor(faces).long()
            self.colors = torch.tensor(colors)
            self.normals = torch.tensor(normals)
            self.vt = torch.tensor(vt)
            self.uv = torch.tensor(uv)
        else:
            self.vertices = np.array(vertices)
            self.faces = np.array(faces)
            self.colors = np.array(colors)
            self.normals = np.array(normals)
            self.vt = np.array(vt)
            self.uv = np.array(uv)
