function pts = critical_points(V,F,u,tol)
%REVERSE_SUBDIVISION Find out which face contains the critical points of a
%function
%
% pts = critical_points(V,F,u,tol);
%
% Inputs:
%  V,F  the coarse input mesh
%  u  the function for which to find critical points
%  tol  the tolerance for writical points (if the gradient norm is below this,
%                                          we are at a critical point)
% Outputs:
%  pts  a list of face indices into the rows of F that tell us which faces
%       contain the critical points.
%

G = grad(V,F);
pts = ...

end

