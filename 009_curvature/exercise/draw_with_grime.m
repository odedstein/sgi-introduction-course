function t = draw_with_grime(V,F)
%DRAW_WITH_GRIME Draws the input mesh with a grime effect applied to
%crevices of the surface.
%
% t = tangents(V,F);
%
% Inputs:
%  V,F  triangle mesh
% Outputs:
%  t  handle to the drawn surface
%

%Compute the principal curvatures
kappa = ...

%Get a function that is 0 when principal curvatures are positive, and
%increases in magnitude when they are negative
c = ...

%Plot the resulting function
t = tsurf(F,V, 'CData',c);
shading interp;
axis equal;
axis off;
colormap(...);
light('Position',[-1.5 1 1],'Style','local');
lights = camlight;
set(t, 'FaceLighting',..., 'FaceColor',...);
set(t, 'DiffuseStrength',0.5, 'SpecularStrength',0.2, 'AmbientStrength',0.3);
camproj(...);
add_shadow([t],lights);

end

