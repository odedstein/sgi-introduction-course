# Normals

In this exercise we will learn what surface normals are, and how to compute
per-face and per-vertex normals in gptoolbox.


## Perpendicular and normal

Two vectors `[x1, y1, z1]` and `[x2, y2, z2]` are perpendicular to each other
(also called _orthogonal_) if
their dot product (or scalar product) is equal to zero:
`[x1, y1, z1]' * [x2, y2, z2] == x1*x2 + y1*y2 + z1*z2 == 0`.

These two vectors are perpendicular:

![two perpendicular vectors](assets/perp_vectors.png)

These two vectors are not perpendicular:

![two not perpendicular vectors](assets/not_perp_vectors.png)


A vector's norm is the square root of its scalar product with itself:
`norm([x y z]) == sqrt(x*x + y*y + z*z)`.
It is computed in Numpy using the `np.linalg.norm` function.
A vector with norm one is also called a _unit vector_.

A vector can be normalized (which means, converted into a parallel vector
of unit norm), unless it has zero length, via the operation
```python
>>> x = x / np.linalg.norm(x)
```

For a collection of vectors in a matrix, where each row of the matrix
corresponds to a vector, one can use the `axis` argument to compute the norm of
each row in parallel:
```python
>>> np.linalg.norm(X, axis=-1)
```

To divide every row of `X` by its norm, we broadcast the result of the norm
computation over the columns of the matrix `X` by adding `NONE` to the computed
result like this:
```python
>>> np.linalg.norm(X, axis=-1)[:,None]
```

So, here is  how to normalize the rows of a matrix X:
```python
>>> X = X / np.linalg.norm(X, axis=-1)[:,None]
```

It is possible to project any vector `u1 = [x1, y1, z1]` onto the
_orthogonal complement_ of a second vector `u2 = [x2, y2, z2]` in order to obtain
two perpendicular vectors by performing an orthogonal projection
`u1 - (u1'*u2)*u2/(u2'*u2)`.
We compute the dot product of two vectors with NumPy's `dot` function:
:
```python
>>> rng = np.random.default_rng(1434251)
>>> u1 = rng.random(3)
>>> print(u1)
[0.13367219 0.53070176 0.91193361]
>>> u2 = rng.random(3)
>>> print(u2)
[0.82107301 0.62538083 0.81860006]
>>> print(u1.dot(u2))
1.1881542412563915
>>> u1 = u1 - np.dot(u1,u2)*u2 / np.dot(u2,u2)
>>> print(u1)
[-0.42849175  0.10252236  0.35146283]
>>> print(np.dot(u1,u2))
-1.5158949498870973e-16
```

The resulting projected vector, in this case `u1`, is guaranteed to be the closest vector to to the
original `u1` that is orthogonal to `u2` with respect to the norm.

_NOTE: The functions `random.default_rng` and `random` are a way to reproducibly
create random numbers in NumPy.
I encourage you read the NumPy documentation on random number generation for
more information!_

Given non-parallel vectors `u1`, `u2` (which means two vectors that are not
simply rescalings of each other), we can construct a third vector that is
orthogonal to both `u1` and `u2` using the
[cross product](https://en.wikipedia.org/wiki/Cross_product)
`cross(u1, u2) == [u1(2)*u2(3) - u1(3)*u2(2), u1(3)*u2(1) - u1(1)*u2(3), u1(1)*u2(2) - u1(2)*u2(1)]`.
In NumPy, this is implemented with the `cross` function:
```python
>>> u3 = np.cross(u1,u2)
>>> print(u3)
[-0.1358733   0.63934001 -0.35214887]
>>> print(np.dot(u1,u3))
1.6691322969430801e-18
>>> print(np.dot(u2,u3))
1.981756080074304e-17
```

If you plug matrices `U1`, `U2`, where each row is a 3D-vector into `cross`,
then the function will return a matrix where each row is the cross product
of the corresponding two rows in `U1` and `U2` as long as you correctly use
the `axis` argument.

The cross product has many interesting mathematical properties.
We will highlight two important ones here:
* The norm of the cross product vector `cross(u1,u2)` is equal to twice the area
of the triangle whose edges are `u1`, `u2`.
* The cross product is _antisymmetric_, i.e., `cross(u1,u2) == -cross(u2,u1)`.
This means the cross product is oriented, and can be used to tell which side
is _up_ and which side is _down_.
If `u1` points in the direction of the x-axis, and `u2` points in the
direction of the y-axis, then `cross(u1,u2)` will point _up_ in the direction of
the z-axis
(more on that in the next section).


## Per-face normals

Each triangle of a mesh has a _normal vector_: the oriented unit vector that is
perpendicular to the triangle itself (i.e., to each triangle edge).
* The normal vector `n` is perpendicular, which means that for each edge `e`
in the triangle, `n' * e == 0`.
* The normal vector `n` is a unit vector, which means that `norm(n) == 1`.
* The normal vector `n` is oriented so that it points _up_ of the triangle.

The orientation of the normal vector means that, for any two _consecutive_ edges
`e1`, `e2` in the triangle, the normal vector can be computed using
```python
>>> n = np.cross(e1, e2);
>>> n = n / np.linalg.norm(n);
```
The two edges `e1`, `e2` have to be two consecutive edges of the triangle.
The convention is that the triangle edges are visited in a counterclockwise
direction, looking down onto the triangle from above.
If a normal points in the wrong direction, it is called a _flipped normal_.

Here is a picture of a triangle and its normal vector:

![a triangle with its normal vector](assets/triangle_with_normal.png)

In Gpytoolbox you can compute the per-face normals of a triangle mesh using
the `per_face_normals` command:
```python
>>> V,F = gpy.read_mesh("data/spot.obj")
>>> N = gpy.per_face_normals(V,F)
```

You can visualize the normals in Polyscope with `add_vector_quantity` (which
works very similar to the `add_scalar_quantity` that you already know):
```python
>>> ps.init()
>>> ps_spot = ps.register_surface_mesh("spot", V, F, smooth_shade=True)
>>> ps_spot.add_vector_quantity("per-face normals", N, defined_on="faces", enabled=True)
>>> ps.show()
```

![spot, with normals](assets/spot_with_normals.png)

If all triangles are consistently oriented so that the _up_ side of each
triangle faces _outside_ of the shape, then all normals will point away from
the shape, as can be seen in above image.
Inconsistent orientation of triangles can easily be detected by looking at the
normals.
Because of that, users will sometimes refere to orientations
that restore triangle orientation as _fixing normals_.


## Per-vertex normals

Smooth surfaces also have normal vectors.
Smooth normal vectors are oriented unit vectors that are perpendicular to a
surface at every point, although the notion of perpendicularity is a bit more
complicated for smooth surfaces (see
[the Wikipedia article](https://en.wikipedia.org/wiki/Tangent_space) for the
definition of a tangent space - smooth normal vectors are perpendicular to the
tangent space of a surface at each point).
Since smooth surfaces have normal vectors at every point, it is natural to want
to compute normal vectors at other parts of our mesh than just at triangle
faces.

For many applications we want _per-vertex normals_, where each vertex of the
mesh is associated with a vector in 3D.
In Gpytoolbox, such a per-vertex normal can be computed with the function
`per_vertex_normals`.
`per_vertex_normals` takes as an input our mesh as a list of vertices `V` and
faces `F`, and returns matrix of normal vectors `N`, where each row of `N`
corresponds to a normalized normal vector at the vertex with the respective
index.

Since at a vertex there are no edges that a vector can be required to be normal
to, there is no unique definition of a per-vertex normal.
There are a variety of definitions that are used in geometry processing.
Here we will look at three definitions that are based on averaging the
per-face normals:

* *Uniform averaging.*
The normal at each vertex is the average of all the normals of faces
that contain the vertex.

* *Angle-weighted averaging*
The normal at each vertex is the average of all the normals of faces containing
the vertex, where each normal is weighted by the _tip angle_, the angle at the
vertex in the normal's face.

* *Area-weighted averaging*
The normal at each vertex is the average of all the normals of faces 
containing the vertex, where each normal
is weighted by the area of the triangle it corresponds to before averaging.
This is the one that Gpytoolbox uses:
```python
>>> N = gpy.per_vertex_normals(V,F)
```

Here is an image of spot with area-weighted per-vertex normals.
If you are not sure which weighting to use, area weighted normals are probably
a reasonable choice.

```python
>>> N = gpy.per_face_normals(V,F)
>>> ps.init()
>>> ps_spot = ps.register_surface_mesh("spot", V, F, smooth_shade=True)
>>> ps_spot.add_vector_quantity("per-vertex normals", N, defined_on='vertices', enabled=True)
>>> ps.show()
```
![spot, with per-vertex normals](assets/spot_with_per_vert_normals.png)



## Exercises

If you are learning geometry processing, try writing the following functions:
* `my_per_face_normals`, which matches the behavior of `Gpytoolbox`'s `per_face_normals` function.
* `my_per_vertex_normals`, which matches the behavior of `Gpytoolbox`'s
`per_vertex_normals` function.
Use Gpytoolbox's `doublearea` function, which returns double the area for each
triangle in the mesh.

If you already know geometry processing well and are familiar with the concept
of normals of (or have already completed above exercise),
try writing the following functions which tests your mastery of normals:
* `flipped_normals`, which returns the flipped normals of a triangle mesh (make sure to set Polyscope to plot only the wireframe of the surface, so you can see inside it and look at the flipped normals!).
* `tangents`, which returns two perpendicular, oriented tangent vectors for each
face of a triangle mesh.
_HINT: Use `np.sum(A*B, axis=-1)` to compute the row-wise dot product of two
matrices._
Olga has kindly provided us with an example of what the tangents should look
like:

![tangents](assets/tangents.png)

As usual, the skeleton for these functions, ready for you to fill in, can be
found in `exercise/`.
Test your functions on `data/spot.obj` and `data/spot_low_resolution.obj`.
