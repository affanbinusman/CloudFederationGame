function [V,D, x, y, c] = eigFunc(A)
%returns diagonal matrix D of eigenvalues and matrix V 
% whose columns are the corresponding right eigenvectors, 
% so that A*V = V*D.

cvx_begin
    variables y(3) w
    maximize w
    subject to
		3*y(1) + 2*y(2) + 4*y(3) >= w    
        4*y(1) + 6*y(2) + 1*y(3) >= w    
        1*y(1) + 4*y(2) + 2*y(3) >= w    
        y(1) + y(2) + y(3) == 1   
        y(1) >= 0
        y(2) >= 0
        y(3) >= 0
cvx_end

cvx_begin
    variables z(3) v
    maximize v
    subject to
        -3*z(1) - 2*z(2) - 4*z(3) >= v
        -4*z(1) - 6*z(2) - 1*z(3) >=v
        -1*z(1) - 4*z(2) - 2*z(3) >=v
		z(1) + z(2) + z(3) == 1   
        z(1) >= 0
        z(2) >= 0
        z(3) >= 0
cvx_end

c = y;

x = "it workssss";
y = 006900;
% [V, D] = eig(A);
V = A
end

