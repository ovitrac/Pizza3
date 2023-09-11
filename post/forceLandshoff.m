function [F,Wout,nout] = forceLandshoff(X,vX,V,config,verbose)
%FORCELANDSHOFF calculates Landshoff forces between fluid atoms (coord X, Verlist list V)
%
%   Syntax: F = forceLandshoff(X,vX [,V,config,verbose])
%           [F,W,n] = forceLandshoff()
%
%   Inputs
%        X: nX x 3 coordinates of atoms
%       vX: nX x 3 velocity components
%        V: nX x 1 cell array (output of buildVerletList)
%           with V{i} = 1 x mi index of neighbors (mi = number of neighbors within the cutoff distance)
%   config: structure with fields
%   gradkernel: gradient kernel (default value = kernelSPH(h,'lucyder',3))
%               it anonymous function depending only the radial distance r @(r)...., not on h
%            h: smoothing length
%           c0: speed of the sound
%           q1: q1 coefficient
%          rho: density
%            m: mass of the bead
%
%   Output (single output provided):
%       F: nX x 3 vector of Landshoff forces
%            with F{i} = mi x 3 forces
%
%   Outputs (two outputs provided):
%       F: nX x 1 Landshoff force magnitudes
%       W: nX x 9 virial stress tensor (use reshape(W(i),3,3) to recover the matrix)
%       n: nX x 3 normal vectors

% MS 3.0 | 2023-03-31 | INRAE\Olivier.vitrac@agroparistech.fr | rev. 2023-09-07

% Revision history
% 2023-04-01 sum forces instead of individual ones,accept X as a table
% 2023-04-02 fix summation bug 
% 2023-09-04 add m, fix config fields check
% 2023-09-07 add W (virial stress)
% 2023-09-09 local virial stress fixed to match https://doi.org/10.1016/j.cplett.2019.07.008
% 2023-09-09 code acceleration

%% Default
h_default = 60e-6; % rough guess (to be adjusted with common value)
config_default = struct( ...real dynamic viscosity: q1 * h * c0 / 8 (2D) or 10 (3D)
   'gradkernel', kernelSPH(h_default,'lucyder',3),...% kernel gradient (note that h is bound with the kernel)
            'h', h_default,...smoothing length
           'c0',10,...        speed of the sound
           'q1',1,...         constant
          'rho', 1000, ...    fluid density
            'm', 1  ...       bead weight
    );
askvirialstress = (nargout==2);

%% Check arguments
if nargin<1, X = []; end
if nargin<2, vX = []; end
if isempty(X), error('one table is at least required with ''x'',''y'',''z'',''vx'',''vy'',vz'' columns'), end
if istable(X)
    if isempty(vX), vX = X{:,{'vx','vy','vz'}}; end
    X = X{:,{'x','y','z'}};
end
if isempty(vX), error('2 inputs are required: [F,n] = forceHertz(X,vX)'), end
if nargin<3, V = []; end
if nargin<4, config = []; end
if nargin<5, verbose = []; end
if isempty(V), V =  buildVerletList(X); end
if isnumeric(V) && ~isnan(V) && length(V)==1, V = buildVerletList(frame,V); end
if isempty(config), config = config_default; end
for f = fieldnames(config_default)'
    if ~isfield(config,f{1}) || isempty(config.(f{1}))
        config.(f{1}) = config_default.(f{1});
    end
end
[nX,dX] = size(X);
if (size(vX,1)~=nX) || (size(vX,2)~=dX), error('vX should be a %d x %d array',nX,dX), end
if length(V)~=nX, error('V must be a %d cell array created with buildVerletList()',nX), end
verbosedefault = nX > 1e2;
if isempty(verbose), verbose = verbosedefault; end


%% verbosity
if verbose
    t0 = clock; %#ok<CLOCK> 
    if askvirialstress
        dispf('Calculate Landshoff forces + virial stress between [%d x %d] atoms...',nX,dX)
    else
        dispf('Calculate Landshoff forces between [%d x %d] atoms...',nX,dX)
    end
end

%% Evaluate forces (and stresses)
% the code is highly vectorized and use only one for loop on primary atoms
% In the case of shock tube problems, it is usual to turn the viscosity 
% on for approaching particles and turn it off for receding particles. 
% In this way, the viscosity is used for shocks and not rarefactions.
% after Monaghan (2005), p 1741
% Source: https://cg.informatik.uni-freiburg.de/intern/seminar/animation%20-%20SPH%20survey%20-%202005.pdf

% allocate
classX = class(X);
F = zeros(nX,1,classX);
n = zeros(nX,dX,classX);

% for virial stress calculation
volmin = config.m/config.rho;
vol = 4/3 * pi * config.h^3;
if askvirialstress
    W = zeros(nX,dX*dX,classX);
    if vol<volmin
        error('the value of h (%0.4g) leads to a volume smaller than atoms (%0.4g)',config.h,volmin)
    end
else
    W = [];
end
stresstensor = zeros(dX,dX,classX);

% for all atoms
prefactor = (config.m/config.rho) * config.q1 * config.c0 * config.h;
epsh = 0.01*config.h^2;
for i=1:nX
    j = V{i}; % neighbors of i
    rij = X(i,:) - X(j,:);    % position vector j->i
    rij2 = dot(rij,rij,2);    % dot(rij,rij,2)
    rij_d = sqrt(rij2);       % norm
    rij_n = rij ./ rij_d;     % normalized vector
    vij = vX(i,:) - vX(j,:);  % relative velocity of i respectively to j
    rvij = dot( rij, vij, 2); % projected velocity
    ok = rvij<0;
    if any(ok)
        % Reference Formulation - p1740 of Rep. Prog. Phys. 68 (2005) 1703–1759
        % http://dx.doi.org/10.1088/0034-4885/68/8/R01
        % before 2023-09-09
        %muij = config.h * rvij(ok) ./ ( rij2(ok) + 0.01*config.h^2 );
        %nuij = (1/config.rho) * (-config.q1 * config.c0 * muij);
        %Fij = - config.m * nuij .* config.gradkernel(rij_d(ok)) .* rij_n(ok,:);
        % after 2023-09-09
        muij = rvij(ok) ./ ( rij2(ok) + epsh );
        Fij = prefactor * muij .* config.gradkernel(rij_d(ok)) .* rij_n(ok,:);
        Fbalance = sum(Fij,1);
        F(i) = norm(Fbalance);
        n(i,:) = Fbalance/F(i);
        if askvirialstress
            stresstensor(:) = 0;
            for ineigh = 1:length(find(ok))
                % -rij' * Fij is the outerproduct (source: doi:10.1016/j.ijsolstr.2008.03.016)
                stresstensor = stresstensor - ( rij(ineigh,:)' * Fij(ineigh,:) )/vol;
            end
            W(i,:) = stresstensor(:)';
        end
    else
        n(i,:) = sum(rij_n,1);
    end % if any(ok)
end % next i


%% outputs
if nargout>1, Wout = W; end
if nargout>2
    nout = n;
else
    F = F .* n;
end


%% verbosity
if verbose
    if askvirialstress
        dispf('\t ... done with virial stress in %0.3g s',etime(clock,t0)) %#ok<DETIM,CLOCK>
    else
        dispf('\t ... done in %0.3g s',etime(clock,t0)) %#ok<DETIM,CLOCK>
    end
end
