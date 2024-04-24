function Vq = interp2SPH(centers,y,Xq,Yq,W,V,forcesilent)
% INTERP2SPH interpolates y at Xq,Yq using the 2D kernel W centered on centers
%
%   Syntax:
%       Vq = interp2SPH(X,y,Xq,Yq [,W,V])
%
%   Inputs:
%     centers : kx2 coordinates of the kernel centers
%           y : kxny values at X (m is the number of values associated with the same center)
%               [] (empty matrix) forces a uniform density calculatoin
%          Xq : array or matrix coordinates along X
%          Yq : array or matrix coordinates along Y
%           W : kernel function @(r) <-- use kernelSPH() to supply a vectorized kernel
%           V : kx1 volume of the kernels (default=1)
%               [] (empty matrix) or scalar value forces uniform volumes (default =1)
%  forcesilent: flag to force silence mode (default = false)
%
%   Output:
%           Vq : same size as Xq, with an additional dimension if y was an array
%
%   See also: interp3SPH, kernelSPH, packSPH
%

% 2023-02-20 | INRAE\Olivier Vitrac | rev. 2024-03-18

%Revision history
% 2023-10-30 remove Zq from the input variables
% 2024-03-18 fixes for production

% arg check
if nargin<1, centers = []; end
if nargin<2, y = []; end
if nargin<3, Xq = []; end
if nargin<4, Yq = []; end
if nargin<5, W = []; end
if nargin<6, V = []; end
if nargin<7, forcesilent = []; end
[k,d] = size(centers);
[ky,ny] = size(y);
kv = length(V);
if k==0, error('please supply some centers'), end
if d~=2, error('2 dimensions (columns) are required'), end
if ky*ny==0, y = ones(k,1); ky=k; ny=1; end
if ky~=k, error('the number of y values (%d) does not match the number of kernels (%d)',ky,k), end
if ~isequal(size(Xq),size(Yq)), error('Xq,Yq and Zq do not have compatible sizes'), end 
if kv==0, V=1;  kv=1; end
if kv==1, V = ones(k,1)*V; kv=k; end
if kv~=k, error('the number of V values (%d) does not match the number of kernels (%d)',kv,k); end
if isempty(forcesilent), forcesilent=false; end
fmtsize = @(array) sprintf([repmat('%d x ', 1, ndims(array)-1), '%d'], size(array));

% main
sumW = cell(1,ny);
verbosity = numel(Xq)>1e4;
largek = k>200;
t0_ = clock; t1_=t0_; screen=''; %#ok<CLOCK,NASGU>

if verbosity, dispf('INTPER2SPH is summing %s grid values over %d kernels (K)...',fmtsize(Xq),k), end
for i=1:k
    % initialization if needed
    if i==1
        for iy=1:ny
            sumW{iy} = zeros(size(Xq),class(Xq));
        end
    end
        % verbosity
    if verbosity
        if largek
            t_ = clock;
            if mod(i,500)==0 || (etime(t_,t1_)>0.5) %#ok<*DETIM> 
                t1_=t_;
                dt_ = etime(t_,t0_); done_ = i/k;
                screen = dispb(screen,'[K%d:%d] INTERP2SPH | elapsed %0.1f s | done %0.1f %% | remaining %0.1f s', ...
                               i,k,dt_,100*done_,(1/done_-1)*dt_);
            end
        else
            dispf('... interpolate respectively to kernel %d of %d',i,k);
        end
    end
    % interpolation
    R = sqrt( (Xq-centers(i,1)).^2 + (Yq-centers(i,2)).^2  );
    for iy = 1:ny
        sumW{iy} = sumW{iy} + y(i,iy) * V(i) * W(R);
    end
end

% output
if ny==1
    Vq = sumW{1};
else
    Vq = cat(ndims(Xq)+1,sumW{:});
end

% verbosity
if verbosity
    dispb(screen,'done in . INTERP2SPH interpolated %s grid points with %d kernels in %0.4g s', ...
                               etime(clock,t0_),fmtsize(Xq),k);
end