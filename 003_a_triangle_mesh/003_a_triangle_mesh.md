# A triangle mesh

In this exercise we will learn about triangle meshes (discrete surfaces made
from piecewise triangles called "faces") stored as triangle soups, and how to
plot them.


## Triangle soups

The most prominent triangle mesh format used by gptoolbox is the
_triangle soup_.
In a triangle soup, the triangle mesh is represented by two matrices,
* a _vertex list_ `V`, where every row represents a vertex in 2D or 3D space
with `x`,`y`, and `z` coordinates; and
* a _face list_ `F`, where every row represents a triangle and consists of
indices into the vertex list `V`.

I.e., the vertex list `V` consists of real numbers and has dimensions
`n x 2` or `n x 3`, where `n` is the number of vertices in the mesh.
The face list `F` consists of positive integers and has dimensions `m x 3`,
where `m` is the number of triangle faces in the mesh.

Let's look at a very simple triangle mesh:
a mesh that consists of only one triangle.
Open up your console or your working script, import everything as you did in
the last exercise, and let's get to our triangle.
This triangle has the vertices `(0,0), (1,0), (0,1)`:
```python
>>> V = np.array([[0.,0.], [1.,0.], [0.,1.]])
>>> print(V)
[[0. 0.]
 [1. 0.]
 [0. 1.]]
```
Now we need to specify the triangle list.
We only have one triangle which indexes the vertices in `V` in counter-clockwise
order:
```python
>>> F = np.array([[0,1,2]])
>>> print(F)
[[0 1 2]]
```

`V,F` is now a triangle mesh consisting of only one triangle.
Let's look at it!
We will use Polyscope to visualize all meshes in this tutorial.
Import it into your Python path now:
```python
import polyscope as ps
```

(you should already have NumPy imported, at the top of every one of your
scripts, with `import numpy as np`)

In Polyscope, triangle meshes are visualized with the `register_surface_mesh`
command, which takes as its argument a name that you choose for the surface,
the face list, and then the vertex list.
```python
>>> ps.init()
>>> ps.register_surface_mesh("triangle", V, F)
<polyscope.surface_mesh.SurfaceMesh object at 0x1043cad90>
>>> ps.show()
```
![Our very first surface plot: a single triangle](assets/firsttriangle.png)

Here is the same plot of our triangle, this time with each vertex labeled by
its index.
![Our very first surface plot: a single triangle, but now labeled](assets/firsttriangle-labeled.png)
We can see that the indices for the triangle list each vertex in order, going
around the triangle counter-clockwise.
This counter-clockwise direction is important for the correct orientation of
the triangle.
If the indices of the triangle are going in the counter-clockwise direction, we
are looking at the front of the triangle (it's _positively oriented_), otherwise
we're looking at the back of the triangle (it's _negatively oriented_).

Let's add a second triangle to our triangle mesh, `(1,0), (1,1), (0,1)`.
Since we already have the vertices `(1,0), (0,1)` in our vertex list, we only
have to add one new vertex:
```python
>>> V = np.array([[0.,0.], [1.,0.], [0.,1.], [1.,1.]])
>>> print(V)
[[0. 0.]
 [1. 0.]
 [0. 1.]
 [1. 1.]]
```
(if we were to add the vertices `(1,0), (0,1)` a second time we would have two
disconnected triangles, and not one coherent triangle mesh.)

We add the second triangle to our triangle list by re-using the indices that
we used for the first triangle, always making sure that the triangles are
oriented counter-clockwise.
```python
>>> F = np.array([[0,1,2], [1,3,2]])
>>> print(F)
[[0 1 2]
 [1 3 2]]
```

Plotting this new triangle mesh we now have a square made from two triangles.
```python
>>> ps.init()
>>> ps.register_surface_mesh("triangle", V, F)
<polyscope.surface_mesh.SurfaceMesh object at 0x1043cad90>
>>> ps.show()
```
![A square made from two triangles](assets/square.png)

If you click the "edges" button in the Polyscope GUI, you can see the two
individual trianges:

![A square made from two triangles with edges visible](assets/square_with_edges.png)


## Constructing a triangle mesh

We now try to construct a slightly more complex surface: a tetrahedron.
Unlike our previous square, the tetrahedron's vertices are in 3D.
This means that the vertex list `V` has three columns.

Let's specify all the vertices we need for our tetrahedron:
```python
>>> V = np.array([[0., 0., 0.], [1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
>>> print(V)
[[0. 0. 0.]
 [1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
```

We now add the four triangle faces which connect the vertices of the
tetrahedron.
We make sure that the triangles are oriented counterclockwise for an observer
that looks onto the tetrahedron from the outside (so we are looking at the
_front_ of the triangles).
```MATLAB
>>> F = np.array([[1,0,2], [0,1,3], [1,2,3], [2,0,3]])
>>> print(F)
[[1 0 2]
 [0 1 3]
 [1 2 3]
 [2 0 3]]
```

It's that easy to construct a tetrahedron!
After plotting it, you should be greeted by the following shape:
![Our very own tetrahedron](assets/tetrahedron.png)


## Make your own meshes

Now it's time to try and create your own triangle meshes.

Try writing the following functions:
* `simple_cube`, which returns the triangle soup `V,F` corresponding to a
simple cube made of triangles with 8 vertices
* `my_very_own_mesh`, which returns the triangle soup `V,F` for a mesh of your
very own creation.

As usual, the skeletons for these functions, ready for you to fill in, can be
found in `exercise/`.