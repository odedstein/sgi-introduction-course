% HKS_matching 
clear all; close all; clc;


%% Example features
% For the cat model:
[V, F] = readOFF('..\data\cat-00.off');
landmarks = [3048; 1997; 6980; 5957]; % right front leg, left front leg, right back leg, left back leg 


% To choose other landmarks and get their verex number, use the function 
% selected_landmark = select_landmark(F,V);


visualize_mesh_with_landmarks(F, V, landmarks);


%% Matching: 
% to compute the HKS, use gptoolbox: [K,MK] = hks(V,F)
% and to mormalize the hks use: K = K./MK 
% which divides each HKS feature vector with its mass-weighted spatial sums






%% Visualize the results
% - Plot the HKS vs log(t) for the landmarks.
% - For a specific landmark, compute the distance ($L_2$ norm) between its scaled HKS and the scaled HKS of all the other vertices. 
%   Visualize the result as a function on the mesh.




