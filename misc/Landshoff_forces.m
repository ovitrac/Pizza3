%% Code to illustrate the developement Landshoff forces between two horizontal layers of layer particles
% translating respectively to each other with a velocity difference

% INRAE\Olivier Vitrac, Han Chen - 2023-02-23

% [ SYNOPSIS ] This code simulates the displacement of two layers of particles
% in a fluid using smoothed particle hydrodynamics (SPH). The two layers are
% represented by the "fixed" and "movable" structures, which contain information
% about the size, number, position, and velocity of the particles in each layer.

% [ DESCRIPTION ] The code simulates the movement of two layers of particles in a fluid
% using smoothed particle hydrodynamics (SPH). The particles in the two layers are
% represented by the "fixed" and "movable" structures, which contain information about
% the size, number, position, and velocity of the particles in each layer. The Landshoff
% forces between particles in the two layers are calculated using the kernel function and
% SPH parameters, and the positions of the particles in the "movable" layer are adjusted
% to be as close as possible to the particles in the "fixed" layer. The forces are plotted
% as arrows on the particle plot using the "arrow" function, and the plot is updated with
% each iteration. The code also includes options for recording the plot as a GIF.


%% The code begins by defining the "layerplot" function, which creates a scatter plot of the particles
% in a layer using circles with a radius equal to the particle size.
% The particle size is set to 0.5 units for both layers, and the "fixed" layer contains 14 particles,
% while the "movable" layer contains 10 particles. The particles in the "fixed" layer are arbitrarily
% fixed in place, while the particles in the "movable" layer are free to move.
% layer plot
layerplot = @(X) viscircles([X.x X.y],X.R*ones(X.n,1),'color',X.color);
% bead size
r = 0.5;
fixed = struct( ...these particles are arbitrarily fixed
    'R',r, ...
    'n',14,...
    'y',-r,...
    'dx',1e-2,...
    'dy',0,...
    'color',rgb('DodgerBlue'),...
    'id',0 ...
    );

movable = struct( ... movable particles
    'R',r,...
    'n',10,...
    'y',+r,...
    'dx',1e-2,...
    'dy',1e-2,...
    'color',rgb('DeepSkyBlue'), ...
    'id',1 ...
    );

% The positions of the particles in each layer are initiallyset up in a linear array along the x-axis,
% with some randomness added to the spacing between particles.
% The positions of the particles in the "fixed" layer are then shifted along the y-axis
% by a fixed amount, while the positions of the particles in the "movable" layer are shifted
% by a smaller amount along both the x- and y-axes.
fixed.x  = linspace(-(fixed.dx+fixed.R*2)*(fixed.n-1)/2,(fixed.dx+fixed.R*2)*(fixed.n-1)/2,fixed.n)';
movable.x = linspace(-(movable.dx+movable.R*2)*(movable.n-1)/2,(movable.dx+movable.R*2)*(movable.n-1)/2,movable.n)';
fixed.y = ones(fixed.n,1) * (fixed.y + fixed.dy);
movable.y = ones(movable.n,1) * (movable.y + movable.dy);

% redistribute with some randomness fixed beads along x
x0 = fixed.x(1);
dx = diff(fixed.x);
dxrandom = abs(randn(fixed.n,1))*fixed.R*0.25;
x = x0+[cumsum([0;dx]+dxrandom)];
fixed.x = x - mean(x);

% redistribute with some randomness top beads along x
x0 = movable.x(1);
dx = diff(movable.x);
dxrandom = abs(randn(movable.n,1))*movable.R*0.4;
x = x0+[cumsum([0;dx]+dxrandom)];
movable.x = x - x(1) + mean(fixed.x(1:2));

% Next, the kernel function and SPH parameters are defined.
% The kernel function is used to calculate the smoothing function
% for the SPH method, and the parameters include the smoothing length (h),
% the density (rho), and the coefficients (c0 and q1) used in the Landshoff force calculation.
h = 2 * r;
dWdr = @(r) (r<h) .* ( (1.0./h.^3.*(r./h-1.0).^3.*-1.5e+1)./pi-(1.0./h.^3.*(r./h-1.0).^2.*((r.*3.0)./h+1.0).*1.5e+1)./pi );
c0 = 10;
q1 = 1;
rho = 1000;


% initial position
v = 0.1; % velocity (arbitrary units)
dt = 0.1;
config = movable;
clf, hold on, axis equal
layerplot(fixed)
[hp,ha] = deal([]);
axis off
RECORD = true; % set it to true to record a video

% The code then enters a loop that simulates the movement of the particles over time.
% In each iteration, the position of the "movable" layer is shifted by a fixed amount
% along the x-axis, and the particles are then repacked along the y-axis to be as close
% as possible to the particles in the "fixed" layer. This is done using the "distance"
% and "iclosest" functions to find the closest particle in the "fixed" layer to each
% particle in the "movable" layer, and then adjusting the positions of the particles
% in the "movable" layer accordingly.
for it=1:350
    shift = dt * v;
    config.x = config.x + shift;
    % repack the top layer respectively to the fixed
    distance = @(i) sqrt((fixed.x-config.x(i)).^2 + (fixed.y-config.y(i)).^2);
    iclosest = arrayfun( @(i) find( distance(i)==min(distance(i)),1),1:config.n );
    distance2closest = sqrt((fixed.x(iclosest)-config.x).^2 + (fixed.y(iclosest)-config.y).^2);
    dtarget = fixed.R*2*(1-abs(randn(config.n,1)*0.01));
    contraction_required = 1-dtarget./distance2closest;
    config.x = config.x + (fixed.x(iclosest)-config.x) .* contraction_required;
    config.y = config.y + (fixed.y(iclosest)-config.y) .* contraction_required;

    %The Landshoff forces are then calculated using a nested loop that iterates
    % over all pairs of particles in both layers. The forces are calculated using
    % the kernel function and the Landshoff force formula, which includes the velocity
    % difference and distance between particles, as well as the SPH parameters
    id = [ fixed.id * ones(fixed.n,1); config.id * ones(config.n,1) ];
    xy = [fixed.x fixed.y; config.x config.y];
    vxy = [repmat([0 0],fixed.n,1); repmat([v 0],config.n,1)];
    n = fixed.n + config.n;
    [mu,nu] = deal(zeros(n,n));
    F = zeros(n,n,2);
    for i = 1:n
        for j = 1:n
            rij = xy(i,:)-xy(j,:);
            vij = vxy(i,:)-vxy(j,:);
            if dot(rij,vij)<0
                mu(i,j) = h * dot(rij,vij)/(dot(rij,rij)+0.01*h^2);
                nu(i,j) = (1/rho) * (-q1*c0*mu(i,j));
                rij_d = norm(rij);
                rij_n = rij/rij_d;
                F(i,j,:) = -nu(i,j)*dWdr(rij_d) * permute(rij_n,[1 3 2]);
            end
        end
    end
    Fbalance = squeeze(sum(F,2));
    f = sum(Fbalance.^2,2);
    fmedian = median(f);
    fmin = fmedian/50;
    fscale = 0.2*r/fmedian;

    %Finally, the forces are plotted as arrows on the particle plot using the "arrow" function,
    % and the plot is updated with each iteration. 
    start = xy;
    stop = start + Fbalance*fscale;
    start(f<fmin,:) = [];
    stop(f<fmin,:) = [];
    if ~isempty(hp), delete(hp); end
    if ~isempty(ha), delete(ha); end
    hp = layerplot(config);
    ha = [
        arrow(start,stop,'length',8,'BaseAngle',60,'Linewidth',2,'color',rgb('ForestGreen'),'Edgecolor',rgb('ForestGreen'))
        arrow(start,[stop(:,1) start(:,2)],'length',4,'BaseAngle',60,'color',rgb('Tomato'))
        arrow(start,[start(:,1) stop(:,2)],'length',4,'BaseAngle',60,'color',rgb('Tomato'),'EdgeColor',rgb('Tomato'))
    ];
    drawnow

   %If the "RECORD" flag is set to true, the plot is also recorded as a GIF using the "gif_add_frame" function.
   if RECORD
       gif_add_frame(gca,'landshoff.gif',15);
   end

end
