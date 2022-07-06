function A = four_corners(m,n)
%FOUR_CORNERS Construct a m x n sparse matrix with ones in each of its four
%corners.
%
% t = four_corners(m,n);
%
% Inputs:
%  m,n  the dimension of the matrix requested
% Outputs:
%  A  the sparse matrix with ones in their four corners
%

A = sparse(m,n);
A(1,1) = 1;
A(m,1) = 1;
A(1,n) = 1;
A(m,n) = 1;

end

