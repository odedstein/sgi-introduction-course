function plot_boundary_orange(V,F)
%PLOT_BOUNDARY_ORANGE  plots the boundary vertices of a triangle mesh in
%orange, and its interior in blue.
%
% plot_boundary_orange(V,F)(V,F);
%
% Input:
%  V,F  mesh whose boundary is to be plotted

%Compute a function u that is 0 on all interior vertices and 1 on all
%boundary vertices.  
u = ...

%Plot the function u with the right colors.
t = tsurf(F,V, 'CData',u);
shading interp;
axis equal;
axis off;
cm = flipud(cbrewer('RdYlBu', 500));
colormap(cm(100:450,:));
light('Position',[-1.5 1 1],'Style','local');
lights = camlight;
set(t, 'FaceLighting','gouraud', 'FaceColor','interp');
set(t, 'DiffuseStrength',0.5, 'SpecularStrength',0.2, 'AmbientStrength',0.3);
camproj('perspective');
add_shadow([t],lights);

end

