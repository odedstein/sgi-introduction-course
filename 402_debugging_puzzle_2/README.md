# Debugging Puzzle 2: Gauss-Bonnet Gone Wrong

Note: unlike the other exercises, there are no specific notes associated with these puzzles. Your job is to practice debugging, and figure out what is going wrong!

In this second puzzle, we will debug a routine that uses the [Gauss-Bonnet Theorem](https://en.wikipedia.org/wiki/Gauss%E2%80%93Bonnet_theorem) to compute the [genus](https://en.wikipedia.org/wiki/Genus_(mathematics)) of a triangle mesh via an expression involving the corner angles (the corner angles actually encode Gaussian curvature, which you saw in a previous tutorial). The _genus_ is a topological property, which is roughly how many 'handles' the shape has: a sphere has 0, a torus has 1, a pretzel has 3, etc. 

The Gauss-Bonnet Theorem is a beautiful relationship involving many key ideas in surface geometry. If you are interested to learn more, one good resource is Chapter 5 of the [Discrete Differential Geometry textbook](https://www.cs.cmu.edu/~kmcrane/Projects/DDG/paper.pdf).

However, here don't necessarily need to know all the details of the underlying theorem. We have some simple geometric code which works, and outputs correct values on most meshes, but on one mesh we give it is it going to fail! We're going to debug the code to understand what is happening.

The provided code in `exercises/compute_gauss_bonnet_broken.py` contains the implementation of the function, and runs it on a handful of meshes in the data directory. For each it should produce output like:

```
=== Processing mesh data/sphere_good.obj
  162 verts   320 faces
  total curvature 12.56 = 4.00 π
  Gauss-Bonnet Theorem says the genus is 0.00 (valid for closed triangle meshes only)
```

However, on the last mesh `sphere_bad.obj`, it will fail!

```
 === Processing mesh data/sphere_bad.obj
  162 verts   320 faces
  total curvature nan = nan π
  Gauss-Bonnet Theorem says the genus is nan (valid for closed triangle meshes only)
```

Our old nemesis [NaN](https://en.wikipedia.org/wiki/NaN), spotted in the wild. There are two parts to this exercise:

1) Determine what is causing these NaN values to arise for this mesh. Where in the code are the coming from? What is different about this mesh compared to the others?

2) Propose a solution! Is there a simple fix that will make this code output the right answer? (The genus of a sphere is 0.)


Food for thought: if you come up with a solution (2), do you think your solution always works in general? Why or why not? Writing robust geometric routines like this which provably _always_ work in _all_ cases is actually very, very, hard!

Tips:
- Try visualizing the loaded mesh
- Once you find one problem, follow it backwards to understand its source
- If you see any error messages, follow-up on them

[exercise](exercise)

[solution](solution)
