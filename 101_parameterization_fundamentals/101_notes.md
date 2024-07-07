# Parameterization Fundamentals

Exercise 101 consists of the follow-along Python notebook [101_parameterization_fundamentals.ipynb](101_parameterization_fundamentals.ipynb), in which you will be shown step-by-step how to compute a mesh parameterization through code, analyze the mapping distortion, and visualize the quantities.

You will first compute a trivial parameterization (local basis projection) of a single triangle, then set up the mass-spring system described in the lecture and solve it using NumPy.

Below is the mathematical construction for the matrices that you will be building to solve the system in the notebook. This isn't necessary to know to complete the exercise, but may be useful for those interested in understanding better where the Laplacian matrix arises from in this system.

We start with the spring energy minimization problem.
$$E = \min_{\mathbf{U}} \sum_{\{i,j\} \in \mathbf{E}} w_{ij} ||\mathbf{u}_i - \mathbf{u}_j||^2$$

The energy is convex, which means we can find the global minimum by setting the derivative to zero. $N_i$ refers to all the neighbors of vertex $i$ (all vertices which share an edge with $i$).

$$\frac{\partial E}{\partial \mathbf{u}_i} = \sum_{j \in N_i} 2 * w_{ij}(\mathbf{u}_i - \mathbf{u}_j) = 0$$

Let $B_i \subset N_i$ be the set of all the boundary vertices which are neighbors of $i$ (can be empty). We can now split up the sum between neighbors which are boundary vertices and those which are not.
$$\sum_{j \in N_i} w_{ij}\mathbf{u}_i - \sum_{j \in N_i/B_i} w_{ij}\mathbf{u}_j - \sum_{j \in B_i} w_{ij}\mathbf{u}_j = 0$$

Moving the sum over the boundary vertiecs to the right-hand side, we now have all the $\mathbf{u}_j$ we need to solve for on the left, and the fixed variables (boundary vertices) on the right.
$$\sum_{j \in N_i} w_{ij}\mathbf{u}_i - \sum_{j \in N_i/B_i} w_{ij}\mathbf{u}_j = \sum_{j \in B_i} w_{ij}\mathbf{u}_j$$

To write this in matrix form, we need to define our sparse matrix "Laplacian".

$$\mathbf{L}_{ij} = \left\{
    \begin{array}{ll}
    -w_{ij} & i \neq j \text{ and } \exists \{i,j\} \in \mathbf{E} \\
    -\sum_{l\neq i} L_{il} & i = j \\
    0 & \text{otherwise}
    \end{array}
\right.$$

From this matrix, we can derive the matrices corresponding to the left-hand and right-hand sides of the linear system. Let $\mathbf{L}_{F} \in \mathbb{R}^{n \times n}$ denote $\mathbf{L}$ with the columns corresponding to the fixed boundary vertices set to 0 (except for the diagonal elements). Let $\mathbf{L}_B \in \mathbb{R}^{n \times b}$ (b = # boundary vertices) denote $-\mathbf{L}$ with just the columns corresponding to the boundary vertices, and $\mathbf{L}_{B_{ii}} = 0$ if $i$ is a boundary vertex. Now we can write our system in matrix form as

$$\mathbf{L}_f \mathbf{U} = \mathbf{L}_b \mathbf{U}_b$$
where $\mathbf{U} \in \mathbb{R}^{n \times 2}$ is the parameterization map we're solving for and $\mathbf{U}_b \in \mathbb{R}^{b \times 2}$ is the matrix containing the fixed UV coordinates for the boundary vertices.