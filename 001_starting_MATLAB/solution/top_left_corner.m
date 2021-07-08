function C = top_left_corner(A, r, c)
%TOP_LEFT_CORNER Select the top-left corner of a matrix
%
% C = top_left_corner(A, r, c)
%
% Inputs:
%  A  a rectangular matrix
%  r  the number of rows of the corner we want to select
%  c  the number of columns of the corner we want to select
% Outputs:
%  C  the r-by-c top left corner of A

C = A(1:r, 1:c);

end

