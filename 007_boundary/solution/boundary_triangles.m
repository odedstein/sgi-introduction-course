function BF = boundary_triangles(F)
%BOUNDARY_TRIANGLES Computes a list of indices of all boundary triangles in
%F.
%
% boundary_triangles(F);
%
% Input:
%  F  triangle list to compute the mesh whose boundary triangles are to be
%     computed
% Output:
%  BF  a list of indices into F of all boundary triangles

BF = find(on_boundary(F));

end

