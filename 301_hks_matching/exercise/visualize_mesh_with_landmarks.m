function visualize_mesh_with_landmarks(F, V, landmarks, landmarks_colors)

if nargin<4
    landmarks_colors = repmat([1 0 0],length(landmarks),1);
end

figure;
p = tsurf(F,V,'CData',zeros(size(F,1),1));
hold on;
sct(V(landmarks,:),40,landmarks_colors,'filled');

colormap(cbrewer('Blues',50));
axis equal; axis off;
cameratoolbar; cameratoolbar('SetCoordSys','none');

end