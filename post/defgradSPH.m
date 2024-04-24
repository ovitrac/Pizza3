function out = defgradSPH(u,correctedgradW,V,config,forcesilent)
%DEFGRAD calculates the solid deformation gradient using the displacement field u according to Eq. 17-24 of Comput. Methods Appl. Mech. Engrg. 286 (2015) 87–106
%
%   Syntax:
%       out = defgradSPH(u,shapeSPHout)  <--- syntax 1 (preferred)
%       out = defgradSPH(u,correctedgradW [,V, config, silent])  <--- syntax 2
%
%   Inputs: (syntax 1)
%               u : kxd displacement field of the kernel centers
%     shapeSPHout : ouput (structure) of shapeSPH
%
%   Inputs: (syntax 2)
%               u : kxd displacement field of the kernel centers
%  correctedgradW : 3xkxk corrected kernel gradient (reference frame), calculated with shapeSPH (3rd output)
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
%          engine : 'defragSPH'
%
%   Refer to Ganzenmuller (2015) for details: https://doi.org/10.1016/j.cma.2014.12.005
%   ~/han/biblio/Ganzenmuller2015-Hourglass_control_algorithm.pdf
%
%
%   See also: shapeSPH, interp2SPH, interp3SPH, kernelSPH, packSPH
%

% 2023-10-31 | INRAE\Olivier Vitrac | rev. 2023-11-01


%{
% Example:
r = 0.5;
X0 = packSPH(10,r);
X0(sqrt(sum((X0-mean(X0,1)).^2,2))>10*r,:) = [];
% deformation (vertical compression + shearing)
Xc = mean(X0,1); Xmin = min(X0,[],1); Xmax = max(X0,[],1)
% compression along z, with support at zmin, compression rate = 20%
X = X0; X(:,3) = 0.8*(X(:,3)-Xmin(1,3)) + Xmin(1,3);
% shearing 20% along y
X(:,2) = X(:,2) + 0.2 * (Xmax(1,2)-Xmin(1,2)) * (X(:,3)-Xmin(1,3))/(Xmax(1,3)-Xmin(1,3));
% displacement
u = X-X0;
% shape matrix
gradW = kernelSPH(2*r,'lucyder',3);
shapeout = shapeSPH(X0,gradW)
% calculates stresses and forces
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
% 2023-11-01 collect all outputs and inputs into out, add f and G
% 2023-11-13 fixes, RC, full example

% Default Lamé parameters
config_default = struct(...
    'lambda',3e4, ...first Lamé  parameter
    'mu',3e3 ... shear modulus (second Lamé parameterà
);

%% arg check
if nargin<2, error('2 arguments are required at least'), end
[k,d] = size(u); if k==0, error('please supply some displacements centers'), end
if isstruct(correctedgradW) && strcmpi(correctedgradW.engine,'shapeSPH') % -- syntax 1: we reuse the arguments of shapeSPH
    args = correctedgradW;
    if (args.d~=d) || (args.k~=k), error('%dx%d u is not compatible with previous %dx%d centers',k,d,args.k,args.d), end
    correctedgradW = args.correctedgradW;
    V = args.V;
    config = args.config;
    forcesilent = args.forcesilent;
    if nargin>2, warning('extra arguments are ignored with syntax 1 (defragSPH)'); end
else % -- syntax 2
    if nargin<3, V = []; end
    if nargin<4, config = []; end
    if nargin<5, forcesilent = []; end
    if ~isnumeric(correctedgradW) || ndims(correctedgradW)~=3, error('correctedgradW should be evaluated with shape SPH (3rd output)'), end
    if d>3, error('3 dimensions maximum'), end
    [dW,k1W,k2W] = size(correctedgradW);
    if k1W~=k2W, error('%dx%dx%d correctedgradW is not consistent, dim 2 and dim 3 should be equal',k1W,k2W); end
    if dW~=d, error('%dx%dx%d correctedgradW has not the same number of dimensions (%d) than u (%d)',dW,k1W,k2W,dW,d); end
    kv = length(V);
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
end

%% initialization
verbosity = (k>1e3) & ~forcesilent;
largek = k>200;
t0_ = clock; t1_=t0_; screen=''; 

% coding linearized outer product (https://en.wikipedia.org/wiki/Outer_product)
[left,right] = ndgrid(1:d,1:d);
outerproductindex = struct('u',left(:),'v',right(:)); % u and n are notations of wiki, not related to displacements

% vec2tensor: indices to convert a vector to a 2D tensor (faster than many reshapes)
vec2tensor_reshape = reshape(1:d^2,d,d);
vec2tensor = @(x) x(vec2tensor_reshape);

%% output F (deformation gradient)
% loop over all j for summation
I = eye(d,class(u));
F = repmat(I(:)',k,1); % we initialize to identity (see Eqs. 17 and 6 F = I + du/dX)
if verbosity, dispf('DEFRAGSPH calculates the deformation gradient for all %d kernels (K) in %d dimensions...',k,d), end
for j=1:k
    % verbosity
    if verbosity
        if largek
            t_ = clock; %#ok<*CLOCK>
            if mod(j,10)==0 || (etime(t_,t1_)>0.5) %#ok<*DETIM> 
                t1_=t_;
                dt_ = etime(t_,t0_); done_ = j/k;
                screen = dispb(screen,'[K%d:%d] DEFRAGSPH | elapsed %0.1f s | done %0.1f %% | remaining %0.1f s', ...
                               j,k,dt_,100*done_,(1/done_-1)*dt_);
            end
        else
            dispf('... DEFRAGSPH - deformation gradient - respectively to kernel %d of %d',j,k);
        end
    end
    % Deformation gradient for atom i due to j
    uij = u(j,:)-u; % j - all i
    for i=1:k
        % Eq. 17, noticing that I is the initial value (no need to add it)
        % u and v are left and right indices with repetitions
        F(i,:) = F(i,:) + V(j) * uij(i,outerproductindex.u).*correctedgradW(outerproductindex.v,i,j)';
    end
end


%% output C (Cauchy-Green deformation tensor)
C = zeros(size(F),class(u));
for i = 1:k
    if verbosity, screen = dispb(screen,'[K%d:%d] DEFRAGSPH, Cauchy-Green tensor...',i,k); end
    Fi = vec2tensor(F(i,:));
    tmp = Fi'*Fi;
    C(i,:) = tmp(:)';
end

%% output E (Green-Lagrange strain)
E = 0.5 * (C - repmat(I(:)',k,1)); % Eq. 18

%% output S (Cauchy stress tensor)
% trace operator is replaced by a sum along dim 2 for indices 1, d+2, 2*d+3
S = config.lambda * sum(E(:,1:d+1:end),2) + 2 * config.mu * E; %Eq. 19 config.lambda*tr(E)+2*config.mu*E

%% output P (first Piola-Kirchoff stress)
P = zeros(size(F),class(u));
for i = 1:k
    if verbosity, screen = dispb(screen,'[K%d:%d] DEFRAGSPH, first Piola-Kirchoff stress tensor...',i,k); end
    tmp = vec2tensor(F(i,:))*vec2tensor(S(i,:));
    P(i,:) = tmp(:)';
end

%% output f (pairwise forces) - Eq. 24
% initialization
f = zeros(k,d,class(u));
% summation loop
for j=1:k
    if verbosity, screen = dispb(screen,'[K%d:%d] DEFRAGSPH, summation pairwise forces...',i,k); end
    Pj = vec2tensor(P(j,:));
    % kernel loop
    for i=1:k
        Pi = vec2tensor(P(i,:));
        f(i,:) = f(i,:) +  ...: means x,y,z
            ( V(i)*V(j)*(Pi*correctedgradW(:,i,j)-Pj*correctedgradW(:,j,i)) )';
    end
end

%% output G (von Mises stress)
if d==3
    % https://en.wikipedia.org/wiki/Von_Mises_yield_criterion
    % https://www.continuummechanics.org/vonmisesstress.html
    [ij11,ij22,ij33,ij23,ij31,ij12] = deal(1,5,9,8,3,2); % indices 11,22,33,12,31,12 as (i,j)
    G = sqrt(0.5*( ...
        (S(:,ij11)-S(:,ij22)).^2+...
        (S(:,ij22)-S(:,ij33)).^2+...
        (S(:,ij33)-S(:,ij11)).^2+...
        6 * (S(:,ij23).^2+S(:,ij31).^2+S(:,ij12).^2) ...
        ));
elseif d==2
    % https://www.omnicalculator.com/physics/von-mises-stress
    [ij11,ij22,ij12] = deal(1,4,2); % indices 11,22,12 as (i,j)
    G = sqrt(...
        S(:,ij11).^2 -...
        S(:,ij11).*S(:,ij22) + ...
        S(:,ij22).^2 +...
        6 * S(:,ij12).^2 ...
        );
end

%% verbosity
if verbosity
    dispb(screen,'DEFRAGSPH %d L matrix calculated in %0.4g s',k,etime(clock,t0_));
end

% collect all outputs
description = struct(...
        'F','deformation gradient',...
        'C','Cauchy-Green deformation tensor',...
        'E','Green-Lagrange strain',...
        'S','Cauchy stress tensor',...
        'P','first Piola-Kirchoff stress', ...
        'f','pairwise forces, so-called nodal forces', ...
        'G','von Mises stress' ...
         );
out = struct( ...
    'k',k,'d',d,'V',V,'correctedgradW',correctedgradW,'config',config,...
    'F',F,'C',C,'E',E,'S',S,'P',P,'f',f,'G',G, ...
    'description',description,'engine','defragSPH','forcesilent',forcesilent);