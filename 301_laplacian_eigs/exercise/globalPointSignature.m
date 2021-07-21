function GPS = globalPointSignature(V, F, k)
  % Compute the global Point Signature
  % "Laplace-Beltrami eigenfunctions for deformation invariant shape
  % representation", Rustamov, 2007
  %
  % Inputs:
  %   V  matrix, size (V,3), of mesh vertex positions
  %   F  matrix, size (F,3), of element indices into V
  %   k  number of eigenvalues and eigenfunctions to use
  % Outputs:
  %   GPS  matrix, size (V,k), of GPS


