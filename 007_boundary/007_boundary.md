# Boundary

In this exercise we will learn what the boundary of a surface is, and how we can
work with it using Gpytoolbox.


## The boundary of a surface

You might know intuitively what the boundary of a surface is.
It is the border between where there is a surface and where there is no surface.
Mathematically speaking, the boundary of a manifold surface is not trivial to
define
(see [the Wikipedia article for more details](https://en.wikipedia.org/wiki/Manifold#Manifold_with_boundary))
and involves a fair bit of differential geometry.
For triangle surface meshes, piecewise triangular surfaces, however,
the boundary is the _set of all points on triangle edges that are only part of
one triangle_, as opposed to the points on interior edges, which are always on
two triangles.[^1]

Consider the following simple mesh:

![simple square mesh](assets/square_nobdries.png)

What are its boundaries?
To determine the boundaries, we look at every point on every edge and check
whether this point is a part of only one triangle (and thus a boundary edge),
or whether the point is a part of two triangles (and thus an interior
edge).

![simple square mesh with boundary edges highlighted](assets/square_bdries.png)

Beyond boundary edges, we also have _boundary vertices_.
Boundary vertices are defined via boundary edges:
_A vertex is a boundary vertex if it is contained in a boundary edge_.
Otherwise, it is an _interior vertex_.

![simple square mesh with boundary vertices highlighted](assets/square_bdryverts.png)

Here are two examples of surfaces with their boundary vertices highlighted:

![goat head with boundary vertices highlighted](assets/goathead_bdryverts.png)

![mountain with boundary vertices highlighted](assets/mountain_bdryverts.png)

Boundary triangles (or boundary faces) occur less than boundary
verties and boundary edges.
_A boundary triangle is a triangle that contains at least one boundary edge_,
otherwise it is an _interior triangle_.


## Computing the boundary in Gpytoolbox

The basic tool in Gpytoolbox to extract the boundary in gptoolbox are the
functions `boundary_edges` and `boundary_vertices`.

`boundary_edges` returns the boundary edges as a list of lines for a triangle
mesh.
Consider the following small mesh of a square:

![a small mesh of a square](assets/small_square.png)

```python
>>> V = np.array([[0, 0], [0, 0.5], [0, 1], [0.5, 0], [0.5, 0.5], [0.5, 1], [1, 0], [1, 0.5], [1, 1]]) 
>>> F = np.array([[0,3,1], [3,4,1], [1,4,2], [4,5,2], [3,6,4], [6,7,4], [4,7,5], [7,8,5]])
>>> print(V)
[[0.  0. ]
 [0.  0.5]
 [0.  1. ]
 [0.5 0. ]
 [0.5 0.5]
 [0.5 1. ]
 [1.  0. ]
 [1.  0.5]
 [1.  1. ]]
>>> print(F)
[[0 3 1]
 [3 4 1]
 [1 4 2]
 [4 5 2]
 [3 6 4]
 [6 7 4]
 [4 7 5]
 [7 8 5]]
```

Just as the variable `F` gives us the triangles on the mesh as collections of
three indices into `V` for each face, `boundary_edges(F)` will return the boundary
edges as collections of two indices into `V` for each boundary edge:
```python
>>> bdry_edges = gpy.boundary_edges(F)
>>> print(bdry_edges)
[[1 0]
 [0 3]
 [2 1]
 [5 2]
 [3 6]
 [8 5]
 [6 7]
 [7 8]]
```

Each row of `bdry_edges` is an edge, a straight line from `V[bdry_edges[i,0],:]`
to `V[bdry_edges[i,1],:]`.
Together, all the rows of `bdry_edges` are the boundary edges of `F`.

With Gpytoolbox's `boundary_vertices` function we can compute the list of
boundary vertices as indices into the vertex list `V`:
```python
bdry_vertices = gpy.boundary_vertices(F)
>>> print(bdry_vertices)
[0 1 2 3 5 6 7 8]
```

As we can see, the boundary vertices are all the vertices with the exception of
`4`, the vertex in the middle of the square.


## Exercises

If you are learning geometry processing, try writing the following function:
* `my_boundary_edges`, which matches the behavior of Gpytoolbox's
`boundary_edges` function.

If you already know geometry processing well and are familiar with the concept
of boundaries of triangle meshes (or have already completed above exercise),
try writing the following functions which tests your mastery of the boundary
command:
* `boundary_triangles`, which takes a triangle mesh as input, and returns a list
of all boundary trianges.
* `boundary_length`, which takes a triangle mesh as input, and returns the
length of the boundary (the combined length of all triangle edges).
You can use the function `normrow` that, when input a matrix, returns a vector
with the norms of each row of the matrix.
You can use the `sum` function that sums all elements of a vector.
HINT: the length of an edge is equal to `norm(edgeEnd - edgeStart)`.

As usual, the skeleton for these functions, ready for you to fill in, can be
found in `exercise/`.
Test your functions on `data/goathead.obj` and `data/mountain.obj`.


[^1]: The situation is a little bit more complicated for points on triangle
corners, which is why they are ignored here.
