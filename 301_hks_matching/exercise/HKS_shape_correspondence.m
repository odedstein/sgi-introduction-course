% HKS_shape_correspondence
clear all; close all; clc;

% Load bith meshes
[V1, F1] = readOFF('..\data\cat-00.off');
[V2, F2] = readOFF('..\data\cat-01.off');


%%
% Compute the hks descriptors for all the vertices of both shapes


% Select a few landmarks on M1
% To easily select landmarks use: select_landmark(F1,V1)

% For each of the selected landmarks, compute the distance ($L_2$ norm) between its scaled HKS and the scaled HKS of all the vertices of the other mesh. 
% Visualize the result as a function on the second mesh.
% Yuu can also try finding a matching vertex on M2 by
% finding the hks signature that is closest (in the L2 sense) to the signatures of the given landmark
% Hint: knnsearch





% Visualize the sparse point to point correspondence
Lankmarks = []; % should be a n landmark X 2 matrix. 
                % The first colounm is a vector of vertices indices on the first shape, 
                % and the second colpumn the matching indices on the second shape
display_p2p_correspondence(F1, V1, F2, V2, Lankmarks);


