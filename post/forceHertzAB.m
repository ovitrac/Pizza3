function [FAB,nAB] = forceHertzAB(XA,XB,config,verbose)
%FORCEHERTZAB calculates Hertz contact forces between atoms A (coord XA) and B (coord B)
%
%   Syntax: FAB = forceHertzAB(XA,XB,config)
%           [FAB,nAB] = forceHertzAB(...)
%
%   Inputs:
%       XA: nA x 3 coordinates of atoms A
%       XB: nB x 3 coordinates of atoms B
%   config: 2x1 structure array with fields
%           R: radius
%           E: elasticity modulus
%           example: config = struct('R',{1 1},'E',{1e6 1e6})
%
%   Outputs (single output provided):
%       FAB: (nA*nB) x 3 Hertz forces
%
%   Outputs (two outputs provided):
%       FAB: (nA*nB) x 1 vector of force magnitudes
%       nAB: (nA*nB) x 3 coordinates of unitary direction vectors AB
%
%   TODO list
%       The code is vectorized and may generate an Overflow/OutOfMemory error
%       an iterative version with automatic switch must be implemented
%
%
%   See also: forceHertz, forceLandshoff


% MS 3.0 | 2023-03-25 | INRAE\Olivier.vitrac@agroparistech.fr | rev.

% Revision history
% 2023-04-02 rename forceHertz into forceHertzAB, to avoid the confusion with the new forceHertz
% 2023-04-03 WJ. update the force Hertz equation to that as set in the SMD source code of LAMMPS:
%            lammps-2022-10-04/src/MACHDYN/pair_smd_hertz.cpp ln. 169
% 2023-04-03 WJ. add an additional delta calculation step
% 2023-04-03 WJ. wrap particles along the x direction



%% Check arguments
if nargin<3, error('3 inputs are required: [FAB,nAB] = forceHertz(XA,XB,config)'), end
if nargin<4, verbose = []; end
if ~isstruct(config), error('config must be a structure'), end
if ~isfield(config,'R'), error('the field R is missing'), end
if ~isfield(config,'E'), error('the field E is missing'), end
if length(config)==1, config = repmat(config,[2,1]); end
if length(config)~=2, error('config must be a 2x1 structure array'), end
[nA,dA] = size(XA);
[nB,dB] = size(XB);
if dA ~= dB, error('the number of dimensions of XA (%d) and XB (%d) are not compatible',dA,dB), end
if dA~=3 || dB~=3, warning('the number of dimensions (%d) are not standard',dA), end
verbosedefault = nA * nB>1e7;
if isempty(verbose), verbose = verbosedefault; end

%% Evaluate all AB vectors (full vectorized code)
% all B-A combinations are calculated
% note that the classes are preserved (single is recommended)
if verbose
    t0 = clock; %#ok<CLOCK> 
    dispf('Calculate Hertz contact forces between [%d x %d] and [%d x %d] atoms...',nA,dA,nB,dB)
end
AB = reshape(   bsxfun(@minus,... the operation B-A is done within the builtin bsxfun
                reshape(XB,1,nB,dB),...  B values are placed column-wise
                reshape(XA,nA,1,dA)),... A values are placed row-wise
                nA*nB,3); % note that bsxfun will expand implicitely dimensions 1 and 2
% wrap coordinates at the edges of the 2 mm box
iswrapcontactpositive = AB(:,1)>0.002-(config(1).R + config(2).R);
iswrapcontactnegative = AB(:,1)<-0.002+(config(1).R + config(2).R);
ABwrappositive = AB(iswrapcontactpositive,:);
ABwrappositive(:,1) = ABwrappositive(:,1) - 0.002;
ABwrapnegative = AB(iswrapcontactnegative,:);
ABwrapnegative(:,1) = ABwrapnegative(:,1) + 0.002;
AB = vertcat(AB, ABwrappositive);
AB = vertcat(AB, ABwrapnegative);
rAB = sqrt(sum(AB.^2,2)); % distances AB
AB = AB./rAB; % normalized vectors
% n.b. data for the simulation box needed for a more generic wrap implementation

%% Evaluated forces
E = sqrt(config(1).E*config(2).E); % Bertholet formula
rcut = config(1).R + config(2).R;  % cut distance
FAB = zeros(length(AB),1,class(AB));    % preallocate
iscontact = rAB<rcut;               % true if contact, false otherwise
% formula as set in the slide of Billy
% FAB(iscontact) = E * sqrt((rcut-rAB(iscontact))*config(1).R*config(2).R/rcut);
% formula as set in the SMD source code of LAMMPS: lammps-2022-10-04/src/MACHDYN/pair_smd_hertz.cpp ln. 169
delta = rcut-rAB(iscontact);
r_geom = config(1).R*config(2).R/rcut;
bulkmodulus = E/(3*(1-2*0.25));
FAB(iscontact) = 1.066666667 * bulkmodulus * delta .* sqrt(delta * r_geom); % units N

%% Output management
if nargout>1
    nAB = AB;
else
    FAB = FAB .* AB;
end
if verbose
    dispf('\t ... done in %0.3g s',etime(clock,t0)) %#ok<DETIM,CLOCK>
end
