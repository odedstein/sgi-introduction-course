function visualize_meshes(F, VA, VB)

figure;
subplot(1,2,1);
tsurf(F,VA);
axis equal; axis off;
title('T_A')
subplot(1,2,2);
tsurf(F,VB)
axis equal; axis off;
title('T_B')
cameratoolbar; cameratoolbar('SetCoordSys','none');

end

