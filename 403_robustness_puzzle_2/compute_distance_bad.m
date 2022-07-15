% Compute geodesic distance along the mesh
%[V,F] = readOBJ('data/spot_good.obj'); % this one will work
[V,F] = readOBJ('data/spot_bad.obj');  % but this one will not!

% NOTE: The result may not be the same on the "bad" mesh after you repair
% it, because this code computes the distance from vertex "1", but which
% vertex is vertex "1" may change. That is fine, as long as it outputs
% reasonable a looking distance.

% Run the algorithm 
% (I promise nothing is wrong with this algorithm, the problem is the mesh)
dists = heat_geodesic(V,F,1);

% Plot the resulting function
t = tsurf(F,V, 'CData',dists);
shading interp;
axis equal;
axis off;
colormap(cbrewer('Blues', 500));
light('Position',[-1.5 1 1],'Style','local');
lights = camlight;
set(t, 'FaceLighting','gouraud', 'FaceColor','interp');
set(t, 'DiffuseStrength',0.5, 'SpecularStrength',0.2, 'AmbientStrength',0.3);
camproj('perspective');