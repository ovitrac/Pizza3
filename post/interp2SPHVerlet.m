function Vq = interp2SPHVerlet(XY,y,XYgrid,GridVerletList,W,V)
% INTERP2SPHVerlet interpolates y at XYgrid using the GridVerletList and the 2D kernel W centered on XY
%
%       Vgrid = interp2SPHVerlet(XY,y,XYgrid,GridVerletList [,W,V])
%
%   Inputs:
%             XY : kx2 coordinates of the kernel centers
%              y : kxny values at XY (m is the number of values associated with the same center)
%                  [] (empty matrix) forces a uniform density calculatoin
%         XYgrid : gx2 grid coordinates
% GridVerletList : VerletList of the grid
%              W : kernel function @(r) <-- use kernelSPH() to supply a vectorized kernel
%              V : kx1 volume of the kernels (default=1)
%                  [] (empty matrix) or scalar value forces uniform volumes (default =1)
%
%   Output:
%       Vgrid : gxny array
%
%
%   See also: buildVerletList, interp3SPH, interp3SPHVerlet, interp2SPH, kernelSPH, packSPH, virialStress

% 2023-10-30 | INRAE\Han CHEN | rev. 

% Revision history
% 2023-10-30 alpha version



% arg check
if nargin<1, XY = []; end
if nargin<2, y = []; end
if nargin<3, XYgrid = []; end
if nargin<4, GridVerletList= []; end
if nargin<5, W = []; end
if nargin<6, V = []; end
[k,d] = size(XY);
if d~=2, error('2 dimensions (columns) are required for XY'), end
[ky,ny] = size(y);
if ky*ny==0, y = ones(k,1); ky=k; ny=1; end
if ky~=k, error('the number of y values (%d) does not match the number of kernels (%d)',ky,k), end
if k==0, error('please supply some centers XY'), end
[kg,dg] = size(XYgrid);
if dg~=2, error('2 dimensions (columns) are required for XYgrid'), end
if ~iscell(GridVerletList) || length(GridVerletList)~=kg
    error('the supplied VerletList (%d atoms) does not match the number of grid points (%d)',length(GridVerletList),kg)
end
kv = length(V);
if kv==0, V=1;  kv=1; end
if kv==1, V = ones(k,1)*V; kv=k; end
if kv~=k, error('the number of V values (%d) does not match the number of kernels (%d)',kv,k); end
fmtsize = @(array) sprintf([repmat('%d x ', 1, ndims(array)-1), '%d'], size(array));

% main
t0_ = clock; t1_=t0_; screen=''; %#ok<CLOCK>
Vq = NaN(kg,ny,class(y));
sizVerlet = cellfun(@length,GridVerletList);
dispf('INTERP2SPHVERLET interpolates %s grid points with a Verlet list including from %d to %d neighbors...',...
    fmtsize(XYgrid),min(sizVerlet),max(sizVerlet))
for i=1:kg
    t_ = clock; %#ok<CLOCK>
    if mod(i,200)==0 || (etime(t_,t1_)>0.5) %#ok<*DETIM> 
        t1_=t_; dt_ = etime(t_,t0_); done_ = i/kg;
        screen = dispb(screen,'[GridPoint %d:%d] INTERP2SPHVerlet | elapsed %0.1f s | done %0.1f %% | remaining %0.1f s', ...
                               i,kg,dt_,100*done_,(1/done_-1)*dt_);
    end
    if ~isempty(GridVerletList{i})
        Vq(i,:) = interp2SPH( ...
            XY(GridVerletList{i},:),...
            y(GridVerletList{i},:),...
            XYgrid(i,1),...
            XYgrid(i,2),...
            W,...
            V(GridVerletList{i}),...volume of the kernel
            true ...silent
            );
    end
end
dispb(screen,'...done in %0.4g s. INTERP2SPHVerlet completed the interpolation of %d points with %d kernels', ...
                               etime(clock,t0_),kg,k); %#ok<CLOCK>
