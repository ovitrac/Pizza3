function [Ximages,updtbox] = PBCimagesshift(X,Pshift,box)
%PBCIMAGESSHIFT shift X coordinates assuming periodic conditions
%
%   USAGE: Ximages = PBCimages(X,box,Pshift)
%          [Ximages,updtbox] = PBCimages(...)
%
%   INPUTS:
%          X: nx2 or nx3 array coding for the coordinates of the n particles in 2D and 3D, respectively
%     Pshift: 1x2 or 1x3 array coding for the translation to apply
%        box: 2x2 or 3x2 array coding for current box dimensions (before translation)
%             the box spans along dimension i between box(i,1) and box(i,2)
%             all X values should lie within box limits, if not an error is generated
%
%   OUTPUTS:
%    Ximages: nx2 or nx3 array coding for the translated coordinates wrapped around periodic boundaries
%    updtbox: 2x2 or 3x3 updated box coordinates
%
%
%   See also: PBCgrid, PBCgridshift, PBCimages, PBCincell



% MS 3.0 | 2024-03-24 | INRAE\han.chen@inrae.fr, INRAE\Olivier.vitrac@agroparistech.fr | rev. 2024-03-16


% Revision history


%% Check arguments
if nargin<3, error('Not enough input arguments. Syntax: Ximages = PBCimagesshift(X,Pshift,box)'), end
[n,d] = size(X); % Number of particles and dimensions
if d>3, error('the number of dimensions should be 1,2,3'), end
Xmin = min(X);
Xmax = max(X);
if size(box,2)~=2 || size(box,1)~=d, error('Box dimensions must be a %dx2 vector',d); end
boxlength = diff(box, 1, 2);

%% Check that all points lie within the box
incellok = true;
for i=1:d
    if box(i,1)>Xmin(i)
        dispf('some particles are outside the lower bound %0.3g along dimension %d',box(i,1),i)
        incellok = false;
    end
    if box(i,2)<Xmax(i)
        dispf('some particles are outside the upper bound %0.3g along dimension %d',box(i,2),i),
        incellok = false;
    end
end
if ~incellok
    disp('use: X = PBCincell(X,box,PBC) to wrap particles around coordinates')
    error('PBCimages: some particles outside the box...')
end


%% Apply shift and wrap around using periodic boundary conditions
boxtranslated = zeros(size(box));
Ximages = zeros(size(X),class(X));
for i = 1:d
    boxtranslated(i,:) = box(i,:) - Pshift(i);
    Ximages(:, i) = mod(X(:, i) - box(i, 1) + Pshift(i), boxlength(i)) + boxtranslated(i, 1);
end

%% Output
if nargout>1
    updtbox = boxtranslated;
end
