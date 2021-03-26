function plot_z_coord(V,F)
%PLOT_Z_COORD  plot the z-coordinate on the input mesh
%
% plot_z_coord(V,F);
%
% Input:
%  V,F  mesh that is to be plotted

f = V(:,3);
tsurf(F,V, 'CData',f);
axis equal;
shading interp;

end

