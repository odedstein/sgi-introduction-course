function A = triangles_matrix(n)
%TRIANGLES_MATRIX Construct a n x n sparse matrix with a triangular pattern
%of ones, as by the following pattern:
% 0 1 1 1 1 1 1 1 1 1 1
% 1 0 1 0 0 0 0 0 0 0 1
% 1 1 0 1 0 0 0 0 0 0 1
% 1 0 1 0 1 0 0 0 0 0 1
% 1 0 0 1 0 1 0 0 0 0 1
% 1 0 0 0 1 0 1 0 0 0 1
% 1 0 0 0 0 1 0 1 0 0 1
% 1 0 0 0 0 0 1 0 1 0 1
% 1 0 0 0 0 0 0 1 0 1 1
% 1 0 0 0 0 0 0 0 1 0 1
% 1 1 1 1 1 1 1 1 1 1 0
%
% t = four_corners(m,n);
%
% Inputs:
%  n  the dimension of the matrix requested
% Outputs:
%  A  the sparse matrix with the requested triangle pattern
%

i = [(2:n)'; (1:(n-1))'; ones(n-2,1); n*ones(n-2,1); ...
    (3:(n-1))'; (2:(n-2))'];

j = [ones(n-1,1); n*ones(n-1,1); (2:(n-1))'; (2:(n-1))'; ...
    (2:(n-2))'; (3:(n-1))']; 

v = ones(size(i));

A = sparse(i, j, v, n, n);

end

