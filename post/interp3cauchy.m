function stress = interp3cauchy(Xw, Yw, Zw, FXw, FYw, FZw)
%INTERP3CAYCHY Computes the local stress tensor at each point in a 3D grid.
%
% stress = interp3cauchy(Xw, Yw, Zw, FXw, FYw, FZw)
%
% This function calculates the local stress tensor at each grid point
% in a non-uniform 3D grid using the given force components at each point.
% The calculated stress tensor reflects the mechanical state of the grid.
%
% Inputs:
% - Xw, Yw, Zw: 3D matrices containing the x, y, and z coordinates of the grid points.
% - FXw, FYw, FZw: 3D matrices containing the x, y, and z components of the force at each grid point.
%
% Output:
% - stress: 4D array where the first three dimensions correspond to the size
%           of the input grid (minus one in each dimension to avoid index overflow),
%           and the fourth dimension contains the 9 components of the
%           local stress tensor for each grid cell (flattened 3x3 tensor).
%
% Example:
% [Xw,Yw,Zw] = meshgrid(1:0.1:2, 1:0.2:3, 1:0.3:2);
% FXw = rand(size(Xw));
% FYw = rand(size(Yw));
% FZw = rand(size(Zw));
% stress = interp3virial(Xw, Yw, Zw, FXw, FYw, FZw);
%
%
% === Interpretation and comparison with Cauchy tensor definition ===
%
% In continuum mechanics, the Cauchy stress tensor, often represented by the symbol
% \( \sigma \), is a second-order tensor describing the stress state at a given point
% in a material. The Cauchy stress tensor is defined as follows:
% 
% \[
% \sigma_{ij} = \lim_{{\Delta A \to 0}} \frac{\Delta F_j}{\Delta A_i}
% \]
% 
% where \( \Delta F_j \) is the force in the \( j \) direction acting on a differential
% area \( \Delta A_i \) oriented along the \( i \) direction. The indices \( i \) and
% \( j \) run from 1 to 3, referring to the spatial dimensions \( x, y, z \).
% 
% In the code, the variable `local_tensor` serves as the Cauchy stress tensor
% for a particular grid cell. For this tensor, the components are computed as:
% 
% \[
% \text{local\_tensor}(\alpha, \beta) = \frac{F_{\text{avg}}(\alpha) \times 
% n_{\beta}(\beta)}{A(\beta)}
% \]
% 
% Here, \( F_{\text{avg}}(\alpha) \) is the average force in the \( \alpha \)
% direction acting on the cell, \( n_{\beta}(\beta) \) is the normal vector to 
% the face of the cell in the \( \beta \) direction, and \( A(\beta) \) is the area
% of the face in the \( \beta \) direction.
% 
% ### Comparison of Indices
% In the Matlab implementation, the components of `local_tensor(alpha, beta)` 
% essentially represent \( \sigma_{\alpha \beta} \) if \( \alpha, \beta \) refer to the 
% \( x, y, z \) directions. In other words, \( \alpha = i \) and \( \beta = j \).
% 
% It's important to note that Matlab uses 1-based indexing, so the components
% \( \sigma_{11}, \sigma_{12}, \sigma_{13}, \ldots, \sigma_{33} \) in continuum 
% mechanics are stored as `local_tensor(1,1), local_tensor(2,1),
% local_tensor(3,1), ..., local_tensor(3,3)` in Matlab.
% 
% So, in conclusion, `local_tensor` in the Matlab code is essentially the Cauchy stress
% tensor \( \sigma \), and its components are consistent with the definitions used
% in continuum mechanics, albeit with 1-based indexing with the following rule:
% first dimension = normal direction, second = considered force component.



% MS 3.0 | 2023-09-09 | INRAE\Olivier.vitrac@agroparistech.fr | rev.

% Revision history

% Check argument compatibility
if nargin~=6, error('Six arguments are required: stress = interp3virial(Xw, Yw, Zw, FXw, FYw, FZw)'), end
if any(size(Xw) ~= size(Yw)) || any(size(Yw) ~= size(Zw)) || ...
        any(size(FXw) ~= size(FYw)) || any(size(FYw) ~= size(FZw)) || ...
        any(size(Xw) ~= size(FXw))
    error('Dimension mismatch among the input matrices.');
end
% Pre-check to ensure Xw, Yw, Zw are meshgrid-generated
tolerance = 1e-10;  % Tolerance for checking uniform increments
if ~all(std(diff(Xw(:,1,1), 1, 1), 0, 2,'omitnan') < tolerance) || ...
   ~all(std(diff(Yw(1,:,1), 1, 2), 0, 1, 'omitnan') < tolerance) || ...
   ~all(std(diff(Zw(1,1,:), 1, 3), 0, 3, 'omitnan') < tolerance)
    error('Input matrices Xw, Yw, and Zw must be generated using meshgrid');
end

% Initialize 4D array to store local stress tensor for each cell
% Dimensions: size(Xw) x 9 (flattened 3x3 tensor)
stress = NaN([size(Xw), 9],class(FXw));

% Loop through all grid points except the last in each dimension
% to avoid index overflow
[ny,nx,nz] = size(Xw);
dispf('Calculate the local Cauchy stress from a [%d x %d x %d] grid...',ny,nx,nz)
t0 = clock; %#ok<CLOCK>

for iy = 1:ny
    for ix = 1:nx
        for iz = 1:nz

            % Initialize local tensor
            local_tensor = zeros(3, 3);

            % Edge cases for dx, dy, dz
            dx = Xw(iy, min(ix+1,nx), iz) - Xw(iy, ix, iz);
            dy = Yw(min(iy+1,ny), ix, iz) - Yw(iy, ix, iz);
            dz = Zw(iy, ix, min(iz+1,nz)) - Zw(iy, ix, iz);

            % Calculate area of each face of this cell
            A = [dy * dz, dx * dz, dx * dy];  % Face areas


            % Calculate tensor components for each face considering only the four vertices of the face

            for beta = 1:3 % -> direction beta=1 (x-face), beta=2 (y-face), beta=3 (z-face)
                
                %vert_idx = []; vert_idy = []; vert_idz = [];
                % Define the indices for the 4 vertices constituting each face
                if beta == 1 && iy < ny && iz < nz
                    vert_idx = repmat(ix, 1, 4);
                    vert_idy = [iy, iy, iy+1, iy+1];
                    vert_idz = [iz, iz+1, iz, iz+1];
                elseif beta == 2 && ix < nx && iz < nz
                    vert_idy = repmat(iy, 1, 4);
                    vert_idx = [ix, ix+1, ix, ix+1];
                    vert_idz = [iz, iz, iz+1, iz+1];
                elseif beta == 3 && ix < nx && iy < ny
                    vert_idz = repmat(iz, 1, 4);
                    vert_idx = [ix, ix+1, ix, ix+1];
                    vert_idy = [iy, iy, iy+1, iy+1];
                else
                    continue;  % Skip, as it's the edge of the grid
                end

                % Translate to 1D indices for force matrices
                ind = sub2ind([ny, nx, nz], vert_idy, vert_idx, vert_idz);

                for alpha = 1:3 % -> force component

                    % Compute average force on vertices
                    if alpha == 1
                        F_alpha_avg = mean(FXw(ind), 'omitnan');
                    elseif alpha == 2
                        F_alpha_avg = mean(FYw(ind), 'omitnan');
                    elseif alpha == 3
                        F_alpha_avg = mean(FZw(ind), 'omitnan');
                    end

                    if isnan(F_alpha_avg), continue; end

                    % Update the stress tensor component
                    local_tensor(beta, alpha) = F_alpha_avg / A(beta);

                end % next alpha

            end % next beta

            % Store this tensor
            stress(iy, ix, iz, :) = local_tensor(:);
        end
    end
end

dispf('\t ... done in %0.3g s',etime(clock,t0)) %#ok<DETIM,CLOCK>
