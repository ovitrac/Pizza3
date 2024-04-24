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
%          rho: density (default value based on X.c_rho_smd if X is a table, 1000 otherwise)
%         mass: mass of the bead (default value based on X.mass if X is a table, 1 otherwise)
%          vol: volume of the bead (default value based on X.c_vol if X is a table, 1 otherwise)
%
%   Output (single output provided):
%       F: nX x 3 vector of Landshoff forces
%            with F{i} = mi x 3 forces
%
%   Outputs (two outputs provided):
%       F: nX x 1 Landshoff force magnitudes
%       W: nX x 9 virial stress tensor (use reshape(W(i),3,3) to recover the matrix)
%       n: nX x 3 normal vectors

% MS 3.0 | 2023-03-31 | INRAE\Olivier.vitrac@agroparistech.fr | rev. 2024-03-30

% Revision history
% 2023-04-01 sum forces instead of individual ones,accept X as a table
% 2023-04-02 fix summation bug 
% 2023-09-04 add m, fix config fields check
% 2023-09-07 add W (virial stress)
% 2023-09-09 local virial stress fixed to match https://doi.org/10.1016/j.cplett.2019.07.008
% 2023-09-09 code acceleration
% 2023-09-11 prevent NaN if the norm is 0 
% 2023-09-12 fix m^2 (ma*mb) instead of mb
% 2023-09-13 upgrade rho, mass, vol from X as a table, adhere to scheme from SPH_virial_stress in Billy's thesis
% 2024-03-30 small control comments by OV

%% Default
h_default = 60e-6; % rough guess (to be adjusted with common value)
config_default = struct( ...real dynamic viscosity: q1 * h * c0 * rho / 8 (2D) or 10 (3D) see Eq. 8.8 Monaghan, J. J. (2005). Smoothed particle hydrodynamics. Reports on Progress in Physics, 68(8), 1703–1759. doi:10.1088/0034-4885/68/8/r01 
   'gradkernel', kernelSPH(h_default,'lucyder',3),...% kernel gradient (note that h is bound with the kernel)
            'h', h_default,...smoothing length
           'c0',10,...        speed of the sound
           'q1',1,...         constant
          'rho', 1000, ...    fluid density
         'mass', 1,...        bead weight
          'vol', 1, ...       bead volume (uniquely for virial stress)
'repulsiononly', false ...    if true, only Landshoff forces when dot(rij,vij)<0
    );
askvirialstress = (nargout==2);

%% Check arguments
if nargin<1, X = []; end
if nargin<2, vX = []; end
if isempty(X), error('one table is at least required with ''x'',''y'',''z'',''vx'',''vy'',vz'' columns'), end
if istable(X)
    if isempty(vX), vX = X{:,{'vx','vy','vz'}}; end
    config_default.mass = X.mass;
    config_default.vol = X.c_vol;
    config_default.rho = X.c_rho_smd;
    X = X{:,{'x','y','z'}};
end
classX = class(X);
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
for f = {'mass','rho','vol'}
    if numel(config.(f{1}))==1, config.(f{1})= config.(f{1})* ones(nX,1,classX); end
    if ~isa(config.(f{1}),classX), config.(f{1})= cast(config.(f{1}),classX); end
end
if length(V)~=nX, error('V must be a %d cell array created with buildVerletList()',nX), end
verbosedefault = nX > 1e2;
if isempty(verbose), verbose = verbosedefault; end


%% verbosity
if verbose
    t0_ = clock; %#ok<CLOCK> 
    t1_ = t0_;
    screen = '';
    if askvirialstress
        dispf('Calculate Landshoff forces + virial stress between [%d x %d] ATOMS...',nX,dX)
    else
        dispf('Calculate Landshoff forces between [%d x %d] ATOMS...',nX,dX)
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
F = zeros(nX,1,classX);
n = zeros(nX,dX,classX);

% for virial stress calculation
% volmin = config.m/config.rho; % depreciated
% vol = 4/3 * pi * config.h^3;  % depreciated
if askvirialstress
    W = zeros(nX,dX*dX,classX);
    %if vol<volmin, error('the value of h (%0.4g) leads to a volume smaller than atoms (%0.4g)',config.h,volmin), end
else
    W = [];
end
stresstensor = zeros(dX,dX,classX);

% for all atoms
% reference formula https://docs.lammps.org/PDF/SPH_LAMMPS_userguide.pdf (page 7, Eqs 18, 19)
q1c0h = config.q1 * config.c0 * config.h; % q1 * c0 * h
epsh = 0.01*config.h^2;   % tolreance
dmin = 0.1 * config.h;    % minimim distance for Landshoff

for i=1:nX

    j = V{i}; % neighbors of i
    mi = config.mass(i);
    rhoi = config.rho(i);
    rij = X(i,:) - X(j,:);    % position vector j->i
    rij2 = dot(rij,rij,2);    % dot(rij,rij,2)
    rij_d = sqrt(rij2);       % norm
    rij_n = rij ./ rij_d;     % normalized vector
    vij = vX(i,:) - vX(j,:);  % relative velocity of i respectively to j
    rvij = dot( rij, vij, 2); % projected velocity
    ok = rij_d>dmin;          % added on 2023-09-13
    if config.repulsiononly, ok = ok & (rvij<0); end
    if any(ok)
        % Reference Formulation - p1740 of Rep. Prog. Phys. 68 (2005) 1703–1759 (attention acceleration, not force)
        % http://dx.doi.org/10.1088/0034-4885/68/8/R01
        % before 2023-09-09
        %muij = config.h * rvij(ok) ./ ( rij2(ok) + 0.01*config.h^2 );
        %nuij = (1/config.rho) * (-config.q1 * config.c0 * muij);
        %Fij = - config.m^2 * nuij .* config.gradkernel(rij_d(ok)) .* rij_n(ok,:);
        % after 2023-09-09
        mj = config.mass(j(ok));
        rhoj = config.rho(j(ok));
        rhoij = 0.5 * (rhoi+rhoj);
        muij = rvij(ok) ./ ( rij2(ok) + epsh );
        Fij = q1c0h * mi * mj./rhoij .* muij .* config.gradkernel(rij_d(ok)) .* rij_n(ok,:);
        Fbalance = sum(Fij,1);
        F(i) = norm(Fbalance);
        if F(i)>0, n(i,:) = Fbalance/F(i); end
        if askvirialstress
            stresstensor(:) = 0;
            for ineigh = 1:length(find(ok))
                % -rij' * Fij is the outerproduct (source: doi:10.1016/j.ijsolstr.2008.03.016)
                stresstensor = stresstensor -rij(ineigh,:)' * Fij(ineigh,:);
            end
            W(i,:) = stresstensor(:)' / (2*config.vol(i)); % origin of 2 ?? in this case (since j-->i not considered)
        end
    else
        n(i,:) = sum(rij_n,1);
    end % if any(ok)

    % verbosity
    t_ = clock; %#ok<CLOCK>
    if verbose && (mod(i,1000)==0 || (etime(t_,t1_)>0.5))  %#ok<*DETIM>
        t1_=t_; dt_ = etime(t_,t0_); done_ = i/nX;
        screen = dispb(screen,'[atom %d:%d] FORCE Landshoff | elapsed %0.1f s | done %0.1f %% | remaining %0.1f s', ...
                               i,nX,dt_,100*done_,(1/done_-1)*dt_);
    end
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
        dispb(screen,'\t ... done with virial stress in %0.3g s for %d atoms',etime(clock,t0_),nX); %#ok<CLOCK>
    else
        dispf(screen,'\t ... done in %0.3g s for %d ATOMS',etime(clock,t0_),nX); %#ok<CLOCK>
    end
end
