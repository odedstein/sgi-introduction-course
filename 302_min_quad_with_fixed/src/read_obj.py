import numpy as np

def read_obj(filepath):
    """
    READOBJ read .obj file

    Input:
      filepath a string of mesh file path
    Output:
      V (|V|,3) numpy array of vertex positions
	  F (|F|,3) numpy array of face indices
    """
    V = []
    F = []
    with open(filepath, "r") as f:
        lines = f.readlines()
    while True:
        for line in lines:
            if line == "":
                break
            elif line.strip().startswith("vn"):
                continue
            elif line.strip().startswith("vt"):
                continue
            elif line.strip().startswith("v"):
                vertices = line.replace("\n", "").split(" ")[1:]
                vertices = np.delete(vertices,np.argwhere(vertices == np.array([''])).flatten())
                V.append(list(map(float, vertices)))
            elif line.strip().startswith("f"):
                t_index_list = []
                for t in line.replace("\n", "").split(" ")[1:]:
                    t_index = t.split("/")[0]
                    try: 
                        t_index_list.append(int(t_index) - 1)
                    except ValueError:
                        continue
                F.append(t_index_list)
            else:
                continue
        break
    V = np.asarray(V)
    F = np.asarray(F)
    return V, F

def read_obj_UV(filepath):
    """
    READOBJ read .obj file

    Input:
      filepath a string of mesh file path
    Output:
      V (|V|,3) numpy array of vertex positions
	  F (|F|,3) numpy array of face indices
    """
    V = []
    UV = []
    UF = []
    F = []
    with open(filepath, "r") as f:
        lines = f.readlines()
    while True:
        for line in lines:
            if line == "":
                break
            elif line.strip().startswith("vn"):
                continue
            elif line.strip().startswith("vt"):
                vertices = line.replace("\n", "").split(" ")[1:]
                vertices = np.delete(vertices,np.argwhere(vertices == np.array([''])).flatten())
                UV.append(list(map(float, vertices)))
            elif line.strip().startswith("v"):
                vertices = line.replace("\n", "").split(" ")[1:]
                vertices = np.delete(vertices,np.argwhere(vertices == np.array([''])).flatten())
                V.append(list(map(float, vertices)))
            elif line.strip().startswith("f"):
                t_index_list = []
                for t in line.replace("\n", "").split(" ")[1:]:
                    t_index = t.split("/")[0]
                    try: 
                        t_index_list.append(int(t_index) - 1)
                    except ValueError:
                        continue
                F.append(t_index_list)

                t_index_list = []
                for t in line.replace("\n", "").split(" ")[1:]:
                    t_index = t.split("/")[1]
                    try: 
                        t_index_list.append(int(t_index) - 1)
                    except ValueError:
                        continue
                UF.append(t_index_list)
            else:
                continue
        break
    V = np.asarray(V)
    F = np.asarray(F)
    UV = np.asarray(UV)
    UF = np.asarray(UF)
    return V, F, UV, UF

def read_obj_vertex_colors(filepath):
    """
    READOBJ read .obj file

    Input:
      filepath a string of mesh file path
    Output:
      V (|V|,3) numpy array of vertex positions
	  F (|F|,3) numpy array of face indices
    """
    V = []
    F = []
    VC = []
    with open(filepath, "r") as f:
        lines = f.readlines()
    while True:
        for line in lines:
            if line == "":
                break
            elif line.strip().startswith("vn"):
                continue
            elif line.strip().startswith("vt"):
                continue
            elif line.strip().startswith("v"):
                vertices = line.replace("\n", "").split(" ")[1:]
                vertices = np.delete(vertices,np.argwhere(vertices == np.array([''])).flatten())
                V.append(list(map(float, vertices)))
            elif line.strip().startswith("f"):
                t_index_list = []
                for t in line.replace("\n", "").split(" ")[1:]:
                    t_index = t.split("/")[0]
                    try: 
                        t_index_list.append(int(t_index) - 1)
                    except ValueError:
                        continue
                F.append(t_index_list)
            else:
                continue
        break
    V = np.asarray(V)
    F = np.asarray(F)
    VC = V[:,3:]
    V = V[:,:3]
    return V, F, VC