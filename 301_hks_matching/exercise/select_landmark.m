function landmarks = select_landmark(F,V)


fig = figure;

p = tsurf(F,V,'CData',zeros(size(F,1),1));
hold on;

axis equal; axis off;
cameratoolbar; cameratoolbar('SetCoordSys','none');

datacursormode on;
dcm_obj = datacursormode(fig);
disp('Click the mesh to select a vertex, then press "Enter". You can also turn off Data Tips, rotate the mesh and then activate Data Tips and select a point.')
set(dcm_obj, 'UpdateFcn', @myupdatefcn)
pause;
selectedPoint = getCursorInfo(dcm_obj).Position;
landmarks = knnsearch(V,selectedPoint);
sct(V(landmarks,:),'filled');
datacursormode off;

% Nested function for custom datatip text
function output_txt = myupdatefcn(~, event_obj)
    pos = get(event_obj, 'Position');
    output_txt = {['V: ', num2str(knnsearch(V,pos))]};
end


end

