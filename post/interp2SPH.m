function Vq = interp2SPH(centers,y,Xq,Yq,Zq,W,V)
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
%
%   Output:
%           Vq : same size as Xq, with an additional dimension if y was an array
%
%   See also: interp3SPH, kernelSPH, packSPH
%

% 2023-02-20 | INRAE\Olivier Vitrac | rev.

% arg check
if nargin<1, centers = []; end
if nargin<2, y = []; end
if nargin<3, Xq = []; end
if nargin<4, Yq = []; end
if nargin<5, W = []; end
if nargin<6, V = []; end
[k,d] = size(centers);
[ky,ny] = size(y);
kv = length(V);
if k==0, error('please supply some centers'), end
if d~=2, error('2 dimensions (columns) are required'), end
if ky*ny==0, y = ones(k,1); ky=k; ny=1; end
if ky~=k, error('the number of y values (%d) does not match the number of kernels (%d)',ky,k), end
if ~isequal(size(Xq),size(Yq)) || ~isequal(size(Yq),size(Zq)), error('Xq,Yq and Zq do not have compatible sizes'), end 
if kv==0, V=1;  kv=1; end
if kv==1, V = ones(k,1)*V; kv=k; end
if kv~=k, error('the number of V values (%d) does not match the number of kernels (%d)',kv,k); end

% main
sumW = cell(1,ny);
verbosity = numel(Xq)>1e4;
for i=1:k
    % initialization if needed
    if i==1
        for iy=1:ny
            sumW{iy} = zeros(size(Xq),class(Xq));
        end
    end
    % interpolation
    if verbosity, dispf('interpolate respectively to kernel %d of %d',i,k); end    
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