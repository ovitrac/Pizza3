function trajunwrapped = trajunwrap(traj, box)
%UNWRAP Unwrap trajectorycoordinates in a periodic box
%
%   USAGE: trajunwrapped = trajunwrap(traj, box, PBC)
%
%   This function unwraps the coordinates of atoms in a periodic simulation
%   box after they have been wrapped due to periodic boundary conditions.
%   It is designed to handle large sets of atom coordinates efficiently
%   through vectorized operations. This function should be used when atoms
%   undergo displacements that might cause them to cross periodic boundaries,
%   ensuring that their continuous trajectory is accurately represented.
%
%   INPUTS:
%      traj: nx2 or nx3 array coding for the initial coordinates of the n particles
%          in 2D and 3D, respectively.
%       box: 2x2 or 3x3 array coding for the dimensions of the periodic simulation box.
%            The box spans along dimension i between box(i,1) and box(i,2).
%            It is assumed that all X values initially lie within these box limits.
%       PBC: 1x2 or 1x3 flags (PBC(j) is true if the jth dimension is periodic)
%
%   OUTPUTS:
%    Xunwrapped: nx2 or nx3 array coding for the unwrapped coordinates of the particles,
%                reflecting their continuous trajectory across periodic boundaries.
%
%
%   See also: PBCimagesshift, PBCgrid, PBCgridshift, PBCimages, PBCincell
%
%
%
%   MS 3.1 | 2024-04-05 | INRAE\olivier.vitrac@agroparistech.fr | rev.
%
%   Revision history:
%       2024-04-05 - Initial version

% Calculate the box lengths in each dimension
boxLength = diff(box, 1, 2);

% Calculate displacement as the difference between wrapped and initial positions
displacement = [zeros(size(traj(1,:))) ; diff(traj,1,1) ];
    
% Identify atoms that crossed the boundary and adjust the displacement accordingly
for j = 1:size(displacement, 2)
    positiveCross = displacement(:, j) > boxLength(j) / 2;
    negativeCross = displacement(:, j) < -boxLength(j) / 2;

    displacement(positiveCross, j) = displacement(positiveCross, j) - boxLength(j);
    displacement(negativeCross, j) = displacement(negativeCross, j) + boxLength(j);
end

% Adjust the positions to get the unwrapped coordinates
trajunwrapped = traj(1,:) + cumsum(displacement,1);

end
