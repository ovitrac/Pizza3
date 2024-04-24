function out = shapeSPH(centers,gradW,V,config,forcesilent)
% SHAPESPH evaluate the solid shape matrix for each center according to Eq. 15 of Comput. Methods Appl. Mech. Engrg. 286 (2015) 87–106
%
%   Syntax:
%       out = shapeSPH(centers,gradW [, V, config, silent])
%
%   Inputs:
%         centers : kxd coordinates of the kernel centers
%           gradW : derivative kernel function @(r) <-- use kernelSPH() to supply a vectorized kernel
%               V : kx1 volume of the kernels (default=1)
%                   [] (empty matrix) or scalar value forces uniform volumes (default =1)
%           config: structure with fields coding for Lamé parameters (not used directly by shapeSPH)
%                   lambda (default = 30 000 Pa)
%                   mu (default = 3000 Pa)
%      forcesilent: flag to force silence mode (default = false)
%
%   Output: out structure with fields
%               L : k x d^2 shape matrix, where reshape(L(i,:),[d d]) is the dxd matrix respectively to kernel i
%            Linv : k x d^2 pseudo-inverse of L so that Linv * L = I
%  correctedgradW : k x d corrected gradient for each kernel (used by defgradSPH)
%    k,d,V,config : inputs
%          engine : 'shapeSPH'
%
%   Refer to Ganzenmuller (2015) for details: https://doi.org/10.1016/j.cma.2014.12.005
%   ~/han/biblio/Ganzenmuller2015-Hourglass_control_algorithm.pdf
%
%
%   See also: defgradSPH, interp2SPH, interp3SPH, kernelSPH, packSPH
%
%
%  
% 2023-10-31 | INRAE\Olivier Vitrac | rev. 2023-11-01


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
f= defgradout.f; fn=sqrt(sum(f.^2,2)); f = f./fn;
f90 = prctile(fn,90); fn(fn>f90) = f90; f = f .* f90;
quiver3(X(:,1),X(:,2),X(:,3),f(:,1),f(:,2),f(:,3))
%}

%Revision history
% 2023-10-31 alpha version
% 2023-11-01 collect all outputs and inputs into out, replace all reshapes by vec2tensor
% 2023-11-13 fixes, RC, example

% Default Lamé parameters
config_default = struct(...
    'lambda',3e4, ...first Lamé  parameter
    'mu',3e3 ... shear modulus (second Lamé parameterà
);

%% arg check
if nargin<1, centers = []; end
if nargin<2, gradW = []; end
if nargin<3, V = []; end
if nargin<4, config = []; end
if nargin<5, forcesilent = []; end
[k,d] = size(centers);
kv = length(V);
if k==0, error('please supply some centers'), end
if d>3, error('3 dimensions maximum'), end
if kv==0, V=1;  kv=1; end
if kv==1, V = ones(k,1)*V; kv=k; end
if kv~=k, error('the number of V values (%d) does not match the number of kernels (%d)',kv,k); end
if isempty(forcesilent), forcesilent = false; end
if isempty(config), config = config_default; end
for f = fieldnames(config_default)'
    if ~isfield(config,f{1}) || isempty(config.(f{1}))
        config.(f{1}) = config_default.(f{1});
    end
end

%% initialization
verbosity = (k>1e3) & ~forcesilent;
largek = k>200;
t0_ = clock; t1_=t0_; screen=''; 

% coding linearized outer product (https://en.wikipedia.org/wiki/Outer_product)
[left,right] = ndgrid(1:d,1:d);
outerproductindex = struct('u',left(:),'v',right(:));

% vec2tensor: indices to convert a vector to a 2D tensor (faster than many reshapes)
vec2tensor_reshape = reshape(1:d^2,d,d);
vec2tensor = @(x) x(vec2tensor_reshape);

%% Output correction/shape matrix: L
L = zeros(k,d*d,class(centers));
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
    % Correction shape matrix (accumulation over j, but computation for all i)
    Xij = centers(j,:)-centers; % j - all i
    Xij_d = sqrt(dot(Xij,Xij,2));
    Xij_n = Xij ./ Xij_d;
    gradWi = gradW(Xij_n).*Xij_n;
    gradWi(j,:) = 0;
    L = L + V(j) * Xij(:,outerproductindex.u).*gradWi(:,outerproductindex.v); % u and v are left and right indices with repetitions

end

%% output Linv (pseudo-inverse of L)
Linv = zeros(size(L),class(centers));
for i = 1:k
    if verbosity, screen = dispb(screen,'[K%d:%d] SHAPESPH, pseudoinverse...',i,k); end
    tmp = pinv(vec2tensor(L(i,:)));
    Linv(i,:) = tmp(:)';
end

%% output correctedgradW (Eq. 14)
correctedgradW = zeros(d,k,k);
for j = 1:k
    Xij = centers(j,:)-centers; % j - all i
    Xij_d = sqrt(dot(Xij,Xij,2));
    Xij_n = Xij ./ Xij_d;
    gradWi = gradW(Xij_n).*Xij_n;
    gradWi(j,:) = 0; % when i=j
    for i=1:k
        if verbosity, screen = dispb(screen,'[K%d:%d]-[K%d:%d] SHAPESPH, corrected gradient...',i,k,j,k); end
        correctedgradW(:,i,j) = vec2tensor(Linv(i,:))*gradWi(i,:)';
    end
end

%% verbosity
if verbosity
    dispb(screen,'SHAPESPH %d L matrix calculated in %0.4g s',k,etime(clock,t0_));
end

% collect outputs
out = struct('k',k,'d',d,'V',V,'config',config,...
    'L',L,'Linv',Linv,'correctedgradW',correctedgradW,...
    'engine','shapeSPH','forcesilent',forcesilent);