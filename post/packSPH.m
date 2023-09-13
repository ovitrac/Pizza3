function X = packSPH(siz, r, typ)
% PACKSPH returns the HCP, FCC, or SC packing of siz spheres of radius r
%
%   Syntax:
%       W = packSPH(siz,r,typ)
%    Inputs:
%         siz : [5 5 5] number of spheres along x,y,z 
%               if siz is a scalar, the same siz is applied to all dimensions [siz siz siz]
%           r : bead radius
%         typ : 'HCP' (default, period 2), 'FCC' (period 3), or 'SC' (period 1)
%               'SC2' and 'SC3' implement Simple Cubic with period 2 and period 3, respectively
%   Output:
%           X : [size(1)xsize(2)xsize(3)] x 3 centers
%
%   Example:
%       X = packSPH(5)
%
%   See also: interp3SPH, interp2SPH, kernelSPH

% 2023-02-20 | INRAE\Olivier Vitrac | rev. 2023-09-11

% Revision History
% 2023-09-11 add SC

% Argument check
rdefault = 0.5;
typdefault = 'HCP';
if nargin < 1, siz = []; end
if nargin < 2, r = []; end
if nargin < 3, typ = ''; end
if numel(siz) == 1, siz = [1,1,1] * siz; end
if isempty(siz) || numel(siz) ~= 3, error('siz must be a 1x3 or 3x1 vector'); end
if isempty(r), r = rdefault; end
if isempty(typ), typ = typdefault; end
if ~ischar(typ), error('typ must be a char array'); end

switch upper(typ)
    case 'HCP'
        lattice_type = 0;
    case 'FCC'
        lattice_type = 1;
    case 'SC'
        lattice_type = 2;
    case 'SC2'
        lattice_type = 3;
    case 'SC3'
        lattice_type = 4;
    otherwise
        error('Valid packaging type is ''HCP'', ''FCC'', ''SC'', ''SC2'', or ''SC3''')
end




% Lattice
[i, j, k] = ndgrid(0:(siz(1) - 1), 0:(siz(2) - 1), 0:(siz(3) - 1));
[i, j, k] = deal(i(:), j(:), k(:));

switch lattice_type
    case 0  % HCP
        X = [
            2 * i + mod(j + k, 2), ...
            sqrt(3) * (j + mod(k, 2) / 3), ...
            (2 * sqrt(6) / 3) * k ...
            ] * r;
    case 1  % FCC
        X = [
            2 * i + mod(j + k, 2), ...
            sqrt(3) * (j + mod(k, 2) / 3) + (mod(k, 3) == 2), ...
            (2 * sqrt(6) / 3) * k ...
            ] * r;
    case 2  % SC (Simple Cubic)
        X = [
            i, ...
            j, ...
            k ...
            ] * r * 2;
    case 3  % SC2 (Simple Cubic with a period 2)
        X = [
            i + 0.5 * mod(j + k, 2), ...
            j + 0.5 * mod(k + i, 2), ...
            k + 0.5 * mod(i + j, 2) ...
            ] * r * 2;
    case 4  % SC3 (Simple Cubic with a period 3)
        X = [
            i + mod(j + k, 3) / 3, ...
            j + mod(k + i, 3) / 3, ...
            k + mod(i + j, 3) / 3 ...
            ] * r * 2;
end

% ---- before 2023-09-11 ----
% % Lattice
% [i,j,k] = ndgrid(0:(siz(1)-1),0:(siz(2)-1),0:(siz(3)-1)); % HCP is period 2, FCC is period 3
% [i,j,k] = deal(i(:),j(:),k(:));
% X = [
%     2*i + mod(j+k,2) ...x
%     sqrt(3)*(j+mod(k,2)/3)  + (mod(k,3)==2)*forceFCC...y
%     (2*sqrt(6)/3)*k ... z
%     ]*r; % https://en.wikipedia.org/wiki/Close-packing_of_equal_spheres