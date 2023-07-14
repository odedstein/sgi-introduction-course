# Robustness puzzle 1

This script tries to load a mesh and visualize it using `tsurf()`. 

Rather than loading from a standard mesh file format, it loads a list of vertices `V` and faces `F` directly from a file that I have saved. Loading directly from manually-written data happens, for instance, when you are transferring the data from some other tool.

However, the script won't work! Something is wrong with the mesh data. I promise these files are (almost) correct. Figure out what is wrong, and fix it.

**Note:** Although the previous parts of the tutorial discuss using software like Blender and Meshlab to debug meshes, in this case the arrays are stored in custom formats, you won't be able to load them in external software. You should debug these from within matlab, try printing out and checking values of the arrays to see if you can find the issue.
