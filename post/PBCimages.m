function [Ximages,indXout] = PBCimages(X,box,PBC,cutoff)
%PBCIMAGES return the coordinates of fictive particle images outside box limits along periodic boundary dimensions
%
%   USAGE: Ximages = PBCimages(X,box,PBC [,cutoff])
%          [Ximages,indX] = PBCimages(...)
%
%   INPUTS:
%          X: nx2 or nx3 array coding for the coordinates of the n particles in 2D and 3D, respectively
%        box: 2x2 or 3x2 array coding for box dimensions
%             the box spans along dimension i between box(i,1) and box(i,2)
%             all X values should lie within box limits, if not an error ois generated
%        PBC: 1x2 or 1x3 boolean array
%             PBC(i) is true if the dimension i is periodic
%     cutoff: scalar or 1xd array with d the number of dimensions (2 or 3)
%             setting the cutoff distance beyond bounds to include fictive images
%             if cutoff is a scalar, it is refedined as cutoff(ones(1,d))
%             cutoff(i) is applied along dimension i
%
%   OUTPUTS:
%    Ximages: mx2 or mx3 array coding for the coordinates of the m particle images in 2D and 3D, respectively
%       indX: corresponding indices of images in X
%
%
%   See also: PBCgrid, PBCgridshift, PBCimageschift, PBCincell
%

% Full example in 2D
%{
    % Parameters
    n_particles = 10000;
    box = [0 10; 0 10]; % Box limits for 2D
    PBC = [true, true]; % Periodic boundary conditions in both dimensions
    cutoff = 3.0; % Cutoff distance
    
    % Generate random particles within the box
    X = rand(n_particles, 2) .* (box(:,2) - box(:,1))' + box(:,1)';
    
    % Calculate fictive images
    Ximages = PBCimages(X, box, PBC, cutoff);
    
    % Plotting
    figure, hold on
    plot(X(:,1), X(:,2), 'g.', 'MarkerSize', 15); % Original particles in green
    if ~isempty(Ximages)
        plot(Ximages(:,1), Ximages(:,2), 'b.', 'MarkerSize', 15); % Images in blue
    end
    xlim([box(1,1) - 2*cutoff, box(1,2) + 2*cutoff]);
    ylim([box(2,1) - 2*cutoff, box(2,2) + 2*cutoff]);
    xlabel('X');
    ylabel('Y');
    title('Original Particles and Their Fictive Images');
    legend('Original Particles', 'Fictive Images');
    grid on;
    hold off;
    axis equal
%}

% Full example in 3D
%{
    % Parameters
    n_particles = 10000;
    box = [0 10; 0 10; 0 10]; % Box limits for 3D
    PBC = [true, true, true]; % Periodic boundary conditions in both dimensions
    cutoff = 3.0; % Cutoff distance
    
    % Generate random particles within the box
    X = rand(n_particles, 3) .* (box(:,2) - box(:,1))' + box(:,1)';
    
    % Calculate fictive images
    Ximages = PBCimages(X, box, PBC, cutoff);
    
    % Plotting
    figure, hold on
    plot3(X(:,1), X(:,2), X(:,3), 'g.', 'MarkerSize', 15); % Original particles in green
    plot3(Ximages(:,1), Ximages(:,2),Ximages(:,3), 'b.', 'MarkerSize', 15); % Images in blue
    xlim([box(1,1) - 2*cutoff, box(1,2) + 2*cutoff]);
    ylim([box(2,1) - 2*cutoff, box(2,2) + 2*cutoff]);
    zlim([box(3,1) - 2*cutoff, box(3,2) + 2*cutoff]);
    xlabel('X'); ylabel('Y'); ylabel('Z'); title('Original Particles and Their Fictive Images');
    legend('Original Particles', 'Fictive Images');
    grid on, hold off, axis equal, view(3)
%}


% MS 3.0 | 2024-03-15 | INRAE\han.chen@inrae.fr, INRAE\Olivier.vitrac@agroparistech.fr | rev. 2024-03-16


% Revision history
% 2024-03-15 release canidate with examples in 2D and 3D
% 2024-03-16 return indX, advise using PBCincell if particles outside are detected

%% Check arguments
if nargin<3, error('Not enough input arguments. Syntax: Ximages = PBCimages(X,box,PBC [,cutoff])'), end
if nargin<4, cutoff = []; end
[n,d] = size(X); % Number of particles and dimensions
if d>3, error('the number of dimensions should be 1,2,3'), end
Xmin = min(X);
Xmax = max(X);
if isempty(cutoff), cutoff = 0.1*(Xmax-Xmin); end % heuristic default value
if length(cutoff)==1, cutoff = cutoff(ones(1,d)); end
if length(cutoff)~=d, error('cutoff must be a scalar or 1x%d vector',d); end
if size(box,2)~=2 || size(box,1)~=d, error('Box dimensions must be a %dx2 vector',d); end
boxlength = diff(box, 1, 2);
if length(PBC)~=d; error('PBC must be a 1x%d logical vector',d), end
PBC = PBC>0;

%% Check that all points lie within the box
incellok = true;
for i=1:d
    if box(i,1)>Xmin(i)
        dispf('some particles are outside the lower bound %0.3g along dimension %d',box(i,1),i)
        incellok = false;
    end
    if box(i,2)<Xmax(i)
        dispf('some particles are outside the upper bound %0.3g along dimension %d',box(i,2),i),
        incellok = false;
    end
end
if ~incellok
    disp('use: X = PBCincell(X,box,PBC) to wrap particles around coordinates')
    error('PBCimages: some particles outside the box...')
end

%% Initialize empty array for images
[Ximages,indX] = deal([]);

%% Generate images for each dimension independently
for i = 1:d
    if PBC(i)
        lowerBound = box(i,1);
        upperBound = box(i,2);

        % Lower and upper images
        islowerImages = X(:, i) < (lowerBound + cutoff(i));
        lowerImages = X(islowerImages, :);
        lowerImages(:, i) = lowerImages(:, i) + (upperBound - lowerBound);

        isupperimages = X(:, i) > (upperBound - cutoff(i));
        upperImages = X(isupperimages, :);
        upperImages(:, i) = upperImages(:, i) - (upperBound - lowerBound);

        Ximages = [Ximages; lowerImages; upperImages]; %#ok<AGROW>
        indX = [indX;find(islowerImages);find(isupperimages)]; %#ok<AGROW>
    end
end

%% Generate corner images if all dimensions are periodic
if all(PBC)
    % Find all combinations for corners
    % corners = dec2bin(1:(2^d)-1) - '0';
    if d==2
        [x,y]=meshgrid([0 1],[0 1]);
        corners = [x(:) y(:)];
    elseif d==3
        [x,y,z]=meshgrid([0 1],[0 1],[0 1]);
        corners = [x(:) y(:) z(:)];
    end
    
    for i = 1:size(corners, 1) % 4 (in 2D), 8 (in 3D)
        cornerCond = true(n, 1);
        cornerImages = X;
        for j = 1:d
            if corners(i,j) == 0
                % Lower corner images
                thisCorner = X(:,j) < (box(j,1) + cutoff(j));
                cornerImages(thisCorner,j) = cornerImages(thisCorner,j) + boxlength(j);
            else
                % Upper corner images
                thisCorner = X(:,j) > (box(j,2) - cutoff(j));
                cornerImages(thisCorner,j) = cornerImages(thisCorner,j) - boxlength(j);
            end
            cornerCond = cornerCond & thisCorner;
        end
        % Add corner images if any particles satisfy the corner condition
        if any(cornerCond)
            Ximages = [Ximages; cornerImages(cornerCond, :)]; %#ok<AGROW>
            indX = [indX;find(cornerCond)]; %#ok<AGROW>
        end
    end
end

%% Generate edge images if two dimensions are at least periodic in 3D
if (d==3) && (sum(PBC)>1)
    dvalid = find(PBC);
    [x,y] = meshgrid(dvalid,dvalid); ok = (x<y);
    dimforedges = [x(ok) y(ok)]; % dimension pairs (with x<y)
    [x,y]=meshgrid([0 1],[0 1]);
    edges = [x(:) y(:)]; % edge pairs
    
    for k = 1:size(dimforedges,1) % number of dimension pairs (max 3)
        for i = 1:size(edges, 1)  % number of lower/upper edges (4) ==> 3x4 = 12 edges at maximum
            edgeCond = true(n, 1);
            edgeImages = X;
            for j = 1:2 % for edges in 3D (2 dimensions only)
                jdim = dimforedges(k,j);
                if edges(i,j) == 0
                    % Lower edge images
                    thisEdge = X(:,jdim) < (box(jdim,1) + cutoff(jdim));
                    edgeImages(thisEdge,jdim) = edgeImages(thisEdge,jdim) + boxlength(jdim);
                else
                    % Upper edge images
                    thisEdge = X(:,jdim) > (box(jdim,2) - cutoff(jdim));
                    edgeImages(thisEdge,jdim) = edgeImages(thisEdge,jdim) - boxlength(jdim);
                end
            end
            edgeCond = edgeCond & thisEdge;
            % Add corner images if any particles satisfy the edge condition
            if any(edgeCond)
                Ximages = [Ximages; edgeImages(edgeCond, :)]; %#ok<AGROW>
                indX = [indX;find(edgeCond)]; %#ok<AGROW>
            end
        end
    end
end


%% Removing duplicates if any
[Ximages,iXuniq] = unique(Ximages, 'rows');
indX = indX(iXuniq);

% output
if nargout>1, indXout = indX; end