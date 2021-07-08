clc; clear all; close all;

% prepare the input mesh
[V,F] = readOBJ('../data/spot.obj');
[V,F,S] = loop(V,F);

% specify handles and handle displacement
handles = [1837; 2274; 1144; 1454]; 
handles_disp = [0.2,0,0;0.2,0,0;0.2,0,0;-0.8,0,0]; 

% solve for deformation
A = cotmatrix(V,F);
B = zeros(size(V,1),3);
tic;
preF = [];
[d1, preF] = ...
    min_quad_with_fixed(...
    A,B,handles,handles_disp,[],[],preF);
toc;

figure(1)
subplot(1,2,1)
tsurf(F,V)
hold on
sct(V(handles,:),'filled', 'r')
qvr(V(handles,:), handles_disp, 'b')
axis equal
title('initial')
subplot(1,2,2)
tsurf(F,V+d1)
axis equal
title('deformation')

% solve for new deformation
handles_disp_new = [0.2,0.2,0;0.2,0.2,0;0.2,-0.2,0;-1,0.3,0];

tic;
[d2, preF] = ...
    min_quad_with_fixed(...
    A,B,handles,handles_disp_new,[],[],preF);
toc;

figure(2)
subplot(1,2,1)
tsurf(F,V)
hold on
sct(V(handles,:),'filled', 'r')
qvr(V(handles,:), handles_disp_new, 'g')
axis equal
title('initial')
subplot(1,2,2)
tsurf(F,V+d2)
axis equal
title('deformation')

