clear all;
warning('off','all');

% parameters & settings
k = 250; % spring stiffness
dt = 0.01; % time step
frame_num = 5000; % number of total frames to run
mass_num = 10; % number of masses in the mass-spring system


% construct a 2-dimensional mass-spring system
V = [linspace(1,1+mass_num,mass_num)',zeros(mass_num,1)];
E = [linspace(1,mass_num-1,mass_num-1)',linspace(2,mass_num,mass_num-1)']; % edges
V = V-(max(V)+min(V))/2; V = V/max(V(:)); % normalize the mesh s.t. it has the right size


vec = @(X) X(:); % vectorization: [x1x2 y1y2] order


% boundary condition (feel free to play with it!)
ci = [1 mass_num]; % fixed vertex indices
ci = [ci ci+mass_num]'; % match the [x1x2 y1y2] order --> Q: why is this important?

M = eye(2*size(V,1)); % mass matrix
g = 1*vec(repmat([0 -9.8],size(V,1),1)); % gravity


% set up the viewer
clf;
hold on;
ts = line('XData',V(:,1),'YData',V(:,2),'LineWidth',2); % draw springs as lines
tp = scatter(V(:,1),V(:,2),'.b','SizeData',400); % draw masses as dots
hold off;
axis equal;
axis([-1.5 1.5 -2 0.2]);
axis manual;
drawnow;


% initialization
P = vec(V); % mass positions for the next time step
Pt = vec(V); % mass positions for the current time step
Ptt = vec(V); % mass positions for the previous time step


for iter = 1:frame_num

  % save the states of previous time steps
  Ptt = Pt; Pt = P;
  
  % implicit euler time stepper
  max_iter = 50;
  for i = 1 : max_iter
  
    % gradient and hessian for the elastic potential energy
    [G,K] = mass_spring_gradient_hessian(V,E,k,reshape(P,size(V)));
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%% solution %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % TASK: Use newton's method to solve the following nonlinear optimization problem
    %   min total_energy(P)
    %       s.t. P(ci,:) = 0
    %
    % White list:
    % - "min_quad_with_fixed" to solve the constrained optimization problem
    %
    % Hint:
    % - total energy = incremental kinetic energy + gravitational
    % potential energy + elastic potential energy
    
    dP = zeros(size(P));
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    if norm(dP) < 1e-6
        break;
    end

    alpha = 1; % fixed step size for newton
    P = P + alpha * dP; % update P

  end

  Vnew = reshape(P,size(V));
  ts.XData = Vnew(:,1); ts.YData = Vnew(:,2); % update springs
  tp.XData = Vnew(:,1); tp.YData = Vnew(:,2); % update masses
  title(sprintf('%d : %d',iter, i),'Fontsize',20);
  drawnow;
%   figgif('./mass-spring.gif'); % uncomment this line to save a .gif
  
end