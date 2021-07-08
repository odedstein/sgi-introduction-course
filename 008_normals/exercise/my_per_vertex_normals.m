function N = my_per_vertex_normals(V,F,varargin)
  % MY_PER_VERTEX_NORMALS  Compute per-vertex (area-weighted) normals over a mesh % (V,F)
  %
  % N = per_vertex_normals(V,F)
  %
  % Inputs:
  %   V  #V by 3 list of vertex positions
  %   F  #F by 3 list of triangle indices
  % Outputs:
  %   N  #V by 3 list of vertex normals, area-weighted
  %

  %Compute per-face normals.
  FN = normalizerow(normals(V,F));
  
  %Average to compute per-vertex normals.
  N = ...

end
