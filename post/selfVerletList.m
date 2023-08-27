function selfV = selfVerletList(V)
% SELFVERLETLIST include self in the VerletList (required for density)
%
%   Syntax: selfV = selfVerletList(V,typ)
%
%
%   See also: buildVerletList, updateVerletList, partitionVerletList, interp3SPHVerlet


% MS 3.0 | 2023-04-02 | INRAE\Olivier.vitrac@agroparistech.fr | rev. 2023-05-17

% Revision history
% 2023-04-02 RC
% 2023-05-16 fix arg check
% 2023-05-17 updated help


% CHeck arguments
if nargin<1, error('one arguments is required:  selfV = selfVerletList(V)'), end
if ~iscell(V)
    error('the supplied VerletList (%d atoms) is invalid',length(V))
end

% Main
selfV = V;
for i=1:n
    selfV{i}(1:end+1) = [i;V{i}(:)]; % instead of crude concatenation, keep column or row vector
end

