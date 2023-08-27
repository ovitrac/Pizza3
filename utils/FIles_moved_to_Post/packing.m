%% Simple HCP (hexagonal closed pack) lattice
% generator from: https://en.wikipedia.org/wiki/Close-packing_of_equal_spheres
% INRAE\Olivier Vitrac, Han Chen - rev. 2023-02-20


% Define parameters
r = 0.5; % Radius of spheres
forceFCC = 0; % 0 for HCP and 1 for FCC

% Lattice
[i,j,k] = ndgrid(0:2,0:2,0:2); % HCP is period 2, FCC is period 3
[i,j,k] = deal(i(:),j(:),k(:));
centers = [
    2*i + mod(j+k,2) ...x
    sqrt(3)*(j+mod(k,2)/3)  + (mod(k,3)==2)*forceFCC...y
    (2*sqrt(6)/3)*k ... z
    ]*r;

% Create sphere coordinates
[xs,ys,zs] = sphere(100);

% Translate spheres to close-packed positions
figure
for i = 1:size(centers, 1)
    surf(xs*r + centers(i,1), ys*r + centers(i,2), zs*r + centers(i,3),'FaceColor',rgb('deepskyblue'),'EdgeColor','none');
    hold on;
end
lighting gouraud
camlight left
shading interp
axis equal


%% Lucy kernel, note that s scales the kernel (different scaling in 2D and 3D)
syms h s W(r)
assume(h,{'real','positive'})
assume(r,{'real','positive'})
W(r) = piecewise(r<h,(1/s)*(1+3*r/h)*(1-r/h)^3,r>=h,0); % kernel definition
s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s);   % scaling factor in 2D
s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D

% radial position where the 3D kernel is equal to its average
r1 = solve(W3(r)==1,r,'Maxdegree',4); % all solutions (4)
% only the second root is real and positive
vpa(subs(r1,h,1))
r1 = simplify(r1(2));

% convert the kernel to a Matlab anonymous function
%   function_handle with value:
%     @(h,r)(1.0./h.^3.*(r./h-1.0).^3.*((r.*3.0)./h+1.0).*(-1.05e+2./1.6e+1))./pi
syms R
assume(R<h)
matlabFunction((subs(W3(R),R,r)))

%% Kernel: numeric implementation
% single accuracy is used instead of double to reduce memory load
r = single(0.5);
h= single(2*r);
cutoff = @(r) single(r<h);
W = @(r) cutoff(r) .* ( (1.0./h.^3.*(r./h-1.0).^3.*((r.*3.0)./h+1.0).*(-1.05e+2./1.6e+1))./pi );
r1expr = matlabFunction(r1);
rplot = linspace(0,1.5*h,1e3);
Wref = 0.1:0.1:floor(W(0));
figure, plot(rplot,W(rplot),'-','linewidth',2), xlabel('r'), ylabel('kernel')
hold on, plot(interpleft(W(rplot),rplot,Wref),Wref,'ro','markerfacecolor',rgb('Crimson'))
line(r1expr(h)*[1;1;0],[0;1;1],'linewidth',1.5,'linestyle',':','color',rgb('deepskyblue'))
line([r h;r h],[0 0;1 1],'linewidth',1.5,'linestyle','--','color',rgb('coral'))
text(double(r),1,sprintf('\\leftarrow r_{bead}=%0.3g',r),'HorizontalAlignment','left','VerticalAlignment','top','fontsize',12,'color',rgb('Coral'))
text(double(h),1,sprintf('\\leftarrow h=%0.3g',h),'HorizontalAlignment','left','VerticalAlignment','top','fontsize',12,'color',rgb('Coral'))

% 3D field
nresolution = 200;
xw = single(linspace(min(centers(:,1))-h,max(centers(:,1))+h,nresolution));
yw = single(linspace(min(centers(:,2))-h,max(centers(:,2))+h,nresolution));
zw = single(linspace(min(centers(:,3))-h,max(centers(:,3))+h,nresolution));
[Xw,Yw,Zw] = meshgrid(xw,yw,zw);
% calculate the radial distance to the center of the ith sphere
R = @(i) sqrt( (Xw-centers(i,1)).^2 + (Yw-centers(i,2)).^2 + (Zw-centers(i,3)).^2 );
sumW = zeros(size(Xw),'single');
for i=1:size(centers,1)
    dispf('evaluate field respective to kernel %d',i)
    sumW = sumW + W(R(i));
end
% full domain
figure, isosurface(Xw,Yw,Zw,sumW,1), axis equal
% cut domain x>1.3
figure
sumWcut = sumW;
xcut = 1.3;
sumWcut(xw>xcut,:,:) = [];
[Xwcut,Ywcut,Zwcut] = deal(Xw,Yw,Zw);
Xwcut(xw>xcut,:,:) = [];
Ywcut(xw>xcut,:,:) = [];
Zwcut(xw>xcut,:,:) = [];
p1 = patch(isosurface(Xwcut,Ywcut,Zwcut,sumWcut, 1),'FaceColor',rgb('tomato'),'EdgeColor','none');
p2 = patch(isocaps(Xwcut,Ywcut,Zwcut,sumWcut, 1),'FaceColor','interp','EdgeColor','none');
colormap(gray(100)), camlight left, camlight, lighting gouraud, view(-138,28), axis equal
% slice
figure, hs= slice(Xw,Yw,Zw,sumW,single(1:3),single(1:3),single([])); set(hs,'edgecolor','none','facealpha',0.5), axis equal

%% Calculate the field between two beads
r = 0.5; % Radius of spheres
forceFCC = 1; % 0 for HCP and 1 for FCC

% Lattice
[i,j,k] = ndgrid(0:4,0:4,0:4); % HCP is period 2, FCC is period 3
[i,j,k] = deal(i(:),j(:),k(:));
centers = [
    2*i + mod(j+k,2) ...x
    sqrt(3)*(j+mod(k,2)/3)  + (mod(k,3)==2)*forceFCC...y
    (2*sqrt(6)/3)*k ... z
    ]*r;

% Create sphere coordinates
[xs,ys,zs] = sphere(100);

% Translate spheres to close-packed positions
figure
ncenters = size(centers,1);
for i = 1:size(centers, 1)
    hs(i) = surf(xs*r + centers(i,1), ys*r + centers(i,2), zs*r + centers(i,3),'FaceColor',rgb('deepskyblue'),'EdgeColor','none','facealpha',0.2);
    hold on;
end
lighting gouraud
camlight left
shading interp
axis equal

% the most central bead and found the next neighbors (coordination number = 12 with HCP)
[~,icentral] = min(sum((centers-mean(centers)).^2,2));
set(hs(icentral),'facecolor',rgb('Crimson'),'FaceAlpha',1)
dcentral = sqrt(sum((centers-centers(icentral,:)).^2,2));
icontact = find( (dcentral>=2*r-0.0001) & (dcentral<=2*r+0.0001) );
ncontact = length(icontact);
set(hs(icontact),'facecolor',rgb('ForestGreen'),'FaceAlpha',1)

%% Averaged field between the icentral (red) bead and the icontact (green) one
nd = 1000;
d = linspace(-0.1*r,2*r+0.1*r,nd)'; % support
r = 0.5;
hlist = r*linspace(1.5,4,20);
nh = length(hlist);
sumW = zeros(nd,nh,ncontact);

for ih = 1:nh
    h= hlist(ih);
    cutoff = @(r) single(r<h);
    W = @(r) cutoff(r) .* ( (1.0./h.^3.*(r./h-1.0).^3.*((r.*3.0)./h+1.0).*(-1.05e+2./1.6e+1))./pi );
    for j = 1:ncontact
        xyz0 = centers(icentral,:);   % red bead coordinates
        xyz = centers(icontact(j),:); % green bead coordinated
        direction = (xyz-xyz0)/norm(xyz-xyz0);
        xyzd = xyz0 + direction .* d;
        R = @(i) sqrt( sum((xyzd-centers(i,:)).^2,2));
        for i=1:size(centers,1)
            sumW(:,ih,j) = sumW(:,ih,j) + W(R(i));
        end
    end
end
figure('defaultAxesColorOrder',parula(nh))
leg = arrayfun(@(x) sprintf('h/r_{bead}=%0.3g',x),hlist/r,'UniformOutput',false);
hp = plot(d/r,mean(sumW,3),'-','linewidth',3);
legend(hp,leg,'location','eastoutside','fontsize',10,'box','off')
formatax(gca,'fontsize',12)
xlabel('r/r_{bead}','fontsize',16)
ylabel('density','fontsize',16)