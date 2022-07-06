# Minimize Quadratic Energy with Fixed Values

This function `min_quad_with_fixed` stands for minimizing quadratic energy with constant constraints on some of the variables. Specifically, this function solves the optimization problem of this form
```svg
minimize_z  z’ * A * z + z’ * b + c
subject to  z(known) = d;
```
where `A` is a n-by-n symmetric matrix, `b` is an n-dimensional vector, `known` is a k-dimensional integer vector containing indices to the constraints variables, and `d` is another k-dimensional vector of constrained values. To solve this problem, we can simply type
```MATLAB
x = min_quad_with_fixed(A,b,known,d);
```
to obtain the solution `x`. 

## Reformulation

Under the hood, `min_quad_with_fixed` solves this quadratic program by reformulating the problem in terms of known and unknown variables `z = [x; y]` where `y = z(known)` are the known variables and `x = z(unknown)` are the rest of the free variables. Specifically,
```svg
E(z) = z’ * A * z + z’ * b + c
     = [x;y]' * A * [x;y] + [x;y]' * b + c
     = [x;0]' * A * [x;0] + [x;0]' * A * [0;y] + 
       [0;y]' * A * [x;0] + [0;y]' * A * [0;y] + 
       [x;0]' * b + [0;y]' * b + c
     = [x;0]' * [A(unknown, unknown), 0; 0 0] * [x;0] + [x;0]' * [0 A(unknown, known); 0 0]  * [0;y] + 
       [0;y]' * [0 0; A(known, unknown) 0] * [x;0]    + [0;y]' * [0 0; 0 A(known, known)] * [0;y]    + 
       [x;0]' * [b(unknown); 0] + [0;y]' * [0; b(known)] + c
     = x' * A(unknown, unknown) * x + x' * A(unknown, known) * y + 
       y' * A(known, unknown) * x + y' * A(known, known) * y + 
       x' * b(unknown) + y' * b(known) + c
     = x' * A(unknown, unknown) * x + x' * A(unknown, known) * y + 
       x' * A(unknown, known) * y + y' * A(known, known) * y + 
       x' * b(unknown) + y' * b(known) + c
     = x' * A(unknown, unknown) * x +
       x' * (A(unknown, known) * y + A(known, unknown)' * y + b(unknown)) +
       y' * A(known, known) * y + y' * b(known) + c
```
Therefore, we can group these terms and re-write the original energy `E(z)` using only the unknown variables as
```svg
E(x) = x' * Anew * x + x’ * bnew + cnew

where
  Anew = A(unknown, unknown)
  bnew = A(unknown, known) * y + A(known, unknown)' * y + b(unknown)
  cnew = y' * A(known, known) * y + y' * b(known) + c
```
Then minimizing this new quadratic energy `E(x)` without any constraint and be easily achieved via a single linear solve. To be more precise, we can obtain the optimal value by setting its derivative to zero as
```svg
dE(x)/dx = 2 * Anew * x + bnew = 0 
=> 2 * Anew * x = -bnew
```
This will result in a linear system with left-hand-side `2*Anew` and right-hand-side `-bnew`.

## Pre-factorization
When having many quadratic programs with the same `A, known` but potentially different `b, d` to solve, we can leverage matrix factorization (or matrix decomposition) techniques to accelerate computation as `min_quad_with_fixed` boils down to solving a single linear system.

The usage of pre-factorization is actually very simple. Instead of calling `x = min_quad_with_fixed(A,b,known,d)` directly, we will first initialize the pre-factorization variable `preF` as an empty list and then pass it into `min_quad_with_fixed` as both the input and output:
```MATLAB
% initialize the pre-factorization
>> preF = [];
>> [x1, preF] = min_quad_with_fixed(A,b1,known,d1,[],[],preF); % original speed
```
Notice that after this call the variable `preF` now contains all information necessary to solve a pre-factored system. Later when different `b2, d2` are passed in, we can reuse `preF` by doing

```MATLAB
% reuse the prefactorization 
>> [x2, preF] = min_quad_with_fixed(A,b2,known,d2,[],[],preF); % much faster
```

One thing to keep in mind is that for the first time we solve the problem with `b1, d1`, the solve time remains the same as the vanilla version of `min_quad_with_fixed`. But for the second time we solve the system with `b2, d2`, this function will reuse the precomputed  information and significantly accelerate the computation. In graphics this is extremely useful for problems like shape deformation where users may want to interactively change the handle positions when posing the shape.

## Additional comments
In addition to fixed-value constraints (Dirichlet boundary conditions), this `min_quad_with_fixed` supports minimizing unconstrained quadratic energies `x = min_quad_with_fixed(A,b)` which is equivalent to solve a linear system `x = (2*A) \ -b`. It also supports general equality constraints 
```svg
minimize_z  z’ * A * z + z’ * b + c
subject to  z(known) = d;
            Aeq * z = beq
```
which corresponds to 
```MATLAB
x = min_quad_with_fixed(A,b,known,d,Aeq,beq);
```
