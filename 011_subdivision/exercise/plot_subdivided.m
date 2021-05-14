function plot_subdivided(V,F,u,k)
%PLOT_SUBDIVIDED Plot the function u on the mesh V,F which has subdivided,
%with Loop subdivision, k times
%
% plot_subdivided(V,F,u,k);
%
% Inputs:
%  V,F  the input mesh to be subdivided
%  u  the input function to be subdivided along with the mesh
%  k  how many times to subdivide
%

Vu = ...
Fu = ...
uu = ...

t = tsurf(Fu,Vu, 'CData',uu);
shading interp;
axis equal;
axis off;
colormap(cbrewer('Blues', 500));
light('Position',[-1.5 1 1],'Style','local');
lights = camlight;
set(t, 'FaceLighting','gouraud', 'FaceColor','interp');
set(t, 'DiffuseStrength',0.5, 'SpecularStrength',0.2, 'AmbientStrength',0.3);
camproj('perspective');
add_shadow([t],lights);

end

