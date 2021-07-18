function Pt = cubic_hermite(P0,P1,M0,M1,t)
% Given a pair of points and a pair of vectors, compute the cubic Hermite
% polynomial they define and evaluate it at time t

Pt = (2.*t.^3 - 3.*t.^2 + 1).*P0 + (t.^3 - 2.*t.^2 + t).*M0 + ...
    (-2.*t.^3 + 3.*t.^2).*P1 + (t.^3 - t.^2).*M1;

end