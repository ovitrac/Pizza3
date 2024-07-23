% First template to retrieve Billy's paper 2 simulation data 
% rev. 2024/03/17 - forked in 2024/03/16 with PBC

% 2024/04/02 fork of Billy_results_template_PBC (version 2024/02/31)
% SUMMARY


%% Definitions
tframe = 0.67; % central
tframe = 0.57; % central-0.1
tframe = 0.77; % central+0.1
tframe = 0.62; % central-0.05
tframe = 0.72; % central+0.05
t0_ = clock;

% check folders
prefetchfolder = fullfile(pwd,'prefetch');
savefolder = fullfile(pwd,'results');
if ~exist(savefolder,'dir'), mkdir(savefolder); end

% Assign default values if needed
if ~exist('RESETPREFETCH','var'), RESETPREFETCH = false; end
if ~exist('PLOTON','var'), PLOTON = true; end
if ~exist('PRINTON','var'), PRINTON = false; end

% Some anaonymous functions
prefetchvar = @(varargin) fullfile(prefetchfolder,sprintf('t%0.4f_%s.mat',tframe,varargin{1}));
isprefetch = @(varargin) exist(prefetchvar(varargin{1}),'file') && ~RESETPREFETCH;
dispsection = @(s) dispf('\n%s\ntframe=%0.4g s \t[  %s  ]   elapsed time: %4g s\n%s',repmat('*',1,120),tframe,regexprep(upper(s),'.','$0 '),etime(clock,t0_),repmat('*',1,120)); %#ok<DETIM>
fighandle = @(id) formatfig(figure,'figname',sprintf('t%0.3g_%s',tframe,id));
printhandle = @(hfig) print_png(300,fullfile(outputfolder,[get(hfig,'filename') '.png']),'','',0,0,0);

% video recording parameters
fps = 10;
moviefolder = fullfile(rootdir(savefolder),'foodsim2024','movies');
moviefile = sprintf('crossection_t%0.4g.gif',tframe);
snapfile = sprintf('crossection_t%0.4g.png',tframe);
if ~exist(moviefolder,'dir'), mkdir(moviefolder), end
fullmoviefile = fullfile(moviefolder,moviefile);
fullsnapfile = fullfile(moviefolder,snapfile);
existmoviefile = @() exist(fullmoviefile,'file');
existsnapfile = @() exist(fullsnapfile,'file');
makemovie = @(hax) gif_add_frame(hax,fullmoviefile,fps);
makesnap = @() print_png(300,fullsnapfile,'','',0,0,0);

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
spherebox = [min(spherexyz)' max(spherexyz)'];
halftoppillar = pillarxyz(:,3)>ztop/2;
pillarbox = [min(pillarxyz(halftoppillar,:))' max(pillarxyz(halftoppillar,:))'];
spherepillarbox = [ min(spherebox(:,1),pillarbox(:,1)) max(spherebox(:,2),pillarbox(:,2)) ]; spherepillarboxdim=diff(spherepillarbox,1,2);
viewbox3d = [(spherepillarbox(:,1)-[0.15;0.5;0].*spherepillarboxdim),...
    (spherepillarbox(:,2)+[0.15;0.5;0.02].*spherepillarboxdim)];


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


% interpolation grid (central grid, no images)
%nresolution = [128 128 128];
nresolution = round(128*diff(viewbox,1,2)'/max(diff(viewbox,1,2)));
xw = linspace(viewbox(1,1),viewbox(1,2),nresolution(1));
yw = linspace(viewbox(2,1),viewbox(2,2),nresolution(2));
zw = linspace(viewbox(3,1),viewbox(3,2),nresolution(3));
[Xw,Yw,Zw] = meshgrid(xw,yw,zw);
XYZgrid = [Xw(:),Yw(:),Zw(:)];

% grid neighbors (incl. images) for interpolation and discarding grid points overlapping solid
VXYZ  = buildVerletList({XYZgrid XYZall},1.2*h);  % neighbors = fluid particles
VXYZs = buildVerletList({XYZgrid XYZs},0.85*s); % neighbors = solid particles

icontactsolid = find(cellfun(@length,VXYZs)>0);
%VXYZ(icontactsolid) = repmat({[]},length(icontactsolid),1);

% interpolation on the grid of the 3D velocity (central grid)
% Do not forget even if we are applying a 2D interpretation, we use a 3D simulation
% 3D velocity are projected on 2D streamlines even if the projection of the 3rd component is 0
W = kernelSPH(h,'lucy',3); % kernel expression
v3XYZgrid = interp3SPHVerlet(XYZall,vXYZall,XYZgrid,VXYZ,W,VbeadXYZall);
vxXYZgrid = reshape(v3XYZgrid(:,1),size(Xw)); vxXYZgrid(icontactsolid) = NaN;
vyXYZgrid = reshape(v3XYZgrid(:,2),size(Xw)); vyXYZgrid(icontactsolid) = NaN;
vzXYZgrid = reshape(v3XYZgrid(:,3),size(Xw)); vzXYZgrid(icontactsolid) = NaN;
vXYZgrid  = reshape(sqrt(sum(v3XYZgrid.^2,2)),size(Xw));

% density on the grid (with a possible different h)
Wd = kernelSPH(1.08*s,'lucy',3); % kernel expression
rhobeadXYZgrid = interp3SPHVerlet(XYZall,rhobeadXYZall,XYZgrid,VXYZ,Wd,VbeadXYZall);
rhobeadXYZgrid = reshape(rhobeadXYZgrid,size(Xw)); rhobeadXYZgrid(icontactsolid) = NaN;

% Plot
if PLOTON
    figure, slice(Xw,Yw,Zw,vXYZgrid,mean(viewbox(1,:)),mean(viewbox(2,:)),mean(viewbox(3,:))), axis equal, view(2), colorbar, title(sprintf('t=%0.3f s - velocity (m/s)',tframe)), view(3)
    figure, slice(Xw,Yw,Zw,rhobeadXYZgrid,mean(viewbox(1,:)),mean(viewbox(2,:)),mean(viewbox(3,:))); axis equal, view(2), colorbar, title(sprintf('t=%0.3f s - density (kg/m3)',tframe)), view(3)
end

%% Plot pillar and sphere atoms, quiver, streamlines
figure, hold on
[xs,ys,zs] = sphere(20); [xs,ys,zs] = deal(xs*rbead,ys*rbead,zs*rbead);
colors = struct('pillar',rgb('DarkGreen'),'sphere',rgb('FireBrick'));
for i=1:size(XYZs,1)
    surf(xs+ XYZs(i,1), ys + XYZs(i,2), zs+ XYZs(i,3),'FaceColor',colors.sphere,'EdgeColor','none');
end
for i=1:size(XYZp,1)
    surf(xs+ XYZp(i,1), ys + XYZp(i,2), zs+ XYZp(i,3),'FaceColor',colors.pillar,'EdgeColor','none');
end
lighting phong, camlight left, camlight right, axis equal, view(3)

% quiver
step = 12;
boundaries = ...
    [ nearestpoint(double(xw([1,end])+viewboxsize(1)/100*[1 -1]),double(xw)) % x
      nearestpoint(double(yw([1,end])+viewboxsize(2)/100*[1 -1]),double(yw)) % y
      nearestpoint(double(zw([1,end])+viewboxsize(3)/100*[1 -1]),double(zw)) % z
                 ];
indxquiver = boundaries(1,1):step:boundaries(1,2); % x indices
indyquiver = boundaries(2,1):step:boundaries(2,2); % y indices
indzquiver = boundaries(3,1):step:boundaries(3,2); % y indices
quiver3( Xw(indyquiver,indxquiver,indzquiver),...
         Yw(indyquiver,indxquiver,indzquiver), ...
         Zw(indyquiver,indxquiver,indzquiver), ...
         vxXYZgrid(indyquiver,indxquiver,indzquiver),...
         vyXYZgrid(indyquiver,indxquiver,indzquiver),...
         vzXYZgrid(indyquiver,indxquiver,indzquiver),...
            'color',rgb('Navy'),'LineWidth',2)

% streamlines
step = 6;
boundaries = ...
    [ nearestpoint(double(xw([1,end])+viewboxsize(1)/100*[1 -1]),double(xw)) % x
      nearestpoint(double(yw([1,end])+viewboxsize(2)/100*[1 -1]),double(yw)) % y
      nearestpoint(double(zw([1,end])+viewboxsize(3)/100*[1 -1]),double(zw)) % z
                 ];
indxstreamline = boundaries(1,1):step:boundaries(1,2); % x indices
indystreamline = boundaries(2,1):step:boundaries(2,2); % y indices
indzstreamline = boundaries(3,1):step:boundaries(3,2); % y indices
[startgenX,startgenY,startgenZ] = meshgrid(double(xw(indxstreamline)),double(yw(indystreamline)),double(ztop));
vxXYZgrid_ = vxXYZgrid; vxXYZgrid_(isnan(vxXYZgrid))=0;
vyXYZgrid_ = vyXYZgrid; vyXYZgrid_(isnan(vyXYZgrid))=0;
vzXYZgrid_ = vzXYZgrid; vzXYZgrid_(isnan(vzXYZgrid))=0;
hstr = streamribbon(double(Xw),double(Yw),double(Zw),vxXYZgrid_,vyXYZgrid_,vzXYZgrid_,startgenX,startgenY,startgenZ);
set(hstr,'edgecolor','none','facecolor',rgb('DeepSkyBlue'),'facealpha',0.4)


% Plot density
% figure, hold on
[Xwcut,Ywcut,Zwcut,Rwcut] = deal(Xw,Yw,Zw,rhobeadXYZgrid);
[Xwcut2,Ywcut2,Zwcut2,Rwcut2] = deal(Xw,Yw,Zw,rhobeadXYZgrid);
zcut = 3e-4;
xcut = 3.1e-4;
Xwcut(:,:,zw>zcut) = [];
Ywcut(:,:,zw>zcut) = [];
Zwcut(:,:,zw>zcut) = [];
Rwcut(:,:,zw>zcut) = [];
Xwcut2(:,xw>xcut,:) = [];
Ywcut2(:,xw>xcut,:) = [];
Zwcut2(:,xw>xcut,:) = [];
Rwcut2(:,xw>xcut,:) = [];
isorho = 1200;
% Rwcut2(Rwcut2<=isorho)=isorho;
p1a = patch(isosurface(Xwcut2,Ywcut2,Zwcut2,Rwcut2, isorho),'FaceColor',rgb('Navy'),'EdgeColor','none');
p1b = patch(isosurface(Xwcut2,Ywcut2,Zwcut2,Rwcut2, isorho-200),'FaceColor',rgb('MediumBlue'),'EdgeColor','none');
p1c = patch(isosurface(Xwcut2,Ywcut2,Zwcut2,Rwcut2, isorho-400),'FaceColor',rgb('RoyalBlue'),'EdgeColor','none');
p1d = patch(isosurface(Xwcut2,Ywcut2,Zwcut2,Rwcut2, isorho-600),'FaceColor',rgb('DodgerBlue'),'EdgeColor','none');
p2 = patch(isocaps(Xwcut,Ywcut,Zwcut,Rwcut, 200),'FaceColor','interp','EdgeColor','none');
colormap(bone(100)), axis equal
%camlight left, camlight right, lighting gouraud, view(-138,28), axis equal
camlight left; % Adds a light to the left of the camera
camlight right; % Adds a light to the right of the camera
light('Position',[-1 -1 0.5],'Style','infinite'); % Additional light source from a specific direction
ambientLight = light('Position',[1 1 1],'Style','infinite');
set(ambientLight,'Color',[0.3 0.3 0.3]); % A soft, white ambient light
lighting phong;

view([-199 24])
camproj perspective
hfig = gcf; hax = gca;
formatfig(hfig,'color','k','InvertHardcopy',false,'position',[-2143   -123    1600    1200],'PaperPosition',[0.6350    7.0918   19.7300   15.5164])
axis off
set(hax,'color','k')
axis([0.2142    0.5488    0.1409    0.4544    0.2046    0.5135]*1e-3)

%% Assuming you have your scene set up before this script
MOVIEON = true;

if ~existsnapfile()
    set(hfig,'color','w')
    set(hax,'color','w')
    makesnap()
    set(hfig,'color','k')
    set(hax,'color','k')
end

if existmoviefile()
    MOVIEON = false;
    dispf('delete(''%s'')',fullmoviefile)
    warning('delete the movie file')
else
    set(hfig,'color','k')
    set(hax,'color','k')
end

% Number of frames for the video
nFrames = 360; % This can be adjusted for smoother animation

% Initial view settings
initialAzimuth = -199; % Adjusting for MATLAB's view system
initialElevation = 24;

% Normalize initialAzimuth to ensure smooth transition
% MATLAB's view system handles azimuths mod 360
if initialAzimuth < 0
    initialAzimuth = 360 + initialAzimuth; % Converts -199 to 161
end

% Animation parameters
azimuthEnd = initialAzimuth + 360; % Completes a full circle
elevationMin = 4; % Minimum elevation
elevationMax = 54; % Maximum elevation
midElevation = (elevationMin + elevationMax) / 2; % Midpoint for elevation
elevationAmplitude = (elevationMax - elevationMin) / 2; % Elevation change amplitude

% Time vector for sinusoidal elevation change, adjusted to start/end at initial elevation
t = linspace(0, 2*pi, nFrames);

% Pre-calculation for azimuth and elevation
azimuths = linspace(initialAzimuth, azimuthEnd, nFrames);
elevations = midElevation + elevationAmplitude * sin(t);

% Make the start and end elevations match the initial setting by adjusting the first and last values
elevations(1) = initialElevation;
elevations(end) = initialElevation;

% Animation loop
for k = 1:nFrames
    % Calculate current azimuth and elevation
    currentAzimuth = azimuths(k);
    currentElevation = elevations(k);
    
    % Ensure the azimuth is within the 0° to 360° range for viewing
    currentAzimuth = mod(currentAzimuth, 360);
    
    % Update view
    view(currentAzimuth, currentElevation);
    
    % Update the scene
    drawnow;
    
    % Optionally, capture the frame for video creation
    % frame = getframe(gcf);
    % writeVideo(videoObject, frame);
    if MOVIEON
        makemovie(hfig)
    end
end



% slice
% figure, hs= slice(Xw,Yw,Zw,sumW,single(1:3),single(1:3),single([])); set(hs,'edgecolor','none','facealpha',0.5), axis equal

