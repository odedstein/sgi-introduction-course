function deform_GUI(V,F,C,W)
%%%%%%%%%%
% you dont  need 

fprintf( ...
    ['Linear Blend Skinning: \n' ...
    '- CLICK handles to visualize weights \n', ...
    '- DRAG a handle to move\n', ... 
    '- SHIFT+DRAG a handle to rotate\n'] ...
    );

P = 1:size(C,1); % set default point handles
if(size(C,2) == 3)
C = C(:,1:2); % Be sure that control vertices are in 2D
end
CW = W; % Weights used for contours
WVW = W;  % Weights used for weight visualization
np = numel(P);  % number of point handles

DeformOBJ.new_C = [];
% keep track of rotations stored at each control point, for 2D this is a m
% by 1 list of angles
DeformOBJ.R = zeros(np,1);
DeformOBJ.update_positions = @update_positions;
  
subplot(1,2,1)
DeformOBJ.tsh = tsurf(F,V);
axis equal
hold on 
C_plot = scatter3( ...
    C(:,1),C(:,2),0.1+0*C(:,1), ... 
    'o','MarkerFaceColor',[0.9 0.8 0.1], 'MarkerEdgeColor','k',...
    'LineWidth',2,'SizeData',100, ...
    'ButtonDownFcn',@oncontrolsdown);
hold off;
% axis manual

subplot(1,2,2)
% plot the original mesh
DeformOBJ.wvsh = tsurf(F,V);
view(2);
axis equal
% axis manual

% keep track of window xmin, xmax, ymin, ymax
win_min = min([C(:,1:2); V(:,1:2)]);
win_max = max([C(:,1:2); V(:,1:2)]);
% keep track of down position
down_pos = [];
% keep track of last two drag positions
drag_pos = [];
last_drag_pos = [];
% keep track of mesh vertices at mouse down
down_V = [];
% keep track of index of selected control point
ci = [];
% type of click ('left','right')
down_type  = '';

% Callback for mouse down on control points
  function oncontrolsdown(src,ev)
    % get current mouse position, and remember old one
    down_pos=get(gca,'currentpoint');
    down_pos=[down_pos(1,1,1) down_pos(1,2,1)];
    last_drag_pos=down_pos;
    drag_pos=down_pos;
    % keep track of control point positions at mouse down
    DeformOBJ.new_C = [get(C_plot,'XData')' get(C_plot,'YData')'];
    % get index of closest control point
    [minD,ci] =  ...
      min(sum((DeformOBJ.new_C(:,1:2) - ...
      repmat(down_pos,size(DeformOBJ.new_C,1),1)).^2,2));
    % keep track of mesh vertices at mouse down
    down_V = get(DeformOBJ.tsh,'Vertices');
    down_V = down_V(:,1:2);

    % tell window that drag and up events should be handled by controls
    set(gcf,'windowbuttonmotionfcn',@oncontrolsdrag)
    set(gcf,'windowbuttonupfcn',@oncontrolsup)
    set(gcf,'KeyPressFcn',@onkeypress)
    if(strcmp('normal',get(gcf,'SelectionType')))
      % left-click
      down_type = 'left';
    else
      % other (right) click
      down_type = 'right';
    end

    % try to find ci in list of point handles
    [found, iP] = ismember(ci,P);
    if(found)
      % set color of mesh plot to weights of selected
      %set(tsh,'CData',W(:,iP));
      % change weights in weight visualization
      set(DeformOBJ.wvsh,'CData',WVW(:,iP));
    end

  end

  % Callback for mouse drag on control points
  function oncontrolsdrag(src,ev)
    % keep last drag position
    last_drag_pos=drag_pos;
    % get current mouse position
    drag_pos=get(gca,'currentpoint');
    drag_pos=[drag_pos(1,1,1) drag_pos(1,2,1)];
    if(strcmp('left',down_type))
      % move selected control point by drag offset
      DeformOBJ.new_C(ci,:) = ...
        DeformOBJ.new_C(ci,:) + drag_pos-last_drag_pos;
    else
      [found, iP] = ismember(ci,P);
      if(found)
        DeformOBJ.R(iP) = ...
          DeformOBJ.R(iP) + 2*pi*(drag_pos(1)-last_drag_pos(1))/100;
      end
    end
    update_positions();
  end

  function update_positions()
    % update display positions
    set(C_plot,'XData',DeformOBJ.new_C(:,1));
    set(C_plot,'YData',DeformOBJ.new_C(:,2));
    
    % USING LINEAR BLEND SKINNING
    % get transformations stored at each point and bone handle
    TR = ...
    skinning_transformations(C,P,[],DeformOBJ.new_C,DeformOBJ.R);

    % linear blend skinning
    [new_V] = linear_blend_skinning(V(:,1:2),TR,W);

    % update mesh positions
    set(DeformOBJ.tsh,'Vertices',new_V(:,1:2));
  end

  % Callback for mouse release of control points
  function oncontrolsup(src,ev)
    % Tell window to handle drag and up events itself
    set(gcf,'windowbuttonmotionfcn','');
    set(gcf,'windowbuttonupfcn','');
    cur_V = get(DeformOBJ.tsh,'Vertices');
    cur_V = cur_V(:,1:2);

    % scale window to fit
    win_min = min([win_min; cur_V]);
    win_max = max([win_max; cur_V]);
    axis(reshape([win_min;win_max],1,2*size(cur_V,2)))
  end

  function onkeypress(src,ev)
    if(strcmp(ev.Character,'r'))
      DeformOBJ.new_C = C;
      DeformOBJ.R = zeros(np,1);
      update_positions();
    elseif(strcmp(ev.Character,'u'))
      update_positions();
    end
  end
end