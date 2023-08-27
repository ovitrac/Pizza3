function [F,nout] = forceLandshoff(X,vX,V,config,verbose)
%FORCELANDSHOFF calculates Landshoff forces between fluid atoms (coord X, Verlist list V)
%
%   Syntax: F = forceLandshoff(X,vX [,V,config,verbose])
%           [F,n] = forceLandshoff()
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
%
%   Output (single output provided):
%       F: nX x 3 vector of Landshoff forces
%            with F{i} = mi x 3 forces
%
%   Outputs (two outputs provided):
%       F: nX x 1 Landshoff force magnitudes
%       n: nX x 3 normal vectors

% MS 3.0 | 2023-03-31 | INRAE\Olivier.vitrac@agroparistech.fr | rev. 2023-04-01

% Revision history
% 2023-04-01 sum forces instead of individual ones,accept X as a table
% 2023-04-02 fix summation bug 

%% Default
h_default = 60e-6; % rough guess (to be adjusted with common value)
config_default = struct( ...
   'gradkernel', kernelSPH(h_default,'lucyder',3),...
            'h', h_default,...
           'c0',10,...
           'q1',1,...
          'rho', 1000 ...
    );

%% Check arguments
if nargin<1, X = []; end
if nargin<2, vX = []; end
if isempty(X), error('one table is at least required with ''x'',''y'',''z'',''vx'',''vy'',vz'' columns'), end
if istable(X)
    if isempty(vX), vX = table2array(X(:,{'vx','vy','vz'})); end
    X = table2array(X(:,{'x','y','z'}));
end
if isempty(vX), error('2 inputs are required: [F,n] = forceHertz(X,vX)'), end
if nargin<3, V = []; end
if nargin<4, config = []; end
if nargin<5, verbose = []; end
if isempty(V), V =  buildVerletList(X); end
if isnumeric(V) && ~isnan(V) && length(V)==1, V = buildVerletList(frame,V); end
if isempty(config), config = config_default; end
for f = fieldnames(config)'
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
    dispf('Calculate Landshoff forces between [%d x %d] atoms...',nX,dX)
end

%% Evaluate forces
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

% for all atoms
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
        muij = config.h * rvij(ok) ./ ( rij2(ok) + 0.01*config.h^2 );
        nuij = (1/config.rho) * (-config.q1 * config.c0 * muij);
        Fij = - nuij .* config.gradkernel(rij_d(ok)) .* rij_n(ok,:);
        Fbalance = sum(Fij,1);
        F(i) = norm(Fbalance);
        n(i,:) = Fbalance/F(i);
    else
        n(i,:) = sum(rij_n,1);
    end
end


%% outputs
if nargout>1
    nout = n;
else
    F = F .* n;
end


%% verbosity
if verbose
    dispf('\t ... done in %0.3g s',etime(clock,t0)) %#ok<DETIM,CLOCK>
end
