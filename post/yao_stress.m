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

%% initialization
close all
clearvars -global -except tframe ztop

%% actions
actions = {'plot','save'};
if exist('D:\Yao','dir')
    local = 'D:\Yao';
else
    local = pwd;
end
backupfolder = fullfile(local,'Yao_xy');
if ~exist(backupfolder,'dir'), mkdir(backupfolder), end

%% load the frame
if ~exist('tframe','var')
    tframe = 0.67; % choose any frame between 0.11 and 1.11
end
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
if ~exist('ztop','var')
    ztop = max(pillarxyz(:,3)); % top z coord of the pillar
end
zthick = ztop*0.15;          % define the thickness of the plane around ztop
ROIbox = details.box;      % select the ROI (region of interest)
ROIbox(3,:) = ztop + [-0.5 +0.5]*zthick; % update the ROI to ztop-zthick/2 and ztop+zthick/2
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
[XYZimagesONLY ,indXimagesONLY]= PBCimages(XYZ,ROIbox,[true,true,false],zthick); % add periodic images within zthick around x and y (z is not periodic)
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



%% Interpolate Virial Stress along an horizontal plane (has Han did)
nresolution = [1024 1024 1];
xw = linspace(ROIbox(1,1),ROIbox(1,2),nresolution(1));
yw = linspace(ROIbox(2,1),ROIbox(2,2),nresolution(1));
zw = ztop; % vertical position used for interpolation
[Xw,Yw,Zw] = meshgrid(xw,yw,zw);
XYZgrid = [Xw(:),Yw(:),Zw(:)];
VXYZgrid = buildVerletList({XYZgrid XYZfluidwithimages},2*h);  % neighbors = fluid particles
W = kernelSPH(2*h,'lucy',3); % kernel expression
Wgrid = zeros(prod(nresolution(1:2)),9,'single');
for i = 1:9 % for all diagonal terms
    Wgrid(:,i) = interp3SPHVerlet(XYZfluidwithimages,Wwithimages(:,i),XYZgrid,VXYZgrid,W,mbead./rhoXYZwithImages(isfluidwithimages));
end

%% Interpolate the Velocity, extraction of the strain rate tensor
vxyzgrid = zeros(prod(nresolution(1:2)),3,'single');
vxyzgridabove = vxyzgrid;
XYZgridabove = XYZgrid;
XYZgridabove(:,3) = XYZgridabove(:,3) + h; % information along z
for i = 1:3
    vxyzgrid(:,i) = interp3SPHVerlet(XYZfluidwithimages,vXYZfluidwithImages(:,i),XYZgrid,VXYZgrid,W,mbead./rhoXYZwithImages(isfluidwithimages));
    vxyzgridabove(:,i) = interp3SPHVerlet(XYZfluidwithimages,vXYZfluidwithImages(:,i),XYZgridabove,VXYZgrid,W,mbead./rhoXYZwithImages(isfluidwithimages));
end
gxz = reshape( (vxyzgridabove(:,1) - vxyzgrid(:,1)) / h, nresolution(1:2));
gyz = reshape( (vxyzgridabove(:,2) - vxyzgrid(:,2)) / h, nresolution(1:2));
gzz = reshape( (vxyzgridabove(:,3) - vxyzgrid(:,3)) / h, nresolution(1:2));
[gxx,gxy] = gradient(reshape(vxyzgrid(:,1),nresolution(1:2)),Xw(1,2)-Xw(1,1),Yw(2,1)-Yw(1,1));
[gyx,gyy] = gradient(reshape(vxyzgrid(:,2),nresolution(1:2)),Xw(1,2)-Xw(1,1),Yw(2,1)-Yw(1,1));
[gzx,gzy] = gradient(reshape(vxyzgrid(:,3),nresolution(1:2)),Xw(1,2)-Xw(1,1),Yw(2,1)-Yw(1,1));
Ggrid = [gxx(:) gxy(:) gxz(:) gyx(:) gyy(:) gyz(:) gzx(:) gzy(:) gzz(:)]; % nine tensor components

% Velocity control
if ismember('plot',actions)
    close all
    formatfig(figure,'figname',sprintf('YAOxy_t%0.3g_z%0.3g',round(tframe*100),round(ztop*1e6)),'PaperPosition',[1.4920    7.8613   18.0000   14.0000]), hold on
    step = 8; [ix,iy] = meshgrid(1:step:nresolution(1),1:step:nresolution(2)); indok = sub2ind(nresolution(1:2),ix,iy);
    quiver3(XYZgrid(indok,1),XYZgrid(indok,2),XYZgrid(indok,3),vxyzgrid(indok,1),vxyzgrid(indok,2),vxyzgrid(indok,3),'r-')
    axis tight
    view(23,29)
    daspect([1 1 0.03 ])
    xlabel('x (m)','fontsize',12)
    ylabel('y (m)','fontsize',12)
    title(sprintf('t = %0.3g s - z = %0.3g µm',tframe,round(ztop*1e6)))
    print_png(200,fullfile(backupfolder,get(gcf,'filename')),'','',0,0,0)
    return
end
%{
figure, hold on
step = 8; [ix,iy] = meshgrid(1:step:nresolution(1),1:step:nresolution(2)); indok = sub2ind(nresolution(1:2),ix,iy);
quiver3(XYZgrid(indok,1),XYZgrid(indok,2),XYZgrid(indok,3),vxyzgrid(indok,1),vxyzgrid(indok,2),vxyzgrid(indok,3),'r-')
quiver3(XYZgridabove(:,1),XYZgridabove(:,2),XYZgridabove(:,3),vxyzgridabove(:,1),vxyzgridabove(:,2),vxyzgridabove(:,3),'g-')
%}

%% save
backfolder = fullfile('backupfolder','details');
backfolder = 'D:\Yao';
if exist(backfolder,'dir') 
    prefetchresult = sprintf('YAO_xy_t%0.3g_z%0.3g',tframe*1e2,ztop*1e6);
    save(fullfile(backfolder,prefetchresult))
end

%% figure of 3D velocity field
figure, hold on
step = 16; [ix,iy] = meshgrid(1:step:nresolution(1),1:step:nresolution(2)); indok = sub2ind(nresolution(1:2),ix,iy);
quiver3(XYZgrid(indok,1),XYZgrid(indok,2),XYZgrid(indok,3),vxyzgrid(indok,1),vxyzgrid(indok,2),vxyzgrid(indok,3),'r-')
view(3)
xlabel('x (m)','fontsize',12)
ylabel('y (m)','fontsize',12)
zlabel('z (m)','fontsize',12)
set(gcf,'color','w')

%% Density
XYZs = atomsROI{atomsROI.issolid,details.coords};
rhobeadXYZ = atomsROI.c_rho_smd; % volume of the bead
rhobeadXYZwithImages = [rhobeadXYZ;rhobeadXYZ(indXimagesONLY)];
VbeadXYZwithImages = mbead./rhobeadXYZwithImages;
VXYZ  = buildVerletList({XYZgrid XYZwithImages},1.2*h);  % neighbors = fluid particles
VXYZs = buildVerletList({XYZgrid XYZs},h); % neighbors = solid particles (0.85*s)
icontactsolid = find(cellfun(@length,VXYZs)>0);
VXYZ(icontactsolid) = repmat({[]},length(icontactsolid),1);
rhobeadXYZgrid = interp3SPHVerlet(XYZwithImages,rhobeadXYZwithImages,XYZgrid,VXYZ,W,VbeadXYZwithImages);
rhobeadXYZgrid = reshape(rhobeadXYZgrid,size(Xw));


%% Symmetric Strain
Straingrid = [gxx(:) 0.5*(gxy(:)+gyx(:)) 0.5*(gxz(:)+gzx(:))   0.5*(gxy(:)+gyx(:))  gyy(:) 0.5*(gyz(:)+gzy(:))  0.5*(gxz(:)+gzx(:))  0.5*(gyz(:)+gzy(:)) gzz(:)];
Straingrid(find(isnan(rhobeadXYZgrid)),:) = NaN;

formatfig(figure,'figname',sprintf('Yao_xy_SHEAR_t%d_z%d',round(tframe*100),round(zw*1e6)))
hs2 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
leg = {'$\dot{\varepsilon}_{xx}$','$\dot{\varepsilon}_{xy}$','$\dot{\varepsilon}_{xz}$',...
       '$\dot{\varepsilon}_{yx}$','$\dot{\varepsilon}_{yy}$','$\dot{\varepsilon}_{yz}$',...
       '$\dot{\varepsilon}_{zx}$','$\dot{\varepsilon}_{zy}$','$\dot{\varepsilon}_{zz}$'};
for i=1:9
    subplot(hs2(i)), imagesc(flipud(reshape(Straingrid(:,i),nresolution([1 2]))))
    c=colorbar; if i==7, c.Label.String = 'strain rate (s^{-1})'; end
    axis image
    caxis([-5 5])
    title(leg{i},'fontsize',12,'visible','on','Interpreter','Latex')
end
set(hs2,'visible','off')
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

%% Stress
formatfig(figure,'figname',sprintf('Yao_xy_STRESS_t%d_z%d',round(tframe*100),round(zw*1e6)))
hs2 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
leg = {'\tau_{xx}','\tau_{xy}','\tau_{xz}','\tau_{yx}','\tau_{yy}','\tau_{yz}','\tau_{zx}','\tau_{zy}','\tau_{zz}'};
Wgrid(find(isnan(rhobeadXYZgrid)),:) = NaN;
for i=1:9
    subplot(hs2(i)), imagesc(flipud(reshape(Wgrid(:,i),nresolution([1 2]))))
    c=colorbar; if i==7, c.Label.String = 'stress (Pa)'; end
    axis image
    caxis([-0.1 0.8])
    title(leg{i},'fontsize',12,'visible','on')
end
set(hs2,'visible','off')
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)


%% Lamé coefficients
% Extract the diagonal terms for the trace calculation
iok = find(~isnan(rhobeadXYZgrid)); nok = length(iok);
% Extract the diagonal terms for the trace calculation
trace_Strain = Straingrid(iok,1) + Straingrid(iok,5) + Straingrid(iok,9);
% Form the matrix A for the global least-square problem
A = zeros(nok* 9, 2);
% Fill in the lambda * trace(Straingrid) * I part
trace_Strain_repeated = repmat(trace_Strain, 9, 1); % Repeat trace_Strain 9 times
A(:, 1) = trace_Strain_repeated(:); % Fill the first column of A with the repeated trace
% Fill in the 2 * mu * Straingrid part
A(:, 2) = reshape(2 * Straingrid(iok,:)', [], 1); % Reshape 2 * Straingrid to a column vector
% Reshape Wgrid to a vector
Wgrid_vectorized = reshape(Wgrid(iok,:)', [], 1);
% Solve the non-negative least squares problem
params = lsqnonneg(A, double(Wgrid_vectorized));
% Extract the results
lam_global = params(1);
mu_global = params(2);

% Display the results
disp(['Lambda (λ): ', num2str(lam_global)]);
disp(['Mu (μ): ', num2str(mu_global)]);

% Local approximates
% Initialize arrays to store the local estimations of mu and lam
mu_local = zeros(1048576, 1);
lam_local = zeros(1048576, 1);

% Extract the diagonal terms of Straingrid for trace calculation
trace_Strain = Straingrid(:,1) + Straingrid(:,5) + Straingrid(:,9);

% Construct the identity matrix as a vector
I_vector = [1 0 0 0 1 0 0 0 1];

for i = 1:1048576
    % Create the system of equations for the current grid point
    A_local = zeros(9, 2);
    
    % Fill in the lambda * trace(Straingrid) * I part
    A_local(:, 1) = trace_Strain(i) * I_vector';
    
    % Fill in the 2 * mu * Straingrid part
    A_local(:, 2) = 2 * Straingrid(i, :)';
    
    % Solve for lam and mu using non-negative least squares
    params_local = lsqnonneg(A_local, double(Wgrid(i, :))');
    
    % Store the results
    lam_local(i) = params_local(1);
    mu_local(i) = params_local(2);
end

% Display a sample of the results
disp('Sample of local Lambda (λ) estimates:');
disp(lam_local(1:10)');
disp('Sample of local Mu (μ) estimates:');
disp(mu_local(1:10)');

%% Lambda, Mu plots
formatfig(figure,'figname',sprintf('Yao_xy_VISCO_L2_t%d_z%d',round(tframe*100),round(zw*1e6)))
imagesc(xw,yw,flipud(reshape(mu_local,nresolution([1 2]))))
c=colorbar; c.Label.String = '\mu (Pa\cdot s^{-1})'; caxis([0 0.15])
c.FontSize=12; formatax(gca,'fontsize',12), c.Label.FontSize=16;
xlabel('x (µm)','fontsize',14), ylabel('y (µm)','fontsize',14)
title({'Dynamic Viscosity' sprintf('t = \\bf%0.3g s\\rm, z = \\bf%0.3g\\rm µm',tframe,1e6*ztop)},'fontsize',14,'visible','on')
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

formatfig(figure,'figname',sprintf('Yao_xy_VISCOVOL_L2_t%d_z%d',round(tframe*100),round(zw*1e6)))
imagesc(xw,yw,flipud(reshape(lam_local,nresolution([1 2]))))
c=colorbar; c.Label.String = '\lambda (Pa\cdot s^{-1})'; caxis([0 2])
c.FontSize=12; formatax(gca,'fontsize',12), c.Label.FontSize=16;
xlabel('x (µm)','fontsize',14), ylabel('y (µm)','fontsize',14)
title({'Elongational Viscosity' sprintf('t = \\bf%0.3g s\\rm, z = \\bf%0.3g\\rm µm',tframe,1e6*ztop)},'fontsize',14,'visible','on')
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

return

RECOresult = fullfile(backfolder,sprintf('YAO_VISCOL2_xy_t%0.3g_z%0.3g',tframe*1e2,ztop*1e6));
save(RECOresult,'mu_local','lam_local','Straingrid','Wgrid','Xw','Yw','xw','yw','tframe','ztop')

%% Comparison
backfolder = 'D:\Yao';
RECO = [
    load('D:\Yao\YAO_VISCOL2_xy_t57_z425.mat')
    load('D:\Yao\YAO_VISCOL2_xy_t67_z425.mat')
    load('D:\Yao\YAO_VISCOL2_xy_t77_z425.mat')
    ];
formatfig(figure,'figname','Yao_distributionStrain'), hold on
for i=1:length(RECO)
    histogram(RECO(i).Straingrid(:,2),linspace(-5,5,100),'DisplayName',sprintf('t=%0.3g s',RECO(i).tframe),'FaceAlpha',0.5)
end
formatax(gca,'fontsize',12)
legend('fontsize',14,'box','off')
xlabel('Strain Rate: $\dot{\varepsilon}_{yx}$ (s$^{-1}$)', 'fontsize', 14, 'Interpreter', 'latex')
ylabel('Counts','fontsize',14)
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

formatfig(figure,'figname','Yao_distributionStress'), hold on
for i=1:length(RECO)
    histogram(RECO(i).Wgrid(:,2),linspace(-0.1,0.1,500),'DisplayName',sprintf('t=%0.3g s',RECO(i).tframe),'FaceAlpha',0.5)
end
formatax(gca,'xlim',[-0.07 0.07],'ylim',[0 2.5]*1e4,'fontsize',12)
legend('fontsize',14,'box','off')
xlabel('Shear Stress: \tau_{yx} (Pa)','fontsize',14)
ylabel('Counts','fontsize',14)
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

formatfig(figure,'figname','Yao_distributionVisco'), hold on
for i=1:length(RECO)
    histogram(RECO(i).mu_local,linspace(0,0.3,100),'DisplayName',sprintf('t=%0.3g s',RECO(i).tframe),'FaceAlpha',0.5)
end
formatax(gca,'xlim',[0 0.18],'ylim',[0 2.5]*1e4,'fontsize',12)
legend('fontsize',14,'box','off')
xlabel('Dynamic Viscosity: \mu (Pa\cdot s^{-1})','fontsize',14)
ylabel('Counts','fontsize',14)
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

formatfig(figure,'figname','Yao_distributionElongVisco'), hold on
for i=1:length(RECO)
    histogram(RECO(i).lam_local,linspace(0,0.5,200),'DisplayName',sprintf('t=%0.3g s',RECO(i).tframe),'FaceAlpha',0.5)
end
formatax(gca,'xlim',[0 0.4],'ylim',[0 2.5]*1e4,'fontsize',12)
legend('fontsize',14,'box','off')
xlabel('Elongational Viscosity: \lambda (Pa\cdot s^{-1})','fontsize',14)
ylabel('Counts','fontsize',14)
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

% obsolete below ---------------------------------------------------------------------------------------------------------

%% Viscosity estimation
% Egrid = abs(Wgrid./Ggrid);
Egrid = 0.5*abs(Wgrid./Straingrid);
formatfig(figure,'figname',sprintf('Yao_xy_VISCO_t%d_z%d',round(tframe*100),round(zw*1e6)))
hs2 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
leg = {'\mu_{xx}','\mu_{xy}','\mu_{xz}','\mu_{yx}','\mu_{yy}','\mu_{yz}','\mu_{zx}','\mu_{zy}','\mu_{zz}'};
for i=1:9
    subplot(hs2(i)), imagesc(reshape(Straingrid(:,i),nresolution([1 2])))
    c=colorbar; if i==7, c.Label.String = 'stress (Pa\cdot s)'; end
    axis image
    caxis([0 1])
    title(leg{i},'fontsize',12,'visible','on')
end
set(hs2,'visible','off')
print_png(400,fullfile(backfolder,get(gcf,'filename')),'','',0,0,0)

% %% plot stress results
% close all
% offdiag = [2 3 4 6 7 8];
% figstresstensor = figure;
% figsheartensor = figure;
% figviscosity = figure;
% formatfig(figstresstensor,'figname',sprintf('STRESS_t%d_z%d',round(tframe*100),round(zw*1e6)))
% formatfig(figsheartensor,'figname',sprintf('SHEAR_t%d_z%d',round(tframe*100),round(zw*1e6)))
% formatfig(figviscosity,'figname',sprintf('VISCO_t%d_z%d',round(tframe*100),round(zw*1e6)))
% 
% figure(figstresstensor), hs1 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
% figure(figsheartensor), hs2 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
% figure(figviscosity), hs3 = subplots([1 1 1],[1 1 1],0.01,0.01); %,'alive',offdiag);
% [Wmin,Wmax,Gmin,Gmax,Emin,Emax] = deal(+Inf,-Inf,+Inf,-Inf,+Inf,-Inf);
% for i=1:9
%     figure(figstresstensor), subplot(hs1(i)), imagesc(reshape(Wgrid(:,i),nresolution([1 2]))), colorbar
%     figure(figsheartensor), subplot(hs2(i)), imagesc(reshape(Ggrid(:,i),nresolution([1 2]))), colorbar
%     figure(figviscosity), subplot(hs3(i)), imagesc(reshape(Egrid(:,i),nresolution([1 2]))), colorbar
%     Wmin = min(Wmin,min(Wgrid(:,i)));
%     Wmax = max(Wmax,max(Wgrid(:,i)));
%     Gmin = min(Wmin,min(Ggrid(:,i)));
%     Gmax = max(Wmax,max(Ggrid(:,i)));
%     Emin = min(Wmin,min(Egrid(:,i)));
%     Emax = max(Wmax,max(Egrid(:,i)));
% end
% set(hs1,'visible','off')
% set(hs2,'visible','off')
% set(hs3,'visible','off')
% for i=1:9
%     figure(figstresstensor), subplot(hs1(i)), clim([Wmin Wmax])
%     figure(figsheartensor), subplot(hs1(i)), clim([Gmin Gmax])
%     figure(figviscosity), subplot(hs1(i)), clim([Emin Emax])
% end
% set(hs3,'clim',[0.01 10 ])
% 
% % plot 
% figsumall = figure;
% formatfig(figsumall,'figname',sprintf('STRESS_sumoff_t%d_z%d',round(tframe*100)))
% title('all off-diagonal terms are added')
% imagesc(reshape(sum(Wgrid(:,offdiag),2),nresolution([1 2])))
% 
% %% print 
% outputfolder = 'YAOresults';
% if ~exist(outputfolder,'dir'), mkdir(outputfolder), end
%  figure(figstresstensor)
%  print_pdf(300,[get(figstresstensor,'filename') '.pdf'],outputfolder,'nocheck') % PDF 300 dpi
%  print_png(300,fullfile(outputfolder,get(figstresstensor,'filename')),'','',0,0,0)
%  figure(figsheartensor)
%  print_pdf(300,[get(figsheartensor,'filename') '.pdf'],outputfolder,'nocheck') % PDF 300 dpi
%  print_png(300,fullfile(outputfolder,get(figsheartensor,'filename')),'','',0,0,0)
%  figure(figviscosity)
%  print_pdf(300,[get(figviscosity,'filename') '.pdf'],outputfolder,'nocheck') % PDF 300 dpi
%  print_png(300,fullfile(outputfolder,get(figviscosity,'filename')),'','',0,0,0)
% figure(figsumall)
%  print_pdf(300,[get(figsumall,'filename') '.pdf'],outputfolder,'nocheck') % PDF 300 dpi
%  print_png(300,fullfile(outputfolder,get(figsumall,'filename')),'','',0,0,0)