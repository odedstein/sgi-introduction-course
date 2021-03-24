function d = det2x2(A)
%DET2X2 Compute the determinant of a 2x2 matrix
%
% d = det2x2(S);
%
% Inputs:
%  A  a 2x2 matrix
% Outputs:
%  d  the determinant of A

d = A(1,1)*A(2,2) - A(1,2)*A(2,1);

end

