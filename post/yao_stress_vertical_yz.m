% Template for Yao
%
%   Authors: INRAE\Olivier Vitrac, INRAE\Yao Liu
%
% The work is based on the simulation of Billy (publication so-called pizza2, and series Thomazo_v2)
% The dataset is accessible on lab PCs via yao_initialization(tframe)
% tframe should be chosen among 0.11:0.01:1.11 (0.11, 0.12, 0.13, ... 1.11 s)
% The data corresponding to tframe and additional details are accessible via
%     [Xframe,details] = yao_initialization(tframe)
% Due to the many depencies with pizza3, the code needs to be run from : Thomazo_v2\
% 
% Revision history
% 2024-05-03 early version
% 2024-05-05 ROI with PBC implemented
% 2024-05-06 shear stress and shear rate implementated on a two 2D 1024*1024 grids separated by h


%% The code is split in blocks starting with "%%", they can be run independently
% by pressing CTRL+Enter or by choosing Run Section.
% The entire script can be run by pressing F5 or by choosing Run
%
% Control sections are enclosed between "%{ ... %}", they can be run by selecting
% the code between {} and by pressing F9 or by using the mouse right click and by
% choosing Evaluating the selection.
%
% visualization of the full dataset as a movie
%{
clf,
coords = {'z','x','y'};
for tframe = 0.11:0.01:1.11
    Xframe = yao_initialization(tframe);
    clf, hold on, axis equal, view(3)
    plot3D(Xframe.ATOMS{Xframe.ATOMS.type==1,coords},'b.','markersize',2)
    plot3D(Xframe.ATOMS{Xframe.ATOMS.type==2,coords},'co')
    plot3D(Xframe.ATOMS{Xframe.ATOMS.type==3,coords},'go')
    plot3D(Xframe.ATOMS{Xframe.ATOMS.type==4,coords},'rs')
    drawnow
end
%}


%% load the frame
tframe = 0.67; % choose any frame between 0.11 and 1.11
[Xframe,details] = yao_initialization(tframe);
pillarxyz = Xframe.ATOMS{Xframe.ATOMS.ispillar,details.coords};
% control
%{
    figure, hold on, axis equal, view(3)
    plot3D(Xframe.ATOMS{Xframe.ATOMS.type==details.type.fluid,details.coords},'b.','markersize',2)
    plot3D(Xframe.ATOMS{Xframe.ATOMS.type==details.type.wall,details.coords},'co')
    plot3D(Xframe.ATOMS{Xframe.ATOMS.type==details.type.pillar,details.coords},'go')
    plot3D(Xframe.ATOMS{Xframe.ATOMS.type==details.type.sphere,details.coords},'rs','markerfacecolor','r')
%}


%% Selection of the thick plane or ROI (region of interest)
xmean = mean(pillarxyz(:,1)); % mean y coord of the pillar
xthick = xmean*0.15*5;          % define the thickness of the plane around ztop
ROIbox = details.box;      % select the ROI (region of interest)
ROIbox(1,:) = xmean + [-0.5 +0.5]*xthick; % update the ROI to ztop-zthick/2 and ztop+zthick/2
insideROIbox = true(height(Xframe.ATOMS),1); % boolean flag (by default all atoms are considered in ROI)
for icoord = 1:3 % for each coordinate
    insideROIbox = insideROIbox ... the operator & ('and') enable to uncheck atoms beyond the bounds
        & Xframe.ATOMS{:,details.coords{icoord}}>=ROIbox(icoord,1) ...
        & Xframe.ATOMS{:,details.coords{icoord}}<=ROIbox(icoord,2);
end
atomsROI = Xframe.ATOMS(insideROIbox,:); % atom table for only ROI atoms

% control
%{
    figure, hold on, axis equal, view(3)
    plot3D(atomsROI{atomsROI.type==details.type.fluid,details.coords},'b.','markersize',2)
    plot3D(atomsROI{atomsROI.type==details.type.wall,details.coords},'co')
    plot3D(atomsROI{atomsROI.type==details.type.pillar,details.coords},'go')
    plot3D(atomsROI{atomsROI.type==details.type.sphere,details.coords},'rs','markerfacecolor','r')
%}

%% add PBC images (periodic boundary)
XYZ = atomsROI{:,details.coords}; % coordinates of ROI atoms
vXYZ = atomsROI{:,details.vcoords}; % coordinates of ROI atoms
rhoXYZ = atomsROI.c_rho_smd;
[XYZimagesONLY ,indXimagesONLY]= PBCimages(XYZ,ROIbox,[false,true,true],xthick); % add periodic images within zthick around x and z (y is not periodic)
XYZwithImages = [XYZ;XYZimagesONLY]; % all atoms including their images
vXYZwithImages = [vXYZ;vXYZ(indXimagesONLY,:)]; % all atoms including their images
rhoXYZwithImages = [rhoXYZ;rhoXYZ(indXimagesONLY,:)];
isImages = true(size(XYZwithImages,1),1); isImages(1:size(XYZ,1))=false; % true if the atom is an image

% control - plot particle positions
%{
    figure, hold on, axis equal, view(3)
    plot3D(XYZ(atomsROI.type==details.type.fluid,:),'b.','markersize',2)
    plot3D(XYZ(atomsROI.type==details.type.wall,:),'co')
    plot3D(XYZ(atomsROI.type==details.type.pillar,:),'go')
    plot3D(XYZ(atomsROI.type==details.type.sphere,:),'rs')
    % add images with filled symbols
    plot3D(XYZimagesONLY(atomsROI.isfluid(indXimagesONLY),:),'bo','markersize',2,'markerfacecolor','b')
    plot3D(XYZimagesONLY(atomsROI.iswall(indXimagesONLY),:),'co','markerfacecolor','c')
    plot3D(XYZimagesONLY(atomsROI.ispillar(indXimagesONLY),:),'go','markerfacecolor','g')
    plot3D(XYZimagesONLY(atomsROI.issphere(indXimagesONLY),:),'rs','markerfacecolor','r')
%}

% control - plot velocity field
%{
    figure, hold on
    quiver3(XYZ(:,1),XYZ(:,2),XYZ(:,3),vXYZ(:,1),vXYZ(:,2),vXYZ(:,3))
    view(3), axis equal
%}

%% determine the separation distance in simulation
boxdims = ROIbox(:,2) - ROIbox(:,1);
Vbead_guess = prod(boxdims)/size(XYZ,1); % m3
rbead_guess = (3/(4*pi)*Vbead_guess)^(1/3);
cutoff = 3*rbead_guess;
[verletList,~,dmin] = buildVerletList(XYZ,cutoff); % ~ means here that the 2nd output is not used
rbead = dmin/2;
s = 2*rbead; % separation distance
h = 2*s;     % smoothing length


%% add 3D Verlet list
% we focus on fluid atoms (only)
XYZfluid = XYZ(atomsROI.isfluid,:);
natomsfluid = size(XYZfluid,1);
isfluidwithimages = [atomsROI.isfluid;atomsROI.isfluid(indXimagesONLY)];
XYZfluidwithimages = XYZwithImages(isfluidwithimages,:);
vXYZfluidwithImages = vXYZwithImages(isfluidwithimages,:);
isImagesfluid =  isImages & isfluidwithimages;
[Vfluidwithimages,cutoff,dmin] = buildVerletList(XYZfluidwithimages,1.2*h,[],[],[],isImagesfluid(isfluidwithimages),isImagesfluid(isfluidwithimages) & false);

% control of neighboring particles or one 
%{
figure, hold on
for itest = unidrnd(natomsfluid,1,100)
    plot3D(XYZfluidwithimages(~isImagesfluid(isfluidwithimages),:),'bo')
    plot3D(XYZfluidwithimages(isImagesfluid(isfluidwithimages),:),'bo','markerfacecolor','b')
    plot3D(XYZfluidwithimages(Vfluidwithimages{itest,:},:),'ro','markerfacecolor','r')
    plot3D(XYZfluidwithimages(itest,:),'ko','markerfacecolor','k')
end
view(3), axis equal
%}


%% ForceLanshoff
% This pairwise force is an artificial force controlling the dissipation of velocity in the simulation
% its value is not stored in the simulation and it needs to be calculated from pairwise distances and
% relative velocities

% General syntax:
% [F,W] = forceLandshoff(XYZ,vXYZ,V,config)
% XYZ   : coordinates
% vXYZ  : velocities
% V     : corresponding Verlet list
% config: configuration for Landshoff calculations based on the properties of the simulation

c0 = 1500; % speed of sound (m/s) % maxVelocity / MachTarget;
dynamicViscosity = 0.13; % Pa.s (viscosity to find)
q1 = 1; % 8 * dynamicViscosity / (hinformed*c0*rho);
mbead = 4.38e-12; % kg
configL  = struct( ...real dynamic viscosity: rho * q1 * h * c0 / 8 (2D) or 10 (3D)
   'gradkernel', kernelSPH(h,'lucyder',3),...% kernel gradient (note that h is bound with the kernel)
            'h', h,...   smoothing length (m)
           'c0',1500,... speed of the sound (m/s)
           'q1',1,...    constant
          'rho', rhoXYZwithImages(isfluidwithimages), ... fluid density
         'mass', mbead,...  bead weight
          'vol', mbead./rhoXYZwithImages(isfluidwithimages), ...       bead volume (uniquely for virial stress)
'repulsiononly', false ...    if true, only Landshoff forces when dot(rij,vij)<0
    );
[Fwithimages,Wwithimages] = forceLandshoff(XYZfluidwithimages,vXYZfluidwithImages,Vfluidwithimages,configL);
wihtoutimages = ~isImagesfluid(isfluidwithimages);
Fland = Fwithimages(wihtoutimages,:); % F Landshoff forces
Wland = Wwithimages(wihtoutimages,:); % corresponding Virial Stress Tensor

% plot the Landshoff forces acting on particles
figure, hold on
plot3D(XYZfluid,'bo','markersize',2)
quiver3(XYZfluid(:,1),XYZfluid(:,2),XYZfluid(:,3),Fland(:,1),Fland(:,2),Fland(:,3),'r-')
axis equal, view(3)
figure, histogram(log10(vecnorm(Fland,2,2))) % magnitude of the force on a log10 scale


%% Interpolate Virial Stress along an xz vertical plane (as Han did)
nresolution = [1 1024 1024];
xw = xmean;
yw = linspace(ROIbox(2,1),ROIbox(2,2),nresolution(2));
zw = linspace(ROIbox(3,1),ROIbox(3,2),nresolution(3)); % vertical position used for interpolation
[Xw,Yw,Zw] = meshgrid(xw,yw,zw);
XYZgrid = [Xw(:),Yw(:),Zw(:)];
VXYZgrid = buildVerletList({XYZgrid, XYZfluidwithimages}, 2*h);  % neighbors = fluid particles
W = kernelSPH(2*h, 'lucy', 3); % kernel expression
Wgrid = zeros(prod(nresolution(1:3)), 9, 'single');
for i = 1:9 % for all diagonal terms
    Wgrid(:,i) = interp3SPHVerlet(XYZfluidwithimages, Wwithimages(:,i), XYZgrid, VXYZgrid, W, mbead./rhoXYZwithImages(isfluidwithimages));
end

%% Interpolate the Velocity, extraction of the strain rate tensor
vxyzgrid = zeros(prod(nresolution(1:3)),3,'single');
vxyzgridabove = vxyzgrid;
XYZgridabove = XYZgrid;
XYZgridabove(:,1) = XYZgridabove(:,1) + h; % information along z
for i = 1:3
    vxyzgrid(:,i) = interp3SPHVerlet(XYZfluidwithimages,vXYZfluidwithImages(:,i),XYZgrid,VXYZgrid,W,mbead./rhoXYZwithImages(isfluidwithimages));
    vxyzgridabove(:,i) = interp3SPHVerlet(XYZfluidwithimages,vXYZfluidwithImages(:,i),XYZgridabove,VXYZgrid,W,mbead./rhoXYZwithImages(isfluidwithimages));
end
gxx = reshape( (vxyzgridabove(:,1) - vxyzgrid(:,1)) / h, nresolution(1:3));
gyx = reshape( (vxyzgridabove(:,2) - vxyzgrid(:,2)) / h, nresolution(1:3));
gzx = reshape( (vxyzgridabove(:,3) - vxyzgrid(:,3)) / h, nresolution(1:3));
[gxy,gxz] = gradient(reshape(vxyzgrid(:,1),nresolution([2 3])),Yw(2,1,1)-Xw(1,1,1),Zw(1,1,2)-Zw(1,1,1));
[gyy,gyz] = gradient(reshape(vxyzgrid(:,2),nresolution([2 3])),Yw(2,1,1)-Xw(1,1,1),Zw(1,1,2)-Zw(1,1,1));
[gzy,gzz] = gradient(reshape(vxyzgrid(:,3),nresolution([2 3])),Yw(2,1,1)-Xw(1,1,1),Zw(1,1,2)-Zw(1,1,1));
Ggrid = [gxx(:) gxy(:) gxz(:) gyx(:) gyy(:) gyz(:) gzx(:) gzy(:) gzz(:)]; % nine tensor components

% Velocity control
%{
figure, hold on
step = 16; [ix,iy,iz] = meshgrid(1,1:step:nresolution(2),1:step:nresolution(3)); indok = sub2ind(nresolution,ix,iy,iz);
quiver3(XYZgrid(indok,1),XYZgrid(indok,2),XYZgrid(indok,3),vxyzgrid(indok,1),vxyzgrid(indok,2),vxyzgrid(indok,3),'g-')

quiver3(XYZgridabove(:,1),XYZgridabove(:,2),XYZgridabove(:,3),vxyzgridabove(:,1),vxyzgridabove(:,2),vxyzgridabove(:,3),'g-')
%}

%% save
backfolder = 'D:\Yao';
if exist(backfolder,'dir') 
    prefetchresult = sprintf('YAO_yz_t%0.3g_x%0.3g',tframe*1e2,xmean*1e6);
    save(fullfile(backfolder,prefetchresult))
end

%% Symmetric Strain
Straingrid = [gxx(:) 0.5*(gxy(:)+gyx(:)) 0.5*(gxz(:)+gzx(:))   0.5*(gxy(:)+gyx(:))  gyy(:) 0.5*(gyz(:)+gzy(:))  0.5*(gxz(:)+gzx(:))  0.5*(gyz(:)+gzy(:)) gzz(:)];
formatfig(figure,'figname',sprintf('Yao_yz_SHEAR_t%d_x%d',round(tframe*100),round(xmean*1e6)))
hs2 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
leg = {'\epsilon_{xx}','\epsilon_{xy}','\epsilon_{xz}','\epsilon_{yx}','\epsilon_{yy}','\epsilon_{yz}','\epsilon_{zx}','\epsilon_{zy}','\epsilon_{zz}'};
for i=1:9
    subplot(hs2(i)), imagesc(flipud(reshape(Straingrid(:,i),nresolution([2 3]))'))
    c=colorbar; if i==7, c.Label.String = 'strain rate (s^{-1})'; end
    axis image
    caxis([-5 5])
    title(leg{i},'fontsize',12,'visible','on')
end
set(hs2,'visible','off')
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

%% Stress
formatfig(figure,'figname',sprintf('Yao_yz_STRESS_t%d_x%d',round(tframe*100),round(xmean*1e6)))
hs1 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
leg = {'\tau_{xx}','\tau_{xy}','\tau_{xz}','\tau_{yx}','\tau_{yy}','\tau_{yz}','\tau_{zx}','\tau_{zy}','\tau_{zz}'};
for i=1:9
    subplot(hs1(i)), imagesc(flipud(reshape(Straingrid(:,i),nresolution([2 3]))'))
    c=colorbar; if i==7, c.Label.String = 'stress (Pa)'; end
    axis image
    caxis([-0.1 0.8])
    title(leg{i},'fontsize',12,'visible','on')
end
set(hs1,'visible','off')
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

%% Viscosity estimation
Egrid = 0.5*abs(Wgrid./Straingrid);
formatfig(figure,'figname',sprintf('Yao_yz_VISCO_t%d_x%d',round(tframe*100),round(xmean*1e6)))
hs1 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
leg = {'\mu_{xx}','\mu_{xy}','\mu_{xz}','\mu_{yx}','\mu_{yy}','\mu_{yz}','\mu_{zx}','\mu_{zy}','\mu_{zz}'};
for i=1:9
    subplot(hs1(i)), imagesc(flipud(reshape(Egrid(:,i),nresolution([2 3]))'))
    c=colorbar; if i==7, c.Label.String = 'viscosity (Pa\cdot s)'; end
    axis image
    caxis([0 0.4])
    title(leg{i},'fontsize',12,'visible','on')
end
set(hs1,'visible','off')
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

%% plot stress results
close all
offdiag = [2 3 4 6 7 8];
figstresstensor = figure;
figsheartensor = figure;
figviscosity = figure;
formatfig(figstresstensor,'figname',sprintf('STRESS_xz_t%d_z%d',round(tframe*100),round(yw*1e6)))
formatfig(figsheartensor,'figname',sprintf('SHEAR_xz_t%d_z%d',round(tframe*100),round(yw*1e6)))
formatfig(figviscosity,'figname',sprintf('VISCO_xz_t%d_z%d',round(tframe*100),round(yw*1e6)))

figure(figstresstensor), hs1 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
figure(figsheartensor), hs2 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
figure(figviscosity), hs3 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
[Wmin,Wmax,Gmin,Gmax,Emin,Emax] = deal(+Inf,-Inf,+Inf,-Inf,+Inf,-Inf);
for i=1:9
    figure(figstresstensor), subplot(hs1(i)), imagesc(flipud(reshape(Wgrid(:,i),nresolution([1 3]))')), colorbar
    figure(figsheartensor), subplot(hs2(i)), imagesc(flipud(reshape(Ggrid(:,i),nresolution([1 3]))')), colorbar
    figure(figviscosity), subplot(hs3(i)), imagesc(flipud(reshape(Egrid(:,i),nresolution([1 3]))')), colorbar
    Wmin = min(Wmin,min(Wgrid(:,i)));
    Wmax = max(Wmax,max(Wgrid(:,i)));
    Gmin = min(Wmin,min(Ggrid(:,i)));
    Gmax = max(Wmax,max(Ggrid(:,i)));
    Emin = min(Wmin,min(Egrid(:,i)));
    Emax = max(Wmax,max(Egrid(:,i)));
end
set(hs1,'visible','off')
set(hs2,'visible','off')
set(hs3,'visible','off')
for i=1:9
    figure(figstresstensor), subplot(hs1(i)), clim([Wmin Wmax])
    figure(figsheartensor), subplot(hs1(i)), clim([Gmin Gmax])
    figure(figviscosity), subplot(hs1(i)), clim([Emin Emax])
end
set(hs3,'clim',[0.01 10 ])

% plot 
figsumall = figure;
formatfig(figsumall,'figname',sprintf('STRESS_sumoff_t%d_z%d',round(tframe*100)))
title('all off-diagonal terms are added')
imagesc(flipud(reshape(sum(Wgrid(:,offdiag),2),nresolution([1 3]))'))

%% print 
outputfolder = 'YAOresults';
if ~exist(outputfolder,'dir'), mkdir(outputfolder), end
 figure(figstresstensor)
 print_pdf(300,[get(figstresstensor,'filename') '.pdf'],outputfolder,'nocheck') % PDF 300 dpi
 print_png(300,fullfile(outputfolder,get(figstresstensor,'filename')),'','',0,0,0)
 figure(figsheartensor)
 print_pdf(300,[get(figsheartensor,'filename') '.pdf'],outputfolder,'nocheck') % PDF 300 dpi
 print_png(300,fullfile(outputfolder,get(figsheartensor,'filename')),'','',0,0,0)
 figure(figviscosity)
 print_pdf(300,[get(figviscosity,'filename') '.pdf'],outputfolder,'nocheck') % PDF 300 dpi
 print_png(300,fullfile(outputfolder,get(figviscosity,'filename')),'','',0,0,0)
figure(figsumall)
 print_pdf(300,[get(figsumall,'filename') '.pdf'],outputfolder,'nocheck') % PDF 300 dpi
 print_png(300,fullfile(outputfolder,get(figsumall,'filename')),'','',0,0,0)