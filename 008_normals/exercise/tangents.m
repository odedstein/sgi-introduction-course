function [T1,T2] = tangents(V,F)
%TANGENTS Computes two orthogonal, oriented tangent vectors for each face
%in a triangle mesh.
%
% [T1,T2] = tangents(V,F);
%
% Inputs:
%  V,F  triangle mesh
% Outputs:
%  T1  one unit tangent vector for each face in F
%  T2  a second unit tangent vector for each face in F, perpendicular to
%      the respective vector in T1.
%      T1,T2 is oriented, which means that their cross product points in
%      the same direction as the normal.

%Extract the first edge of each face and normalize it.
E1 = ...

%Extract the second edges and project onto the orthogonal complement of E1.
E2 = ...

%Normalize to get unit vectors

end

