% First template to retrieve Billy's paper 2 simulation data 
% rev. 2024/03/07

% 2024/03/07 implementation of reverse streamlines, streamline binning from their initial positions, subsampling
% 2024/03/12 implement bead along streamlines (bug:NaN and Inf not allowed.) 
%% path and metadata
originalroot = '/media/olivi/T7 Shield/Thomazo_V2';
if exist(originalroot,'dir')
    root = originalroot;
else
    root = fullfile(pwd,'smalldumps');
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
% Simulation parameters
mbead = 4.38e-12; % kg
rho = 1000; % kg / m3 (density of the fluid)
Vbead = mbead/rho;

%% Estimate bead size from the first frame
% first estimate assuming that the bead is a cube
fluidxyz0 = X0.ATOMS{T==fluidtype,coords};
boxdims = X0.BOX(:,2) - X0.BOX(:,1);
Vbead_guess = prod(boxdims)/natoms;
rbead_guess = (3/(4*pi)*Vbead_guess)^(1/3);
cutoff = 3*rbead_guess;
[verletList,cutoff,dmin,config,dist] = buildVerletList(fluidxyz0,cutoff); %#ok<ASGLU>
rbead = dmin/2;
s = 2*rbead; % separation distance
h = 2*s;     % smoothing length

%% load the frame closest to simulation time: tframe
% with the mini dataset, are available:
% 0.30s 0.40s 0.45s 0.50s 0.55s 0.60s 0.65s 0.70s 0.75s 0.80s 0.85s 0.90s 0.95s 1.00s 1.05s 1.10s 
tframe = 0.8; % s <-------------------- select time here 
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
fluidbox = [ min(Xframe.ATOMS{Xframe.ATOMS.isfluid,coords})
    max(Xframe.ATOMS{Xframe.ATOMS.isfluid,coords}) ]';
fluidboxsize = double(diff(fluidbox,1,2)); % for control
% restrict interpolation to the viewbox
viewbox = fluidbox; viewbox(3,:) = [ztop-2*h ztop+2*h];
insideviewbox = true(height(Xframe.ATOMS),1);
for icoord = 1:3
    insideviewbox = insideviewbox ...
        & Xframe.ATOMS{:,coords{icoord}}>=viewbox(icoord,1) ...
        & Xframe.ATOMS{:,coords{icoord}}<=viewbox(icoord,2);
end
XYZ  = Xframe.ATOMS{insideviewbox & Xframe.ATOMS.isfluid,coords}; % fluid kernel centers
vXYZ = Xframe.ATOMS{insideviewbox & Xframe.ATOMS.isfluid,vcoords}; % velocity of fluid kernel centers
XYZs = Xframe.ATOMS{insideviewbox & Xframe.ATOMS.issolid,coords};
% interpolation grid
nresolution = [1024 1024 1];
xw = linspace(viewbox(1,1),viewbox(1,2),nresolution(1));
yw = linspace(viewbox(2,1),viewbox(2,2),nresolution(1));
zw = ztop;
[Xw,Yw,Zw] = meshgrid(xw,yw,zw);
XYZgrid = [Xw(:),Yw(:),Zw(:)];
% grid neighbors for interpolation and discarding grid points overlapping solid
VXYZ  = buildVerletList({XYZgrid XYZ},1.2*h);  % neighbors = fluid particles
VXYZs = buildVerletList({XYZgrid XYZs},0.85*s); % neighbors = solid particles
icontactsolid = find(cellfun(@length,VXYZs)>0);
VXYZ(icontactsolid) = repmat({[]},length(icontactsolid),1);
% neighbors statistics for control
% example with grid points having 20 neighbors or less: plot(XYZgrid(nn<20,1),XYZgrid(nn<20,2),'o','markerfacecolor','k')
%{
    nn = cellfun(@length,VXYZ);
    [nnu,~,innu] = unique(nn);
    cnnu = accumarray(innu,nn,[],@length);
%}

% interpolation stuff
W = kernelSPH(h,'lucy',3); % kernel expression
v3XYZgrid = interp3SPHVerlet(XYZ,vXYZ,XYZgrid,VXYZ,W,Vbead);
vxXYZgrid = reshape(v3XYZgrid(:,1),size(Xw)); %vxXYZgrid(isnan(vxXYZgrid)) = 0;
vyXYZgrid = reshape(v3XYZgrid(:,2),size(Xw)); %vyXYZgrid(isnan(vyXYZgrid)) = 0;
vzXYZgrid = reshape(v3XYZgrid(:,3),size(Xw)); %vzXYZgrid(isnan(vzXYZgrid)) = 0;
vXYZgrid  = reshape(sqrt(sum(v3XYZgrid.^2,2)),size(Xw));

%% Plot (attention 2D)
figure, hold on
% velocity magnitude
imagesc(xw,yw,vXYZgrid)
axis tight, axis equal
% quiver configuration and plot
step = 8;
boundaries = [ nearestpoint(double(xw([1,end]))+fluidboxsize(1)/30*[1 -1],double(xw))
               nearestpoint(double(yw([1,end]))+fluidboxsize(2)/30*[1 -1],double(yw))
             ];
indxquiver = boundaries(1,1):step:boundaries(1,2);
indyquiver = boundaries(2,1):step:boundaries(2,2);
quiver(Xw(indxquiver,indyquiver),Yw(indxquiver,indyquiver), ...
          vxXYZgrid(indxquiver,indyquiver),vyXYZgrid(indxquiver,indyquiver), ...
        'color','k','LineWidth',1)
% streamline configuration and plot
boundaries = [ nearestpoint(double(xw([1,end]))+fluidboxsize(1)/30*[1 -1]*1.5,double(xw))
               nearestpoint(double(yw([1,end]))+fluidboxsize(2)/30*[1 -1]*1,double(yw))
             ];
step = step/2;
indxstreamline = boundaries(1,1):step:boundaries(1,2);
indystreamline = boundaries(2,1):step:boundaries(2,2);
nstreamlines = length(indxstreamline);
% streamlines from bottom to top
[startX,startY,startZ] = meshgrid(double(xw(indxstreamline)),double(yw(indystreamline(1))),double(ztop));
vertices = stream2(double(Xw),double(Yw),vxXYZgrid,vyXYZgrid,startX,startY);
xinitialposition = cellfun(@(v) v(1,1),vertices);
yinitialposition = cellfun(@(v) v(1,2),vertices);
xfinalposition = cellfun(@(v) v(end,1),vertices);
yfinalposition = cellfun(@(v) v(end,2),vertices);
yfinaldefaultposition = yfinalposition(find(~isnan(yfinalposition),1,'first'));
indclosestToInitial = nearestpoint(xfinalposition,xinitialposition);
isinterrupted = isnan(yfinalposition);
% Build the adjacency matrix the initial and final position
A = false(nstreamlines,nstreamlines); %initial x final positions
for i=1:nstreamlines
    if ~isnan(indclosestToInitial(i))
        A(i,indclosestToInitial(i)) = true;
    end
end
isreached = any(A,1);
% Missinf streamlines from top to bottom
[startX2,startY2,startZ2] = meshgrid(xinitialposition(~isreached),yfinaldefaultposition,double(ztop));
vertices2 = stream2(double(Xw),double(Yw),-vxXYZgrid,-vyXYZgrid,startX2,startY2);
% streamlines from top to bottom (for unreached positions)

% control plot
% figure, hold on
% colors = tooclear(parula(nstreamlines));
% for i=1:nstreamlines
%     if isinterrupted(i)
%         plot(vertices{i}(:,1),vertices{i}(:,2),'-','linewidth',2,'color',colors(i,:));
%     else
%         plot(vertices{i}(:,1),vertices{i}(:,2),'--','linewidth',2,'color',colors(i,:));
%         plot( [xinitialposition(i);xinitialposition(indclosestToInitial(i))],...
%               [yinitialposition(i);yfinaldefaultposition],...
%               '-','linewidth',2,'color',colors(i,:))
%     end
%     text(xinitialposition(i),yinitialposition(i),sprintf('%d',i),'fontsize',8,'fontweight','bold','HorizontalAlignment','center','VerticalAlignment','middle')
%     if isreached(i), col = 'blue'; else col = 'red'; end
%     text(xinitialposition(i),yfinaldefaultposition,sprintf('%d',i),'fontsize',8,'fontweight','bold','HorizontalAlignment','center','VerticalAlignment','middle','color',col)
% end

% Merge all streamlines and create flags
allvertices = [vertices,vertices2];
idvertices = [ones(1,length(vertices)),2*ones(1,length(vertices2))];
[xallvertices,ind] = sort(cellfun(@(v) v(1,1),allvertices),'ascend'); % mean(v(:,1),'omitnan')
allvertices = allvertices(ind);
idvertices = idvertices(ind);
allbroken = cellfun(@(v) any(isnan(v(:,1))),allvertices);
allcomplete = ~allbroken;
allup =  cellfun(@(v) v(2,2)>v(1,2),allvertices);
alldown = ~allup;

% Pick streamlines from binning
nbins = 80;
xbins = linspace(xinitialposition(1),xinitialposition(end),nbins); % desired bin centers
dxbins = xbins(2)-xbins(1); % bin width (for control)
% Binning for complete streamlines
ibinsall = nearestpoint(xbins,xallvertices); %interpleft(xallvertices,1:length(allvertices),xbins);
ibinsall = ibinsall(allcomplete(ibinsall)); % we keep complete
% extract the initial (0) and final (1) positions of up/down streamlines
isselected = false(1,length(allvertices)); isselected(ibinsall)=true;
x0up = cellfun(@(v) v(1,1),allvertices(isselected & allup));
x1up = cellfun(@(v) v(end,1),allvertices(isselected & allup));
x0down = cellfun(@(v) v(1,1),allvertices(isselected & alldown));
x1down = cellfun(@(v) v(end,1),allvertices(isselected & alldown));
xdeviation = cellfun(@(v) abs(v(1,1)-v(end,1)),allvertices(isselected)); % for control
% Binning from incomplete (broken) streamlines
% all bins required
xbins_broken = xbins(setdiff(1:nbins,nearestpoint(xallvertices(ibinsall),xbins)));
if isempty(x1down)
    valid_up = true(size(xbins_broken));
else
    valid_up = abs(x1down(nearestpoint(xbins_broken,x1down))-xbins_broken)>(0.5*dxbins);
end
if isempty(x1up)
    valid_down = true(size(xbins_broken));
else
    valid_down = abs(x1up(nearestpoint(xbins_broken,x1up))-xbins_broken)>(0.5*dxbins);
end
iupbroken = find(allup & allbroken);
xupbroken = xallvertices(iupbroken);
ibinsupbroken = iupbroken(nearestpoint(xbins_broken(valid_up),xupbroken));
idownbroken = find(alldown & allbroken);
xdownbroken = xallvertices(idownbroken);
ibinsdownbroken = idownbroken(nearestpoint(xbins_broken(valid_down),xdownbroken));
% Merge and sort all bins
ibins = unique([ibinsall,ibinsdownbroken,ibinsupbroken]);

% check for holes/gaps between streamlines and overlopping streamlines
% The two passes are sequenced to avoid an infinite loop between fill/remove steps
% pass 1: fill the gaps (bottom and top) iteratively
% pass 1: remove ovelaps (bottom and top) iteratively (this step is always after the first filling procedure)
% pass 2: fill the gaps (bottom and top)
[holechecked, overlapchecked] = deal(false);
gapthreshmax = 1.9; % max gap (1=bin distance)
gapthreshmin = 0.5; % minimum gap
iter = 0; maxiter = 100;
pass2 = false;
while (~holechecked || ~overlapchecked) && iter<maxiter
    iter = iter + 1;
    ispicked = false(1,length(allvertices)); ispicked(ibins)=true;
    xbottom = union(cellfun(@(v) v(1,1),allvertices(ispicked & allup)),...
                    cellfun(@(v) v(end,1),allvertices(ispicked & allcomplete & alldown)));
    dxbottom = diff(xbottom)/dxbins;
    if any(dxbottom>gapthreshmax) && ~holechecked
        xholebottom = xallvertices(ibins(nearestpoint(xbottom(dxbottom>gapthreshmax),xallvertices(ibins))))+dxbins;
        iup = find(allup);
        ibinsholebottom = iup(nearestpoint(xholebottom,xallvertices(allup)));
        ibins = union(ibins,ibinsholebottom);
        holecheckbottom = false;
        overlapcheckbottom = false;
        dispf('add %d streamlines to the bottom',length(ibinsholebottom))
    elseif ~holechecked
        holecheckbottom = true;
    elseif any(dxbottom<gapthreshmin) && ~pass2
        ioverlapbottom = nearestpoint(xbottom(dxbottom<gapthreshmin),xallvertices(ibins));
        ibins(ioverlapbottom) = [];
        overlapcheckbottom = false;
        dispf('remove %d streamlines from the bottom',length(ioverlapbottom))
    else
         overlapcheckbottom = true;
    end
    ispicked = false(1,length(allvertices)); ispicked(ibins)=true;
    xtop = union(   cellfun(@(v) v(end,1),allvertices(ispicked & allcomplete & allup)),...
                    cellfun(@(v) v(1,1),allvertices(ispicked & alldown)));
    dxtop = diff(xtop)/dxbins;
    if any(dxtop>gapthreshmax) && ~holechecked
        xholetop = xallvertices(ibins(nearestpoint(xtop(dxtop>gapthreshmax),xallvertices(ibins))))+dxbins;
        idown = find(alldown);
        ibinsholetop = idown(nearestpoint(xholetop,xallvertices(alldown)));
        ibins = union(ibins,ibinsholetop);
        holechecktop = false;
        overlapchecktop = false;
        dispf('add %d streamlines to the top',length(ibinsholetop))
    elseif ~holechecked
        holechecktop = true;
    elseif any(dxtop<gapthreshmin) && ~pass2
        ioverlaptop = nearestpoint(xbottom(dxtop<gapthreshmin),xallvertices(ibins));
        ibins(ioverlaptop) = [];
        overlapcheckbottom = false;
        dispf('remove %d streamlines from the top',length(ioverlaptop))
    else
        overlapchecktop = true;
    end
    holechecked = holecheckbottom && holechecktop;
    overlapchecked = overlapcheckbottom && overlapchecktop;
    if overlapchecked && ~pass2
        pass2=true;
        holechecked = false; % we restart the filling gap correction
    end
end
if iter>=maxiter, error('Gaps cannot be filled, decrease step (current=%d) !', step), end

% plot streamlines
hsl = streamline(allvertices); set(hsl,'linewidth',0.1,'color',[0.8 0.8 0.8]);
hsl = streamline(allvertices(ibins)); set(hsl,'linewidth',2,'color',[0.4375    0.5000    0.5625])
plot(startX(:),startY(:),'ro','markerfacecolor',[0.4375    0.5000    0.5625])


%% put beads along selected streamlines 
% get informations of streamlines
sl = allvertices(ibins);
nsl = length(sl); % number of selected streamlines
sall = cell(1,nsl);
for i=1:nsl
    csl = sl{i}; % select current streamline
    xcsl = csl(:,1); ycsl = csl(:,2);
    Tcsl = [diff(xcsl) diff(ycsl); NaN NaN];
    Tcsl_norm = Tcsl./sqrt(sum(Tcsl.^2,2));
    lcsl = [0; cumsum(sqrt(sum(Tcsl(1:end-1,:).^2,2)))];
    Vxcsl = interp2(Xw,Yw,vxXYZgrid,xcsl,ycsl);
    Vycsl = interp2(Xw,Yw,vyXYZgrid,xcsl,ycsl);
    Vcsl = [Vxcsl,Vycsl];
    Vlcsl = dot(Vcsl,Tcsl_norm,2);
    s = table(xcsl,ycsl,lcsl,Tcsl_norm,Vcsl,Vlcsl,'VariableNames',["x","y","l","T","V","Vl"]);
    sall{i} = s;
end
% put beads
dt = 0.01;
figure, hold on
for i=1:nsl
    [x,y,Vl,l] = add_bead(sall{i},rbead,dt);
    centers = [x,y];
    viscircles(centers,rbead)
end