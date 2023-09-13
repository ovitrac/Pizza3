% EXAMPLE 3
% This theoretical example shows how the Landshoff forces and stresses develop in "ideal" shear flows
%   several packing effects are analyzed:  HCP, FCC, SC, SC2, SC3
%
% INRAE\Olivier Vitrac, Han Chen

% 2023-09-13 release candidate - scarce comments (agree), read example2bis.m for justifications

%% Input variables
rbead = 1.0414980e-05;
hLandshoff = 1.5*2*rbead; %1.25e-5; % m
configLandshoff = struct( ...
    'gradkernel', kernelSPH(hLandshoff,'lucyder',3),...kernel gradient
    'h', hLandshoff,...smoothing length (m)
    'c0',0.32,...speed of the sound (m/s)
    'q1',30,... viscosity coefficient (-)
    'rho', 987.3691, ...density
    'mass', 9.0418e-12,...bead mass
    'vol', 9.1580e-15...bead volume
    );
shearrate = 1; % Hz;
mu = configLandshoff.rho*configLandshoff.q1*configLandshoff.c0*configLandshoff.h/10; 

% Dynamic simulation
packingmode = 'HCP';
% packingmode = 'FCC';
% packingmode = 'SC';
% packingmode = 'SC2';
% packingmode = 'SC3';
XYZ0 = packSPH(15,rbead,packingmode); nbeads = size(XYZ0,1);
fluidbox = [min(XYZ0);max(XYZ0)]';
XYZ0 = XYZ0 + [0 rbead 0];
fluidbox(2,2) = fluidbox(2,2) + 2*rbead;
fluidboxdim = diff(fluidbox,1,2);
boxcenter = mean(fluidbox,2)';
vmax = shearrate * fluidbox(2,2);
vx = vmax * XYZ0(:,2)/fluidbox(2,2);
[vy,vz] = deal(zeros(size(vx)));
vXYZ = [vx,vy,vz];
[~,i]=min(sum((XYZ0-boxcenter).^2,2));
insearch0 = false(nbeads,1); insearch0(i) = true;
V0 = buildVerletList(XYZ0,hLandshoff,[],[],[],~insearch0,insearch0);
j0 = V0{i}; j = j0; insearch = insearch0; insearch(j) = true; nj = length(j);
V  = buildVerletList(XYZ0,hLandshoff,[],[],[],~insearch);


figure, hold on
XYZ = XYZ0;
others = ~insearch; others(j) = false;
hothers = plot3D(XYZ(others,:),'bo','markersize',8);
hj = plot3D(XYZ(j,:),'go','markerfacecolor','g','markersize',16);
hi = plot3D(XYZ(i,:),'ro','markerfacecolor','r','markersize',24);
xlabel('X'), ylabel('Y'),zlabel('Z'), title(sprintf('\\bf%s\\rm configuration',packingmode),'FontSize',18)
view(3), drawnow
tmax = 10*hLandshoff/vXYZ(i,1);
nt = 500; dt = tmax/(nt-1); t = (0:dt:(nt-1)*dt)';
Flandshoff = forceLandshoff(XYZ,vXYZ,V,configLandshoff);
[Fi,Fsum] = deal(zeros(nt,3)); Fj = zeros(nt,nj,3);
Fi(1,:) = Flandshoff(i,:);
Fj(1,:,:) = permute(Flandshoff(j,:),[1 3 2]);
ax = axis;
for it=2:nt
    dispf('[%d/%d] iteration t=%0.3g s',it,nt,(it+1)*dt)
    XYZ = XYZ + vXYZ*dt;
    XYZ = XYZ-(XYZ(i,:)-XYZ0(i,:)); % i is not moving
    % noise = (rand(nbeads,1)-0.5).*vXYZ*dt/2;
    reflect = (XYZ(:,1)>fluidbox(1,2)); XYZ(reflect) = XYZ(reflect) - fluidbox(1,2) + fluidbox(1,1);
    reflect = (XYZ(:,1)<fluidbox(1,1)); XYZ(reflect) = XYZ(reflect) + fluidbox(1,2) - fluidbox(1,1);
    V = buildVerletList(XYZ,hLandshoff,[],[],[],~insearch);
    j = V{i}; others = ~insearch; others(j) = false;
    set(hothers,'XData',XYZ(others,1),'YData',XYZ(others,2),'ZData',XYZ(others,3))
    set(hj,'XData',XYZ(j,1),'YData',XYZ(j,2),'ZData',XYZ(j,3))
    set(hi,'XData',XYZ(i,1),'YData',XYZ(i,2),'ZData',XYZ(i,3))
    axis(ax), drawnow
    Flandshoff = forceLandshoff(XYZ,vXYZ,V,configLandshoff);
    Fi(it,:) = Flandshoff(i,:);
    Fj(it,:,:) = permute(Flandshoff(j0,:),[1 3 2]);
    Fsum(it,:) = sum(Flandshoff,1);
end

% plot
col = [0    0.4470    0.7410; 0.8500    0.3250    0.0980; 0.9290    0.6940    0.1250];
hfig=figure; set(hfig,'defaultAxesColorOrder',col), hold on
hp = [
    plot(t,Fi,'-','linewidth',6);
    plot(t,Fsum,'--','linewidth',4);
];
legend(hp,{'F_x','F_y','F_z','sum F_x','sum F_y','sum F_z'},'fontsize',20,'Location','best','AutoUpdate','off')
plot(t,Fj(:,:,1),':','color',col(1,:),'linewidth',2);
plot(t,Fj(:,:,2),':','color',col(2,:),'linewidth',2);
plot(t,Fj(:,:,3),':','color',col(3,:),'linewidth',2);
xlabel('time (s)','fontsize',20)
ylabel('Landshoff force','fontsize',20)
title(sprintf('\\bf%s\\rm',packingmode),'FontSize',18)

%% Static configuration
XYZ = packSPH(10,rbead,'HCP'); nbeads = size(XYZ,1);
fluidbox = [min(XYZ);max(XYZ)]';
XYZ = XYZ + [0 rbead 0];
fluidbox(2,2) = fluidbox(2,2) + 2*rbead;
fluidboxdim = diff(fluidbox,1,2);
boxcenter = mean(fluidbox,2);
vmax = shearrate * fluidbox(2,2);
vx = vmax * XYZ(:,2)/fluidbox(2,2);
[vy,vz] = deal(zeros(size(vx)));
vXYZ = [vx,vy,vz];
in = true(nbeads,1);
for i=1:3
    in = in & (XYZ(:,i)>=(hLandshoff+fluidbox(i,1))) & (XYZ(:,i)<=(fluidbox(i,2)-hLandshoff));
end
% control
close all
figure, plot3D(XYZ,'ro'), view(3)
quiver3(XYZ(:,1),XYZ(:,2),XYZ(:,3),vXYZ(:,1),vXYZ(:,2),vXYZ(:,3),2,'linewidth',2,'color','k')
xlabel('X'), ylabel('Y'),zlabel('Z'), title('initial configuration')

% Landshoff forces
V = buildVerletList(XYZ,hLandshoff); % figure, hist(cellfun(@length,V))
[Flandshoff,Wlandshoff] = forceLandshoff(XYZ,vXYZ,V,configLandshoff);
flandshoff = sqrt(sum(Flandshoff.^2,2));
figure, plot3D(XYZ,'k.'), view(3)
quiver3(XYZ(in,1),XYZ(in,2),XYZ(in,3),Flandshoff(in,1),Flandshoff(in,2),Flandshoff(in,3),1,'linewidth',2,'color','r')
xlabel('X'), ylabel('Y'),zlabel('Z'), title('Landshoff forces'), view(-25,90);
figure, hist(Flandshoff(in,1)), xlabel('component X - Forcefield')

%% Grid interpolation of Landshoff forces
% number of grid points along the largest dimension
resolution = ceil(50 * diff(fluidbox,[],2)'./max(diff(fluidbox,[],2)));
xw = linspace(fluidbox(1,1),fluidbox(1,2),resolution(1));
yw = linspace(fluidbox(2,1),fluidbox(2,2),resolution(2));
zw = linspace(fluidbox(3,1),fluidbox(3,2),resolution(3));
[Xw,Yw,Zw] = meshgrid(xw,yw,zw);
XYZgrid = [Xw(:),Yw(:),Zw(:)];
VXYZ = buildVerletList({XYZgrid XYZ},hLandshoff); % special grid syntax
% Interpolate Landshoff forces, extract components for plotting
W = kernelSPH(hLandshoff,'lucy',3); % kernel for interpolation (not gradkernel!)
FXYZgrid = interp3SPHVerlet(XYZ,Flandshoff,XYZgrid,VXYZ,W,configLandshoff.vol);
FXYZgridx = reshape(FXYZgrid(:,1),size(Xw));
FXYZgridy = reshape(FXYZgrid(:,2),size(Yw));
FXYZgridz = reshape(FXYZgrid(:,3),size(Zw));
% Interpolate the tensor xy
WXYZgrid = interp3SPHVerlet(XYZ,Wlandshoff(:,2),XYZgrid,VXYZ,W,configLandshoff.vol);
WXYZgrid = reshape(WXYZgrid,size(Xw));

%% === PLot WLandshoff - Landshoff forces only 
figure, hold on
hs = slice(Xw,Yw,Zw,WXYZgrid, ...
    [xw(1)+2*hLandshoff boxcenter(1)],...
    [yw(2)+2*hLandshoff boxcenter(2) yw(end)-2*hLandshoff],...
    [fluidbox(3,1)+2*hLandshoff boxcenter(3)]);
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