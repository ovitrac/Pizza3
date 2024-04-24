function out = hourglassSPH(X0,X,W,defgradout,V,config,forcesilent)
%HOURGLASS calculates the total hourglss correction force according to Eq. 17-24 of Comput. Methods Appl. Mech. Engrg. 286 (2015) 87–106
%
%   Syntax:
%       out = hourglassSPH(X0,X,defgradSPHout)  <--- syntax 1 (preferred)
%       out = hourglassSPH(X0,X,F [,V, config, silent])  <--- syntax 2
%
%   Inputs: (syntax 1)
%              X0 : kxd coordinates of the kernel centers of reference configuration
%               X : kxd coordinates of the kernel centers of deformed configuration
%   defgradSPHout : ouput (structure) of defgradSPH
%
%   Inputs: (syntax 2)
%              X0 : kxd coordinates of the kernel centers of reference configuration
%               X : kxd coordinates of the kernel centers of deformed configuration
%               F : k x d^2 deformation gradient
%               f : k x d pairwise forces
%               V : kx1 volume of the kernels (default=1)
%                   [] (empty matrix) or scalar value forces uniform volumes (default =1)
%      forcesilent: flag to force silence mode (default = false)
%           config: structure with fields coding for Lamé parameters
%                   lambda (default = 30 000 Pa)
%                   mu (default = 3000 Pa)
%
%   Output: out a structure with fields:
%               F : k x d^2 deformation gradient
%               C : k x d^2 Cauchy-Green deformation tensor
%               E : k x d^2 Green-Lagrange strain tensor
%               S : k x d^2 Second Piola-Kirchoff stress tensor replacing Cauchy stress (Elastic stress = config.lambda*trace(E) + 2*config.mu*E)
%               P : k x d^2 First Piola-Kirchoff stress
%               f : k x d pairwise forces
%               G : k * d von Mises stress
%     description : tensor description
%           k,d,V,correctedgradW,config are also included
%          engine : 'hourglassSPH'
%
%   Refer to Ganzenmuller (2015) for details: https://doi.org/10.1016/j.cma.2014.12.005
%   ~/han/biblio/Ganzenmuller2015-Hourglass_control_algorithm.pdf
%
%
%   See also: defgradSPH, shapeSPH, interp2SPH, interp3SPH, kernelSPH, packSPH
%

% 2023-10-31 | INRAE\Han CHEN | rev. 2023-11-15

%{
% Example:
r = 0.5;
X0 = packSPH(5,r);
X0(sqrt(sum((X0-mean(X0,1)).^2,2))>4*r,:) = [];
[xs,ys,zs] = sphere(100);

% Translate spheres to close-packed positions
figure, hold on
for i = 1:size(X0, 1), surf(xs*r + X0(i,1), ys*r + X0(i,2), zs*r + X0(i,3),'FaceColor',rgb('deepskyblue'),'EdgeColor','none'); end
lighting gouraud, camlight left, shading interp, axis equal, view(3)

% deformation (vertical compression + shearing)
Xc = mean(X0,1); Xmin = min(X0,[],1); Xmax = max(X0,[],1)

% compression along z, with support at zmin, compression rate = 20%
X = X0; X(:,3) = 0.8*(X(:,3)-Xmin(1,3)) + Xmin(1,3);
% shearing 20% along y
X(:,2) = X(:,2) + 0.2 * (Xmax(1,2)-Xmin(1,2)) * (X(:,3)-Xmin(1,3))/(Xmax(1,3)-Xmin(1,3));

% plot
figure, hold on
for i = 1:size(X, 1), surf(xs*r + X(i,1), ys*r + X(i,2), zs*r + X(i,3),'FaceColor',rgb('deepskyblue'),'EdgeColor','none'); end
lighting gouraud, camlight left, shading interp, axis equal, view(3)

% displacement
u = X-X0;
% shape matrix
gradW = kernelSPH(2*r,'lucyder',3);
shapeout = shapeSPH(X0,gradW)
defgradout = defgradSPH(u,shapeout)

% visualization
figure, hold on
scatter3(X(:,1),X(:,2),X(:,3),40,defgradout.G)
f = defgradout.f; fn=sqrt(sum(f.^2,2)); f = f./fn;
f90 = prctile(fn,90); fn(fn>f90) = f90; f = f .* fn;
quiver3(X(:,1),X(:,2),X(:,3),f(:,1),f(:,2),f(:,3))
view(3)

%hourglass force
W = kernelSPH(2*r,'lucy',3);
fhgout = hourglassSPH(X0,X,W,defgradout);
figure, hold on
scatter3(X(:,1),X(:,2),X(:,3),40)
fhg= fhgout.fHG; fn=sqrt(sum(fhg.^2,2)); fhg = fhg./fn;
f90 = prctile(fn,90); fn(fn>f90) = f90; fhg = fhg .* fn;
quiver3(X(:,1),X(:,2),X(:,3),fhg(:,1),fhg(:,2),fhg(:,3))
view(3)
%}

%Revision history
% 2023-11-15 alpha version

% Default Lamé parameters
config_default = struct(...
    'lambda',3e4, ...first Lamé  parameter
    'mu',3e3, ... shear modulus (second Lamé parameter)
    'E',9e3, ... young's modulus
    'alpha',1 ... a dimensionless coefficient that controls the amplitude of hourglass correction
);

%% arg check
if nargin<4, error('4 arguments are required at least'), end
[k,d] = size(X0); if k==0, error('please supply some displacements centers'), end
if isstruct(defgradout) && strcmpi(defgradout.engine,'defragSPH') % -- syntax 1: we reuse the arguments of shapeSPH
    args = defgradout;
    if (args.d~=d) || (args.k~=k), error('%dx%d u is not compatible with previous %dx%d centers',k,d,args.k,args.d), end
    F = args.F;
    f = args.f;
    V = args.V;
    config = args.config;
    for fig = fieldnames(config_default)'
        if ~isfield(config,fig{1}) || isempty(config.(fig{1}))
            config.(fig{1}) = config_default.(fig{1});
        end
    end
    forcesilent = args.forcesilent;
else % -- syntax 2
    if nargin<5, V = []; end
    if nargin<6, config = []; end
    if nargin<7, forcesilent = []; end
    if d>3, error('3 dimensions maximum'), end
    kv = length(V);
    if kv==0, V=1;  kv=1; end
    if kv==1, V = ones(k,1)*V; kv=k; end
    if kv~=k, error('the number of V values (%d) does not match the number of kernels (%d)',kv,k); end
    if isempty(forcesilent), forcesilent = false; end
    if isempty(config), config = config_default; end
    for fig = fieldnames(config_default)'
        if ~isfield(config,fig{1}) || isempty(config.(fig{1}))
            config.(fig{1}) = config_default.(fig{1});
        end
    end
end

%% initialization
verbosity = (k>1e3) & ~forcesilent;
largek = k>200;
t0_ = clock; t1_=t0_; screen=''; 

% vec2tensor: indices to convert a vector to a 2D tensor (faster than many reshapes)
vec2tensor_reshape = reshape(1:d^2,d,d);
vec2tensor = @(x) x(vec2tensor_reshape);

%% Output total hourglass correction force fHG
fHG = zeros(k,d,class(f));
Xij = zeros(k,k,d);
xij = zeros(k,k,d);
Xij_d = zeros(k,k);
xij_d = zeros(k,k);
deltaij = zeros(k,k);
if verbosity, dispf('SHAPESPH calculate L correction matrix for all %d kernels (K) in %d dimensions...',k,d), end
% loop over all j for summation
for j=1:k
    % verbosity
    if verbosity
        if largek
            t_ = clock; %#ok<*CLOCK>
            if mod(j,10)==0 || (etime(t_,t1_)>0.5) %#ok<*DETIM> 
                t1_=t_;
                dt_ = etime(t_,t0_); done_ = j/k;
                screen = dispb(screen,'[K%d:%d] SHAPESPH | elapsed %0.1f s | done %0.1f %% | remaining %0.1f s', ...
                               j,k,dt_,100*done_,(1/done_-1)*dt_);
            end
        else
            dispf('... SHAPESPH respectively to kernel %d of %d',j,k);
        end
    end
    for i=1:k
        if i~=j
            Fi = vec2tensor(F(i,:));
            Xij(i,j,:) = X0(j,:) - X0(i,:);
            Xij_d(i,j) = sqrt(dot(Xij(i,j,:),Xij(i,j,:)));
            xij(i,j,:) = X(j,:) - X(i,:);
            xij_d(i,j) = sqrt(dot(xij(i,j,:),xij(i,j,:)));
            xij_i = Fi*(X0(j,:) - X0(i,:))';
            deltaij(i,j) = (xij_i' - (X(j,:) - X(i,:))) * xij_i / xij_d(i,j);
        end 
    end
end
for i = 1:k
    for j = 1:k
        if j~=i
            coef = - 0.5*config.alpha*V(i)*V(j)*W(Xij(i,j));
            fHG(i,:) = fHG(i,:) + squeeze(coef*config.E*(deltaij(i,j)+deltaij(j,i))*xij(i,j,:)/(Xij_d(i,j)^2*xij_d(i,j)))';
        end
    end
end

%% verbosity
if verbosity
    dispb(screen,'DEFRAGSPH %d L matrix calculated in %0.4g s',k,etime(clock,t0_));
end

% collect all outputs
description = struct(...
        'fHG','hourglass correction force'...
         );
out = struct( ...
    'k',k,'d',d,'V',V,'fHG',fHG,...
    'description',description,'engine','hourglassSPH','forcesilent',forcesilent);



