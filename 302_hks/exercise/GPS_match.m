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


GPS1 = globalPointSignature_sol(V1, F1, 15);
GPS2 = globalPointSignature_sol(V2, F2, 15);

%%
% First, let's compute matching points on near-isometric shapes for some selected landmarks:

LankmarksInd = [7203; 3805; 3072]; % tip of the cat's tail, left ear, right front leg

% Find the matching vertices on M2 by finding signatures from GPS2 that are
% most similar to the signatures of the given landmarks.
% Hint: knnsearch
closestPoints = 


figure;
MESH_VIS.displayp2pCorrespondence(F1, V1, F2, V2, [LankmarksInd, closestPoints],'cam1',cam1,'cam2',cam2);


% You can try this for additional landmarks.
% To easily select more landmarks use: MESH_VIS.selectLandmark(F1,V1)
% Or compute a full map by finding a matching vertex on M2 for each vertex
% of M1




