% cot_lap_eigendecomposition
clear all; close all; clc;

gptoolbox_path = ''; % complete
addpath(genpath(gptoolbox_path));

data_folder = '..\data\';
meshes = dir([data_folder,'*.o*']); % a list of all the meshes in the data folder
meshes = {meshes.name}; % access each mesh name by meshes{i}

cam_folder = [data_folder, 'cams\'];
cams = dir([cam_folder,'*.mat']); % a list of all the cam in the cams folder
cams = {cams.name};

addpath(data_folder); addpath(cam_folder);


%% Task 1:
% load a few meshes using the readOFF or readOBJ function from gptoolbox,
% use lap_eig to compute its eigen decomposition and MESH_VIS to look at
% the eigenfunctions

% Remember  to adjust the colorbar to see all the eigenfunctions at the same scale

k = 6;




%% Task 2:
% Rotation matrices:
rotx = @(ang) [1 0 0; 0 cos(ang) -sin(ang) ; 0 sin(ang) cos(ang)] ; % rotate about the x axis
roty = @(ang) [cos(ang) 0 sin(ang) ; 0 1 0 ; -sin(ang) 0  cos(ang)] ;
rotz = @(ang) [cos(ang) -sin(ang) 0 ; sin(ang) cos(ang) 0 ; 0 0 1] ;

% Compute the new vertices positions:
V_new = [];


%% Task 3:




