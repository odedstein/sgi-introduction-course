import os
import numpy as np

# This is a simple .obj file format parser. It does not handle all features of the format, 
# just the absolute most basic features. For real code, you use should use 
# `gpytoolbox.read_mesh()` or other libraries instead, this is just a basic example.

# THIS FUNCTION IS BROKEN! It has a small bug, your job is to find it and fix it.
#
# Fun fact: this buggy code was generated by ChatGPT 
def my_read_mesh_from_obj_file(obj_filename):

    # store the vertices and faces here
    vertices = []
    faces = []

    # open the file
    with open(obj_filename, 'r') as file:

        # walk through each line of the file
        for line in file:

            # if it starts with 'v', read a vertex
            if line.startswith('v '):
      
                # parse the line, discard the 'v', then read it into a list of 3 coordinates
                parts = line.strip().split()
                vertex = [float(coord) for coord in parts[1:4]]

                # add this vertex to the list of vertices
                vertices.append(vertex)

            # if it starts with 'f', read a face
            elif line.startswith('f '):

                # parse the line, discard the 'f', then read it into a list of 3 indices
                parts = line.strip().split()
                face = [int(index.split('/')[0]) for index in parts[1:]]
                
                # add this face to the list of faces
                faces.append(face)

   
    # The above code stores faces and vertices as lists-of-lists, but we usually 
    # work with numpy arrays. Convert them to numpy arrays.
    vertices = np.array(vertices)
    faces = np.array(faces)

    # SOLUTION 
    # this line fixes the function
    # faces = faces - 1 # shift from 1-based to 0-based indexing

    return vertices, faces

# manage paths 
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "..", "data")

# Call the function a mesh file
# Something is wrong with the resulting V,F!
# We promise nothing is wrong with this file itself.
V, F = my_read_mesh_from_obj_file(os.path.join(DATA_DIR, "fox.obj"))



# Always start by visualizing!
# If you run this on the initial V,F, Polyscope will helpfully-give out a warning that the face indices contain out of-bounds values.

import polyscope as ps

ps.init()
ps.register_surface_mesh("mesh", V, F)
ps.show()


# Now let's try printing some values
# (delete/comment-out the lines above so the code goes past them)
print(V)
print(F) # these all seeeeem to be reasonable


# Wait a minute, the smallest index in F is 1, and the largest index is one-past the size of our vertex array V!
print(V.shape) 
print(F.min())
print(F.max())


# The problem is that F uses 1-based indices starting at 1, rather than 0-based indices!
# The underlying cause is that .obj files use 1 based indices, but Python uses 0-based. We forgot to take that into account in the parser.
# We can subtract 1 from the indices in the paser like
# `faces = faces - 1`
# As implemented above
