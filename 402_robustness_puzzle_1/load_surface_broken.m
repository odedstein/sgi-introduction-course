V = importdata('data/V.dat');
F = importdata('data/F.dat');

% Doesn't work... figure out why not and fix it!
% NOTE: You *do not* need to edit the `tsurf` function
% itself. This can be fixed by modifying the `F` and/or `V`
% matrices loaded above.
tsurf(F,V)