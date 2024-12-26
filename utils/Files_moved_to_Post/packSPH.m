function X = packSPH(siz,r,typ)
% PACKSPH returns the HCP or FCC packing of siz spheres of radius r
%
%   Syntax:
%       W = packSPH(siz,r,typ)
%    Inputs:
%         siz : [5 5 5] number of spheres along x,y,z 
%               if siz is a scalar, the same siz is applied to all dimensions [siz siz siz]
%           r : bead radius
%         typ : 'HCP' (default, period 2) or 'FCC' (period 3)
%   Output:
%           X : [size(1)xsize(2)xsize(3)] x 3 centers
%
%   Example:
%       X = packSPH(5)
%
%
%   See also: interp3SPH, interp2SPH, kernelSPH


% 2023-02-20 | INRAE\Olivier Vitrac | rev.

% arg check
rdefault = 0.5;
typdefault = 'HCP';
if nargin<1, siz = []; end
if nargin<2, r = []; end
if nargin<3, typ = ''; end
if numel(siz)==1, siz = [1,1,1]*siz; end
if isempty(siz) || numel(siz)~=3, error('siz must be 1x3 or 3x1 vector'); end
if isempty(r), r = rdefault; end
if isempty(typ), typ = typdefault; end
if ~ischar(typ), error('typ must be a char array'); end
switch upper(typ)
    case 'HCP'
        forceFCC = 0; % 0 for HCP and 1 for FCC
    case 'FCC'
        forceFCC = 1; % 0 for HCP and 1 for FCC
    otherwise
        error('valid packaging typ is ''HCP'' or ''FCC''')
end

% Lattice
[i,j,k] = ndgrid(0:(siz(1)-1),0:(siz(2)-1),0:(siz(3)-1)); % HCP is period 2, FCC is period 3
[i,j,k] = deal(i(:),j(:),k(:));
X = [
    2*i + mod(j+k,2) ...x
    sqrt(3)*(j+mod(k,2)/3)  + (mod(k,3)==2)*forceFCC...y
    (2*sqrt(6)/3)*k ... z
    ]*r;