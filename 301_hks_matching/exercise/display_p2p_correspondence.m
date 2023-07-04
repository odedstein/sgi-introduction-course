function display_p2p_correspondence(F1, V1, F2, V2, landmarks)

landmarks_colors = cbrewer('Set1',size(landmarks,1));
landmarks_colors = landmarks_colors(1:size(landmarks,1),:);

figure; 
subplot(1,2,1);
tsurf(F1,V1,'CData',zeros(size(F1,1),1)); hold on;
sct(V1(landmarks(:,1),:),60,landmarks_colors,'filled');
axis equal; axis off;
title('T_A')
subplot(1,2,2);
tsurf(F2,V2,'CData',zeros(size(F2,1),1)); hold on;
sct(V2(landmarks(:,2),:),60,landmarks_colors,'filled');
axis equal; axis off;
title('T_B')
cameratoolbar; cameratoolbar('SetCoordSys','none');



end

