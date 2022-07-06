# Eigendecomposition in MATLAB

It is fascinating to use MATLAB for reliable and efficient eigendecomposition. Eigendecomposition is a fundamental operation in linear algebra and has many applications in geometry processing and beyond. Given a square n-by-n matrix $A$, eigendecomposition aims at finding a non-zero vector $x$ such that it satisfies $Ax = \lambda x$ where $x$ is called an _eigenvector_ with unit length and $\lambda$ is its corresponding _eigenvalue_. A geometric interpretation is that $x$ is a special vector such that when you multiply the matrix $A$ by this vector $x$, you preserve the direction of $x$ and get a scaled version $\lambda x$ of the vector. 

![eigenvector](assets/eigenvector.jpg)

The eigenvector and the eigenvalue have tremendous implications (e.g., the convergence of iterative solvers, frequencies of vibration modes) and applications. They are impossible to cover within this short document. We encourage interested readers to other textbooks for a dedicated introduction. 



## eig & eigs

In MATLAB, there are two functions for doing eigendecomposition: `eig` for dense matrices and `eigs` for sparse matrices. In the following examples, we will be mainly using `eigs` because most matrices we encountered in geometry processing are sparse matrices. Figuring out its corresponding version for dense matrices using `eig` should be trivial. 

To obtain solutions to the eigenvalue problem $Ax = \lambda x$, we can simply type
```MATLAB
>> k = 5;
>> [X, D] = eigs(A, k);
```
where $k$ is the number of eigenvalues/eigenvectors we would like to compute, each column of $X$ is an eigenvector `x = X(:,index)`, $D$ is a diagonal matrix of eigenvalues `λ = D(index,index)`. 

This `eigs` also supports the generalized eigenvalue problem of the form $Ax = λMx$ and we can simply solve it with 
```MATLAB
>> [X, D] = eigs(A, M, k);
```

By default, `eigs` outputs the first $k$ eigenvalues with the largest magnitude (and their eigenvectors). But if you are interested in sorting from the ones with the smallest eigenvalues, you can use
```MATLAB
[X, D] = eigs(A, M, k, 'sm'); 
```
to obtain eigenpairs with the smallest eigenvalues. In a lot of geometry processing, sorting from the smallest eigenvalues is used more often, such as computing Laplacian bases 

![spectralBases](assets/spectralBases.jpg)

