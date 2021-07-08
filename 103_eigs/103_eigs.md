# Eigendecomposition in MATLAB

It is fascinating to use MATLAB for reliable and efficient eigendecomposition. Eigendecomposition is a fundamental operation in linear algebra and has many applications in geometry processing and beyond. Given a square n-by-n matrix <img src="svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879834999999pt height=22.465723500000017pt/>, eigendecomposition aims at finding a non-zero vector <img src="svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.39498779999999pt height=14.15524440000002pt/> such that it satisfies <img src="svgs/4cc103f3eeb0d48b1c4d816d4ca52803.svg?invert_in_darkmode" align=middle width=62.62548764999999pt height=22.831056599999986pt/> where <img src="svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.39498779999999pt height=14.15524440000002pt/> is called an _eigenvector_ with unit length and <img src="svgs/fd8be73b54f5436a5cd2e73ba9b6bfa9.svg?invert_in_darkmode" align=middle width=9.58908224999999pt height=22.831056599999986pt/> is its corresponding _eigenvalue_. A geometric interpretation is that <img src="svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.39498779999999pt height=14.15524440000002pt/> is a special vector such that when you multiply the matrix <img src="svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879834999999pt height=22.465723500000017pt/> by this vector <img src="svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.39498779999999pt height=14.15524440000002pt/>, you preserve the direction of <img src="svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.39498779999999pt height=14.15524440000002pt/> and get a scaled version <img src="svgs/923b800cc40cebb92c8eb318ba81bc0d.svg?invert_in_darkmode" align=middle width=18.98407169999999pt height=22.831056599999986pt/> of the vector. 

![eigenvector](assets/eigenvector.jpg)

The eigenvector and the eigenvalue have tremendous implications (e.g., the convergence of iterative solvers, frequencies of vibration modes) and applications. They are impossible to cover within this short document. We encourage interested readers to other textbooks for a dedicated introduction. 



## eig & eigs

In MATLAB, there are two functions for doing eigendecomposition: `eig` for dense matrices and `eigs` for sparse matrices. In the following examples, we will be mainly using `eigs` because most matrices we encountered in geometry processing are sparse matrices. Figuring out its corresponding version for dense matrices using `eig` should be trivial. 

To obtain solutions to the eigenvalue problem <img src="svgs/4cc103f3eeb0d48b1c4d816d4ca52803.svg?invert_in_darkmode" align=middle width=62.62548764999999pt height=22.831056599999986pt/>, we can simply type
```MATLAB
>> k = 5;
>> [X, D] = eigs(A, k);
```
where <img src="svgs/63bb9849783d01d91403bc9a5fea12a2.svg?invert_in_darkmode" align=middle width=9.075367949999992pt height=22.831056599999986pt/> is the number of eigenvalues/eigenvectors we would like to compute, each column of <img src="svgs/cbfb1b2a33b28eab8a3e59464768e810.svg?invert_in_darkmode" align=middle width=14.908688849999992pt height=22.465723500000017pt/> is an eigenvector `x = X(:,index)`, <img src="svgs/78ec2b7008296ce0561cf83393cb746d.svg?invert_in_darkmode" align=middle width=14.06623184999999pt height=22.465723500000017pt/> is a diagonal matrix of eigenvalues `λ = D(index,index)`. 

This `eigs` also supports the generalized eigenvalue problem of the form <img src="svgs/25b7866d6e5acb46caf48823e3b77436.svg?invert_in_darkmode" align=middle width=70.77612134999998pt height=22.465723500000017pt/> and we can simply solve it with 
```MATLAB
>> [X, D] = eigs(A, M, k);
```

By default, `eigs` outputs the first <img src="svgs/63bb9849783d01d91403bc9a5fea12a2.svg?invert_in_darkmode" align=middle width=9.075367949999992pt height=22.831056599999986pt/> eigenvalues with the largest magnitude (and their eigenvectors). But if you are interested in sorting from the ones with the smallest eigenvalues, you can use
```MATLAB
[X, D] = eigs(A, M, k, 'sm'); 
```
to obtain eigenpairs with the smallest eigenvalues. In a lot of geometry processing, sorting from the smallest eigenvalues is used more often, such as computing Laplacian bases 

![spectralBases](assets/spectralBases.jpg)

