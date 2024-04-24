function Xincell = PBCincell(X,box,PBC)
%PBCINCELL force incell coordinates (without X coordinates outside the box along perodic coordinates)
%
%   USAGE: Xincell = PBCincell(X,box,PBC)
%
%   INPUTS:
%          X: nx2 or nx3 array coding for the coordinates of the n particles in 2D and 3D, respectively
%        box: 2x2 or 3x2 array coding for box dimensions
%             the box spans along dimension i between box(i,1) and box(i,2)
%        PBC: 1x2 or 1x3 boolean array
%             PBC(i) is true if the dimension i is periodic
%
%   OUTPUTS:
%    Xincell: nx2 or nx3 array coding for the coordinates incell
%
%
%
%   See also: PBCgrid, PBCgridshift, PBCimages, PBCimageschift, PBCincell



% MS 3.0 | 2024-03-16 | INRAE\han.chen@inrae.fr, INRAE\Olivier.vitrac@agroparistech.fr |


% Revision history


% Initialize the output array with the same size as input coordinates
Xincell = X;

% Number of dimensions (2D or 3D)
dims = size(X, 2);

% Loop over each dimension to apply periodic boundary conditions
for i = 1:dims
    if PBC(i)
        % Get the box size for the current dimension
        boxSize = box(i, 2) - box(i, 1);
        % Adjust positions for periodic boundary conditions
        % Use mod to wrap coordinates within the box dimensions
        Xincell(:, i) = mod(X(:, i) - box(i, 1), boxSize) + box(i, 1);
    end
end
