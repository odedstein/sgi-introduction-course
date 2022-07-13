classdef MESH_VIS
    % Based on code writen by Omri Azencot and Danielle Ezuz.
    
    properties
    end
    
    methods (Static)
        
        function landcolor = mesh(F,V,varargin)
            
            p = inputParser;
            p.KeepUnmatched=true;
            % Optional inputs:
            addOptional(p,'FaceColor','w');
            addOptional(p,'EdgeColor','none');
            addOptional(p,'landmarks',0); % a vector of landmark indices
            addOptional(p,'landSize',0); % size of the sphere marking the landmarks
            addOptional(p,'landColor',[]);
            addOptional(p,'FaceAlpha',.8);
            addOptional(p,'LineWidth',.5);
            addOptional(p,'docked',0);
            addOptional(p,'cam',[]); % cam full path
            addOptional(p,'CData',[]); % function to display on mesh
            addOptional(p,'title',[]);
            addOptional(p,'Caxis','auto'); % a vector containing [cmin cmax]
            addOptional(p,'colorbar',1); % 0 - to not display a colorbar
            addOptional(p,'Colormap','jet');
            
            parse(p,varargin{:});
            
            if isempty(p.Results.CData)
                if strcmp(p.Results.EdgeColor,'none')
                    EdgeColor = 'k';
                else
                    EdgeColor = p.Results.EdgeColor;
                end
                patch('faces',F,'vertices',V, ...
                    'FaceColor',p.Results.FaceColor, ...
                    'EdgeColor',EdgeColor, ...
                    'FaceAlpha',p.Results.FaceAlpha, ...
                    'linewidth',p.Results.LineWidth);
                
            elseif length(p.Results.CData)==size(V,1)
                patch('faces',F,'vertices',V, ...
                    'FaceVertexCData',p.Results.CData, ...
                    'FaceColor','interp', ...
                    'EdgeColor',p.Results.EdgeColor, ...
                    'FaceAlpha',p.Results.FaceAlpha, ...
                    'linewidth',p.Results.LineWidth);
                
            elseif length(p.Results.CData)==size(F,1)
                patch('faces',F,'vertices',V, ...
                    'FaceVertexCData',p.Results.CData, ...
                    'FaceColor','flat', ...
                    'EdgeColor',p.Results.EdgeColor, ...
                    'FaceAlpha',p.Results.FaceAlpha, ...
                    'linewidth',p.Results.LineWidth);
            else
                error('bad function size');
            end

            if p.Results.landmarks(1) ~= 0
                if p.Results.landSize==0
                    M1_peri = max([max(V(:,1)) - min(V(:,1)), max(V(:,2)) - min(V(:,2)), max(V(:,3)) - min(V(:,3))]);
                    landSize = 0.02*M1_peri;
                else 
                    landSize = p.Results.landSize;
                end
                landcolor = MESH_VIS.vis_landmarks( V, p.Results.landmarks,  landSize, p.Results.landColor); 
            else
                landcolor = [];
            end
            
            if ~isempty(p.Results.cam)
                load(p.Results.cam);
                MESH_VIS.set_camera(gca,cam);
            end

            camlight; lighting phong; material dull;

            cameratoolbar; cameratoolbar('SetCoordSys','none');
            axis equal; axis off;
            if p.Results.docked
                set(gcf,'windowstyle','docked');
            end
            
            if ~isempty(p.Results.CData)
                caxis(p.Results.Caxis);
                colormap(p.Results.Colormap);
                if p.Results.colorbar
                    colorbar;
                end
            end
            
            if ~isempty(p.Results.title)
                title(p.Results.title, 'interpreter','latex');
            end
            
        end
        
        
        function set_camera(ca,cam)
            set(ca, 'PlotBoxAspectRatio',cam.pba);
            set(ca, 'DataAspectRatio',cam.dar);
            set(ca, 'CameraViewAngle',cam.cva);
            set(ca, 'CameraUpVector',cam.cuv);
            set(ca, 'CameraTarget',cam.ct);
            set(ca, 'CameraPosition',cam.cp);
        end
        
        function cam = get_camera(ca)
            cam.pba = get(ca, 'PlotBoxAspectRatio');
            cam.dar = get(ca, 'DataAspectRatio');
            cam.cva = get(ca, 'CameraViewAngle');
            cam.cuv = get(ca, 'CameraUpVector');
            cam.ct = get(ca, 'CameraTarget');
            cam.cp = get(ca, 'CameraPosition');
        end
        
        function color = vis_landmarks( V, p, s, color )
            % p - vertex indices
            
            [SX,SY,SZ] = sphere;
            a = s;
            SX = SX*a; SY = SY*a; SZ = SZ*a;
            
            if isempty(color)
                color = jet(length(p));
            elseif size(color,1)==1
                color = repmat(color,length(p),1);
            end
            hold on;
            for i = 1:length(p)
                xs = V(p(i),:);
                surf(SX+xs(1),SY+xs(2),SZ+xs(3),'FaceColor',color(i,:),...
                    'EdgeColor','none','FaceAlpha',0.7);
            end
            hold off;
        end
        
        function land = selectLandmark( F, V )
            fig = figure;
            MESH_VIS.mesh(F,V);
            datacursormode on;
            dcm_obj = datacursormode(fig);
            disp('Click mesh to display a data tip, then press "Enter". You can rotate the mesh and then select a data tip if needed.')
            pause;
            selectedPoint = getCursorInfo(dcm_obj).Position;
            land = dsearchn(V,selectedPoint);
            close(fig);
        end
            
        % a matriix, size(np,2) containing pairs of vertices' indices
        % i.e. V1(p2p(1,1),:) matches V2(p2p(1,2),:)
        % displays up to 50 points (selected randomly if the inputs map is larger)
        function displayp2pCorrespondence(F1, V1, F2, V2, p2p,varargin)
            
             
            p = inputParser;
            p.KeepUnmatched=true;
            % Optional inputs:
            addOptional(p,'cam1',[]); % cam full path
            addOptional(p,'cam2',[]); % cam full path
            parse(p,varargin{:});
            
            
            if size(p2p,1)>50
                randInd = randperm(size(p2p,1));
                p2p = p2p(randInd(1:50),:);
            end
            colors = jet(size(p2p,1));
            
            subplot(1,2,1);
            if isempty(p.Results.cam1)
                MESH_VIS.mesh(F1,V1,'landmarks',p2p(:,1),'landColor',colors);
            else
                 MESH_VIS.mesh(F1,V1,'landmarks',p2p(:,1),'landColor',colors,'cam',p.Results.cam1);
            end

            subplot(1,2,2);
            if isempty(p.Results.cam2)
                MESH_VIS.mesh(F2,V2,'landmarks',p2p(:,2),'landColor',colors);
            else
                 MESH_VIS.mesh(F2,V2,'landmarks',p2p(:,2),'landColor',colors,'cam',p.Results.cam2);
            end

        end


    end
    
end

