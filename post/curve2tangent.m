function XYt = curve2tangent(XY)
%CURVE2TANGENT Calculate the tangent of a curve XY using a second-order and centered approximation scheme
%
% Syntax: XYt = curve2tagent(XY)
%   XY is a Nx2 or Nx3 matrix where N is the number of points
%   XYt is a Nx2 or Nx3 matrix containing the coordinates of the tangent vector at each point
%
% The tangent vector is computed using a centered difference method for interior points.
% For the endpoints, forward and backward differences are used.
%
% MS 3.0 | 2024-03-27 | INRAE\han.chen@inrae.fr, INRAE\Olivier.vitrac@agroparistech.fr | rev.


% Determine the number of points and dimensionality
[N, dim] = size(XY);

% Initialize the output matrix
XYt = zeros(N, dim);

% Calculate tangents for interior points using centered differences
for i = 2:N-1
    XYt(i, :) = (XY(i+1, :) - XY(i-1, :)) / 2;
end

% Calculate tangent for the first point using forward difference
XYt(1, :) = (XY(2, :) - XY(1, :));

% Calculate tangent for the last point using backward difference
XYt(N, :) = (XY(N, :) - XY(N-1, :));

% Normalize the tangent vectors
for i = 1:N
    XYt(i, :) = XYt(i, :) / norm(XYt(i, :));
end
