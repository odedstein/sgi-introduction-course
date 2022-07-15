[V,F] = readOBJ('data/armadillo_bad.obj');

shadingParams = {'FaceLighting','gouraud', 'FaceColor','interp'};
u = ones(size(V,1),1);
tsurf(F,V, 'CData',u, shadingParams{:});
shading interp;
axis equal;
axis off;
light('Position',[-1.5 1 1],'Style','local');
lights = camlight;