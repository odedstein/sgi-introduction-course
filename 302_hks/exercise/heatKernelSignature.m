function [HKS, t] = heatKernelSignature(V, F)
  % Compute the heat kernel signature
  % "A Concise and Provably Informative Multi-Scale SignatureBased on 
  % Heat Diffusion", Sun et al., 2009
  %
  % Inputs:
  %   V  matrix, size (V,3), of mesh vertex positions
  %   F  matrix, size (F,3), of element indices into V
  %   k  number of eigenvalues and eigenfunctions to use
  % Outputs:
  %   HKS  matrix, size (V,nt), of HKS
  


ki = 300; % amount of eigenvalues and functions to use, you can add more
  
% Compute the first k eigenvalues and eigenfunctions of the laplacain
% Don't forget to sort them....


% We uniformly sample 100 points in the logarithmically scale over the following time
% interval, as suggested in the paper:
nt = 100;
tmin = 4*log(10)/evals(end); % evals is a vector of ki eigenvalues of the laplacian
tmax = 4*log(10)/evals(2);
t = logspace(log10(tmin),log10(tmax),nt); 


% Compute the HKS descriptor

