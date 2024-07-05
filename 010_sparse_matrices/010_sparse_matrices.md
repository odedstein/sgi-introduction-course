# Sparse matrices
In this exercise we will learn what sparse matrices are, and how to construct
them with NumPy / SciPy.
Sparse matrices are an important tool for many linear algebra applications, and
are used by many different geometry processing methods.


## Dense matrices

All matrices that we have used so far in NumPy, created with the `np.array`
function have been _dense_ matrices.
What this means is that the computer stores every single value of the matrix:
for a matrix with `n` rows and `m` columns this means that a storage capacity
of `n*m` is required.
This seems reasonable, and also the only way to store a matrix like `A`.
After all, every entry has a different value, so we need to store every entry.

But what about when the matrix contains entries that are mostly the same, with only
a few one different?
For such matrices it does not make sense to store every single value in memory.
For very large matrix systems, it can even be impossible to store everything in
memory.
For a linear system `A@x = b`, `x` has `n` rows and `A` has `n^2` elements.
Since `n^2` grows much faster than `n`, it can be impossible to fit `A` into
memory if `n` is large.


## Sparse matrices

The solution to the storage problem of matrices is to use _sparse_ matrices.
If most of the entries of a matrix have one value, we can store only the values
that are different from that value.
Without loss of generality, let's pick `0` as the value of most entries.
This is true in practice for many applications, and if it is not, then it is
easy to just add a constant matrix.

There are many ways to store all nonzero values.
One could store the row and column information for all nonzero values like so:
```
(row1, col1, val1)
(row2, col2, val2)
...

(rowk, colk, valk)

```
This format is called
[coordinate list](https://en.wikipedia.org/wiki/Sparse_matrix#Coordinate_list_(COO)).
It is not the format used by Python internally, but it is important, as it is
very easy to construct sparse matrices from this format, and Python displays
sparse matrices as a coordinate list when prompted.

A more popular format is the
[compressed sparse row format](https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format)).
In this format one stores, for each row, the number of nonzero entries,
the column for the nonzero entries in each row, and a pointer into a large
vector of values for each nonzero entries.
This format is particularly beneficial for a variety of linear algebra
algorithms.

It is, in most cases, not important to know which sparse matrix format is used
by your application.
Your linear algebra library should correctly handle all sparse matrix
operations.
Asymptotically, all sparse matrix formats are similar:
their most important property is the fact that they only store the nonzero
matrix entries.

How can we construct sparse matrices in Python?
We will use SciPy's sparse matrix library for this.
Import SciPy into your Python environment now:
```python
>>> import scipy as sp
```

The easiest way to get a sparse matrix is taking a dense matrix and transforming
it into a sparse matrix using the `csr_matrix` command:
```python
>>> A = np.array([[0,0,1],[0,1,0],[0,2,-1]])
>>> print(A)
[[ 0  0  1]
 [ 0  1  0]
 [ 0  2 -1]]
>>> As = sp.sparse.csr_matrix(A)
>>> print(As)
  (0, 2) 1
  (1, 1) 1
  (2, 1) 2
  (2, 2) -1
```

This method is however not practical for constructing large matrices, since it
requires us to construct a dense matrix first, which is exactly what we are
trying to avoid.
To construct a general sparse matrix, we also use the `csr_matrix` command, but
with the syntax `csr_matriy((values, (rows,cols)), shape=(m,n))`.
We provide the `sparse` command with triples in the coordinate list format:
the first value of the triple (which row) in the `rows` vector, the second
value of the triple (which column) in the `cols` vector, and the third
value of the triple (which matrix entry value) in the `values` vector.
`m` and `n` specify the number of rows and columns in the sparse matrix,
respectively.
```python
>>> rows = np.array([0,1,1,2])
>>> cols = np.array([0,1,2,2])
>>> values = np.array([1., -1., -2., 1.])
>>> As = sp.sparse.csr_matrix((values, (rows,cols)), shape=(3,3))
>>> print(As)
  (0, 0) 1.0
  (1, 1) -1.0
  (1, 2) -2.0
  (2, 2) 1.0
```

This method allows us to construct arbitrarily large sparse matrices by only
enumerating nonzero elements, and is the most general way to construct a
sparse matrix in Python.

There are two more specialized ways to construct sparse matrices in MATLAB:
identity matrices and diagonal/banded matrices.
We have already dealt with dense identity matrices.
A sparse identity matrix is the same thing:
a matrix with ones on the diagonal, and zeros elsewhere.
It is constructed in SciPy via the command `sparse.eye`:
```python
>>> I = sp.sparse.eye(4, 4, format='csr')
>>> print(I)
  (0, 0) 1.0
  (1, 1) 1.0
  (2, 2) 1.0
  (3, 3) 1.0
```
With `sparse.eye` we can immediately visualize the advantage of sparse matrices.
While it is impossible to construct giant dense identity matrices, it is quick
and easy to do so for giant sparse identity matrices:
```python
>>> n = 10000000
>>> np.eye(n,n)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/gp/lib/python3.9/site-packages/numpy/lib/twodim_base.py", line 211, in eye
    m = zeros((N, M), dtype=dtype, order=order)
numpy.core._exceptions.MemoryError: Unable to allocate 728. TiB for an array with shape (10000000, 10000000) and data type float64
>>> sp.sparse.eye(n,n, format='csr')
<10000000x10000000 sparse matrix of type '<class 'numpy.float64'>'
   with 10000000 stored elements in Compressed Sparse Row format>
(no error)
```

A diagonal matrix is a matrix that has arbitrary values on the diagonal, but
zeroes elsewhere.
It is constructed via the command
`sparse.diags(v, 0, shape=(rows,cols), format='csr')`,
where the diagonal values are supplied in the vector `v`.
```python
>>> v = np.array([1,2,3,4,5,6])
>>> A = sp.sparse.diags(v, 0, shape=(6,6), format='csr')
>>> print(A)
  (0, 0) 1
  (1, 1) 2
  (2, 2) 3
  (3, 3) 4
  (4, 4) 5
  (5, 5) 6
```

The concept of a diagonal matrix extends to the concept of banded matrices.
Banded matrices are zero, except for the diagonal and a number of off-diagonal
diagonals.
The central diagonal has index `0`, and other diagonals are referenced
by their positive or negative distance from the central diagonal.
`sparse.diags` can construct banded matrices via the command
`sparse.diags(v, diagonals, rows, cols)`, where `v` contains the diagonal values,
and `diagonals` contains the diagonal index for each column in `v`.
```python
>>> n = 6
>>> v1 = np.ones(n)
>>> v2 = -2. * np.ones(n)
>>> v = np.stack((v2, v1, v2))
>>> L = sp.sparse.diags(v, [-1, 0, 1], shape=(n,n), format='csr')
>>> print(L)
  (0, 0) 1.0
  (0, 1) -2.0
  (1, 0) -2.0
  (1, 1) 1.0
  (1, 2) -2.0
  (2, 1) -2.0
  (2, 2) 1.0
  (2, 3) -2.0
  (3, 2) -2.0
  (3, 3) 1.0
  (3, 4) -2.0
  (4, 3) -2.0
  (4, 4) 1.0
  (4, 5) -2.0
  (5, 4) -2.0
  (5, 5) 1.0
```

If you quickly want to inspect the _sparsity pattern_ of a matrix, i.e., look at
where exactly its zero and where its nonzero entries are, you can use the
library matplotlib.
You install it via your command line:
```console
python -m pip install matplotlib
```

Once you have done that, import matplotlib and its pyplot library into Python:
```python
>>> import matplotlib
>>> from matplotlib import pyplot
```

Matploblib's function `pyplot.spy` allows you to quickly look at the
sparsity pattern of a matrix.
The visualization shows where the matrix contains nonzero elements.
This can be very useful for debugging your sparse matrix construction
algorithm.
Here's what the identity matrix and the banded matrix look like:
```python
>>> n = 100
>>> matplotlib.pyplot.spy(sp.sparse.eye(n,n, format='csr'))
>>> matplotlib.pyplot.show()
>>> v1 = np.ones(n)
>>> v2 = -2. * np.ones(n)
>>> v = np.stack((v2, v1, v2))
>>> L = sp.sparse.diags(v, [-10, 0, 10], shape=(n,n), format='csr')
>>> matplotlib.pyplot.spy(L)
>>> matplotlib.pyplot.show()
```

![sparsity pattern of identity matrix](assets/identity-sparsity-pattern.png)
![sparsity pattern of banded matrix](assets/banded-sparsity-pattern.png)

_NOTE: Arithmetic of sparse matrices works almost exactly the same as with dense
matrices, but with one crucial difference: `*` and `/` are no longer elementwise
operators.
Instead, `*` does a matrix multiplication (like `@` does for normal dense
matrices)._


## Sparse linear systems

One of the important things we can do with sparse matrices is solving sparse
linear systems, `A*x=b`.
There are specialized algorithm for the solution of sparse linear systems that
are more efficient than the usual dense algorithm.
In SciPy, this is done with the function `sp.linalg.sparse.spsolve`:
```python
>>> i = np.array([0,1,1,2])
>>> j = np.array([0,1,2,2])
>>> k = np.array([1., -1., -2., 1.])
>>> A = sp.sparse.csr_matrix((k, (i,j)), shape=(3,3))
>>> b = np.array([-1., 2., 1.])
>>> print(f"inv(A)*b = {sp.sparse.linalg.spsolve(A,b)}")
inv(A)*b = [-1. -4.  1.]
```

For some algorithms, solving a linear system involves two steps:
* decomposition; and
* solution.

Decomposition involves only the matrix `A` and not the right-hand side `b`.
Decomposition is also more expensive than just the solution step.
Thus, if we have to solve two linear systems, `A*x=b` and `A*x=c`, we can
save time by only performing the decomposition step once.
This two-step process in SciPy can be done with the `splu` command:
```python
>>> precomp = sp.sparse.linalg.splu(A)
>>> b = np.array([-1., 2., 1.])
>>> print(f"inv(A)*b = {precomp.solve(b)}")
inv(A)*b = [-1. -4.  1.]
>>> c = np.array([3., 1., -1.])
>>> print(f"inv(A)*c = {precomp.solve(c)}")
inv(A)*c = [ 3.  1. -1.]
>>> d = np.array([1., 1., -2.])
>>> print(f"inv(A)*d = {precomp.solve(d)}")
inv(A)*d = [ 1.  3. -2.]
```

## Exercises

Try writing the following functions which tests your mastery of sparse matrices:
* `four_corners`, which constructs a `m x n` sparse matrix with ones in all
of its four corners.
* `my_diags`, which mimics the behavior of SciPy's `sp.diags` and allows the
construction of banded matrices.
* `triangles_matrix`, which constructs a sparse matrix with a triangular
nonzero pattern.
_HINT: Look up the NumPy function `concatenate`!_

As usual, the skeleton for these functions, ready for you to fill in, can be
found in `exercise/`.
