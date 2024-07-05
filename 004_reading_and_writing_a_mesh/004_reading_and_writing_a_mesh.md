# Reading and writing a mesh

In this exercise we will learn how to read and write meshes to and from popular
file formats.


## Reading a mesh

Most triangle meshes are not created by hand or by using a function, but read
from an input file.
Gpytoolbox can read a number of mesh formats.
Here, we will take a look at the OBJ format.

From now on, to be able to use Gpytoolbox functions in Python, be sure to always
import the library:
```python
>>> import gpytoolbox as gpy
```

To read an OBJ mesh, use the command
```python
V,F = gpy.read_mesh('data/bunny.obj')
```
The resulting variables `V,F` will contain the vertex and face lists.
For this to work, you need to be in the correct directory, since the path to
the mesh, `'data/bunny.obj'`, is relative to your current directory.
Navigate your terminal to the folder where you downloaded the tutorial, and go
into the folder for this exercise, `004_reading_and_writing_a_mesh`, and start
your console (or put your working script here).

In this case, we read the Stanford bunny, which looks like this:
> Remember the visualization commands from [exercise 003!](../003_a_triangle_mesh/003_a_triangle_mesh.md)

![The Stanford bunny, loaded from an OBJ file](assets/bunnyread.png)


## Writing a mesh

When you want to save a generated mesh, or the result of a geometry processing
calculation, you can use Gpytoolbox to _save_ it to an OBJ file.
This works with the command
```python
>>> gpy.write_mesh('data/bunny.obj', V,F);
```

_NOTE: This will overwrite whatever is in that file currently!
Make sure to only do this if you actually want to overwrite a file._


## Other file formats

Gpytoolbox supports a variety of other mesh formats that are read using a
similar syntax.
They are:
* STL
* PLY


## Try writing your own mesh

Try writing the following function:
* `write_tetrahedron`, which writes the simple tetrahedron from 003 to a file.

As usual, the skeleton for this function, ready for you to fill in, can be
found in `exercise/`.
