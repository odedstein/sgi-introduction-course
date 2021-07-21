% GPS_match
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

[V1, F1] = readOFF([data_folder, meshes{1}]);
[V2, F2] = readOFF([data_folder, meshes{2}]);
cam1 = cams{1};
cam2 = cams{2};


%%
% Compute descriptors


% Select a few landmarks on M1
% To easily select landmarks use: MESH_VIS.selectLandmark(F1,V1)
LankmarksInd = [];

% Find the matching vertices on M2 by finding signatures that are
% closest (in L2 sense) to the signatures of the given landmarks.
% Hint: knnsearch
closestPoints = [];


% Visualize the correspondence
figure;
MESH_VIS.displayp2pCorrespondence(F1, V1, F2, V2, [LankmarksInd, closestPoints],'cam1',cam1,'cam2',cam2);


% You can try this for additional landmarks.
% Or compute a full map by finding a matching vertex on M2 for each vertex
% of M1




