% ####################################################################################
%   This is fork of the main script Billy_reusults_template_PBC
%   To be used for testing alternative parameters on a non main stream machine
% ####################################################################################

% First template to retrieve Billy's paper 2 simulation data 
% rev. 2024/03/17 - forked in 2024/03/16 with PBC

% 2024/03/07 implementation of reverse streamlines, streamline binning from their initial positions, subsampling
% 2024/03/12 implement bead along streamlines (bug:NaN and Inf not allowed.) 
% 2024/03/16 fork from Billy_results_template.m (MAJOR UPDATE)
% 2024/03/17 release candidate
% 2024/03/21 preproduction
% 2024/03/24 major update: full implementation of density correction and force contours around objects
% 2024/03/24 selective copy possible if originalroot is made available
% 2024/03/24 add prefetch management
% 2024/03/25 first batch of preproduction tframe 0.3->1.1 (step 0.01)
% 2024/03/26 second batch of preproduction tframe 0.11->0.4 (step 0.01)
% 2024/03/27 fix streamlines when less than one bead must be added (tframe = 0.11 and 0.27)
% 2024/03/27 fix contour, tangents/normals, add perssure
% 2024/03/27 Senstivity challenge test using ngenerations = 8 and xshift = double(mod(igen-1,2)*(xwPBC(indxstreamline(2))-xwPBC(indxstreamline(1))));


% SUMMARY

% This MATLAB script is a comprehensive framework for analyzing fluid dynamics simulations, specifically focusing on the distribution and movement of particles or beads in a fluid environment. Key functionalities include:
% 
% 1. Environment Setup:
%   Initializes the simulation environment by clearing variables, setting up output folders, and defining file paths to simulation data, with adjustments for periodic boundary conditions (PBC).
% 2. Data Retrieval:
%   Loads simulation data from specified file paths, handling different configurations and viscosity models.
% 3. Simulation Analysis:
%   Processes the simulation data to calculate parameters such as bead sizes, timestep intervals, and spatial distributions of particles.
% 4. Frame Selection:
%   Identifies simulation frames for detailed analysis based on time criteria, with capabilities to adjust for available data subsets.
% 5. Velocity Field and Density Calculation:
%   Computes the velocity field at a specific plane in the simulation domain and estimates the local density of particles.
% 6. Streamline and Bead Distribution Analysis:
%   Generates streamlines and distributes beads along these lines, incorporating PBC adjustments to simulate continuous fluid flow across boundaries.
% 7. Overlap Removal:
%   Implements algorithms to remove overlapping beads based on their spatial proximity and streamline generation, ensuring a realistic particle distribution.
% 8. Density Filtering:
%   Filters out beads in regions of excessively high simulated density to adhere to physical constraints.
% 9. Contact Detection with Objects:
%   Identifies beads in contact with solid objects within the simulation, leveraging density information to infer interaction dynamics.
% 10. Visual Representation:
%   Provides extensive plotting capabilities to visualize various aspects of the simulation, including velocity fields, bead distributions, and pressure around objects, with options to export figures.

%% Definitions
close all
clearvars -except tframe tframelist RESETPREFETCH
outputfolder = fullfile(pwd,'preproduction');
prefetchfolder = fullfile(pwd,'prefetch');
if ~exist(outputfolder,'dir'), mkdir(outputfolder); end
if ~exist(prefetchfolder,'dir'), mkdir(prefetchfolder); end
fighandle = @(id) formatfig(figure,'figname',sprintf('t%0.3g_%s',tframe,id));
printhandle = @(hfig) print_png(300,fullfile(outputfolder,[get(hfig,'filename') '.png']),'','',0,0,0);
if ~exist('RESETPREFETCH','var'), RESETPREFETCH = false; end
prefetchvar = @(varargin) fullfile(prefetchfolder,sprintf('t%0.4f_%s.mat',tframe,varargin{1}));
isprefetch = @(varargin) exist(prefetchvar(varargin{1}),'file') && ~RESETPREFETCH;

%% path and metadata
originalroot = '/media/olivi/T7 Shield/Thomazo_V2';
if exist(originalroot,'dir')
    root = originalroot;
    rootlocal = fullfile(pwd,'smalldumps');
    copymode = true;
else
    root = fullfile(pwd,'smalldumps');
    copymode = false;
end

simfolder = ...
    struct(...
    'A1',struct('artificial',...
'Production/numericalViscosimeter_reference_ulsphBulk_hertzBoundary/dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle.tar.gz',...
    'Morris',...
'Production/numericalViscosimeter_reference_morrisBulk_hertzBoundary/dump.morrisBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle.tar.gz' ...
                ),...
    'A2',struct('artificial',...
'./Production/numericalViscosimeter_reference_ulsphBulk_hertzBoundary/dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle_2.tar.gz' ...
    ),...
    'B1',struct('Morris',...
'./Production/numericalViscosimeter_reference_morrisBulk_hertzBoundary/dump.morrisBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle_soft.tar.gz' ...
    ),...
    'B2',struct('Morris',...
'Production/numericalViscosimeter_reference_morrisBulk_hertzBoundary/dump.morrisBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle_soft_1.tar.gz' ...
    ),...
    'B3',struct('Morris',...
'/Production/numericalViscosimeter_reference_morrisBulk_hertzBoundary/dump.morrisBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle_soft_2_3.tar.gz' ...
    ) ...
    );

% selection (not change it if you do not have the full dataset/hard disk attached to your system)
config = 'A1';
viscosity = 'Morris';
sourcefolder= fullfile(root,rootdir(simfolder.(config).(viscosity)));
sourcefile = regexprep(lastdir(simfolder.(config).(viscosity)),'.tar.gz$','');
dumpfile = fullfile(sourcefolder,sourcefile);

%% extract information
X0 = lamdumpread2(dumpfile); % first frame
natoms = X0.NUMBER;
timesteps = X0.TIMESTEPS;
X1 = lamdumpread2(dumpfile,'usesplit',[],timesteps(2));
dt = (X1.TIME-X0.TIME)/(timesteps(2)-timesteps(1)); % integration time step
times = double(timesteps * dt); % in seconds 
atomtypes = unique(X0.ATOMS.type);
ntimesteps = length(timesteps);
T = X0.ATOMS.type;
natomspertype = arrayfun(@(t) length(find(T==t)),atomtypes);
[~,ind] = sort(natomspertype,'descend');
% Thomazo simulation details
fluidtype  = ind(1);
pillartype = ind(2);
walltype   = ind(3);
spheretype = ind(4);
coords = {'z','x','y'}; % to match Thomazo's movies
vcoords = cellfun(@(c) sprintf('v%s',c),coords,'UniformOutput',false);
icoords = cellfun(@(c) find(ismember({'x','y','z'},c)),coords); %<- use this index for BOX
% Simulation parameters
mbead = 4.38e-12; % kg
rho = 1000; % kg / m3 (density of the fluid)
Vbead = mbead/rho;


%% copy files (if possible)
if copymode
    myprefetchfile = @(itime) sprintf('%s%09d.mat','TIMESTEP_',itime);
    myprefetchfolder = @(d) fullfile(d,sprintf('PREFETCH_%s',lastdir(dumpfile)));
    destinationfolder = fullfile(rootlocal,rootdir(simfolder.(config).(viscosity)));
    sourcefolderPREFETCH = myprefetchfolder(sourcefolder);
    destinationfolderPREFETCH = myprefetchfolder(destinationfolder);
    tcopy = 0.1:0.01:1.1;
    tfile = arrayfun(@(t) myprefetchfile(t), timesteps(unique(nearestpoint(tcopy,times))),'UniformOutput',false);
    oksource = all(cellfun(@(f) exist(fullfile(sourcefolderPREFETCH,f),'file'),tfile));
    if ~oksource, error('the source folder is corrupted, please check'), end
    existingfiles = cellfun(@(f) exist(fullfile(destinationfolderPREFETCH,f),'file'),tfile);
    dispf('Number of files to copy: %d (%d already available)',length(find(~existingfiles)),length(find(existingfiles)))
    copysuccess = cellfun(@(f) copyfile(fullfile(sourcefolderPREFETCH,f),fullfile(destinationfolderPREFETCH,f)),tfile(~existingfiles));
    dispf('%d of %d files have been copied',length(find(copysuccess)),length(copysuccess));
end

%% Estimate bead size from the first frame
% first estimate assuming that the bead is a cube
fluidxyz0 = X0.ATOMS{T==fluidtype,coords};
boxdims = X0.BOX(:,2) - X0.BOX(:,1);
Vbead_guess = prod(boxdims)/natoms;
rbead_guess = (3/(4*pi)*Vbead_guess)^(1/3);
cutoff = 3*rbead_guess;
if isprefetch('verletList')
    load(prefetchvar('verletList'))
else
    [verletList,cutoff,dmin,config,dist] = buildVerletList(fluidxyz0,cutoff);
    save(prefetchvar('verletList'),'verletList','cutoff','dmin','config','dist')
end
rbead = dmin/2;
s = 2*rbead; % separation distance
h = 2*s;     % smoothing length

%% load the frame closest to simulation time: tframe
% with the mini dataset, are available:
% 0.30s 0.40s 0.45s 0.50s 0.55s 0.60s 0.65s 0.70s 0.75s 0.80s 0.85s 0.90s 0.95s 1.00s 1.05s 1.10s 
% tframelist = [0.3 0.4 0.45:0.05:1.10]; % verysmalldumps
tframelist = 0.1:0.01:1.1; % updated time frames
if ~exist('tframe','var')
    tframe = 0.85; %0.55; % s <-------------------- select time here
else
    tframe = tframelist(nearestpoint(tframe,tframelist)); % restrict to existing tframes
end
iframe = nearestpoint(tframe,times); % closest index
Xframe = lamdumpread2(dumpfile,'usesplit',[],timesteps(iframe));
Xframe.ATOMS.isfluid = Xframe.ATOMS.type==fluidtype;
Xframe.ATOMS.ispillar = Xframe.ATOMS.type==pillartype;
Xframe.ATOMS.issphere = Xframe.ATOMS.type==spheretype;
Xframe.ATOMS.issolid = Xframe.ATOMS.type==spheretype | Xframe.ATOMS.type==pillartype;
fluidxyz = Xframe.ATOMS{Xframe.ATOMS.isfluid,coords};
fluidid = X0.ATOMS{Xframe.ATOMS.isfluid,'id'};
pillarxyz = Xframe.ATOMS{Xframe.ATOMS.ispillar,coords};
pillarid = X0.ATOMS{Xframe.ATOMS.ispillar,'id'};
spherexyz = Xframe.ATOMS{Xframe.ATOMS.issphere,coords};
sphereid = X0.ATOMS{Xframe.ATOMS.issphere,'id'};
solidxyz = Xframe.ATOMS{Xframe.ATOMS.issolid,coords};
solidid = X0.ATOMS{Xframe.ATOMS.issolid,'id'};
ztop = max(pillarxyz(:,3)); % pillar top

%% Interpolate velocity field at z = ztop
% full box (note that atoms may be outside of this box)
box = Xframe.BOX(icoords,:); % note that the order is given by coords, here {'z'}    {'x'}    {'y'}
boxsize = diff(box,1,2);
% fluidbox (box for atoms to consider)
xmin = min(Xframe.ATOMS{Xframe.ATOMS.isfluid,coords{1}});
xmax = max(Xframe.ATOMS{Xframe.ATOMS.isfluid,coords{1}});
ymin = min(Xframe.ATOMS{Xframe.ATOMS.isfluid,coords{2}});
ymax = max(Xframe.ATOMS{Xframe.ATOMS.isfluid,coords{2}});
zmin = min(Xframe.ATOMS{Xframe.ATOMS.isfluid,coords{3}});
zmax = max(Xframe.ATOMS{Xframe.ATOMS.isfluid,coords{3}});
fluidbox = [xmin xmax;ymin ymax;zmin zmax];
% restrict interpolation to the viewbox
viewbox = fluidbox; viewbox(3,:) = [ztop-2*h ztop+2*h];
insideviewbox = true(height(Xframe.ATOMS),1);
for icoord = 1:3
    insideviewbox = insideviewbox ...
        & Xframe.ATOMS{:,coords{icoord}}>=viewbox(icoord,1) ...
        & Xframe.ATOMS{:,coords{icoord}}<=viewbox(icoord,2);
end
XYZ  = Xframe.ATOMS{insideviewbox & Xframe.ATOMS.isfluid,coords};  % fluid kernel centers
vXYZ = Xframe.ATOMS{insideviewbox & Xframe.ATOMS.isfluid,vcoords}; % velocity of fluid kernel centers
XYZs = Xframe.ATOMS{insideviewbox & Xframe.ATOMS.issolid,coords};  % solid kernel centers
rhobeadXYZ = Xframe.ATOMS.c_rho_smd(insideviewbox & Xframe.ATOMS.isfluid); % volume of the bead

% force incell (this step is needed to apply PBC)
XYZ = PBCincell(XYZ,box,[true,true,false]);
XYZs = PBCincell(XYZs,box,[true,true,false]);

% add PBC images
[XYZimagesONLY ,indXimagesONLY]= PBCimages(XYZ,box,[true,true,false],2*h);
figure, hold on, plot3D(XYZ,'go')
plot3D(XYZ(indXimagesONLY,:),'go','markerfacecolor','g')
plot3D(XYZimagesONLY,'ro','markerfacecolor','r'), view(3), axis equal, view(2)
XYZwithImages = [XYZ;XYZimagesONLY];
vXYZwithImages = [vXYZ;vXYZ(indXimagesONLY,:)];
rhobeadXYZwithImages = [rhobeadXYZ;rhobeadXYZ(indXimagesONLY)];
VbeadXYZwithImages = mbead./rhobeadXYZwithImages;
isImages = true(size(XYZwithImages,1),1); isImages(1:size(XYZ,1))=false;

% interpolation grid (central grid, no images)
nresolution = [1024 1024 1];
xw = linspace(box(1,1),box(1,2),nresolution(1));
yw = linspace(box(2,1),box(2,2),nresolution(1));
zw = ztop;
[Xw,Yw,Zw] = meshgrid(xw,yw,zw);
XYZgrid = [Xw(:),Yw(:),Zw(:)];

% grid neighbors (incl. images) for interpolation and discarding grid points overlapping solid
if isprefetch('VXYZ')
    load(prefetchvar('VXYZ'))
else
    VXYZ  = buildVerletList({XYZgrid XYZwithImages},1.2*h);  % neighbors = fluid particles
    VXYZs = buildVerletList({XYZgrid XYZs},0.85*s); % neighbors = solid particles
    save(prefetchvar('VXYZ'),'VXYZ','VXYZs')
end
icontactsolid = find(cellfun(@length,VXYZs)>0);
VXYZ(icontactsolid) = repmat({[]},length(icontactsolid),1);

% interpolation on the grid of the 3D velocity (central grid)
% Do not forget even if we are applying a 2D interpretation, we use a 3D simulation
% 3D velocity are projected on 2D streamlines even if the projection of the 3rd component is 0
W = kernelSPH(h,'lucy',3); % kernel expression
if isprefetch('v3XYZgrid')
    load(prefetchvar('v3XYZgrid'))
else
    v3XYZgrid = interp3SPHVerlet(XYZwithImages,vXYZwithImages,XYZgrid,VXYZ,W,VbeadXYZwithImages);
    save(prefetchvar('v3XYZgrid'),'v3XYZgrid')
end
vxXYZgrid = reshape(v3XYZgrid(:,1),size(Xw)); %vxXYZgrid(isnan(vxXYZgrid)) = 0;
vyXYZgrid = reshape(v3XYZgrid(:,2),size(Xw)); %vyXYZgrid(isnan(vyXYZgrid)) = 0;
vzXYZgrid = reshape(v3XYZgrid(:,3),size(Xw)); %vzXYZgrid(isnan(vzXYZgrid)) = 0;
vXYZgrid  = reshape(sqrt(sum(v3XYZgrid.^2,2)),size(Xw));

% density on the grid (with a possible different h)
if isprefetch('rhobeadXYZgrid')
    load(prefetchvar('rhobeadXYZgrid'))
else
    rhobeadXYZgrid = interp3SPHVerlet(XYZwithImages,rhobeadXYZwithImages,XYZgrid,VXYZ,W,VbeadXYZwithImages);
    save(prefetchvar('rhobeadXYZgrid'),'rhobeadXYZgrid')
end
rhobeadXYZgrid = reshape(rhobeadXYZgrid,size(Xw));

% add PBC (add periodic PBC)
[vxXYZPBC,XwPBC,YwPBC] = PBCgrid(Xw,Yw,vxXYZgrid,[true,true],boxsize(1:2)./[8;2]);
rhobeadXYZPBC = PBCgrid(Xw,Yw,rhobeadXYZgrid,[true,true],boxsize(1:2)./[8;2]);
xwPBC = XwPBC(1,:); ywPBC = YwPBC(:,1)';
fluidboxPBC = double([xwPBC([1 end]);ywPBC([1 end]);fluidbox(3,:)]);
fluidboxsizePBC = diff(fluidboxPBC,1,2);
vyXYZPBC = PBCgrid(Xw,Yw,vyXYZgrid,[true,true],boxsize(1:2)./[8;2]);
vzXYZPBC = PBCgrid(Xw,Yw,vzXYZgrid,[true,true],boxsize(1:2)./[8;2]);
vXYZPBC = sqrt(vxXYZPBC.^2 + vyXYZPBC.^2 + vzXYZPBC.^2);
figure, mesh(XwPBC,YwPBC,vXYZPBC), axis equal, view(2), colorbar, title(sprintf('t=%0.3f s - velocity (m/s)',tframe))
figure, mesh(XwPBC,YwPBC,rhobeadXYZPBC); axis equal, view(2), colorbar, title(sprintf('t=%0.3f s - density (kg/m3)',tframe))

%% Plot (attention 2D, meshgrid convention)
figure, hold on
% velocity magnitude
imagesc(xwPBC,ywPBC,vXYZPBC)
axis tight, axis equal
colorbar
title(sprintf('t=%0.3f s - velocity (m/s)',tframe))

% quiver configuration and plot (boundaries are with PBC)
stepPBC = 16;
boundariesPBC = ...
             [ nearestpoint(double(xwPBC([1,end]))+fluidboxsizePBC(1)/100*[1 -1],double(xwPBC)) % x
               nearestpoint(double(ywPBC([1,end]))+fluidboxsizePBC(2)/100*[1 -1],double(ywPBC)) % y
             ];
indxquiver = boundariesPBC(1,1):stepPBC:boundariesPBC(1,2); % x indices
indyquiver = boundariesPBC(2,1):stepPBC:boundariesPBC(2,2); % y indices
quiver(XwPBC(indyquiver,indxquiver),YwPBC(indyquiver,indxquiver), ...
          vxXYZPBC(indyquiver,indxquiver),vyXYZPBC(indyquiver,indxquiver), ...
        'color','k','LineWidth',1)


%% streamlines
% UP from bottom (starting position) to top
% DOWN from top to bottom (same starting position by reversing the velocity field)
% assembled as [flipud(DOWN(2:end,:));UP]
% CELL streamlines along a y period, the separation distance is added to avoid gap

% streamline configuration and plot
boundaries = [ nearestpoint(double(xw([1,end])),double(xwPBC))
               nearestpoint(double(yw([1,end])),double(ywPBC))
             ];
step = 8;
indxstreamline = boundaries(1,1):step:boundaries(1,2);
indystreamline = boundaries(2,1):step:boundaries(2,2);
nstreamlines = length(indxstreamline);

% Generative streamlines
ngenerations = 4*2;
iygen = unique(round(linspace(indystreamline(1),indystreamline(end),ngenerations)));
ngenerations = length(iygen);
[verticesgenUP,verticesgenDOWN,verticesgen,verticesgenCELL,verticesgenCELLid] = deal({});
validstreamline = @(v) (v(:,2)-v(1,2))<=(boxsize(2)*1.5) & (v(:,2)-v(1,2))>=(boxsize(2)*0.01); % longer than 1% but not exceeding 150%
for igen = 1:ngenerations
    % ith generation of stream line (from indystreamline(1))
    dispf('generates the %dth of %d generation of streamlines',igen,ngenerations)
    xshift = double(mod(igen-1,2)*(xwPBC(indxstreamline(2))-xwPBC(indxstreamline(1))));
    [startgenX,startgenY,startgenZ] = meshgrid(...
        double(xwPBC(indxstreamline))+xshift,...
        double(ywPBC(iygen(igen))),double(ztop));
    verticesgenUP{igen} = stream2(double(XwPBC),double(YwPBC),vxXYZPBC,vyXYZPBC,startgenX,startgenY,[0.03 5e4]);
    verticesgenDOWN{igen} = stream2(double(XwPBC),double(YwPBC),-vxXYZPBC,-vyXYZPBC,startgenX,startgenY,[0.03 5e4]);
    verticesgen{igen} = cellfun(@(d,u) [flipud(d(2:end,:)); u],verticesgenDOWN{igen},verticesgenUP{igen},'UniformOutput',false);
    verticesgen{igen} = cellfun(@(v) v(~isnan(v(:,2)),:),verticesgen{igen},'UniformOutput',false);
    verticesgenCELL{igen} = cellfun(@(v) v(validstreamline(v),:),verticesgen{igen},'UniformOutput',false);
    verticesgenCELLid{igen} = igen*ones(1,length(verticesgenCELL{igen}));
end

% merge all verticesCELL
verticesCELL = cat(2,verticesgenCELL{:});
verticesCELLid = cat(2,verticesgenCELLid{:});
okverticesCELL = cellfun(@length,verticesCELL)>100; % remove empty and too short streamlines (as a result of filtering by validstreamline)
verticesCELL = verticesCELL(okverticesCELL);
verticesCELLid = verticesCELLid(okverticesCELL);

% retrieve the separation distance
sLagrangian = startgenX(1,2,1) - startgenX(1,1,1); % separation distance between streamlines at injection/starting
rLagrangian = sLagrangian/2;


% detect interruption (for control)
% yfinalposition1UP = cellfun(@(v) v(end,2),vertices1UP);
% yfinalposition1DOWN = cellfun(@(v) v(end,2),vertices1DOWN);
% isinterrupted1 = isnan(yfinalposition1UP) | isnan(yfinalposition1DOWN);

% control plot
figure, hold on
imagesc(xwPBC,ywPBC,vXYZPBC)
colors = jet(ngenerations);

for igen = 1:ngenerations
    for i=1:nstreamlines
        plot(verticesgen{igen}{i}(:,1),verticesgen{igen}{i}(:,2),'-','LineWidth',0.5,'color',colors(igen,:))
        plot(verticesgenCELL{igen}{i}(:,1),verticesgenCELL{igen}{i}(:,2),'-','linewidth',1,'color',colors(igen,:));
    end
end
axis equal
title(sprintf('t=%0.3f s - streamlines',tframe))

%% Distribute beads along streamlines tagged as CELL
% Once PBC are applied, space is filled with possibly overlaping streamlines
% the control plot is showing this effect


traj = fillstreamline2(verticesCELL,XwPBC,YwPBC,vxXYZPBC,vyXYZPBC,rLagrangian,0);
ntraj = length(traj);
%trajUP = fillstreamline2(verticesUPCELL,XwPBC,YwPBC,vxXYZPBC,vyXYZPBC,rLagrangian,0);
%traj(~isinterrupted) = trajUP(~isinterrupted);
XYZbeads = arrayfun(@(t) t.cart_distribution,traj,'UniformOutput',false);
% we apply PBC while keeping the id of the streamline
[XYZbeadsPBC,XYZbeadsPBCid] = deal(cell(ntraj,1));
for itraj=1:ntraj % trajectories and streamlines are assumed equivalent at steady state
    XYZbeadsPBC{itraj} = PBCincell(XYZbeads{itraj},box(1:2,:),[true true]); % wrapping along PBC
    XYZbeadsPBCid{itraj} = ones(size(XYZbeadsPBC{itraj},1),1)*verticesCELLid(itraj);
end

% control plots
figure, hold on
colors = tooclear(jet(ntraj));
for itraj = 1:ntraj
    plot(XYZbeadsPBC{itraj}(:,1),XYZbeadsPBC{itraj}(:,2),'o','markerfacecolor',colors(itraj,:),'markeredgecolor',colors(itraj,:))
end
title(sprintf('t=%0.3f s - colors match streamline index',tframe))

figure, hold on
colors = tooclear(jet(ngenerations));
for itraj = 1:ntraj
    plot(XYZbeadsPBC{itraj}(:,1),XYZbeadsPBC{itraj}(:,2),'o','markerfacecolor',colors(XYZbeadsPBCid{itraj}(1),:),'markeredgecolor',colors(XYZbeadsPBCid{itraj}(1),:))
end
title(sprintf('t=%0.3f s - colors match generation index',tframe))

%% remove duplicated beads between streamlines (too close)
% defined as beads from another streamline located at less than rbead
% this version incorporate the effect of the generational distance (somekind of age)
% beads from other injections points should emerge from positions farther from first generations (older ones)
% the generation index starts from the source of the flow (bottom), using streamlines from other positions is discouraged (since younger)
% 
% Note: streamlines are indexed from oldest (closest to the source) to youngest (farthest from the source)

% beads from different streamlines
for i=1:ntraj % reference streamline (higher precedence)
    for j=1:ntraj % the other streamline
        if i~=j
            indj = find(~isnan(XYZbeadsPBC{j}(:,1)));
            dij=pdist2(XYZbeadsPBC{i},XYZbeadsPBC{j}(indj,:)); % Euclidian distance
            % the criterion on age is too strict
            %dgenij = pdist2(XYZbeadsPBCid{i},XYZbeadsPBCid{j}(indj,:)); % generational distance (0 for the same generation)
            %XYZbeadsPBC{j}(indj(any(dij<rLagrangian*sqrt(2)*(1+dgenij),1)),:) = NaN;
            XYZbeadsPBC{j}(indj(any(dij<rLagrangian*sqrt(2),1)),:) = NaN;
        end
    end
end

% beads from the same streamline
% two populations of beads are created (those inside and those outside (images) that could overlap those inside when they coordinates are wrapped)
%
% Note: we do not consider the overlapping of north and south images (the total height of a streamline is considered not to exceed 150% of the box height)
for i=1:ntraj
    isoutside =  (XYZbeads{i}(:,1)<box(1,1)) | (XYZbeads{i}(:,1)>box(1,2)) | ...
                 (XYZbeads{i}(:,2)<box(2,1)) | (XYZbeads{i}(:,2)>box(2,2) );
    isvalid = ~isnan(XYZbeadsPBC{i}(:,1));
    ioutside = find(isoutside & isvalid);  % these beads are possible images of beads already inside
    iinside =  find(~isoutside & isvalid); % these beads have higher precedence, they are already inside
    divsout=pdist2(XYZbeadsPBC{i}(iinside,:),XYZbeadsPBC{i}(ioutside,:));
    XYZbeadsPBC{i}(ioutside(any(divsout<rLagrangian*sqrt(2),1)),:) = NaN;
end

XYZbeadsPBCall = cat(1,XYZbeadsPBC{:});
XYZbeadsPBCidall = cat(1,XYZbeadsPBCid{:});
isPBCallok = ~isnan(XYZbeadsPBCall(:,1));
XYZbeadsPBCall = XYZbeadsPBCall(isPBCallok,:);
XYZbeadsPBCidall = XYZbeadsPBCidall(isPBCallok,:);

% control while keeping the generational index
hfig = fighandle('packing');  hold on
colors = tooclear(hsv(ngenerations)); %turbo
for igen=1:ngenerations
    viscircles(XYZbeadsPBCall(XYZbeadsPBCidall==igen,:),rLagrangian,'color',colors(igen,:));
end
title(sprintf('t=%0.3f s - one color per injection line',tframe)), axis equal

PRINTON = true;
if PRINTON, printhandle(hfig), end

%% Filtering: remove overlapping from different injections using a first estimate of density

% Summary
% This methodology effectively redistributes beads to ensure that local densities do not exceed
% the physical limits of the simulation, enhancing realism and accuracy. By adjusting bead 
% distributions based on calculated densities and employing PBC to handle edge cases, the script 
% ensures a uniformly plausible representation of bead distributions across the simulation domain.

hfilter = 4*rLagrangian;
XYbeadsfilterid = XYZbeadsPBCidall;
XYbeadsfilter = XYZbeadsPBCall; 
nfilter = size(XYbeadsfilter,1);
XYbeadsfilter_images= PBCimages(XYbeadsfilter,box(1:2,:),[true,true],2*hfilter);
XYbeadsfilterwithImages = [XYbeadsfilter;XYbeadsfilter_images];
Vbeadsfilter = buildVerletList(XYbeadsfilter,hfilter);
VbeadsfilterBC = buildVerletList({XYbeadsfilter XYbeadsfilterwithImages},hfilter);
Volfilter = length(find(~isnan(rhobeadXYZgrid(:))))/numel(rhobeadXYZgrid) * boxsize(1) * boxsize(2) * s;
mfilter = rho*Volfilter/size(XYbeadsfilter,1); % mass of a single bead (informed)
Vfilter = mfilter/rho;
Wfilter = kernelSPH(hfilter,'lucy',2);
rhofilter = interp2SPHVerlet(...
    XYbeadsfilterwithImages,...
    rho*ones(size(XYbeadsfilterwithImages,1),1),...
    XYbeadsfilter,VbeadsfilterBC,Wfilter,Vfilter)/s; 

% target
rhomax = 1500;
ok = rhofilter<=rhomax;

% before
hfig = fighandle('packing_rhomax');  hold on
viscircles(XYbeadsfilter(ok,:),rLagrangian,'color','b');
viscircles(XYbeadsfilter(~ok,:),rLagrangian,'color','r');
title(sprintf('t=%0.3f s - in red: excess density',tframe)), axis equal


PRINTON = true;
if PRINTON, printhandle(hfig), end

% do filter
itoohigh = find(~ok);
[rhotoohigh,ind] = sort(rhofilter(itoohigh),'descend');
itoohigh = itoohigh(ind);
kept = true(nfilter,1);
for k=1:length(itoohigh)
    % valid neighbors (only)
    jBC = VbeadsfilterBC{itoohigh(k)}; % it includes self with images
    njBC = length(jBC);
    j = Vbeadsfilter{itoohigh(k)}; % it includes self without images
    j = j(kept(j));
    [idj,ind] = sort(XYbeadsfilterid(j),'ascend');
    j = j(ind);  nj = length(j);
    jdeletable = j(find(idj>min(idj),1,'first'):end); % we keep the first type
    [rhojdeletable,ind] = sort(rhofilter(jdeletable),'descend');
    jdeletable = jdeletable(ind); njdeletable = length(jdeletable);
    njexcess = floor( (1 - rhomax/rhotoohigh(k)) * njBC );
    kept(jdeletable(1:min(njexcess,njdeletable))) = false;
end

% after
hfig = fighandle('packing_rhomax_fix');  hold on
viscircles(XYbeadsfilter(kept,:),rLagrangian,'color','g');
viscircles(XYbeadsfilter(~kept,:),rLagrangian,'color','r');
title(sprintf('t=%0.3f s - in red: removed beads',tframe)), axis equal

if PRINTON, printhandle(hfig), end



%% calculate density
XYinformed = PBCincell(XYZbeadsPBCall(kept,:),box,[true true]); % PBC just to be sure
ninformed = size(XYinformed,1);
rinformed = rLagrangian; %radius
sinformed = 2*rinformed; % separation distance
hinformed = 5*sinformed; % for integration

% add PBC images
[XYinformed_images ,indimages]= PBCimages(XYinformed,box(1:2,:),[true,true],2*hinformed);
XYinformedwithImages = [XYinformed;XYinformed_images];
% Verlet list for the original grid
XYgrid = [Xw(:) Yw(:)];
if isprefetch('VXYinformed')
    load(prefetchvar('VXYinformed'))
else
    VXYinformed  = buildVerletList({XYgrid XYinformedwithImages},hinformed);
    save(prefetchvar('VXYinformed'),'VXYinformed')
end
% Verlet list for the informed beads
if isprefetch('VXYbeadinformed')
    load(prefetchvar('VXYbeadinformed'))
else
    VXYbeadinformed = buildVerletList({XYinformed XYinformedwithImages},hinformed);
    save(prefetchvar('VXYbeadinformed'),'VXYbeadinformed')
end
   

% Calculate the mass of informed beads
% total volume of fluid in the image
Volinformed = length(find(~isnan(rhobeadXYZgrid(:))))/numel(rhobeadXYZgrid) * boxsize(1) * boxsize(2) * s;
mbeadinformed = rho*Volinformed/ninformed; % mass of a single bead (informed)

% 2D Kernel
Winformed = kernelSPH(hinformed,'lucy',2); % kernel expression [/m2]

% Calculate the volume of the beads
Vbeadinformedguess = mbeadinformed/rho; % first guess
% density at the centers of the informed beads
rhobeadinformed = interp2SPHVerlet(XYinformedwithImages,rho*ones(size(XYinformedwithImages,1),1),XYinformed,VXYbeadinformed,Winformed,Vbeadinformedguess);
rhobeadinformed = rhobeadinformed/s;
% rhobeadinformed(rhobeadinformed<200) = NaN;
% rhobeadinformed(isnan(rhobeadinformed)) = median(rhobeadinformed,'omitmissing'); 

% volume of the informed beads
Vbeadinformed = mbeadinformed./rhobeadinformed;
% normalized radius of informed beads
rbeadinformed = sqrt(Vbeadinformed/(s*pi));
rbeadinformed = rbeadinformed/median(rbeadinformed,'omitmissing') * rLagrangian;
% control figure
figure, viscircles(XYinformed,rLagrangian,'color','g'), axis equal, hold on
viscircles(XYinformed,rbeadinformed,'color','r')

% reference density at the same positions
XYZeqinformed = [XYinformed ones(ninformed,1)*ztop];
VXYZeqinformed  = buildVerletList({XYZeqinformed XYZwithImages},1.2*h);
rhobeadXYZ2XYinformed = interp3SPHVerlet(XYZwithImages,rhobeadXYZwithImages,XYZeqinformed,VXYZeqinformed,W,VbeadXYZwithImages);

% density on the grid
if isprefetch('dgrid')
    load(prefetchvar('dgrid'))
else
    dgrid = interp2SPHVerlet(XYinformedwithImages,rho*ones(size(XYinformedwithImages,1),1),XYgrid,VXYinformed,Winformed,Vbeadinformedguess);
    save(prefetchvar('dgrid'),'dgrid')
end
dgrid = reshape(dgrid/s,size(Xw)); % /s to get in kg/m3 from kg/m2
dgrid(isnan(rhobeadXYZgrid)) = NaN; % we mask the objects (pillar and sphere) the same way as in the reference


%% ---------------------------- PRODUCTION FIGURES
hfig = []; close all

% Density mapped on beads
hfig(end+1) = fighandle('d_bead_informed'); hold on, title(sprintf('[t=%0.3g s] density mapped to informed beads',tframe))
scatter(XYinformed(:,1),XYinformed(:,2),100*(rbeadinformed/min(rbeadinformed)).^2,rhobeadinformed,'filled'), colorbar
hfig(end+1) = fighandle('d_bead_reference'); hold on, title(sprintf('[t=%0.3g s] reference density mapped to informed beads',tframe))
scatter(XYZeqinformed(:,1),XYZeqinformed(:,2),100*(rbeadinformed/min(rbeadinformed)).^2,rhobeadXYZ2XYinformed,'filled'), colorbar
hfig(end+1) = fighandle('d_bead_informed_vs_reference'); plot(rhobeadXYZ2XYinformed(:),rhobeadinformed(:),'ro'), xlabel('reference density (back mapped)'), ylabel('informed density')
title(sprintf('[t=%0.3g s] informed vs. reference density',tframe))

% density mapped on the grid
hfig(end+1) = fighandle('d_grid_informed'); hp = pcolor(xw,yw,dgrid); hp.EdgeColor = 'none'; colorbar, title(sprintf('[t=%0.3g s] informed density (kg/m3)',tframe)), axis equal %, clim([500 1300])
haxtomodify = gca;
hfig(end+1) = fighandle('d_grid_reference'); hp = pcolor(xw,yw,rhobeadXYZgrid); hp.EdgeColor = 'none'; colorbar, title(sprintf('[t=%0.3g s] reference density (kg/m3)',tframe)), axis equal %, clim([500 1300])
clim(haxtomodify,clim)

% distribution of densities
hfig(end+1) = fighandle('distribution_rho');  hold on
histogram(rhobeadinformed), histogram(rhobeadXYZ2XYinformed), legend({'informed density','reference density'})
title(sprintf('[t=%0.3g s] Density distributions',tframe))


%% -- identify the beads in contact with objects based on density
% SUMMARY.
% This section outlines a methodology for identifying beads in contact with solid objects
% in a fluid simulation, particularly focusing on density-based criteria to determine close
% interactions and potential contact forces.

% Attention the sphere can exceed the area observed (overflow condition)
% Safe coordinates are only use for contour identification
isynan = isnan(mean(rhobeadXYZgrid(:,floor(size(rhobeadXYZgrid,2)*0.6):end),2));
isoverflow =  (find(isynan,1,'last')-find(isynan,1,'first')+1)==size(rhobeadXYZgrid,1);
if (find(isynan,1,'last')-find(isynan,1,'first')+1)==size(rhobeadXYZgrid,1) % reach top
    iyoverflow = find(~isynan,1,'first');
    iymargin = round(size(rhobeadXYZgrid,1)*0.1); % margin to add
    iysafe = iyoverflow+iymargin;          % index translation (along y)
    dysafe = -iysafe * ( Yw(2,1)-Yw(1,1) ); % distance translation (along y)
    [rXYgridsafe,Xwsafe,Ywsafe] = PBCgridshift(Xw,Yw,rhobeadXYZgrid,[0 iysafe]); % translate
    dgridsafe = PBCgridshift(Xw,Yw,dgrid,[0 iysafe]); % translate
    [XYinformedsafe,boxsafe] = PBCimagesshift(XYinformed,[0 dysafe],box(1:2,1:2));
elseif find(isynan,1,'first')==1
    iymargin = round(size(rhobeadXYZgrid,1)*0.1); % margin to add
    iyoverflow = iymargin;
    if isynan(end), iyoverflow = iyoverflow + length(iyoverflow)-find(~isynan,1,'last'); end
    iysafe = -iyoverflow;
    dysafe = -iysafe * ( Yw(2,1)-Yw(1,1) ); % distance translation (along y)
    [rXYgridsafe,Xwsafe,Ywsafe] = PBCgridshift(Xw,Yw,rhobeadXYZgrid,[0 iysafe]); % translate
    dgridsafe = PBCgridshift(Xw,Yw,dgrid,[0 iysafe]); % translate
    [XYinformedsafe,boxsafe] = PBCimagesshift(XYinformed,[0 dysafe],box(1:2,1:2));
else
    dysafe = 0;
    [rXYgridsafe,Xwsafe,Ywsafe] = deal(rhobeadXYZgrid,Xw,Yw);
    [dgridsafe,XYinformedsafe,boxsafe] = deal(dgrid,XYinformed,box);
end

% Volume of objects (GRID points): XYobjects where density is NaN vy definition
XYobjects = [Xwsafe(:) Ywsafe(:)];
XYobjects = XYobjects(isnan(rXYgridsafe),:);
% Looking for beads in contact with XYobjects (grid points)
V2 = buildVerletList({XYinformedsafe XYobjects},3*sinformed);
% Index of beads in contact with XYobjects (grid points)
icontact = find(cellfun(@length,V2)>0);
XYcontact = double(XYinformedsafe(icontact,:));
% Enclosed beads
k = boundary(XYcontact,1); nk = length(k);
XYcontactk = XYcontact(k,:);

% separation of the objects, contour parameterization, tangents, normals
% the pillar is assumed fixed
pillarcenter = [2.87,3.08]*1e-4; % 0.2880e-3    0.3131e-3, mean(objects(1).XY)
ispillar = vecnorm(XYcontactk - pillarcenter,2,2)<0.8e-4; %  7.7859e-05, max(vecnorm(XYcontactk(ispillar,:) - pillarcenters,2,2))
objects = struct('XY',{XYcontactk(ispillar,:) XYcontactk(~ispillar,:)},'marker',{'bo','ms'},'line',{'b-','m-'},'color',{'b','m'});
anglestep = pi/32;
angles = (-pi:anglestep:pi)';
for k = 1:length(objects)
    % fit each object as a circle to try to close the boundaries
    objects(k).fit = fitCircleFromPoints(objects(k).XY);
    missingangles = angles(abs(angles-objects(k).fit.angles(nearestpoint(angles,objects(k).fit.angles)))>anglestep);
    XYtoadd = objects(k).fit.XYgenerator(missingangles);
    XYclosed = [objects(k).XY;XYtoadd]; nXYclosed = floor(size(XYclosed,1)/2)*2;
    [anglesclosed,ind] = sort(objects(k).fit.angleGenerator(XYclosed));
    XYclosed = XYclosed (ind,:); % sort points according to angles
    % enforce periodic conditions along the index dimension
    objects(k).XYclosed = [XYclosed((nXYclosed/2+1):end,:) ; XYclosed ; XYclosed(1:(nXYclosed/2),:)];
    objects(k).n = size(objects(k).XYclosed,1);

    % First pass - contour twice longer than the real one
    % fit each obhect using a regularized spline approximation
    sp = csaps((1:objects(k).n)',objects(k).XYclosed',0.25); % smoothed cubic spline
    %sp = spaps((1:objects(k).n)',objects(k).XYclosed',0.001*sum(var(objects(k).XYclosed))*objects(k).n);
    spder = fnder(sp,1);

    % Second pass - approximation based on angles
    xycontours = fnval(sp,sp.breaks)';
    dxycontours = fnval(spder,sp.breaks)';
    xycircle = fitCircleFromPoints(xycontours);
    [xyangles,ind] = sort(xycircle.angles,'ascend');
    minangle = min(xyangles);
    maxangle = max(xyangles);
    xyangles = (2*(xyangles-minangle)/(maxangle-minangle)-1) * pi; % rescaled to close the figure
    xycontoursf = [ smooth(xyangles,xycontours(ind,1),0.15,'rloess'),...
                    smooth(xyangles,xycontours(ind,2),0.15,'rloess') ];
    dxycontoursf = [ smooth(xyangles,dxycontours(ind,1),0.15,'rloess'),...
                    smooth(xyangles,dxycontours(ind,2),0.15,'rloess') ];

    % Make all data unique
    [xyangles,ind] = unique(xyangles,'stable');
    xycontoursf = xycontoursf(ind,:);
    dxycontoursf = dxycontoursf(ind,:);
    xycontoursf([1 end],:) = [1;1] * mean(xycontoursf([1 end],:));
    dxycontoursf([1 end],:) = [1;1] * mean(dxycontoursf([1 end],:));

    % Third Pass using contour length instead of angle as variable
    % ATTENTION: for averaging it is preferable to use curvilinear coordinates
    lxycontour = [0; cumsum(sqrt(sum(diff(xycontoursf,1,1).^2,2)))];
    sp2 = csaps(lxycontour',xycontoursf');


    % Extract tangents at prescribed curvilinear coordinates
    xp = linspace(lxycontour(1),lxycontour(end),objects(k).n)';
    % center and apparent radius (for visualizing the force acting on the object)
    objects(k).XYboundary = fnval(sp2,xp)';
    objects(k).center = mean(objects(k).XYboundary);
    objects(k).radius = min(vecnorm(objects(k).XYboundary-objects(k).center,2,2));
    % tangents (from the spline approximation)
    %objects(k).tangents = ndf(xp,objects(k).XYboundary,1,[],'makeuniform',true); %curve2tangent(objects(k).XYboundary); %fnval(fnder(sp2,1),xp)';
    objects(k).tangents = fnval(fnder(sp2,1),xp)';
    objects(k).tangents = objects(k).tangents./vecnorm(objects(k).tangents,2,2); % Normalize the tangent vectors
    % normals (turn the normals to be inwards using inpolygon)
    objects(k).normals = [-objects(k).tangents(:,2),objects(k).tangents(:,1)]; % % Calculate the centroid of the shape
    testPoints = objects(k).XYboundary + 0.01 * objects(k).radius * objects(k).normals; % Choose a test point slightly offset from each boundary point along the normal
    isInside = inpolygon(testPoints(:,1), testPoints(:,2),...
        objects(k).XYboundary(:,1), objects(k).XYboundary(:,2)); % Use inpolygon to check if each test point is inside the shape
    objects(k).normals(~isInside, :) = -objects(k).normals(~isInside, :); % Flip the normals where the test point is outside the shape
    % add density, pressure information (look for the nearest beads closest to the boundary, average the value)
    objects(k).Vcontact = buildVerletList({objects(k).XYboundary XYcontact},3*sinformed);
    objects(k).Vcontact = cellfun(@(v) icontact(v)',objects(k).Vcontact,'UniformOutput',false); % Vcontact{i} index of beads in contact with XYboundary(i,:)
    objects(k).rhocontact = cellfun(@(v) mean(rhobeadinformed(v)),objects(k).Vcontact);
    objects(k).Pcontact = 1 + (objects(k).rhocontact/rho).^7-1; % reduced pressure P/B with P0/B=1
    objects(k).densitynormals = objects(k).rhocontact.*objects(k).normals/rho;
    objects(k).avdensitynormals = mean(objects(k).densitynormals,'omitmissing');
    objects(k).pressurenormals = objects(k).Pcontact.*objects(k).normals;
    objects(k).avpressurenormals = mean(objects(k).pressurenormals,'omitmissing');
end

% plot
hfig(end+1) = fighandle('distribution_forces');  hold on
set(hfig(end),'PaperPosition',[ -2.0000    1.7000   30.0000   30.0000])
step = 2;
hp = pcolor(Xwsafe(1,:),Ywsafe(:,1),dgridsafe); hp.EdgeColor = 'none'; colorbar
quiv = struct('xy',[],'nxy',[],'mag',[],'nscale',2);
for k = 1:length(objects)
    % viscircles(XYcontact,rinformed,'color','r')
    % plot(objects(k).XY(:,1),objects(k).XY(:,2),objects(k).marker)
    % plot(objects(k).XYboundary(:,1),objects(k).XYboundary(:,2),objects(k).line,'linewidth',2,'marker','x')
    quiv.xy  = [quiv.xy;  objects(k).XYboundary(1:step:end,:);      objects(k).center];
    quiv.nxy = [quiv.nxy; objects(k).pressurenormals(1:step:end,:); quiv.nscale*objects(k).avpressurenormals];
    quiv.mag = [quiv.mag; objects(k).Pcontact(1:step:end);mean(objects(k).Pcontact,'omitmissing')];
end
% all quivers at once (color 
hq = quiver(quiv.xy(:,1),quiv.xy(:,2),quiv.nxy(:,1),quiv.nxy(:,2),3,'color','k','LineWidth',0.5);
SetQuiverColor(hq,tooclear(jet),'mags',quiv.mag,'range',[0 0.5])
axis equal, title(sprintf('[t=%0.3g s] Pressure around objects',tframe))

%% print
PRINTON = true;
if PRINTON
    for i=1:length(hfig)
        figure(hfig(i)), drawnow
        printhandle(hfig(i))
    end
end



% relative pressure via Tait equation
% Pref = (rhobeadXYZgrid./rho).^7 - 1; % reference pressure
% Pbead = (rhobeadinformed./rho).^7 - 1; % pressure at kernel positions
% Pgrid = (dgrid./rho).^7 - 1; % pressure at grid nodes
% Pgrid = min(Pref(:)) + (max(Pref(:))-min(Pref(:)))*(Pgrid-min(Pgrid(:)))/(max(Pgrid(:))-min(Pgrid(:)));
% figure, imagesc(xw,yw,Pgrid), colorbar, title('dimensionless pressure (-)'), axis equal
% clim([-1 3]), colorbar
% figure, imagesc(xw,yw,Pref), colorbar, title('reference dimensionless pressure (-)'), axis equal
% clim([-1 3]), colorbar
% figure, scatter(XYinformed(:,1),XYinformed(:,2),rbeadinformed,Pbead,'filled')