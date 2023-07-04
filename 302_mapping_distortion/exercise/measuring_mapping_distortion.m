% measuring_mapping_distortion

clear all; close all; clc;

% Load two meshes A and B with common connectivity
[VA, FA] = readOBJ('..\data\T_A.obj');
[VB, FB] = readOBJ('..\data\T_B.obj');


% verify both meshes have the same connectivity
assert(all(FA(:)==FB(:)));
F = FA; % since the connectivity is the same


% visualize both meshes
visualize_meshes(F, VA, VB);


% Compute per-triangle distortion between A and B.
% We assume that there are no degenerate triangles.
nf = size(F,1); % the number of faces

% distortion measures per face
dirichlet     = zeros(nf,1);
sym_dirichlet = zeros(nf,1);
arap          = zeros(nf,1);


for i = 1:nf
    abc = F(i,:);

    % Find the 3D vertex positions of triangle a, b, c on meshes A and B
    % and use them as input to compute the Jacobian matrix
    J = triangle_jacobian();

    % Using the svd of the Jacobian, compute the distortion measures

    dirichlet(i)     = 0;
    sym_dirichlet(i) = 0;
    arap(i)          = 0;
end



view_log_heatmap(F, VA, VB, dirichlet, 4.0, 100.0, 'Dirichlet');
view_log_heatmap(F, VA, VB, sym_dirichlet, 4.0, 100.0, 'Symmetric Dirichlet');
view_log_heatmap(F, VA, VB, arap, 4.0, 100.0, 'ARAP');


