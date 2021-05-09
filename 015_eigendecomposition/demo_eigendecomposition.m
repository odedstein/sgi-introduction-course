clc; clear all; close all;
 
[V,F] = readOBJ('./data/spot.obj');

L = cotmatrix(V,F);
M = massmatrix(V,F);
numEigs = 20;
[eVec, eVal] = eigs(-L,M,numEigs,'sm');

for ii = 2:numEigs
    tsurf(F,V, 'CData',eVec(:,ii)); 
    axis equal;
    shading interp;
    pause(0.5)
end
