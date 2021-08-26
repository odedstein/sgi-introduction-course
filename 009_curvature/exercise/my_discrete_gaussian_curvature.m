function k = my_discrete_gaussian_curvature(V,F)
% MY_DISCRETE_GAUSSIAN_CURVATURE Compute discrete gaussian curvature
% using the angle defect
%
% k = my_discrete_gaussian_curvature(V,F)
%
% Inputs:
%   V  #V by 3 list of vertex positions
%   F  #F by 3 list of face indies
% Outputs:
%   k  #V by 1 list of discrete gaussian curvature values
%

k = 2*pi*ones(size(V,1),1);

%   for i=1:size(F,1)
%       for j=1:3
%           e1 = V(F(i,mod(j,3)+1),:) - V(F(i,j),:);
%           e2 = V(F(i,mod(j+1,3)+1),:) - V(F(i,j),:);
%           e1 = e1 / norm(e1);
%           e2 = e2 / norm(e2);
%           k(F(i,j)) = k(F(i,j)) - acos(e1*e2');
%       end
%   end

for i=1:size(F,1)
    e1 = V(F(i,2),:) - V(F(i,1),:);
    e2 = V(F(i,3),:) - V(F(i,1),:);
    e3 = V(F(i,3),:) - V(F(i,2),:);
    
    e1 = e1 / norm(e1);
    e2 = e2 / norm(e2);
    e3 = e3 / norm(e3);
    
    k(F(i,1)) = k(F(i,1)) - acos(e1*e2');
%     
%     e1 = V(F(i,3),:) - V(F(i,2),:);
%     e2 = V(F(i,1),:) - V(F(i,2),:);
%     e1 = e1 / norm(e1);
%     e2 = e2 / norm(e2);
%     k(F(i,2)) = k(F(i,2)) - acos(e1*e2');
    k(F(i,2)) = k(F(i,2)) - acos(-e3*e1');
    
    e1 = V(F(i,1),:) - V(F(i,3),:);
    e2 = V(F(i,2),:) - V(F(i,3),:);
    e1 = e1 / norm(e1);
    e2 = e2 / norm(e2);
    k(F(i,3)) = k(F(i,3)) - acos(e1*e2');
end

% for t=1:size(F,1) %loops through each triagle
%     e1=V(F(t,2),:)-V(F(t,1),:); %finds each edge of triangle t
%     e2=V(F(t,3),:)-V(F(t,2),:);
%     e3=V(F(t,1),:)-V(F(t,3),:);
%
%     e1 = e1/norm(e1);
%     e2 = e2/norm(e2);
%     e3 = e3/norm(e3);
%
%     %finds theta between each pair of edges and subtracts from 2pi to vetex in common
%     k(F(t,1)) = k(F(t,1)) - acos(dot(e1,e3));
%     k(F(t,2)) = k(F(t,2)) - acos(dot(e1,e2));
%     k(F(t,3)) = k(F(t,3)) - acos(dot(e3,e2));
% end

end
