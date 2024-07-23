function [XYZout, isReunitedout] = PBCoutcell(XYZ, box, PBC)
%PBCOUTCELL reunite atoms crossing PBC boundaries on one side based on the centroid's location
%
%   USAGE: XYZout = PBCoutcell(XYZ, box, PBC)
%          [XYZout, isReunited] = PBCoutcell(...)
%
%   INPUTS:
%          XYZ: nx2 or nx3 array coding for the coordinates of the n atoms in 2D or 3D
%          box: 2x2 or 3x2 array coding for box dimensions
%               the box spans along dimension i between box(i,1) and box(i,2)
%          PBC: 1x2 or 1x3 boolean array
%               PBC(i) is true if the dimension i is periodic
%
%   OUTPUT:
%       XYZout: nx2 or nx3 array with coordinates adjusted to reunite atoms on one side of the boundaries
%   isReunited: true if reunion has been applied

% Example in 2D:
%{
    % Box limits
    box = [0 10; 0 10];
    % PBC in both dimensions
    PBC = [true, true];
    % Generate random points in a disk
    n_particles = 10000;
    radius = 0.55 * min(box(:,2) - box(:,1)) / 2;
    theta = 2 * pi * rand(n_particles, 1);
    r = radius * sqrt(rand(n_particles, 1));
    center = (box(:,2) - box(:,1))' .* rand(1, 2) + box(:,1)';
    XYZ0 = [center(1) + r .* cos(theta), center(2) + r .* sin(theta)];
    % Apply PBC to bring coordinates within the box
    XYZ = PBCincell(XYZ0,box,PBC);
    XYZout = PBCoutcell(XYZ, box, PBC);
    % Plotting
    figure, hold on
    plot(XYZ0(:,1), XYZ0(:,2), 'g.', 'MarkerSize', 10); % OUTCELL Original points in green
    plot(XYZ(:,1), XYZ(:,2), 'r.', 'MarkerSize', 10); % Original INCELL points in red
    plot(XYZout(:,1), XYZout(:,2), 'b.', 'MarkerSize', 10); % Adjusted points in blue
    xlabel('X'); ylabel('Y'); title('Reunited Atoms in 2D');
    legend('True', 'Original', 'Adjusted');
    grid on; axis equal; hold off;
%}
%
% Example in 3D:
%{
    % Box limits
    box = [0 10; 0 10; 0 10];
    % PBC in all dimensions
    PBC = [true, true, true];
    % Generate random points in a sphere
    n_particles = 10000;
    radius = 4.4*0.25 * min(box(:,2) - box(:,1)) / 2;
    phi = 2 * pi * rand(n_particles, 1);
    costheta = 2 * rand(n_particles, 1) - 1;
    u = rand(n_particles, 1);
    theta = acos(costheta);
    r = radius * u.^(1/3);
    center = (box(:,2) - box(:,1))' .* rand(1, 3) + box(:,1)';
    XYZ0 = [center(1) + r .* sin(theta) .* cos(phi), ...
           center(2) + r .* sin(theta) .* sin(phi), ...
           center(3) + r .* cos(theta)];
    % Apply PBC to bring coordinates within the box
    XYZ = PBCincell(XYZ0,box,PBC)
    XYZout = PBCoutcell(XYZ, box, PBC);
    figure, hold on
    plot3(XYZ0(:,1), XYZ0(:,2), XYZ0(:,3), 'g.', 'MarkerSize', 10); % OUTCELL Original points in green
    plot3(XYZ(:,1), XYZ(:,2), XYZ(:,3), 'r.', 'MarkerSize', 10); % Original INCELL points in red
    plot3(XYZout(:,1), XYZout(:,2), XYZout(:,3), 'b.', 'MarkerSize', 10); % Adjusted points in blue
    xlabel('X'); ylabel('Y'); zlabel('Z'); title('Reunited Atoms in 3D');
    legend('True','Original', 'Adjusted');
    grid on; axis equal; view(3); hold off;
%}


[n, d] = size(XYZ);

% Validate inputs
if size(box, 2) ~= 2 || size(box, 1) ~= d
    error('Box dimensions must be a %dx2 vector', d);
end

if length(PBC) ~= d
    error('PBC must be a 1x%d logical vector', d);
end

% Calculate the center of the box
box_center = mean(box, 2)';

% Initialize output
XYZout = XYZ;
isReunited = false;

% Maximum iterations to avoid infinite loops
max_iters = 10;
iter = 0;

while iter < max_iters
    iter = iter + 1;
    XYZout_prev = XYZout;

    % Calculate the centroid of the points
    centroid = mean(XYZout, 1);

    % Adjust coordinates based on the centroid's location
    for i = 1:d
        if PBC(i)
            box_length = box(i, 2) - box(i, 1);
            for j = 1:n
                if abs(XYZout(j, i) - centroid(i)) > box_length / 2
                    if XYZout(j, i) > centroid(i)
                        XYZout(j, i) = XYZout(j, i) - box_length;
                    else
                        XYZout(j, i) = XYZout(j, i) + box_length;
                    end
                end
            end
        end
    end

    % Recalculate the centroid
    new_centroid = mean(XYZout, 1);

    % If the output is stable, break the loop
    if isequal(XYZout, XYZout_prev)
        break;
    end

    % Update the centroid
    centroid = new_centroid;
end

% Calculate the inertia before and after adjustment
initial_inertia = sum(sum((XYZ - mean(XYZ, 1)).^2));
adjusted_inertia = sum(sum((XYZout - mean(XYZout, 1)).^2));

% If the adjusted inertia is larger, revert to the original coordinates
if adjusted_inertia >= initial_inertia
    XYZout = XYZ;
    isReunited = false;
else
    isReunited = true;
end

if nargout > 1
    isReunitedout = isReunited;
end

end


% function [XYZout,isReunitedout] = PBCoutcell(XYZ, box, PBC)
% %PBCOUTCELL reunite atoms crossing PBC boundaries on one side based on the centroid's location
% %
% %   USAGE: XYZout = PBCoutcell(XYZ, box, PBC)
% %          [XYZout,isreunited] = PBCoutcell(...)
% %
% %   INPUTS:
% %          XYZ: nx2 or nx3 array coding for the coordinates of the n atoms in 2D or 3D
% %          box: 2x2 or 3x2 array coding for box dimensions
% %               the box spans along dimension i between box(i,1) and box(i,2)
% %          PBC: 1x2 or 1x3 boolean array
% %               PBC(i) is true if the dimension i is periodic
% %
% %   OUTPUT:
% %       XYZout: nx2 or nx3 array with coordinates adjusted to reunite atoms on one side of the boundaries
% %   isreunited: true if reunion has been applied
% 
% %   Example in 2D:
% %{
%     % Box limits
%     box = [0 10; 0 10];
%     % PBC in both dimensions
%     PBC = [true, true];
%     % Generate random points in a disk
%     n_particles = 10000;
%     radius = 0.35 * min(box(:,2) - box(:,1)) / 2;
%     theta = 2 * pi * rand(n_particles, 1);
%     r = radius * sqrt(rand(n_particles, 1));
%     center = (box(:,2) - box(:,1))' .* rand(1, 2) + box(:,1)';
%     XYZ0 = [center(1) + r .* cos(theta), center(2) + r .* sin(theta)];
%     % Adjust coordinates
%     XYZ = PBCincell(XYZ0,box,PBC);
%     XYZout = PBCoutcell(XYZ, box, PBC);
%     % Plotting
%     figure, hold on
%     plot(XYZ(:,1), XYZ(:,2), 'r.', 'MarkerSize', 10); % Original points in red
%     plot(XYZout(:,1), XYZout(:,2), 'b.', 'MarkerSize', 10); % Adjusted points in blue
%     xlabel('X'); ylabel('Y'); title('Reunited Atoms in 2D');
%     legend('Original', 'Adjusted');
%     grid on; axis equal; hold off;
% %}
% %
% %   Example in 3D:
% %{
%     % Box limits
%     box = [0 10; 0 10; 0 10];
%     % PBC in all dimensions
%     PBC = [true, true, true];
%     % Generate random points in a sphere
%     n_particles = 10000;
%     radius = 0.25 * min(box(:,2) - box(:,1)) / 2;
%     phi = 2 * pi * rand(n_particles, 1);
%     costheta = 2 * rand(n_particles, 1) - 1;
%     u = rand(n_particles, 1);
%     theta = acos(costheta);
%     r = radius * u.^(1/3);
%     center = (box(:,2) - box(:,1))' .* rand(1, 3) + box(:,1)';
%     XYZ0 = [center(1) + r .* sin(theta) .* cos(phi), ...
%            center(2) + r .* sin(theta) .* sin(phi), ...
%            center(3) + r .* cos(theta)];
%     % Adjust coordinates
%     XYZ = PBCincell(XYZ0,box,PBC)
%     XYZout = PBCoutcell(XYZ, box, PBC);
%     figure, hold on
%     plot3(XYZ0(:,1), XYZ0(:,2), XYZ0(:,3), 'g.', 'MarkerSize', 10); % OUTCELL Original points in green
%     plot3(XYZ(:,1), XYZ(:,2), XYZ(:,3), 'r.', 'MarkerSize', 10); % Original INCELL points in red
%     plot3(XYZout(:,1), XYZout(:,2), XYZout(:,3), 'b.', 'MarkerSize', 10); % Adjusted points in blue
%     xlabel('X'); ylabel('Y'); zlabel('Z'); title('Reunited Atoms in 3D');
%     legend('True','Original', 'Adjusted');
%     grid on; axis equal; view(3); hold off;
% %}
% 
% 
% % MS 3.0 | 2024-07-16 | INRAE\han.chen@inrae.fr, INRAE\Olivier.vitrac@agroparistech.fr | rev. 
% 
% 
% % Revision history
% 
% 
% % Number of atoms and dimensions
% [n, d] = size(XYZ);
% 
% % Validate inputs
% if size(box,2) ~= 2 || size(box,1) ~= d
%     error('Box dimensions must be a %dx2 vector', d);
% end
% 
% if length(PBC) ~= d
%     error('PBC must be a 1x%d logical vector', d);
% end
% 
% % Calculate the centroid of the object
% centroid = mean(XYZ, 1);
% 
% % Calculate the initial inertia
% initial_inertia = sum(sum((XYZ - centroid).^2));
% 
% % Initialize output
% XYZout = XYZ;
% 
% % Adjust coordinates based on the centroid's half-space
% for i = 1:d
%     if PBC(i)
%         box_length = box(i,2) - box(i,1);
%         half_box_length = box_length / 2;
%         centroid_half_space = (centroid(i) > (box(i,1) + half_box_length));
% 
%         % Check and adjust atoms' coordinates
%         for j = 1:n
%             if centroid_half_space
%                 % If centroid is in the upper half-space, move atoms in the lower half-space up
%                 if XYZ(j,i) < (box(i,1) + half_box_length)
%                     XYZout(j,i) = XYZout(j,i) + box_length;
%                 end
%             else
%                 % If centroid is in the lower half-space, move atoms in the upper half-space down
%                 if XYZ(j,i) > (box(i,1) + half_box_length)
%                     XYZout(j,i) = XYZout(j,i) - box_length;
%                 end
%             end
%         end
%     end
% end
% 
% % Calculate the adjusted inertia
% adjusted_inertia = sum(sum((XYZout - mean(XYZout, 1)).^2));
% 
% % If the adjusted inertia is larger, revert to the original coordinates
% if adjusted_inertia >= initial_inertia
%     XYZout = XYZ;
%     isReunited = false;
% else
%     isReunited = true;
% end
% 
% if nargout>1, isReunitedout = isReunited; end
% 
% end