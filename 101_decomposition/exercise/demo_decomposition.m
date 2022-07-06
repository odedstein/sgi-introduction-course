% Implement a simple version of "Geodesics in Heat" by Crane et al. 2013

clc; clear all; close all;
[V,F] = readOBJ('../data/spot.obj');
[V,F,S] = loop(V,F,2); % upsample the mesh to see the speed difference
use_prefactorization = true; % set it to "true" or "false" to see speed difference

% precompute matrices
A = massmatrix(V,F);
Lc = cotmatrix(V,F);
t = avgedge(V,F)^2;
LHS = A - t*Lc;
G = grad(V,F); % #F*dim by #V
D = div(V,F); % #V by #F*dim

% prefactorization
preLHS = decomposition(LHS);
preLc = decomposition(Lc);

%% change heat source
heatSrcIdx = 1;

tic;

% step 1
delta = zeros(size(V,1),1);
delta(heatSrcIdx) = 1;
if use_prefactorization
    u = preLHS \ delta;
else 
    u = LHS \ delta;
end

% step 2
gradu = G*u;
gradu = reshape(gradu, size(F,1), 3);
gradu_normalized = gradu ./ normrow(gradu);
X = -gradu_normalized;

% step 3
divX = D * reshape(X, size(F,1)*3, 1);
if use_prefactorization
    phi = preLc \ divX;
else
    phi = Lc \ divX;
end
phi = phi - phi(heatSrcIdx);

toc;

%% visualization
tsurf(F,V, 'CData', phi); 
axis equal;
CM = cbrewer('Reds', 500);
CM = CM(size(CM,1):-1:1,:);
colormap(CM);
colorbar
shading interp
drawnow 
