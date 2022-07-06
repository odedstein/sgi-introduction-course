# Skinning

![beast-weights](assets/beast-weights.gif)
(_image source: Alec Jacobson_)

Hello everyone, are you ready to implement (perhaps) the most widely used technique in industries for shape deformation!!!? This method is called **linear blend skinning**. In practice, given a 3D character, artists often build a set of handles (e.g., skeletons) in order to control the character. This way of controlling a digital character is called _rigging_. Rigging is so important that you can even find a job as a professional _3D Rigger_. Linear blend skinning is the backbone of rigging, it studies how to transfer the handle movement back to deforming the 3D character. 

In this exercise, we are going to implement a handle-based linear blend skinning in 2D. Roughly speaking, linear blend skinning expresses the output deformed vertex locations as a linear combination of input vertex locations, which can be written as

<p align="center"><img src="svgs/f652802a0a634b865dbe26989ca02b38.svg?invert_in_darkmode" align=middle width=145.94435625pt height=50.947635749999996pt/></p>

where 
- <img src="svgs/194516c014804d683d1ab5a74f8c5647.svg?invert_in_darkmode" align=middle width=14.061172949999989pt height=14.15524440000002pt/> is the deformed location of vertex <img src="svgs/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode" align=middle width=5.663225699999989pt height=21.68300969999999pt/>, 
- <img src="svgs/9f7365802167fff585175c1750674d42.svg?invert_in_darkmode" align=middle width=12.61896569999999pt height=14.15524440000002pt/> is the location of the input vertex <img src="svgs/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode" align=middle width=5.663225699999989pt height=21.68300969999999pt/>, 
- <img src="svgs/64e70e84545b2941bed8aa7fe2211cde.svg?invert_in_darkmode" align=middle width=22.523917349999987pt height=14.15524440000002pt/> is a scalar of the skinning weight, and 
- <img src="svgs/6700c5860aa69a6e385a063c4000f436.svg?invert_in_darkmode" align=middle width=15.710696099999991pt height=22.465723500000017pt/> is a 2-by-3 transformation matrix for handle <img src="svgs/36b5afebdba34564d884d347484ac0c7.svg?invert_in_darkmode" align=middle width=7.710416999999989pt height=21.68300969999999pt/> (2-by-3 is because we are implementing a 2D version).

To implement this, we require to (1) compute skinning weights <img src="svgs/64e70e84545b2941bed8aa7fe2211cde.svg?invert_in_darkmode" align=middle width=22.523917349999987pt height=14.15524440000002pt/> for each pair between the vertex and the handle, and (2) the linear blend skinning formula mentioned above. Specifically, we already provide a skeleton code so that you only need to complete 1 mathematical derivation and 2 coding tasks.

## Task 1: Solve a quadratic program
In this task, you are going to manually derive how to solve this optimization problem 
```svg
minimize    u’ * Q * u
subject to  u(b) = bc
```
where `u, b, bc` are vectors and `Q` is a symmetric matrix. Deriving the optimal value of `u` is very similar to how you find the optimal <img src="svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.39498779999999pt height=14.15524440000002pt/> of a quadratic function <img src="svgs/85b40b52737dc2911dc23543fac9b1c7.svg?invert_in_darkmode" align=middle width=89.20457369999998pt height=26.76175259999998pt/>. (Hint: in this derivation, you might need to split `u` into knowns and unknowns).

You may wonder why we would like you to derive the solution of this quadratic program, right? One reason is that we can solve problems of this type reliably and efficiently (you will know why after your derivation). Thus, many researchers formulated their problems (e.g., shape deformation, parameterization, smoothing, etc.) as quadratic programs. So after you go through this exercise, you would be able to understand (and even derive) many of those beautiful algorithms.

## Task 2: implement the solver in Task 1
In this part, you will code up a solver (`computing_skinning_weights.m`) based on the derivation in Task 1 for computing skinning weights <img src="svgs/64e70e84545b2941bed8aa7fe2211cde.svg?invert_in_darkmode" align=middle width=22.523917349999987pt height=14.15524440000002pt/>, where <img src="svgs/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode" align=middle width=5.663225699999989pt height=21.68300969999999pt/> is the index to a vertex and <img src="svgs/36b5afebdba34564d884d347484ac0c7.svg?invert_in_darkmode" align=middle width=7.710416999999989pt height=21.68300969999999pt/> is the index to a handle. We can collect all the entries <img src="svgs/9bb289e84da9f97f31780a5c55f1608e.svg?invert_in_darkmode" align=middle width=39.78420929999999pt height=24.65753399999998pt/> and assemble them into a matrix <img src="svgs/84c95f91a742c9ceb460a83f9b5090bf.svg?invert_in_darkmode" align=middle width=17.80826024999999pt height=22.465723500000017pt/> of size #vertices by #handles such that `w_ij = W(i,j)`.

The method we want to implement here is called **biharmonic weights**. This can be computed by solving the following optimization problem for each handle `b(j)`
```svg
minimize    W(:,j)' * Q * W(:,j)
subject to  W(b,j) = bc(:,j)
```
where 
- `Q` is a #vertices by #vertices matrix of the _BiLaplacian_ operator, 
- `b` is a vector containing all the handle indices, and 
- `bc` is a #handles by #handles matrix of the constraints on the skinning weights. 

The goal is to solve for a vector of weights `W(:,j)` associate to each handle `b(j)`. As we want the weights to be 1 on the handle `W(b(j),j) = 1` and 0 on the other handles. This gives us the constraints that `bc(:,j) = [0, ..., 0, 1, 0, ... ,0]`, where the 1 lies at the location `bc(j,j) = 1`. Then, we can follow the derivation in Task 1 to solve for `W(:,j)` for each handle `b(j)` as
```MATLAB
for j = 1:length(b)
  W(:,j) = ...; % results of Task 1
end
```

In the above optimization problem, the BiLaplacian `Q` is the square of the Laplace operator <img src="svgs/ae8b98841004a386f50d934767483a40.svg?invert_in_darkmode" align=middle width=20.25121889999999pt height=26.76175259999998pt/>. Practically, if we want to implement this BiLaplacian, one way is to use the _mixed finite element methods_ which will result in the following formula
```svg
Q = L * inv(M) * L
```
where `M` is the lumped mass matrix and `L` is the cotangent matrix. If your memory on `M, L` has faded, please visit `013_laplacian` for more details. You may wonder where does this formula come from or why is this a good choice, right? A very detailed answer is provided in this [write-up](http://odedstein.com/projects/sgp-2021-lap-bilap-course/sgp-2021-lap-bilap-course.pdf) by another of our lecturers [Oded Stein](http://odedstein.com). (Hint: inverting the lumped mass matrix `inv(M)` should be trivial and efficient, but how?)


After your implementation, you should see resulting weights (right) of each handle (left, yellow dots) like this
![biharmonicW](assets/biharmonicW.jpg)

**Optional Challenge**
The above solution involves looping over all the handle indices one-by-one `b(j)`. But actually, you don't need to do that. The solution of Task 2 is equivalent to the solution the following problem
```svg
minimize    trace( W' * Q * W )
subject to  W(:,b) = bc
```
So an optional challenge is how can you derive the optimal solution to this problem and then solve this directly, without the need of looping over all the `b(j)` one-by-one?

**Limitations**
The above implementation still need one addition modification. Would you like to guess what is that based on your experience playing with the tool? 


## Task 3: implement linear blend skinning
In this exercise, you are going to implement a 2D version of the linear blend skinning (`linear_blend_skinning.m`), which is basically an implementation of Equation (1). In the case of 2D, <img src="svgs/194516c014804d683d1ab5a74f8c5647.svg?invert_in_darkmode" align=middle width=14.061172949999989pt height=14.15524440000002pt/> is a column vector of length 2, containing the <img src="svgs/65f1b48fb5f326a680b0f7393b9d8b6d.svg?invert_in_darkmode" align=middle width=18.044213549999988pt height=14.15524440000002pt/> location of the deformed vertex, <img src="svgs/64e70e84545b2941bed8aa7fe2211cde.svg?invert_in_darkmode" align=middle width=22.523917349999987pt height=14.15524440000002pt/> is the weight computed in Task 2, <img src="svgs/6700c5860aa69a6e385a063c4000f436.svg?invert_in_darkmode" align=middle width=15.710696099999991pt height=22.465723500000017pt/> is a 2-by-3 transformation matrix associated to handle <img src="svgs/36b5afebdba34564d884d347484ac0c7.svg?invert_in_darkmode" align=middle width=7.710416999999989pt height=21.68300969999999pt/>, and <img src="svgs/9f7365802167fff585175c1750674d42.svg?invert_in_darkmode" align=middle width=12.61896569999999pt height=14.15524440000002pt/> is a column vector of **length 3** (`vi_x, vi_y, 1`) because we represent the input vertex in the [homogeneous coordinates](https://en.wikipedia.org/wiki/Homogeneous_coordinates).
<p align="center"><img src="svgs/f782dffa13ae7532661c49a20f46066b.svg?invert_in_darkmode" align=middle width=307.5142059pt height=59.1786591pt/></p>

**Optional Challenge**
Simply implementing linear blend skinning using Equation (1) is fine, but this will result in a slower runtime in MATLAB. This is because a direct implementation of that involves double for loops (one for the vertices, one for the handles). A rule of thumb in MATLAB programming is to avoid for/while loops as many as possible. And, actually, we can implement a (faster) linear blend skinning without any loops at all, but with only matrix multiplications. Specifically, 
<p align="center"><img src="svgs/2110a26e0908af1aa4f3b579a0ed85d0.svg?invert_in_darkmode" align=middle width=59.151679949999995pt height=11.232861749999998pt/></p>
where <img src="svgs/6bac6ec50c01592407695ef84f457232.svg?invert_in_darkmode" align=middle width=13.01596064999999pt height=22.465723500000017pt/> her is a 2-by-#vertices matrix (since we are working on 2D) of deformed vertex locations (_warning: the dimension of <img src="svgs/6bac6ec50c01592407695ef84f457232.svg?invert_in_darkmode" align=middle width=13.01596064999999pt height=22.465723500000017pt/> in the implementation may require a transpose_), <img src="svgs/2f118ee06d05f3c2d98361d9c30e38ce.svg?invert_in_darkmode" align=middle width=11.889314249999991pt height=22.465723500000017pt/> is a 2-by-3x#handles matrix which concatenate all the <img src="svgs/6700c5860aa69a6e385a063c4000f436.svg?invert_in_darkmode" align=middle width=15.710696099999991pt height=22.465723500000017pt/> as different columns `T = [T1, T2, ...]`, and the <img src="svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879834999999pt height=22.465723500000017pt/> is a matrix of size 3x#handles-by-#vertices that represents <img src="svgs/3772fcee64a3507eb0b3ace1e8f2411e.svg?invert_in_darkmode" align=middle width=35.96475629999999pt height=14.15524440000002pt/>. Specifically, the structure of <img src="svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879834999999pt height=22.465723500000017pt/> looks like
<p align="center"><img src="svgs/c249f3b0d2b6ea004caeb1872f253e93.svg?invert_in_darkmode" align=middle width=205.2037053pt height=147.9466857pt/></p>
This formula in Equation (2) is just the result of expanding and reorganizing Equation (1). But this reformulation can turn it into a single matrix multiplication. Furthermore, if you are interested in making it even faster, you can pre-compute the matrix <img src="svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879834999999pt height=22.465723500000017pt/> (because it only depends on the weights and the input shape) and reuse it whenever the user specify a different handle transformations <img src="svgs/2f118ee06d05f3c2d98361d9c30e38ce.svg?invert_in_darkmode" align=middle width=11.889314249999991pt height=22.465723500000017pt/>.


## For Fun
After you finish implementing the above tasks, you now have your first 2D shape deformer!!! Instead of using our default `woody.obj` mesh, you can now follow the instructions in `201_polylines` to use the `get_pencil_curves.m` function to draw your favorite 2D shapes, follow the instructions in `202_wrappers` to triangulate the mesh using the function `triangle.m`, and then you can pass your 2D shape into your implemented shape deformer to create an animation of your drawings. PLEASE share your results with us, we are super super interested in knowing what you have created!