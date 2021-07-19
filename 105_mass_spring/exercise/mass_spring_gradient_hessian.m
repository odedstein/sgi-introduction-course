function [G,H] = mass_spring_gradient_hessian(V,E,k,U)

  % Compute the gradient and hessian of a mass-spring system defined for (V,E)
  % with the stiffness k and displacement U
  % Inputs:
  %   V  #V by 2 list of rest curve vertex positions
  %   E  #E by 2 list of edge indices
  %   k  scalar spring stiffness parameter
  %   U  #V by 2 list of deformed curve vertex displacements from the rest pose
  % Outputs:
  %   G  #V*2 list of gradient vectors per vertex defined at the current deformed position
  %   H  #V*2 by #V*2 hessian matrix defined at the current deformed position

  assert(size(E,2) == 2);
  U = reshape(U,size(V));
  
  % rest edge lengths
  LV = edge_lengths(V,E);
  LU = edge_lengths(U,E);
  f = k*0.5*sum((LV-LU).^2);

  if nargout==0
    return;
  end

  I = E(:,2);
  J = E(:,1);
  T0 = U(I,:) - U(J,:);
  t1 = normrow(T0);

  GI = ((t1-LV)./t1).*T0;
  GJ = -GI;

  dim = size(V,2);
  G = k*full(sparse([repmat(I,1,dim) repmat(J,1,dim)],repmat(1:dim,size(E,1),2),[GI GJ],size(V,1),dim));
  G = G(:); % to match the dimension: not sure if correct

  if nargout==1
    return;
  end

  % Outer product
  vec = @(X) X(:);
  T2 = T0(:,vec(repmat(1:dim,dim,1))').*T0(:,vec(repmat(1:dim,1,dim))');
  t3 = t1 - LV;

  HIJ = (t3./(t1.^3) - 1./(t1.^2)).*T2 - t3./t1.*(vec(eye(dim))');
  HII = -HIJ;
  HJJ = -HIJ;
  HJI = HIJ;
  n = size(V,1);
  H = sparse(n*dim,n*dim);
  for ii = 1:dim
    for jj = 1:dim
      oi = (ii-1)*dim+jj;
      Hiijj = sparse( ...
        [I I J J],[I J I J],[HII(:,oi) HIJ(:,oi) HJI(:,oi) HJJ(:,oi)],n,n);
      H(((ii-1)*n)+(1:n),((jj-1)*n)+(1:n)) = Hiijj;
    end
  end
  H = k*H;

end
