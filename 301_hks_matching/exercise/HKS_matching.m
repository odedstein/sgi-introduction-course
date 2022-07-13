% HKS_matching 
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


%% 
% % For dragon model:
% [V, F] = readOBJ(meshes{8});
% cam = cams{8};
% landmarks = [6921; 6827; 9683; 9710]; % right front leg, left front leg, right back leg, left back leg, 
% figure; MESH_VIS.mesh(F,V,'cams',cam,'landmarks',landmarks);


% % For cat model:
[V, F] = readOFF(meshes{4});
cam = cams{4};
landmarks = [3048; 1994; 6621; 5560]; % right front leg, left front leg, right back leg, left back leg, 
figure; MESH_VIS.mesh(F,V,'cams',cam,'landmarks',landmarks);


% % For xyzrgb_dragon1 model:
% [V, F] = readOBJ(meshes{14});
% cam = cams{8};
% landmarks = [91921; 58423; 51903; 52775]; % right front leg, left front leg, right back leg, left back leg, 



%% Matching: 
% to compute the HKS, use gptoolbox's: [K,MK] = hks(V,F)
% and to mormalize the hks use: K./MK



