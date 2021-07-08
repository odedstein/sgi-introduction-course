% implement a simple version of 
% "Spectral Conformal Parameterization" by Mullen et al. 2008

clc; clear all; close all;
[V,F] = readOBJ('../data/ogre.obj');

L = cotmatrix(V,F); % #V- by - #V
LD = repdiag(L, 2); % 2V by 2V
A = 2 * vector_area_matrix(F);
LC = LD - A;

bEdges = outline(F);
bIdx = unique(bEdges);

% build top left block
row = bIdx;
col = bIdx;
val = ones(length(bIdx),1);
B_block = sparse(row, col, val, size(V,1), size(V,1));
B = repdiag(B_block, 2);

% eigs
[eVec, eVal] = eigs(LC, B, 5, 'sm');
u = eVec(:,3);
UV = reshape(u, size(V,1), 2);

figure(1)
subplot(1,2,1)
tsurf(F,V); axis equal
subplot(1,2,2)
tsurf(F,UV); axis equal