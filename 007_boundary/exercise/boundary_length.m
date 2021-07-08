function L = boundary_length(V,F)
%BOUNDARY_LENGTH Compute the length of a mesh's boundary
%
% Input:
%  V,F  input mesh
% Output:
%  L  the length of the boundary

%Compute the indices of all boundary edges.
O = ...

%Compute a matrix whose rows are equal to edgeEnd-edgeStart for each
%boundary edge.
BE = ...

%Compute the total length of all boundary edges.
L = ...

end

