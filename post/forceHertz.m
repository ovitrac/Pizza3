function [F,Wout,nout] = forceHertz(X,V,config,verbose)
%FORCEHERTZ calculates Hertz contact forces for all atoms assuming that the Verlist list V has been partitioned (coord X)
%
%   Syntax: F = forceHertz(X,[,V,config,verbose])
%           [F,W,n] = forceHertz()
%
%   Inputs
%        X: nX x 3 coordinates of atoms
%        V: nX x 1 cell array (output of partitionVerletList)
%           a partition is required
%           V{i} should include all atoms which are not of the same type of i
%   config: 2x1 structure array with fields
%           R: radius
%           E: elasticity modulus
%         rho: density
%           m: mass of the bead
%
%           example: config = struct('R',{1 1},'E',{1e6 1e6})
%
%   Output (single output provided):
%       F: nX x 3 vector of Hertz forces
%            with F{i} = mi x 3 forces
%
%   Outputs (two outputs provided):
%       F: nX x 1 Hertz force magnitudes
%       W: nX x 9 virial stress tensor (use reshape(W(i),3,3) to recover the matrix)
%       n: nX x 3 normal vectors

% MS 3.0 | 2023-04-02 | INRAE\Olivier.vitrac@agroparistech.fr | rev. 2023-09-07 

% Revision history
% 2023-04-02 rename forceHertz into forceHertzAB, to avoid the confusion with the new forceHertz
% 2023-04-03 WJ. update the force Hertz equation to that as set in the SMD source code of LAMMPS:
%            lammps-2022-10-04/src/MACHDYN/pair_smd_hertz.cpp ln. 169
% 2023-04-03 WJ. add an additional delta calculation step
% 2023-09-07 add W (virial stress)
% 2023-09-09 local virial stress fixed to match https://doi.org/10.1016/j.cplett.2019.07.008


%% Check arguments
if nargin<1, X = []; end
if nargin<2, V = []; end
if isempty(X), error('one table is at least required with ''x'',''y'',''z'',''type'' columns'), end
if istable(X)
    typ = X.type;
    X = table2array(X(:,{'x','y','z'}));
    if isempty(V)
        V =  partitionVerletList(buildVerletList(X),typ);
    end
end
if nargin<3, config = []; end
if nargin<4, verbose = []; end
if isnumeric(V) && ~isnan(V) && length(V)==1
    error('a partioned Verletlist is required');
end
if ~isstruct(config), error('config must be a structure'), end
if ~isfield(config,'R'), error('the field R is missing'), end
if ~isfield(config,'E'), error('the field E is missing'), end
if length(config)==1, config = repmat(config,[2,1]); end
if length(config)~=2, error('config must be a 2x1 structure array'), end
[nX,dX] = size(X);
if length(V)~=nX, error('V must be a %d cell array created with buildVerletList()',nX), end
verbosedefault = nX > 1e7;
if isempty(verbose), verbose = verbosedefault; end
askvirialstress = (nargout==2);

if askvirialstress
    if ~isfield(config,'rho'), error('the field rho is missing'), end
    if ~isfield(config,'m'), error('the field m is missing'), end
    if ~isfield(config,'h'), error('the field h is missing'), end
    volmin = mean([config.m],'omitnan')/mean([config.rho],'omitnan');
    hmean = mean([config.h],'omitnan');
    vol = 4/3 * pi * hmean^3;
    if vol<volmin
        error('the value of h (%0.4g) leads to a volume smaller than atoms (%0.4g)',hmean,volmin)
    end
end

%% verbosity
if verbose
    t0 = clock; %#ok<CLOCK> 
    dispf('Calculate Hertz contact forces between [%d x %d] atoms...',nX,dX)
end

%% Evaluate forces

% parameters
E = sqrt(config(1).E*config(2).E); % Bertholet formula
rcut = config(1).R + config(2).R; 

% allocate
classX = class(X);
F = zeros(nX,1,classX);
n = zeros(nX,dX,classX);

% for virial stress calculation;

if askvirialstress
    W = zeros(nX,dX*dX,classX);
else
    W = [];
end
stresstensor = zeros(dX,dX,classX);

% for all atoms
for i=1:nX
    j = V{i}; % neighbors of i
    if any(j) % if any neighbor of other type
        rij = X(i,:) - X(j,:);    % position vector j->i
        rij2 = dot(rij,rij,2);    % dot(rij,rij,2)
        rij_d = sqrt(rij2);       % norm
        rij_n = rij ./ rij_d;     % normalized vector
        iscontact = rij_d < rcut;
        stresstensor(:) = 0;
        if any(iscontact) % if they are contact
            %Fij = E * sqrt((rcut-rij_d(iscontact))*config(1).R*config(2).R/rcut) .* rij_n(iscontact,:);
            % formula as set in the SMD source code of LAMMPS: lammps-2022-10-04/src/MACHDYN/pair_smd_hertz.cpp ln. 169
            delta = rcut-rij_d(iscontact);
            r_geom = config(1).R*config(2).R/rcut;
            bulkmodulus = E/(3*(1-2*0.25));
            Fij = 1.066666667 * bulkmodulus * delta .* sqrt(delta * r_geom).* rij_n(iscontact,:); % units N
            Fbalance = sum(Fij,1);
            F(i) = norm(Fbalance);
            n(i,:) = Fbalance/F(i);
            if askvirialstress
                stresstensor(:) = 0;
                for ineigh = 1:length(find(iscontact))
                    % -rij' * Fij is the outerproduct (source: doi:10.1016/j.ijsolstr.2008.03.016)
                    stresstensor = stresstensor - ( rij(ineigh,:)' * Fij(ineigh,:) ) /vol;
                end
                W(i,:) = stresstensor(:)';
            end
        else
            n(i,:) = sum(rij_n,1);
        end
    end % if any neighbor of other type
end


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
