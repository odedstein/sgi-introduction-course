# NumPy for geometry processing

In this part of the tutorial we will install the gptoolbox library and make
sure that it runs correctly.
There are no exercises in this part of the tutorial.

## Testing out NumPy for geometry processing

Now that Python is installed, and all packages are working correctly, let us
boot up Python and do some basic arithmetic!

First, try some basic arithmetic:
```python
>>> 3+5
8
>>> -1+1
0
>>> 1.2 * 0.3
0.36
```

You can assign any value to a variable using the `=` sign, as follows:
```python
>>> a = 1
>>> print(a)
1
```

### Python functions

The main way with which we can abstract code in Python is the _function_.

Functions in Python are created with the syntax `def function_name():`.
Open your working script `myfile.py` (this step is much easier in the working
script than it would be typing line-by-line in the console), and create your
first function:
```python
def function_name(i1,i2):
     sum_of_inputs = i1 + i2
     return sum_of_inputs
```

This function will return the sum of the two input variables.
So, if you write the following working script that calls your function:
```python
def function_name(i1,i2):
     sum_of_inputs = i1 + i2
     return sum_of_inputs

print(function_name(1., 4.))
```

Then you should see the following output in your terminal:
```
5.0
```

You can return multiple variables from your function by separating them with
commas like so:
```python
def function_name(i1,i2):
     sum_of_inputs = i1 + i2
     diff_of_inputs = i1 - i2
     return sum_of_inputs, diff_of_inputs

s,d = function_name(1., 4.)
print(f"My function returned {s} and {d}.")
```

You should see the following output in your terminal:
```
My function returned 5.0 and 5.0.
```

Let's try to create a function that adds two numbers, and then multiplies them
by a third number.
Fill in the skeleton in `exercises/add_then_multiply.py` so that it has one
output variable called `result` and three input variables `a1`, `a2`, `m`.
The function should add the numbers provided in the input variables `a1` and
`a2`, and then multiply the result of that calculation with `m`.
Store the result in `result`.
Finally, document what your new function does by writing it into a
_docstring_ after the function definition:
```python
def function_name(i1,i2):
     """This is the docstring for the function
     """
     return 0.
```

Try out your function!
If you are in the same directory as the file in which the function is defined,
you can import it and then use it like so:
```MATLAB
>>> from add_then_multiply import add_then_multiply
>>> add_then_multiply(2,3,5)
25
```

Alternatively, if you just define the function in the same file as your command,
before you issue the command, it will also work.

You will find the solutions to each exercise in the subfolder `solution/`.


### Vectors and matrices

Python is a great tool for working with vectors and matrices through the
NumPy library.

First, let's import the numpy library into our Python environment.
```python
>> import numpy as np
```

There is a lot of convenient syntax for dealing with vectors and matrices.

You can create a vector using a simple python comma-separated list `[..., ...]`:
```python
>>> vec = np.array([1.,2.,3.])
>>> print(vec)
[1. 2. 3.]
```

NumPy has a variety of convenience functions for creating, for example, vectors
that count from one number to another:
```python
>>> vec = np.arange(2,7)
>>> print(vec)
[2 3 4 5 6]
```

NumPy usually uses C-style indexing and boundary, so ranges will always include
the lower boundary and exclude the upper boundary.

You can create a matrix by specifying entries in row-major format, by putting
the row of each matrix into a bracketed, comma-separated list `[..., ...]`, and
them putting each row into one larger list:
```python
>>> mat = np.array([[1.,2.,3.], [4.,5.,6.], [7.,8.,9.]])
>>> print(mat)
[[1. 2. 3.]
 [4. 5. 6.]
 [7. 8. 9.]]
```

The dimension of an array (a vector or matrix in NumPy) is available in the
array's `shape` property:
```python
>>> vec = np.arange(2,7)
>>> print(vec.shape)
(5,)
>>> print(f"vec is a {vec.shape[0]} vector.")
vec is a 5 vector.
>>> mat = np.array([[1.,2.,3.], [4.,5.,6.], [7.,8.,9.]])
>>> print(mat.shape)
(3, 3)
>>> print(f"mat is a {mat.shape[0]} x {mat.shape[1]} matrix.")
mat is a 3 x 3 matrix.
```

The identity matrix of dimension `d` is constructed using `np.eye(d)`.
```python
>>> mat = np.eye(4)
>>> print(mat)
[[1. 2. 3.]
 [4. 5. 6.]
 [7. 8. 9.]]
```

Using the arithmetic operators `+`, `-`, `*`, `/` and `**` on numpy arrays
(i.e., vectors and matrices), results in elementwise operations.
This is different from MATLAB, where, for example, `*` will perform a matrix
multiplication.
In order to perform an elementwise operation, your operands must be two array
of compatible sizes, or an array and a scalar.
So, the following elementwise operations are legal:
```python
>>> A = np.array([[1., 2.], [3., 4.], [5., 6.]])
>>> np.array([[13., 14.], [15., 16.], [17., 18.]])
>>> print(f"A+B: {A+B}")
A+B: [[14. 16.]
 [18. 20.]
 [22. 24.]]
>>> print(f"B*A: {B*A}")
B*A: [[ 13.  28.]
 [ 45.  64.]
 [ 85. 108.]]
>>> print(f"A-3: {A-3}")
A-3: [[-2. -1.]
 [ 0.  1.]
 [ 2.  3.]]
>>> print(f"1./A: {1./A}")
1./A: [[1.         0.5       ]
 [0.33333333 0.25      ]
 [0.2        0.16666667]]
```

The following elementwise operations are illegal:
```python
>>> A = np.array([[1., 2.], [3., 4.], [5., 6.]])
>>> u = np.array([1., 2., 3., 4.])
>>> B = np.array([[13., 14.], [15., 16.]])
>>> A+u
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: operands could not be broadcast together with shapes (3,2) (4,)
>>> A-B
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: operands could not be broadcast together with shapes (3,2) (2,2)
```

There are a variety of mathematic operations in NumPy that are specific to
matrices.
_Matrix multiplication_ is performed via the `@` operator:
```python
>>> A = np.array([[1., 2.], [3., 4.], [5., 6.]])
>>> u = np.array([7., 8.])
>>> print(f"A@u matrix multiplication: {A@u}")
A@u matrix multiplication: [23. 53. 83.]
```

The _transpose_ of a matrix can be taken with the simple `.T` operator:
```python
>>> A = np.array([[1., 2.], [3., 4.], [5., 6.]])
>>> print(f"Transpose A.T: {A.T}")
Transpose A.T: [[1. 3. 5.]
 [2. 4. 6.]]
```

While matrixes in NumPy can be inverted with `np.linalg.inv`, it is generally
not advisable to do so.
Instead, one can solve the linear equation `A@u == b` with the `np.linalg.solve`
function:
```python
>>> A = np.array([[1., 2.], [3., 4.]])
>>> b = np.array([-2, -3])
>>> print(f"inv(A)@b = {np.linalg.solve(A,b)}")
inv(A)@b = [ 1.  -1.5]
```

The last thing we will cover in this intro is how to access matrix elements.
NumPy uses square bracket access for array elements:
```python

```

MATLAB uses bracket access for vector elements.
Bracket access with the index `i` will select the `i`-th element of a vector.
For a matrix, you must specify rows and columns.
Python uses zero-indexing: the first element of an array has index `0`.
```python
>>> a = np.array([1,2,4])
>>> print(a)
[1 2 4]
>>> a[2]
4
>>> A = np.array([[3,7], [1,2]])
>>> print(A)
[[3 7]
 [1 2]]
>>> print(A[0,1])
7
```

Multiple elements of a vector or matrix can be selected at the same time by
indexing the bracket operator with a Python list, another vector, or a range
selector.
So, just like `[1,2,3,4][-2:]` returns the last two elements of a list, and
`[1,2,3,4][:3]` returns the first three, it works exactly the same on NumPy
arrays:
```python
>>> a = np.array([1,2,3,4])
>>> print(a[-2:])
[3 4]
>>> print(a[:3])
[1 2 3]
```

These are the very basics of vector and matrix operations in NumPy.
There are many more, but this should be enough to get us started!


## if, while, for

We will now quickly go through the basic programming control statements and how
they are implemented in Python.
This section assumes that you already know the programming concepts behind
`if`, `while`, and `for`, and will only quickly explain how to use these.

An `if` block in Python has the form
```python
if CONDITION:
    statement
```
The `if` block executes if the condition is true.
The `CONDITION` is any Python statement that can evaluate into `True` or
`False` (`0`).
You can employ the usual logical operators `and`, `or`, `not`.

A `while` block has the form
```python
while CONDITION:
    statement
```
The `while` block loops until `CONDITION` is false.
It can be exited at any time with the `break` statement.

The `for` block in Python is slightly different than `for` in other languages.
It has the form
```MATLAB
for i in a_list:
    statement
```
where `a_list` is a list (or NumPy array).
The statements inside the block will be run for every element in `a_list`, where
`i` will advance to the next element in `vec` for each iteration of the loop.
```python
>>> for i in [1,2,6]:
...   print(f"i: {i}")
... 
i: 1
i: 2
i: 6
```

_NOTE: In all of these, the indentation it not optional.
Indentation leven in Python signifies where a block starts, unlike in languages
like C and Javascript that have curly brackets._

To get more of the usual for loop experience which loops from `a` to `b`,
inclusively, we can use a `range`.
```python
>>> for i in range(0,6):
...   print(f"i: {i}")
... 
i: 0
i: 1
i: 2
i: 3
i: 4
i: 5
```

## This is where the fun begins!

You have now verified that your Python installation works correctly, and have
learned the most basic elements of the Python programming language.
You are ready to play around a bit.

There are many more Python functions that you will need to actually use
Python for linear algebra.
This tutorial will hint at functions you should use.
Whenever you see a hint, look up the function name using Python's help function,
`help(function_name)`.
The documentation, together with what you have learned in this tutorial, will
help you to use the function `function_name`.

Try writing the following functions:
* `top_left_corner`, which selects the top left corner of each input matrix
* `det2x2`, which computes the determinant of a 2x2 matrix
* `shuffle_by_1`, which shuffles the columns of a matrix to the right by 1.

The skeletons for these functions, ready for you to fill in, can be found in
`exercise/`.



