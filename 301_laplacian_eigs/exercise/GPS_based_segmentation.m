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

[V, F] = readOFF(meshes{1});
cam = cams{1};




%% USe k-means algorithm (clustering algorithm) to segment the shape based on the GPS and visualize the results
% Hint: use Matlab's kmeans function.
% Try 5 or 6 segments for the armadillo.
% Feel free to try it with other meshes as well!


d = 5; % GPS embedding dimention





