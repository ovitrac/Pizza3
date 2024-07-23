function [Xframe,details] = yao_initialization(tframe)
%YAO_INITIALIZATION load data corresponding to tframe
%   Typical usages
%      Xframe = yao_initialization(tframe)
%      [Xframe,details] = yao_initialization(tframe)

% INRAE\Olivier Vitrac, Yao Liu

% 2024-05-03 first version

if nargin<1, tframe = []; end
if isempty(tframe), error('set tframe first'), end

%% Definitions
t0_ = clock;

%% check folders
outputfolder = fullfile(pwd,'preproduction');
savefolder = fullfile(pwd,'results');
prefetchfolder = fullfile(pwd,'prefetch');
if ~exist(outputfolder,'dir'), mkdir(outputfolder); end
if ~exist(prefetchfolder,'dir'), mkdir(prefetchfolder); end
if ~exist(savefolder,'dir'), mkdir(savefolder); end

% Anonymous functions
prefetchvar = @(varargin) fullfile(prefetchfolder,sprintf('t%0.4f_%s.mat',tframe,varargin{1}));
isprefetch = @(varargin) exist(prefetchvar(varargin{1}),'file') && ~RESETPREFETCH;
dispsection = @(s) dispf('\n%s\ntframe=%0.4g s \t[  %s  ]   elapsed time: %4g s\n%s',repmat('*',1,120),tframe,regexprep(upper(s),'.','$0 '),etime(clock,t0_),repmat('*',1,120)); %#ok<DETIM>
fighandle = @(id) formatfig(figure,'figname',sprintf('t%0.3g_%s',tframe,id));
printhandle = @(hfig) print_png(300,fullfile(outputfolder,[get(hfig,'filename') '.png']),'','',0,0,0);

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
% coordinate system
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

%% Implement isfluid, issphere, iswall, ispillar
Xframe.ATOMS.isfluid = Xframe.ATOMS.type==fluidtype;
Xframe.ATOMS.ispillar = Xframe.ATOMS.type==pillartype;
Xframe.ATOMS.issphere = Xframe.ATOMS.type==spheretype;
Xframe.ATOMS.iswall = Xframe.ATOMS.type==walltype;
Xframe.ATOMS.issolid = Xframe.ATOMS.type==spheretype | Xframe.ATOMS.type==pillartype;

%% second output
if nargout>1
details = struct(...
    'tframe',tframe,...
    'iframe',iframe,...
    'dt',dt,...
    'ntimesteps',ntimesteps,...
    'coords',{coords},...
    'vcoords',{vcoords},...
    'type',struct('fluid',fluidtype,'pillar',pillartype,'wall',walltype,'sphere',spheretype),...
    'mbead',mbead,...
    'Vbead',Vbead,...
    'box',Xframe.BOX(icoords,:),...
    'boxsize',diff(Xframe.BOX(icoords,:),1,2),...
    'dumpfile',dumpfile ...
    );
end