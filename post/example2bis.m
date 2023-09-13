%% Workshop Main File - Part 2bis
% This script discusses advanced shear details beyond those shown in Part2
% Only advanced features are kept

% File Structure (change your local path to reflect the content)
% ├── example2bis.m
% └── ...
% └── data folder (dumps/pub1/)

%INRAE\Olivier Vitrac, Han Chen 2023-09-07

% Revision history
% 2023-09-09 major increment
% 2023-09-10 finalization and copy to notebook/
% 2023-09-13 update for new Landshoff and Hertz virial calculations (fixes)

%% Definitions
% We assume that the dump file has been preprocessed (see example1.m and example2.m)
statvec = @(f,before,after) dispf('%s: %s%d values | average = %0.5g %s', before, ...
    cell2mat(cellfun(@(x) sprintf(' %0.1f%%> %10.4g | ', x, prctile(f, x)), {2.5, 25, 50, 75, 97.5}, 'UniformOutput', false)), ...
    length(f), mean(f),after); % user function to display statistics on vectors (usage:  statvec(f,'myvar','ok'))
coords = {'x','y','z'};
vcoords = cellfun(@(c) ['v',c],coords,'UniformOutput',false); % vx, vy, vz
% dump file and its parameterization
datafolder = './dumps/pub1/';
dumpfile = 'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle';
datafolder = lamdumpread2(fullfile(datafolder,dumpfile),'search'); % fix datafolder based on initial guess
X0 = lamdumpread2(fullfile(datafolder,dumpfile)); % default frame
boxdims = X0.BOX(:,2) - X0.BOX(:,1);              % box dims
natoms = X0.NUMBER;                               % number of atoms
timesteps = X0.TIMESTEPS;                         % time steps
ntimesteps = length(timesteps);                   % number of time steps
T = X0.ATOMS.type;                                % atom types
% === IDENTIFICATION OF ATOMS ===
atomtypes = unique(T);                            % list of atom types
natomspertype = arrayfun(@(t) length(find(T==t)),atomtypes);
[~,fluidtype] = max(natomspertype); % fluid type
[~,solidtype] = min(natomspertype); % solid type
walltypes = setdiff(atomtypes,[fluidtype,solidtype]); % wall types
nfluidatoms = natomspertype(fluidtype);
nsolidatoms = natomspertype(solidtype);
% === FLOW DIRECTION ===
[~,iflow] = max(boxdims);
iothers = setdiff(1:size(X0.BOX,1),iflow);
% === GUESS BEAD SIZE ===
% not needed anymore since the mass, vol and rho are taken from the dump file
Vbead_guess = prod(boxdims)/natoms;
rbead_guess = (3/(4*pi)*Vbead_guess)^(1/3);
cutoff = 3*rbead_guess;
[verletList,cutoff,dmin,config,dist] = buildVerletList(X0.ATOMS(T==fluidtype,coords),cutoff);
rbead = dmin/2;  % based on separation distance

%% Frame and Corresponding ROI for Stress Analysis
list_timestepforstess = unique(timesteps(ceil((0.1:0.1:0.9)*ntimesteps)));
timestepforstress = list_timestepforstess(end);
% stress frame
Xstress = lamdumpread2(fullfile(datafolder,dumpfile),'usesplit',[],timestepforstress); % middle frame
Xstress.ATOMS.isfluid = Xstress.ATOMS.type==fluidtype;
Xstress.ATOMS.issolid = Xstress.ATOMS.type==solidtype;
Xstress.ATOMS.iswall  = ismember(Xstress.ATOMS.type,walltypes);
% == control (not used) ==
% average bead volume and bead radius (control, min separation distance was used in the previous section)
fluidbox = [min(Xstress.ATOMS{Xstress.ATOMS.isfluid,coords});max(Xstress.ATOMS{Xstress.ATOMS.isfluid,coords})]';
vbead_est = prod(diff(fluidbox,1,2))/(length(find(Xstress.ATOMS.isfluid))+length(Xstress.ATOMS.issolid));
rbead_est = (3*vbead_est/(4*pi))^(1/3);
mbead_est = vbead_est*1000;
% Verlet List Construction with Short Cutoff
% Builds a Verlet list with a short cutoff distance, designed to identify only the closest neighbors.
[verletList,cutoff,dmin,config,dist] = buildVerletList(Xstress.ATOMS,3*rbead);
% Partition Verlet List Based on Atom Types
% This Verlet list is partitioned based on atom types, distinguishing between interactions
% that are exclusively fluid-fluid, solid-fluid, or solid-solid.
verletListCross = partitionVerletList(verletList,Xstress.ATOMS);
% Identify Contacting Atoms
Xstress.ATOMS.isincontact = ~cellfun(@isempty,verletListCross);
Xstress.ATOMS.contacttypes = cellfun(@(v) Xstress.ATOMS.type(v)',verletListCross,'UniformOutput',false);
% Identify Atoms in Contact with Solids and Fluids
Xstress.ATOMS.isincontactwithsolid = cellfun(@(c) ismember(solidtype,c), Xstress.ATOMS.contacttypes);
Xstress.ATOMS.isincontactwithfluid = cellfun(@(c) ismember(fluidtype,c), Xstress.ATOMS.contacttypes);
Xstress.ATOMS.isincontactwithwalls = cellfun(@(c) ~isempty(intersect(walltypes,c)), Xstress.ATOMS.contacttypes);
% Flag Fluid Atoms in Contact with Solid and Vice Versa
Xstress.ATOMS.fluidincontactwithsolid = Xstress.ATOMS.isfluid & Xstress.ATOMS.isincontactwithsolid;
Xstress.ATOMS.solidincontactwithfluid = Xstress.ATOMS.issolid & Xstress.ATOMS.isincontactwithfluid;
Xstress.ATOMS.fluidincontactwithwalls = Xstress.ATOMS.isfluid & Xstress.ATOMS.isincontactwithwalls;
Xstress.ATOMS.wallsincontactwithfluid = Xstress.ATOMS.iswall & Xstress.ATOMS.isincontactwithfluid;
% Identify Indices for Analysis
ROI = [
    min(Xstress.ATOMS{Xstress.ATOMS.fluidincontactwithsolid,coords})
    max(Xstress.ATOMS{Xstress.ATOMS.fluidincontactwithsolid,coords})
    ]';
ROI(iflow,:) = mean(ROI(iflow,:)) + [-1 1] * diff(ROI(iflow,:));
for j = iothers
    ROI(j,:) = Xstress.BOX(j,:) ;
end
inROI = true(size(Xstress,1),1);
for c=1:length(coords)
    inROI = inROI & (Xstress.ATOMS{:,coords{c}}>=ROI(c,1)) & (Xstress.ATOMS{:,coords{c}}<=ROI(c,2));
end
ifluid = find(inROI & (Xstress.ATOMS.isfluid));
isolid = find(inROI & (Xstress.ATOMS.issolid));
iwall = find(inROI & (Xstress.ATOMS.iswall));
isolidcontact = find(Xstress.ATOMS.solidincontactwithfluid);
iwallcontact = find(inROI & Xstress.ATOMS.wallsincontactwithfluid);
% control
figure, hold on
plot3D(Xstress.ATOMS{ifluid,coords},'bo','markersize',3,'markerfacecolor','b')
plot3D(Xstress.ATOMS{iwallcontact,coords},'ko','markersize',12,'markerfacecolor','k')
plot3D(Xstress.ATOMS{isolidcontact,coords},'ro','markersize',16,'markerfacecolor','r')
axis equal, view(3), drawnow

% triangulation of the solid
DT = delaunayTriangulation(double(Xstress.ATOMS{isolidcontact,{'x','y','z'}}));
K = convexHull(DT);
plotsolid = @()trisurf(K, DT.Points(:,1), DT.Points(:,2), DT.Points(:,3), 'FaceColor', 'w','Edgecolor','k','FaceAlpha',0.6);

%% Landshoff forces and stresses in the fluid
% these forces are the viscous forces in the fluid
% we calculate:
%   Flandshoff(i,:) the local Landshoff force (1x3 vector) for the atom i
%   Wlandshoff(i,:) is the local virial stress tensor (3x3 matrix stored as 1x9 vector with Matlab conventions)
%       row-wise: force component index
%       columm-wise: coord component index
%   The virial tensor reads:
%        \[
%        \sigma =
%        \begin{pmatrix}
%        \sigma_{11} & \sigma_{12} & \sigma_{13} \\
%        \sigma_{21} & \sigma_{22} & \sigma_{23} \\
%        \sigma_{31} & \sigma_{32} & \sigma_{33}
%        \end{pmatrix}
%        \]
%
%   The viscous tensor component is associated to the flow (x)
%      $ \tau_{xy} = \mu \left( \frac{\partial u}{\partial y} \right) $
%   it is derived from the virial stress tensor:
%       $ \sigma_{\alpha\beta} = \frac{1}{V} \sum_{i<j} r_{ij,\alpha} f_{ij,\beta} $
%   where  $ V $ is the volume, $ r_{ij,\alpha} $ is the $ \alpha $-component of the distance vector between particles $ i $ and $ j $, and $ f_{ij,\beta} $ is the $ \beta $-component of the force between particles $ i $ and $ j $.
%
% For this specific problem, the most relevant components would be those relating to shear and normal forces, specifically $ \sigma_{xy} $ and $ \sigma_{yy} $. 
% 1. $ \sigma_{xy} $ corresponds to the shear effects and should be closely related to the SPH-based shear stress $ \tau_{xy} $ in the fluid. This component would be a primary point of comparison.% 
% 2. $ \sigma_{yy} $ will capture the effects of the Hertzian contacts along the $ y $-direction (i.e., the direction opposite to which the wall is moving). In your Hertz contact model, the normal force is acting along the $ y $-direction, which contributes to this component.
% 
% Therefore, based on the equality of mechanical states between the fluid and the wall, we should expect:
% $\sigma_{xy}^{\text{SPH}} = \sigma_{xy}^{\text{Hertz}}$  (shear)
% $\sigma_{yy}^{\text{SPH}} = \sigma_{yy}^{\text{Hertz}}$  (normal)
% which reads (first index: direction, second index: vcomponent)
% $ \sigma_{21}^{\text{SPH}} = \sigma_{21}^{\text{Hertz}} $
% $ \sigma_{22}^{\text{SPH}} = \sigma_{22}^{\text{Hertz}} $

% === Build the Verlet list consistently with the local Virial Stress Tensor ===
% Changing h can affect the value of viscosity for Landshoff foces and shear stress.
% While keeping the same hLandshoff, the results can be rescaled to the value of h
% applied in the simulations.
Xfluid  = Xstress.ATOMS(ifluid,:);
hLandshoff = 4*rbead; %1.25e-5; % m
Vfluid = buildVerletList(Xfluid,hLandshoff);
configLandshoff = struct( ...
    'gradkernel', kernelSPH(hLandshoff,'lucyder',3),...kernel gradient
    'h', hLandshoff,...smoothing length (m)
    'c0',0.32,...speed of the sound (m/s)
    'q1',30 ... viscosity coefficient (-)
    );
rhofluid = mean(Xfluid.c_rho_smd);
mbead = mean(Xfluid.mass);
Vbead = mean(Xfluid.c_vol);
mu = rhofluid*configLandshoff.q1*configLandshoff.c0*configLandshoff.h/10; % viscosity estimate
dispf('Atificial viscosity: %0.4g Pa.s',mu)

% Landshoff forces and local virial stress
[Flandshoff,Wlandshoff] = forceLandshoff(Xfluid,[],Vfluid,configLandshoff);
flandshoff = sqrt(sum(Flandshoff.^2,2));
statvec(flandshoff,' Force Landshoff',sprintf('<-- TIMESTEP: %d',timestepforstress))
statvec(Wlandshoff(:,2),'Virial Landshoff',sprintf('<-- TIMESTEP: %d',timestepforstress))

% number of grid points along the largest dimension
fluidbox = [ min(Xfluid{:,coords}); max(Xfluid{:,coords}) ]';
boxcenter = mean(fluidbox,2);
resolution = ceil(50 * diff(fluidbox,[],2)'./max(diff(fluidbox,[],2)));
xw = linspace(fluidbox(1,1),fluidbox(1,2),resolution(1));
yw = linspace(fluidbox(2,1),fluidbox(2,2),resolution(2));
zw = linspace(fluidbox(3,1),fluidbox(3,2),resolution(3));
[Xw,Yw,Zw] = meshgrid(xw,yw,zw);
XYZgrid = [Xw(:),Yw(:),Zw(:)];
hLandshoff = 5*rbead; %1.25e-5; % m

% Build the Grid Verlet list
VXYZ = buildVerletList({XYZgrid Xfluid{:,coords}},1.001*hLandshoff); % special grid syntax
% Interpolate Landshoff forces, extract components for plotting
W = kernelSPH(hLandshoff,'lucy',3); % kernel for interpolation (not gradkernel!)
FXYZgrid = interp3SPHVerlet(Xfluid{:,coords},Flandshoff,XYZgrid,VXYZ,W,Vbead);
FXYZgridx = reshape(FXYZgrid(:,1),size(Xw));
FXYZgridy = reshape(FXYZgrid(:,2),size(Yw));
FXYZgridz = reshape(FXYZgrid(:,3),size(Zw));
% Interpolate local virial stress tensor, extract s12 which is stored as s(2,1)
WXYZgrid = interp3SPHVerlet(Xfluid{:,coords},Wlandshoff,XYZgrid,VXYZ,W,Vbead);
s12grid = reshape(WXYZgrid(:,2),size(Xw)); % extract \sigma_{xy} i.e. forces along x across y
% Alternative estimation of the virial from the Cauchy stress tensor
WXYZgrid2 = interp3cauchy(Xw,Yw,Zw,FXYZgridx,FXYZgridy,FXYZgridz);
s12grid2 = reshape(WXYZgrid2(:,:,:,2),size(Xw));
% Interpolate the velocities, extract components for plotting
vXYZgrid = interp3SPHVerlet(Xfluid{:,coords},Xfluid{:,vcoords},XYZgrid,VXYZ,W,Vbead);
vXYZgridx = reshape(vXYZgrid(:,1),size(Xw));
vXYZgridy = reshape(vXYZgrid(:,2),size(Yw));
vXYZgridz = reshape(vXYZgrid(:,3),size(Zw));
vdXYZgridxdy = gradient(vXYZgridx,xw(2)-xw(1),yw(2)-yw(1),zw(2)-zw(1));
s12grid_est = mu * vdXYZgridxdy;

% === Plot Estimated shear stress (it should be the theoretical value)
figure, hold on
hs = slice(Xw,Yw,Zw,s12grid_est,[boxcenter(1) xw(end)],...
    [boxcenter(2) yw(end)],...
    [fluidbox(3,1) boxcenter(3)]);
set(hs,'edgecolor','none','facealpha',0.6)
plotsolid()
lighting gouraud, camlight('left'), axis equal, view(3) % shading interp
hc = colorbar('AxisLocation','in','fontsize',14); hc.Label.String = '\sigma_{XY}';
title('Stress from velocity field: \sigma_{XY}=\eta\cdot\partial v_x/\partial y','fontsize',20)
xlabel('X'), ylabel('Y'), zlabel('Z')
step = [3 10 5];
quiver3( ...
    Xw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    Yw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    Zw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    vXYZgridx(1:step(1):end,1:step(2):end,1:step(3):end), ...
    vXYZgridy(1:step(1):end,1:step(2):end,1:step(3):end), ...
    vXYZgridz(1:step(1):end,1:step(2):end,1:step(3):end) ...
    ,1,'color','k','LineWidth',2)
npart = 30;
[startX,startY,startZ] = meshgrid( ...
    double(xw(1)), ...
    double(yw(unique(round(1+(1+(linspace(-1,1,npart).*linspace(-1,1,npart).^2))*floor(length(yw)/2))))),...
    double(yw(unique(round(1+(1+(linspace(-1,1,npart).*linspace(-1,1,npart).^2))*floor(length(yw)/2))))) ...
  );
vstart = interp3(Xw,Yw,Zw,vXYZgridx,startX,startY,startZ); startX(vstart<0) = double(xw(end));
hsl = streamline(double(Xw),double(Yw),double(Zw),vXYZgridx,vXYZgridy,vXYZgridz,startX,startY,startZ);
set(hsl,'linewidth',2,'color',[0.4375    0.5000    0.5625])
plot3(startX(:),startY(:),startZ(:),'ro','markerfacecolor',[0.4375    0.5000    0.5625])
% fix the view
view(-90,90), clim([-1e-1 1e-1])

% === Plot Estimated shear stress from Cauchy Tensor
figure, hold on
s1299 = prctile(abs(s12grid2(~isnan(s12grid2))),99);
isosurface(Xw,Yw,Zw,s12grid2,s1299)
isosurface(Xw,Yw,Zw,s12grid2,-s1299)
hs = slice(Xw,Yw,Zw,s12grid2,[boxcenter(1) xw(end)],...
    [boxcenter(2) yw(end)],...
    [fluidbox(3,1) boxcenter(3)]);
set(hs,'edgecolor','none','facealpha',0.6)
plotsolid()
lighting gouraud, camlight('left'), axis equal, view(3) % shading interp
hc = colorbar('AxisLocation','in','fontsize',14); hc.Label.String = '\sigma_{XY}';
title('Local Cauchy stress: \sigma_{XY}','fontsize',20)
xlabel('X'), ylabel('Y'), zlabel('Z')
npart = 20;
[startX,startY,startZ] = meshgrid( ...
    double(xw(1)), ...
    double(yw(unique(round(1+(1+(linspace(-1,1,npart).*linspace(-1,1,npart).^2))*floor(length(yw)/2))))),...
    double(yw(unique(round(1+(1+(linspace(-1,1,npart).*linspace(-1,1,npart).^2))*floor(length(yw)/2))))) ...
  );
vstart = interp3(Xw,Yw,Zw,vXYZgridx,startX,startY,startZ); startX(vstart<0) = double(xw(end));
hsl = streamline(double(Xw),double(Yw),double(Zw),vXYZgridx,vXYZgridy,vXYZgridz,startX,startY,startZ);
set(hsl,'linewidth',2,'color','k')
plot3(startX(:),startY(:),startZ(:),'ro','markerfacecolor',[0.4375    0.5000    0.5625])


% === Plot local virial stess: s12 (s12 is stored as s(2,1))
figure, hold on
s1299 = prctile(abs(s12grid(~isnan(s12grid))),99);
isosurface(Xw,Yw,Zw,s12grid,s1299)
isosurface(Xw,Yw,Zw,s12grid,-s1299)
hs = slice(Xw,Yw,Zw,s12grid,[boxcenter(1) xw(end)],...
    [boxcenter(2) yw(end)],...
    [fluidbox(3,1) boxcenter(3)]);
set(hs,'edgecolor','none','facealpha',0.6)
plotsolid()
lighting gouraud, camlight('left'), axis equal, view(3) % shading interp
hc = colorbar('AxisLocation','in','fontsize',14); hc.Label.String = '\sigma_{XY}';
title('Local virial stress: \sigma_{XY}','fontsize',20)
xlabel('X'), ylabel('Y'), zlabel('Z')
npart = 20;
[startX,startY,startZ] = meshgrid( ...
    double(xw(1)), ...
    double(yw(unique(round(1+(1+(linspace(-1,1,npart).*linspace(-1,1,npart).^2))*floor(length(yw)/2))))),...
    double(yw(unique(round(1+(1+(linspace(-1,1,npart).*linspace(-1,1,npart).^2))*floor(length(yw)/2))))) ...
  );
vstart = interp3(Xw,Yw,Zw,vXYZgridx,startX,startY,startZ); startX(vstart<0) = double(xw(end));
hsl = streamline(double(Xw),double(Yw),double(Zw),vXYZgridx,vXYZgridy,vXYZgridz,startX,startY,startZ);
set(hsl,'linewidth',2,'color','k')
plot3(startX(:),startY(:),startZ(:),'ro','markerfacecolor',[0.4375    0.5000    0.5625])


% === PLot Landshoff forces only 
figure, hold on
hs = slice(Xw,Yw,Zw,FXYZgridx,[xw(1) boxcenter(1)],...
    [yw(2) boxcenter(2) yw(end)],...
    [fluidbox(3,1) boxcenter(3)]);
set(hs,'edgecolor','none','facealpha',0.9)
axis equal, view(3),
hc = colorbar('AxisLocation','in','fontsize',14); hc.Label.String = 'Landshoff along X';
xlabel('X'), ylabel('Y'), zlabel('Z')
title('Landshoff forces along X','fontsize',20)
step = [3 5 5];
quiver3( ...
    Xw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    Yw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    Zw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridx(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridy(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridz(1:step(1):end,1:step(2):end,1:step(3):end) ...
    ,1,'color','k','LineWidth',2)


%% Hertz contact solid-fluid
% ===========================
XFluidSolid = Xstress.ATOMS(union(ifluid,isolid),:);
figure, hold on
plot3D(XFluidSolid{XFluidSolid.isfluid,coords},'bo','markersize',3,'markerfacecolor','b')
plot3D(XFluidSolid{XFluidSolid.issolid,coords},'ro','markersize',16,'markerfacecolor','r')
Rfluid = 1.04e-5; % m
Rsolid = 1.56e-5; % m
Rfluid = Rsolid;
hhertz = 2*Rsolid;
[Vcontactsolid,~,dmincontact] = buildVerletList(XFluidSolid,hhertz,[],[],[],XFluidSolid.isfluid,XFluidSolid.issolid);
configHertz = struct('R',{Rsolid Rfluid},'E',2000);
[FHertzSolid,WHertzSolid] = forceHertz(XFluidSolid,Vcontactsolid,configHertz);
fhertz = sqrt(sum(FHertzSolid.^2,2));
statvec(fhertz(fhertz>0),'Hertz',sprintf('<-- TIMESTEP: %d\n\tsubjected to Rsolid=[%0.4g %0.4g] dmin/2=%0.4g',timestepforstress,configHertz(1).R,configHertz(2).R,dmincontact/2))

% project Hertz contact on accurate grid (Cartesian)
soliddbox = [ min(Xstress.ATOMS{isolid,coords})-4*rbead
              max(Xstress.ATOMS{isolid,coords})+4*rbead ]';
boxcenter = mean(soliddbox,2);
resolution = ceil(50 * diff(soliddbox,[],2)'./max(diff(soliddbox,[],2)));
xw = linspace(soliddbox(1,1),soliddbox(1,2),resolution(1));
yw = linspace(soliddbox(2,1),soliddbox(2,2),resolution(2));
zw = linspace(soliddbox(3,1),soliddbox(3,2),resolution(3));
[Xw,Yw,Zw] = meshgrid(xw,yw,zw);
XYZgrid = [Xw(:),Yw(:),Zw(:)];
VXYZ = buildVerletList({XYZgrid XFluidSolid{:,coords}},1.1*hhertz);
W = kernelSPH(hhertz,'lucy',3); % kernel for interpolation (not gradkernel!)
FXYZgrid = interp3SPHVerlet(XFluidSolid{:,coords},FHertzSolid,XYZgrid,VXYZ,W,Vbead);
FXYZgridx = reshape(FXYZgrid(:,1),size(Xw));
FXYZgridy = reshape(FXYZgrid(:,2),size(Yw));
FXYZgridz = reshape(FXYZgrid(:,3),size(Zw));
WXYZgrid2 = interp3cauchy(Xw,Yw,Zw,FXYZgridx,FXYZgridy,FXYZgridz);
s12grid2 = reshape(WXYZgrid2(:,:,:,2),size(Xw));

%% Rough plot of Hertz Contact Tensor (component xy) - SOLID-FLUID
figure, hold on
hs = slice(Xw,Yw,Zw,s12grid2, ...
    boxcenter(1),...
    boxcenter(2),...
    boxcenter(3));
set(hs,'edgecolor','none','facealpha',0.9)
axis equal, view(3),
hc = colorbar('AxisLocation','in','fontsize',14); hc.Label.String = 'Hertz Tensor xy';
xlabel('X'), ylabel('Y'), zlabel('Z')
title('Hertz tensor','fontsize',20)
step = [2 2 2];
quiver3( ...
    Xw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    Yw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    Zw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridx(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridy(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridz(1:step(1):end,1:step(2):end,1:step(3):end) ...
    ,1.5,'color','k','LineWidth',2)


%% Advanced plot for Hertz Contacts
% almost same code as example2: 

% === STEP 1/5 === Original Delaunay triangulation and the convex hull
% this step has been already done as the begining of example2bis.m
% DT = delaunayTriangulation(double(Xstress.ATOMS{isolidcontact, coords}));
% K = convexHull(DT);
% === STEP 2/5 === refine the initial mesh by adding midpoints
% Extract the convex hull points and faces
hullPoints = DT.Points;
hullFaces = DT.ConnectivityList(K, :);
% Initialize a set to keep track of midpoints to ensure they are unique
midpointSet = zeros(0, 3);
% Calculate midpoints for each edge in each triangle and add to the point list
for faceIdx = 1:size(hullFaces, 1)
    face = hullFaces(faceIdx, :);
    for i = 1:3
        for j = i+1:3
            midpoint = (hullPoints(face(i), :) + hullPoints(face(j), :)) / 2;        
            if isempty(midpointSet) || ~ismember(midpoint, midpointSet, 'rows')
                midpointSet = [midpointSet; midpoint]; %#ok<AGROW>
            end
        end
    end
end
% Merge the original points and the new midpoints, update the the Delaunay triangulation
newDT = delaunayTriangulation([hullPoints; midpointSet]);
newK = convexHull(newDT);
% === STEP 3/5 ===  Laplacian Smoothing
points = newDT.Points;         % === Extract points and faces
faces = newDT.ConnectivityList(newK, :);
n = size(points, 1);           % === Initialize new points
newPoints = zeros(size(points)); 
neighbors = cell(n, 1);        % List of neighbors
for faceIdx = 1:size(faces, 1) % === Find the neighbors of each vertex
    face = faces(faceIdx, :);
    for i = 1:3
        vertex = face(i);
        vertex_neighbors = face(face ~= vertex);
        neighbors{vertex} = unique([neighbors{vertex}; vertex_neighbors(:)]);
    end
end
for i = 1:n                   % === Laplacian smoothing
    neighbor_indices = neighbors{i};
    if isempty(neighbor_indices) % Keep the point as is if it has no neighbors
        newPoints(i, :) = points(i, :); 
    else % Move the point to the centroid of its neighbors
        newPoints(i, :) = mean(points(neighbor_indices, :), 1);
    end
end
% Update the Delaunay triangulation with the smoothed points
newDT = delaunayTriangulation(newPoints);
newK = convexHull(newDT);
% === STEP 4/5 === Interpolate the Hertz forces on the triangular mesh
XYZhtri = newDT.Points;
XYZh = XFluidSolid{:,coords}; % kernel centers
VXYZh = buildVerletList({XYZhtri XFluidSolid{:,coords}},1.1*hhertz); % special grid syntax
W = kernelSPH(hhertz,'lucy',3); % kernel expression
FXYZtri = interp3SPHVerlet(XFluidSolid{:,coords},FHertzSolid,XYZhtri,VXYZh,W,Vbead);
% === STEP 5/5 === Extract tagential forces
% Calculate face normals and centroids
points = newDT.Points;
faces = newK;
v1 = points(faces(:, 1), :) - points(faces(:, 2), :);
v2 = points(faces(:, 1), :) - points(faces(:, 3), :);
faceNormals = cross(v1, v2, 2);
faceNormals = faceNormals ./ sqrt(sum(faceNormals.^2, 2));
centroids = mean(reshape(points(faces, :), size(faces, 1), 3, 3), 3);
% Interpolate force at each centroid using scatteredInterpolant for each component
FInterp_x = scatteredInterpolant(XYZhtri, double(FXYZtri(:,1)), 'linear', 'nearest');
FInterp_y = scatteredInterpolant(XYZhtri, double(FXYZtri(:,2)), 'linear', 'nearest');
FInterp_z = scatteredInterpolant(XYZhtri, double(FXYZtri(:,3)), 'linear', 'nearest');
FXYZtri_at_centroids = [FInterp_x(centroids), FInterp_y(centroids), FInterp_z(centroids)];
% Calculate normal and tangential components of the force at each face centroid
normalComponent = dot(FXYZtri_at_centroids, faceNormals, 2);
normalForce = repmat(normalComponent, 1, 3) .* faceNormals;
tangentialForce = FXYZtri_at_centroids - normalForce;
tangentialMagnitude = sqrt(sum(tangentialForce.^2, 2));
% Do the figure
figure, hold on
trisurfHandle = trisurf(newK, newDT.Points(:, 1), newDT.Points(:, 2), newDT.Points(:, 3), 'Edgecolor', 'k', 'FaceAlpha', 0.6);
set(trisurfHandle, 'FaceVertexCData', tangentialMagnitude, 'FaceColor', 'flat');
colorbar;
% Quiver plot to show the forces with an adjusted step
step = [2 2 2]*2;
quiver3( ...
    Xw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    Yw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    Zw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridx(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridy(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridz(1:step(1):end,1:step(2):end,1:step(3):end) ...
    ,1.5,'color','k','LineWidth',2)
axis equal; view(3), camlight('headlight'); camlight('left'); lighting phong; colorbar;
title('Hertz Forces onto the Tessellated Surface','fontsize',20);
xlabel('X'); ylabel('Y'); zlabel('Z')
hc = colorbar('AxisLocation','in','fontsize',14); 


%% Hertz contact wall-fluid
% ==========================
XFluidWall = Xstress.ATOMS(union(ifluid,iwall),:);
figure, hold on
plot3D(XFluidWall{XFluidWall.isfluid,coords},'bo','markersize',3,'markerfacecolor','b')
plot3D(XFluidWall{XFluidWall.iswall,coords},'ko','markersize',16,'markerfacecolor','k')
Rfluid = 1.04e-5; % m
Rsolid = 1.56e-5; % m
Rfluid = Rsolid;
hhertz = 2*Rsolid;
[Vcontactwall,~,dmincontact] = buildVerletList(XFluidWall,hhertz,[],[],[],XFluidWall.isfluid,XFluidWall.iswall);
configHertz = struct('R',{Rsolid Rfluid},'E',2000,'rho',1000,'m',9.04e-12,'h',hhertz);
[FHertzWall,WHertzWall] = forceHertz(XFluidWall,Vcontactwall,configHertz);
fhertz = sqrt(sum(FHertzWall.^2,2));
statvec(fhertz(fhertz>0),'Hertz',sprintf('<-- TIMESTEP: %d\n\tsubjected to Rsolid=[%0.4g %0.4g] dmin/2=%0.4g',timestepforstress,configHertz(1).R,configHertz(2).R,dmincontact/2))
figure, stem3(XFluidWall.x,XFluidWall.y,FHertzWall(:,1),'k.')

% project Hertz contact on accurate grid (Cartesian)
[wallbox1,wallbox2] = deal(fluidbox);
wallbox1(2,1) = fluidbox(2,1) - 1.5*hhertz;
wallbox1(2,2) = fluidbox(2,1) + 1.5*hhertz;
wallbox2(2,1) = fluidbox(2,2) - 1.5*hhertz;
wallbox2(2,2) = fluidbox(2,2) + 1.5*hhertz;
boxcenter = mean(fluidbox,2);
boxcenter1 = mean(wallbox1,2);
boxcenter2 = mean(wallbox2,2);
resolution1 = ceil(120 * diff(wallbox1,[],2)'./max(diff(wallbox1,[],2)));
resolution2 = ceil(120 * diff(wallbox2,[],2)'./max(diff(wallbox2,[],2)));
xw = linspace(wallbox1(1,1),wallbox1(1,2),resolution1(1));
yw1 = linspace(wallbox1(2,1),wallbox1(2,2),resolution1(2));
yw2 = linspace(wallbox2(2,1),wallbox2(2,2),resolution2(2));
zw = linspace(wallbox1(3,1),wallbox1(3,2),resolution1(3));
[Xw,Yw,Zw] = meshgrid(xw,[yw1 boxcenter(2) yw2],zw);
XYZgrid = [Xw(:),Yw(:),Zw(:)];
VXYZ = buildVerletList({XYZgrid XFluidWall{:,coords}},1.1*hhertz);
W = kernelSPH(hhertz,'lucy',3); % kernel for interpolation (not gradkernel!)
FXYZgrid = interp3SPHVerlet(XFluidWall{:,coords},FHertzWall,XYZgrid,VXYZ,W,Vbead);
FXYZgridx = reshape(FXYZgrid(:,1),size(Xw));
FXYZgridy = reshape(FXYZgrid(:,2),size(Yw));
FXYZgridz = reshape(FXYZgrid(:,3),size(Zw));
WXYZgrid2 = interp3cauchy(Xw,Yw,Zw,FXYZgridx,FXYZgridy,FXYZgridz);
s12grid2 = reshape(WXYZgrid2(:,:,:,2),size(Xw));

%% Rough plot of Hertz Contact Tensor (component xy)
figure, hold on
hs = slice(Xw,Yw,Zw,s12grid2, ...
    single([]),...
    [fluidbox(2,1)-[-.1 0 .1 0.5 1]*rbead/2 ,fluidbox(2,2)+[-.1 0 .1 0.5 1]*rbead/2],...
    single([]));
set(hs,'edgecolor','none','facealpha',0.9)
axis equal, view(3),
hc = colorbar('AxisLocation','in','fontsize',14); hc.Label.String = 'Hertz Tensor xy';
xlabel('X'), ylabel('Y'), zlabel('Z')
title('Hertz tensor','fontsize',20)
step = [4 1 4];
quiver3( ...
    Xw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    Yw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    Zw(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridx(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridy(1:step(1):end,1:step(2):end,1:step(3):end), ...
    FXYZgridz(1:step(1):end,1:step(2):end,1:step(3):end) ...
    ,.5,'color','k','LineWidth',.1)
caxis([-.1 .1]), view([-50,42])