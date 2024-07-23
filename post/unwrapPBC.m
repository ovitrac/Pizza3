function Xunwrapped = unwrapPBC(X, Pshift, box, PBC)
%UNWRAPBC Unwrap atom coordinates in a periodic box
%
%   USAGE: Xunwrapped = unwrapPBC(X, Pshift, box, PBC)
%
%   This function unwraps the coordinates of atoms in a periodic simulation
%   box after they have been wrapped due to periodic boundary conditions.
%   It is designed to handle large sets of atom coordinates efficiently
%   through vectorized operations. This function should be used when atoms
%   undergo displacements that might cause them to cross periodic boundaries,
%   ensuring that their continuous trajectory is accurately represented.
%
%   INPUTS:
%       X: nx2 or nx3 array coding for the initial coordinates of the n particles
%          in 2D and 3D, respectively.
%    Pshift: 1x2 or 1x3 array coding for the translation applied to the coordinates,
%            which is subject to periodic wrapping.
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
%   Example:
%       % Define initial positions, a periodic shift, and box dimensions
%       X = [1.0, 1.5; 0.5, 2.0]; % Example in 2D
%       Pshift = [0.5, 0.0]; % Shift right by 0.5 units
%       box = [0, 3; 0, 3]; % Square box with sides of length 3
%       Xunwrapped = unwrapPBC(X, Pshift, box);
%       disp('Unwrapped Coordinates:');
%       disp(Xunwrapped);
%
%   This function is part of a suite designed to facilitate simulations and
%   analyses using periodic boundary conditions. It relies on MATLAB's ability
%   to perform array operations efficiently and is optimized for handling
%   large numbers of particles.
%
%   MS 3.1 | 2024-04-04 | INRAE\olivier.vitrac@agroparistech.fr | rev.
%
%   Revision history:
%       2024-04-04 - Initial version


    % Apply the periodic shift and wrapping
    %[Xwrapped, ~] = PBCimagesshift(X, Pshift, box);
    Xwrapped = PBCincell(X+Pshift, box, PBC);
    
    % Calculate the box lengths in each dimension
    boxLength = diff(box, 1, 2);
    
    % Calculate displacement as the difference between wrapped and initial positions
    displacement = Xwrapped - X;
    
    % Identify atoms that crossed the boundary and adjust the displacement accordingly
    for j = 1:size(X, 2)
        positiveCross = displacement(:, j) > boxLength(j) / 2;
        negativeCross = displacement(:, j) < -boxLength(j) / 2;
        
        displacement(positiveCross, j) = displacement(positiveCross, j) - boxLength(j);
        displacement(negativeCross, j) = displacement(negativeCross, j) + boxLength(j);
    end
    
    % Adjust the positions to get the unwrapped coordinates
    Xunwrapped = X + displacement;

end
