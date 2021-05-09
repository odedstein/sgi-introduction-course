clc; clear all; close all;
 
[V,F] = readOBJ('./data/spot.obj');

fixed_idx = [1837, 2274, 1144];
fixed_location = V(fixed_idx,:);
handle_idx = [1454];
handle_location = V(handle_idx,:);

nSteps = 100;
thetaList = linspace(0, 5*pi, nSteps);
L = cotmatrix(V,F);
prefactor_L = [];
for ii = 1:length(thetaList)
    % get handle displacement
    handle_disp = [sin(thetaList(ii)),0,0];
    
    % solve deformation field which minimizes the Dirichlet energy
    b = [handle_idx, fixed_idx]';
    bc = [handle_disp; zeros(length(fixed_idx), 3)];
    [dV, prefactor_L] = min_quad_with_fixed(L, zeros(size(V,1),3),b, bc, [], [], prefactor_L);
    
    % visualization
    U = V+dV; % deformed location
    tsurf(F,U,'FaceColor',[144,210,236]/255);
    hold on
    scatter3(U(fixed_idx,1),U(fixed_idx,2),U(fixed_idx,3),'r','filled')
    scatter3(U(handle_idx,1),U(handle_idx,2),U(handle_idx,3),'b','filled')
    hold off
    view(0,90)
    axis off equal
    pause(0.02)
end