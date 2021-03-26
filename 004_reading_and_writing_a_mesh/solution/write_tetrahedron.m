function write_tetrahedron()
%WRITE_TETRAHEDRON  write a tetrahedron to the file "tetrahedron.obj".
%
% write_tetrahedron();
%

V = [0, 0, 0; 1, 0, 0; 0, 1, 0; 0, 0, 1];
F = [1, 2, 3; 1, 2, 4; 2, 3, 4; 3, 1, 4];
writeOBJ('tetrahedron.obj', V, F);

end

