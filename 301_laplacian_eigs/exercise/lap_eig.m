function [evals, evecs] = lap_eig(V, F, k)
  % Compute the eigendecomposition of the laplacian
  %
  % Inputs:
  %   V  matrix, size (V,3), of mesh vertex positions
  %   F  matrix, size (F,3), of element indices into V
  %   k  number of eigenvalues and eigenfunctions to compute
  % Outputs:
  %   evals  vector, length k, of eigenvalues
  %   evecs  matrix, size (V,k), list of eigenfunctions
  
  
  
  
% Compute the k smallest eigenvalues and eigenfunctions of the laplacian.
% Return then in a sorted order - from the smallest eigenvalue to the largest