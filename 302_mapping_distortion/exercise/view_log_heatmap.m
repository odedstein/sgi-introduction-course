function view_log_heatmap(F, VA, VB, f, min_range, max_range, title_str)
% visualize the distortion using a log heatmap 
            

lambda = (log(f) - log(min_range)) / (log(max_range) - log(min_range));
lambda = min(max(lambda, 0), 1);

figure;
subplot(1,2,1);
tsurf(F,VA, 'CData',lambda);
axis equal; axis off;
title('T_A')
subplot(1,2,2);
tsurf(F,VB, 'CData',lambda)
axis equal; axis off;
title('T_B')
cameratoolbar; cameratoolbar('SetCoordSys','none');

% colormap(cbrewer('Blues',256));

sgtitle(title_str);


end

