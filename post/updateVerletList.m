function [verletList,configout] = updateVerletList(X, previousVerletList, config)
%UPDATEVERLETLIST update the verlet list if the number of sampled modified neighbors exceed a threshold
%
%   Syntax: [verletList,configout] = updateVerletList(X, previousVerletList, config)
%
%   Inputs:
%                   X: n x 3 updated X
%  previousVerletList: n x 1 cell array corresponding to the previous list
%              config: output of buildVerletList
%                   config.tolerance set the tolerance
%                   config.nsamples set the number of samples
%
%   Outputs:
%         verletList: n x 1 cell coding for the verletList
%             config: configuration structure to be used with updateVerletList()
%
%
%   See also: buildVerletList, partitionVerletList, selfVerletList, interp3SPHVerlet


% MS 3.0 | 2023-04-01 | INRAE\Olivier.vitrac@agroparistech.fr | rev. 2023-05-17

% Revision history
% 2023-05-17 updated help



%% Check arguments
if nargin<3, error('three arguments are reqiured: [verletList,configout] = updateVerletList(X, previousVerletList, config)'), end
if istable(X), X = table2array(X(:,{'x','y','z'})); end
[n,d] = size(X); % number of particless
typ = class(X);  % class of coordinates
if ~iscell(previousVerletList) || length(previousVerletList)~=n
    error('the supplied VerletList (%d atoms) is not compatible with X (% atoms)',length(previousVerletList),n)
end
if isstruct(config)
    if isfield(config,'engine') && strcmp(config.engine,'buildVerletList')
        if (config.natoms ~= n) || (config.dimensions~=d)
            error('the number of atoms (%d) or/and dimensions (%d) have changed, expected %d x %d',...
                n,d,config.natoms,config.dimensions)
        end
    else
        error('unrecognized configuration structure')
    end
end
nsamples = min(config.nsamples,n/10);

%% check the stability of the previousVerletList
cutoff2 = config.cutoff^2;
stable = true;
i = 0;
while (i < nsamples) && stable
    i = i + 1;
    isample = unidrnd(n);
    Xsample = X(isample,:);
    jneigh = find( sum((X-Xsample).^2,2) <= cutoff2 );
    stable = length(intersect(jneigh,previousVerletList{isample})) > ...
        ((1-config.tolerance)*length(previousVerletList{isample}));
end

%% take decision
if stable
    verletList = previousVerletList;
else
    if config.verbose, dispf('The current VerletList is obsolete'), end
    verletList = buildVerletList(X, config.cutoff, config.sorton, config.nblocks, config.verbose);
end

% output
if nargout>1, configout = config; end
