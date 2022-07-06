function V = get_pencil_spline(n)
% This function will prompt the user to draw a coarse polyline on a figure
% window and then will upsample it into a very fine curve by sampling new
% points in the Catmull-Rom spline described by the points of the polyline.

% First, obtain coarse points by calling get_pencil_curve
V_coarse = get_pencil_curve();

% Now, create n equally spaced points between 0 and 1
t = linspace(0,1,n);

% Use a catmull-rom spline to interpolate at times t between the points in
% V_coarse
% 
%
%
%
% THIS IS FOR YOU TO FILL OUT
%
%
%
%
% At the end, you can plot(V) to see if your solution is correct.

end