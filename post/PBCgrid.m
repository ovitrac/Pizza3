function [Vp,Xout,Yout,Zout] = PBCgrid(varargin)
%PBCgrid add periodic boundary conditions to meshgrid/ndgrid meshed values
%
%   USAGE in 3D
%       [Vp,Xp,Yp,Zp] = PBCgrid(X,Y,Z,V,PBC [,cutoff])
%   USAGE in 2D
%       [Vp,Xp,Yp] = PBCgrid(X,Y,V,PBC [,cutoff])
%   USAGE in 1D
%       [Vp,Xp] = PBCgrid(X,V,PBC [,cutoff])
%
%   INPUTS (3D):
%            X: a x b x c array created by meshgrid, ndgrid coding for X coordinates
%            Y: a x b x c array created by meshgrid, ndgrid coding for Y coordinates
%            Z: a x b x c array created by meshgrid, ndgrid coding for Z coordinates
%            V: a x b x c array where V(i,j,k) is the value at X(i,j,k), Y(i,j,k) and Z(i,j,k)
%          PBC: 3 x 1 boolean array (true if the dimension is periodic)
%       cutoff: cutoff value either scalar or vector
%               [cutoff;cutoff;cutoff] or [cutoffx;cutoffy;cutoffz]
%
%   INPUTS (2D):
%            X: a x b array created by meshgrid, ndgrid coding for X coordinates
%            Y: a x b array created by meshgrid, ndgrid coding for Y coordinates
%            V: a x b array where V(i,j) is the value at X(i,j) and Y(i,j)
%          PBC: 2 x 1 boolean array (true if the dimension is periodic)
%       cutoff: cutoff value either scalar or vector
%               [cutoff;cutoff] or [cutoffx;cutoffy]
%
%   INPUTS (1D):
%            X: a x 1 array created by linspace or equivalent
%            V: a x 1 array where V(i) is the value at X(i)
%          PBC: boolean (true if the dimension is periodic)
%       cutoff: cutoff value
%
%   OUTPUTS (1-3D)
%           Vp: array with ndims(Vp) = ndims(V) augmented with perodic values
%           Xp,Yp,Zp corresponding coordinates
%
%
%
%   See also: PBCgridshift, PBCimages, PBCimageschift, PBCincell
%
%
%
% Example:
%      [X,Y,V] = peaks(100);
%      [Vp,Xp,Yp] = PBCgrid(X,Y,V,[true,true],[1.5 3]);
%      figure, mesh(Xp,Yp,Vp)


% MS 3.0 | 2024-03-15 | INRAE\han.chen@inrae.fr, INRAE\Olivier.vitrac@agroparistech.fr | rev. 2024-03-16


% Revision history
% 2024-03-15 release candidate with example
% 2024-03-16 fix nmirror when more than available points are required


%% check arguments
if nargin<3, error('Syntax: [Vp,Xp,Yp,Zp] = PBCgrid(X,Y,Z,V,PBC [,cutoff]) in 3D (other syntaxes available)'), end
X = varargin{1};
d = ndims(X); %<<- the number of dimensions in X sets 1D, 2D or 3D syntax
if d==3 && nargin<5, error('five arguments are at least required in 3D:  [Vp,Xp,Yp,Zp] = PBCgrid(X,Y,Z,V,PBC [,cutoff])'), end
if d==2 && nargin<4, error('four arguments are at least required in 2D:  [Vp,Xp,Yp] = PBCgrid(X,Y,V,PBC [,cutoff])'), end
if d>1
    Y = varargin{2};
    if ~isequal(size(X),size(Y)), error('X and Y are not compatible'), end
    if d>2 % 3D
        Z = varargin{3};
        if ~isequal(size(X),size(Z)), error('X, Y and Z are not compatible'), end
        V = varargin{4};
        if ~isequal(size(X),size(V)), error('V is not compatible with supplied X, Y and Z'), end
        PBC = varargin{5};
        if nargin>5, cutoff = varargin{6}; else cutoff = []; end %#ok<*SEPEX>
    else % 2D
        V = varargin{3};
        if ~isequal(size(X),size(V)), error('V is not compatible with supplied X and Y'), end
        PBC = varargin{4};
        if nargin>4, cutoff = varargin{5}; else cutoff = []; end
    end
else % 1D
    V = varargin{2};
    if ~isequal(size(X),size(V)), error('V is not compatible with supplied X'), end
    PBC = varargin{3};
    if nargin>3, cutoff = varargin{4}; else cutoff = []; end
end
% fix PBC
if length(PBC)~=d, error('PBC should be a %dx1 boolean array',d), end
PBC = PBC>0; % convert to boolean
% fix cutoff (heuristic for the default value)
if isempty(cutoff), cutoff = max(abs(X(1:2,1:2,1)-X(1,1,1)),[],'all')*(numel(X).^(1/d))/4; end
if length(cutoff)==1, cutoff = cutoff(ones(d,1)); end
cutoff(~PBC) = 0;
% discriminat between meshgrid or ndgrid generation
if d>1
    ismeshgrid =  all(diff(X(1:2,:,:),1,1)==0); % true if X,Y,Z generated with meshgrid
else
    ismeshgrid = false; % by convention
    X = X(:); % force column-wise
    V = V(:); % force column-wise
end
% Found bounds along X and Y (dependent on meshgrid or ndgrid generation)
nmirror = zeros(d,1); % number of values to mirror along each dimension
if ismeshgrid % 2D or 3D
    % bounds
    xmin = min(X(1,:,1));
    xmax = max(X(1,:,1));
    ymin = min(Y(:,1,1));
    ymax = max(Y(:,1,1));
    if cutoff(1)>0
        ntmp = find(abs(X(1,:,1)-X(1,1,1))>cutoff(1),1,'first')-1;
        if isempty(ntmp), nmirror(1) = size(X,2); else, nmirror(1) = ntmp; end
    end
    if cutoff(2)>0
        ntmp = find(abs(Y(:,1,1)-Y(1,1,1))>cutoff(2),1,'first')-1;
        if isempty(ntmp), nmirror(2) = size(X,1); else, nmirror(2) = ntmp; end
    end
    dx = diff(X(1,:,1),1,2);
    dy = diff(Y(:,1,1),1,1);
else % ndgrid: 1D, 2D or 3D
    xmin = min(X(:,1,:));
    xmax = max(X(:,1,:));
    if cutoff(1)>0
        ntmp = find(abs(X(:,1,1)-X(1,1,1))>cutoff(1),1,'first')-1;
        if isempty(ntmp), nmirror(1) = size(X,1); else, nmirror(1) = ntmp; end
    end
    dx = diff(X(:,1,1),1,1);
    if d>1
        ymin = min(Y(1,:,1));
        ymax = max(Y(1,:,1));
        if cutoff(2)>0
            ntmp = find(abs(Y(1,:,1)-Y(1,1,1))>cutoff(2),1,'first')-1;
            if isempty(ntmp), nmirror(2) = size(X,2); else, nmirror(2) = ntmp; end
        end
        dy = diff(X(1,:,1),1,2);
    else
        [ymin,ymax] = deal(NaN);
    end
end
% Found bounds along Z. Note that it is managed independently of ndgrid, meshgrid
if d>2 %3D
    zmin = min(Z(:,:,1));
    zmax = max(Z(:,:,1));
    if cutoff(3)>0
        ntmp = find(abs(Z(:,:,1)-Z(1,1,1))>cutoff(3),1,'first')-1;
        if isempty(ntmp), nmirror(3) = size(X,3); else, nmirror(3) = ntmp; end
    end
    dz = diff(X(1,1,:),1,3);
else
    [zmin,zmax] = deal(NaN);
end
% full bounds
bounds = [xmin xmax; ymin ymax; zmin zmax]; % NaN values for non-defined dimensions
dimensions = diff(bounds,1,2);

%% apply PBC to V
% nmirror(1) -> number of points to translate along X (regardless the value of ismeshgrid)
% nmirror(2) -> number of points to translate along Y (idem)
% nmirror(3) -> number of points to translate along Z (idem)
% dimensions
% a = length of grid along Y (if ismeshgrid), along X instead (ndgrid)
% b = length of grid along X (if ismeshgrid), along Y instead (ndgrid)
% c = length of grid along Z
[a,b,c] = size(X);
if ismeshgrid % 2D, 3D
    left = (b-nmirror(1)+1):b;
    right = 1:nmirror(1);
    indx = [left, 1:b, right];
    top = (a-nmirror(2)+1):a;
    bottom = 1:nmirror(2);
    indy = [top, 1:a, bottom];
else % 1D, 2D, 3D
    left = (a-nmirror(1)+1):a;
    right = 1:nmirror(1);
    indx = [left, 1:a, right];
    if d>1
        top = (b-nmirror(2)+1):b;
        bottom = 1:nmirror(2);
        indy = [top, 1:b, bottom];
    end
end
if d>2
    front = (c-nmirror(3)+1):c;
    back = 1:nmirror(3);
    indz = [front, 1:c, back];
end


%% duplication and translation
% (note that dimensions and nmirror obey to the same convention independently of ismeshgrid)
% nmirror(1) and dimensions(1) are always along X, 2 for Y and 3 for Z
if ismeshgrid % 2D and 3D
    if d==2
        Vp = V(indy,indx);
        Xp = X(indy,indx);
        Yp = Y(indy,indx);
    else
        Vp = V(indy,indx,indz);
        Xp = X(indy,indx,indz);
        Yp = Y(indy,indx,indz);
        Zp = Y(indy,indx,indz);
    end
    % translation X and Y (Z common with ndgrid)
    Xp(:,1:nmirror(1),:) = Xp(:,1:nmirror(1),:)-dimensions(1)-dx(end); % left translation
    Xp(:,(end-nmirror(1)+1):end,:) = Xp(:,(end-nmirror(1)+1):end,:)+dimensions(1)+dx(1); % right translation
    Yp(1:nmirror(2),:,:) = Yp(1:nmirror(2),:)-dimensions(2)-dy(end); % top translation
    Yp((end-nmirror(2)+1):end,:,:) = Yp((end-nmirror(2)+1):end,:,:)+dimensions(2)+dy(1); % bottom translation   
else % ndgrid in 1D, 2D and 3D
    if d==1
        Vp = V(indx);
        Xp = X(indx);
    elseif d==2
        Vp = V(indx,indy);
        Xp = X(indx,indy);
        Yp = Y(indx,indy);
    else
        Vp = V(indx,indy,indz);
        Xp = X(indx,indy,indz);
        Yp = Y(indx,indy,indz);
    end
    Xp(1:nmirror(1),:,:) = Xp(1:nmirror(1),:,:)-dimensions(1)-dx(end); % left translation
    Xp((end-nmirror(1)+1):end,:,:) = Xp((end-nmirror(1)+1):end,:,:)+dimensions(1)+dx(1); % top translation
    if d>1
        Yp(:,1:nmirror(2),:) = Yp(:,1:nmirror(2),:)-dimensions(2)-dy(end); % top translation
        Yp(:,(end-nmirror(2)+1):end,:) = Yp(:,(end-nmirror(2)+1):end,:)+dimensions(2)+dy(1); % bottom translation
    end
end
if d>2
    Zp(:,:,1:nmirror(3)) = Zp(:,:,1:nmirror(3))-dimensions(3)-dz(end); % front translation
    Zp(:,:,(end-nmirror(3)+1):end) = Zp(:,:,(end-nmirror(3)+1):end)+dimensions(3)+dz(1); % back translation
end

%% outputs
if nargout>1, Xout = Xp; end
if nargout>2 && d>1, Yout = Yp; end
if nargout>3 && d>2, Zout = Zp; end