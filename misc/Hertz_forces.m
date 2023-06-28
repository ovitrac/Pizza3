%% Code to explain the displacement of SPH particles (amorphous) along a rigid wall made with beads of the same size (organized)
% INRAE\Olivier Vitrac, Han Chen - 2023-02-23

% [ SYNOPSIS ] This code simulates the displacement of spherical particles in a rigid wall made with beads of the
% same size, by calculating the normal force and contact radius between the particles % and the wall. The contact
% depth between each pair of particles and the wall is calculated using the Hertz model.

% [ DESCRIPTION ] The code simulates the displacement of amorphous fluid particles along a
% rigid wall made of beads of the same size that are organized in a fixed pattern. The code
% defines the initial configuration of the system, with the wall and fluid beads arranged in their
% respective layers. The fluid beads are then redistributed with some randomness along the x-axis.
% The code then finds the closest wall bead to each fluid bead and calculates the contraction
% required for the fluid bead to move towards the wall bead. The final configuration of the fluid
% beads is then computed with the required contraction, and the physical interpretation of the
% contraction is calculated using Hertz contact mechanics. The dynamic configuration is then plotted,
% showing the motion of the fluid beads towards the wall beads, with arrows indicating the force
% direction and magnitude. The code also allows the user to record a video of the dynamic configuration.

%% layer definitions and initial configuration
% The code defines the properties of the wall and the fluid particles,
% including their size, number, and position. The particles are initially
% randomly distributed along the x-axis, and then redistributed to the
% nearest wall bead with some randomness.

% layer plot
layerplot = @(X) viscircles([X.x X.y],X.R*ones(X.n,1),'color',X.color);
% bead size
r = 0.5;
wall = struct( ...
    'R',r, ...
    'n',14,...
    'y',-r,...
    'dx',1e-2,...
    'dy',0,...
    'color',rgb('DarkBlue') ...
    );

fluid = struct( ...
    'R',r,...
    'n',10,...
    'y',+r,...
    'dx',1e-2,...
    'dy',1e-2,...
    'color',rgb('Gold') ...
    );
wall.x  = linspace(-(wall.dx+wall.R*2)*(wall.n-1)/2,(wall.dx+wall.R*2)*(wall.n-1)/2,wall.n)';
fluid.x = linspace(-(fluid.dx+fluid.R*2)*(fluid.n-1)/2,(fluid.dx+fluid.R*2)*(fluid.n-1)/2,fluid.n)';
wall.y = ones(wall.n,1) * (wall.y + wall.dy);
fluid.y = ones(fluid.n,1) * (fluid.y + fluid.dy);
% redistribute with some randomness fluid beads along x
x0 = fluid.x(1);
dx = diff(fluid.x);
dxrandom = abs(randn(fluid.n,1))*fluid.R*0.5;
x = x0+[cumsum([0;dx]+dxrandom)];
fluid.x = x - mean(x);

% find the closest wall bead and calculate the final configuration (used to get fmax)
distance = @(i) sqrt((wall.x-fluid.x(i)).^2 + (wall.y-fluid.y(i)).^2);
iclosest = arrayfun( @(i) find( distance(i)==min(distance(i)),1),1:fluid.n );
distance2closest = sqrt((wall.x(iclosest)-fluid.x).^2 + (wall.y(iclosest)-fluid.y).^2);
dtarget = wall.R*2*(1-abs(randn(fluid.n,1)*0.02));
contraction_required = 1-dtarget./distance2closest;
final = fluid;
final.x = final.x + (wall.x(iclosest)-final.x) .* contraction_required;
final.y = final.y + (wall.y(iclosest)-final.y) .* contraction_required;


% Physical intepretation
% The force required to maintain the contact between the particles and the wall is
% calculated based on the Hertz model, and the dynamic configuration of the particles
% is then calculated using the applied load.
distance2closest = sqrt((wall.x(iclosest)-final.x).^2 + (wall.y(iclosest)-final.y).^2);
E = 1e5;
rcut = wall.R + final.R;
direction = - [wall.x(iclosest)-final.x (wall.y(iclosest)-final.y)]./distance2closest(:,[1 1]);
f = E * sqrt((rcut-distance2closest)*wall.R*final.R/rcut);
f(distance2closest>rcut) = 0;
fmax = max(f);

% dynamic configuration
nt = 200;
t = linspace(0,1,nt);
clf, hold on, axis equal
layerplot(wall)
[hp,ha] = deal([]);
axis off
RECORD = true; % set it to true to record a video

% The code then iterates over a certain number of time steps,calculating
% the dynamic configuration of the particles in each step and plotting their
% positions and contact depths using the Hertz model.
for it = 1:nt
    layerplot(fluid)
    config = fluid;
    config.x = config.x + (wall.x(iclosest)-config.x) .* contraction_required*t(it);
    config.y = config.y + (wall.y(iclosest)-config.y) .* contraction_required*t(it);

    % Physical intepretation
    distance2closest = sqrt((wall.x(iclosest)-config.x).^2 + (wall.y(iclosest)-config.y).^2);
    min(distance2closest)
    rcut = wall.R + config.R;

    direction = - [wall.x(iclosest)-config.x (wall.y(iclosest)-config.y)]./distance2closest(:,[1 1]);
    f = E * sqrt((rcut-distance2closest)*wall.R*config.R/rcut);
    f(distance2closest>rcut) = 0;
    fmax = max(f);
    fscale = 2*r/fmax;
    start = [config.x config.y];
    stop = start + direction.*f*fscale;
    start(f==0,:)=[];
    stop(f==0,:)=[];

    % plot
    if ~isempty(hp), delete(hp); end
    if ~isempty(ha), delete(ha); end
    hp = layerplot(config);
    if any(start)
        ha = [
            arrow(start,stop,'length',8,'BaseAngle',60,'Linewidth',2,'color',rgb('ForestGreen'),'Edgecolor',rgb('ForestGreen'))
            arrow(start,[stop(:,1) start(:,2)],'length',4,'BaseAngle',60,'color',rgb('Tomato'))
            arrow(start,[start(:,1) stop(:,2)],'length',4,'BaseAngle',60,'color',rgb('Tomato'),'EdgeColor',rgb('Tomato'))
            ];
    else
        ha = [];
    end
    drawnow

   % record video
   if RECORD
       gif_add_frame(gca,'hertz.gif',15);
   end

end
    
%% Template
% A similar code template is also provided at the end, which calculates the Hertz contact depth
% between two series of parallel spheres aligned along the x-axis, with a fixed distance between
% adjacent spheres. It calculates the normal force and contact radius based on the material
% properties of the spheres, and then loops over all possible pairs of spheres to calculate
% the Hertz contact depth between them. Finally, it plots the sphere positions and contact depths.


% % This code assumes that the two series of parallel spheres are aligned 
% % along the x-axis, with a fixed distance between adjacent spheres. 
% % It calculates the normal force and contact radius based on the material 
% % properties of the spheres, and then loops over all possible pairs of spheres
% % to calculate the Hertz contact depth between them. 
% % Finally, it plots the sphere positions and contact depths. 
% % You can modify the code to suit your specific geometry and material properties.
% 
% % Define material properties
% E = 2.1e11; % Young's modulus in Pa
% v = 0.3; % Poisson's ratio
% R = 0.5e-3; % Sphere radius in m
% 
% % Define sphere geometry and spacing
% n1 = 10; % Number of spheres in the first row
% n2 = 10; % Number of spheres in the second row
% d = 1e-3; % Distance between spheres in m
% 
% % Calculate normal force and contact radius
% P = 1; % Applied load in N
% a = (3*P*(1-v^2)/(4*E))^(1/3); % Contact radius in m
% F = 4/3*E*sqrt(R)*a^(3/2); % Normal force in N
% 
% % Define sphere positions
% x1 = linspace(-d*(n1-1)/2,d*(n1-1)/2,n1);
% x2 = linspace(-d*(n2-1)/2,d*(n2-1)/2,n2)+1e-4;
% y1 = -R;
% y2 = 0.98*R;
% 
% % Initialize contact matrix
% C = zeros(n1,n2);
% 
% % Loop over all sphere pairs and calculate contact
% for i = 1:n1
%     for j = 1:n2
%         dx = x2(j) - x1(i);
%         if abs(dx) > d
%             % Spheres are too far apart to be in contact
%             continue;
%         end
%         r = sqrt( (x2(j) - x1(i))^2 + (y2 - y1)^2 );
%         if r >= 2*R
%             % Spheres are not in contact
%             continue
%         end
%         C(i,j) = a - sqrt((2*R-r)*r); % Hertz contact depth in m
%     end
% end
% 
% %% Plot sphere positions and contact depths
% figure, hold on
% for i = 1:n1
%     viscircles([x1(i) y1],R,'color','b');
%     for j = 1:n2
%         viscircles([x2(j) y2],R-C(i,j),'color','r');
%         if C(i,j) > 0
%             plot([x1(i),x2(j)],[y1+R,y1+R-C(i,j)],'k');
%         end
%     end
% end
% axis equal