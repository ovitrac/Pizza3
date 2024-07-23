% Second template to retrieve Billy's paper 2 simulation data 
% rev. 2024/04/29

% 2024/04/29 retrive 3D data around the top of the pillar

% SUMMARY

% This MATLAB script is a comprehensive framework for analyzing fluid dynamics simulations, specifically focusing on the distribution and movement of particles or beads in a fluid environment. Key functionalities include:
% 
% 1. Environment Setup:
%   Initializes the simulation environment by clearing variables, setting up output folders, and defining file paths to simulation data, with adjustments for periodic boundary conditions (PBC).
% 2. Data Retrieval:
%   Loads simulation data from specified file paths, handling different configurations and viscosity models.

%% Definitions (it is a script accepting ONE variable and FLAGS)
%
%   List of of variables
%           tframe <-- use this variable a in for-loop or choose a particular frame before calling this script
%       tframelist (not used)
%
%   List of available FLAGS
%       RESETPREFETCH forces all prefetch files to be regenerated in true (default=false)
%              PLOTON enables to plot results (default=true)
%             PRINTON prints figures as PNG images for control (in outputfolder) (default=false)
%              SAVEON saves the results R0 (original), R1 (informed) (default=true)
%           OVERWRITE enables already saved results to overwritte (default=false)

% close, delete everything except variables and FLAGS
clc
close all
clearvars -except tframe tframelist RESETPREFETCH PLOTON PRINTON SAVEON OVERWRITE
t0_ = clock;

% check folders
outputfolder = fullfile(pwd,'preproduction');
savefolder = fullfile(pwd,'results');
prefetchfolder = fullfile(pwd,'prefetch');
if ~exist(outputfolder,'dir'), mkdir(outputfolder); end
if ~exist(prefetchfolder,'dir'), mkdir(prefetchfolder); end
if ~exist(savefolder,'dir'), mkdir(savefolder); end

% Assign default values if needed
if ~exist('RESETPREFETCH','var'), RESETPREFETCH = false; end
if ~exist('PLOTON','var'), PLOTON = true; end
if ~exist('PRINTON','var'), PRINTON = false; end
if ~exist('SAVEON','var'), SAVEON = true; end
if ~exist('OVERWRITE','var'), OVERWRITE = false; end

% Anonymous functions
prefetchvar = @(varargin) fullfile(prefetchfolder,sprintf('t%0.4f_%s.mat',tframe,varargin{1}));
isprefetch = @(varargin) exist(prefetchvar(varargin{1}),'file') && ~RESETPREFETCH;
dispsection = @(s) dispf('\n%s\ntframe=%0.4g s \t[  %s  ]   elapsed time: %4g s\n%s',repmat('*',1,120),tframe,regexprep(upper(s),'.','$0 '),etime(clock,t0_),repmat('*',1,120)); %#ok<DETIM>
fighandle = @(id) formatfig(figure,'figname',sprintf('t%0.3g_%s',tframe,id));
printhandle = @(hfig) print_png(300,fullfile(outputfolder,[get(hfig,'filename') '.png']),'','',0,0,0);

% results saved in two variables to avoid any confusion
R0 = struct([]); % reference data
R1 = struct([]);  % informed ones

%% path and metadata
dispsection('INITIALIZATION')
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
dispf('config: %s | viscosity: %s | source: %s',config,viscosity,dumpfile)

%% extract information
dispsection('OVERVIEW')
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
% Billy choose a reference density of 900 kg/m3 for a physical density of 1000 kg/m3
% Viscosity: 0.13 Pa.s
mbead = 4.38e-12; % kg
rho = 1000; % kg / m3 (density of the fluid)
Vbead = mbead/rho;
dispf('SUMMARY: natoms: %d | dt: %0.3g s | rho: %0.4g',natoms,dt,rho)

%% selective copy of PREFETCH files (if possible)
if copymode
    dispsection('COPY')
    myprefetchfile = @(itime) sprintf('%s%09d.mat','TIMESTEP_',itime);
    myprefetchfolder = @(d) fullfile(d,sprintf('PREFETCH_%s',lastdir(dumpfile)));
    destinationfolder = fullfile(rootlocal,rootdir(simfolder.(config).(viscosity)));
    sourcefolderPREFETCH = myprefetchfolder(sourcefolder);
    destinationfolderPREFETCH = myprefetchfolder(destinationfolder);
    % Choose the frames needed here
    tcopy = 0.0:0.01:1.2;
    % files to copy
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
dispsection('BEAD SIZE')
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
dispf('SUMMARY: s: %0.4g m | h: %0.4g m',s,h)
%% load the frame closest to simulation time: tframe
% with the mini dataset, are available:
% 0.30s 0.40s 0.45s 0.50s 0.55s 0.60s 0.65s 0.70s 0.75s 0.80s 0.85s 0.90s 0.95s 1.00s 1.05s 1.10s 
% tframelist = [0.3 0.4 0.45:0.05:1.10]; % verysmalldumps
tframelist = 0.0:0.01:1.2; % updated time frames
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

% Definitions based on actual tframe
dispsection = @(s) dispf('\n%s\ntframe=%0.4g s \t[  %s  ]   elapsed time: %4g s\n%s',repmat('*',1,120),tframe,regexprep(upper(s),'.','$0 '),etime(clock,t0_),repmat('*',1,120)); %#ok<DETIM>
prefetchvar = @(varargin) fullfile(prefetchfolder,sprintf('t%0.4f_%s.mat',tframe,varargin{1}));
isprefetch = @(varargin) exist(prefetchvar(varargin{1}),'file') && ~RESETPREFETCH;
savefile = @() fullfile(savefolder,sprintf('Rt.%0.4f.mat',tframe));


%% Interpolate velocity field at z = ztop
dispsection('REFERENCE VELOCITY FIELD')
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
viewbox = viewbox3d; %fluidbox; viewbox(3,:) = [ztop-2*h ztop+2*h];
viewboxsize = diff(viewbox,1,2);
insideviewbox = true(height(Xframe.ATOMS),1);
for icoord = 1:3
    insideviewbox = insideviewbox ...
        & Xframe.ATOMS{:,coords{icoord}}>=viewbox(icoord,1) ...
        & Xframe.ATOMS{:,coords{icoord}}<=viewbox(icoord,2);
end
XYZall  = Xframe.ATOMS{Xframe.ATOMS.isfluid,coords};  % fluid kernel centers
vXYZall = Xframe.ATOMS{Xframe.ATOMS.isfluid,vcoords}; % velocity of fluid kernel centers
XYZ  = Xframe.ATOMS{insideviewbox & Xframe.ATOMS.isfluid,coords};  % fluid kernel centers
vXYZ = Xframe.ATOMS{insideviewbox & Xframe.ATOMS.isfluid,vcoords}; % velocity of fluid kernel centers
XYZp = Xframe.ATOMS{insideviewbox & Xframe.ATOMS.ispillar,coords};  % solid kernel centers
XYZs = Xframe.ATOMS{insideviewbox & Xframe.ATOMS.issphere,coords}; 
rhobeadXYZall = Xframe.ATOMS.c_rho_smd(Xframe.ATOMS.isfluid); % volume of the bead
rhobeadXYZ = Xframe.ATOMS.c_rho_smd(insideviewbox & Xframe.ATOMS.isfluid); % volume of the bead
VbeadXYZall = mbead./rhobeadXYZall;
VbeadXYZ = mbead./rhobeadXYZ;


% Plot
if PLOTON
    figure, hold on
    plot3D(XYZ,'bo')
    plot3D(XYZs,'ro')
    plot3D(XYZp,'go')
    view(3)
end
