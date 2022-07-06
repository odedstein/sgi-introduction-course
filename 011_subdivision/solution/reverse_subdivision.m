function u = reverse_subdivision(V,F,uu,k)
%REVERSE_SUBDIVISION Given a function uu on a mesh which has been
%subdivided k times from the coarse V,F, reconstruct a function u on the
%coarse mesh V,F.
%
% u = reverse_subdivision(V,F,uu,k);
%
% Inputs:
%  V,F  the coarse input mesh
%  uu  a function on the subdivided mesh loop(V,F,k)
%  k  how many times to subdivide
% Outputs:
%  u  a proxy for the function uu on the coarse mesh V,F
%

[~,~,S] = loop(V,F,k);
u = (S'*S) \ (S'*uu);

end

