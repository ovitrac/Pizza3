function partV = partitionVerletList(V,typ)
% PARTITIONVERLETLIST partition an existing Verlet list based on type (cross-terms)
%
%   Syntax: partV = partitionVerletList(V,typ)
%
%
%   See also: buildVerletList, updateVerletList, selfVerletList


% MS 3.0 | 2023-04-01 | INRAE\Olivier.vitrac@agroparistech.fr | rev.

% CHeck arguments
if nargin<2, error('two arguments are required:  partV = partitionVerletList(V,typ)'), end
if istable(typ), typ = typ.type; end
n = length(typ); % number of particless
if ~iscell(V) || length(V)~=n
    error('the supplied VerletList (%d atoms) is not compatible with X (% atoms)',length(V),n)
end

% Main
partV = cell(n,1);
for i=1:n
    partV{i} = V{i}(typ(V{i})~=typ(i));
end

