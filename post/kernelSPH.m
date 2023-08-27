function W = kernelSPH(h,type,d)
% KERNELSPH return a SPH kernel
%
%   Syntax:
%       W = kernelSPH(h,type,d)
%    Inputs:
%           h : cutoff
%        type : kenel name (default = Lucy)
%           d : dimension
%   Output:
%           W : kernel function @(r)
%   TODO list
%       double check the cubic spline kernel, the symengine unable to generate code
%   Example:
%       W = kernelSPH(1,'lucy',3)
%
%   Kernels
%   lucy and lucydir:  used for the Morris calculation in the SPH source code of LAMMPS:
%                       lammps-2022-10-04/src/SPH/pair_sph_taitwater_morris.cpp ln. 138
%   poly6kernel:       used for ULSPH density calculation in SMD source code of LAMMPS:
%                       lammps-2022-10-04/src/MACHDYN/pair_smd_ulsph.cpp
%   cubicspline:       used for ULSPH artificial pressure calculation in SMD source code of LAMMPS:
%                       lammps-2022-10-04/src/MACHDYN/pair_smd_ulsph.cpp
%   spikykernel:       used for ULSPH and TLSPH force calculation in SMD source code of LAMMPS:
%                       lammps-2022-10-04/src/MACHDYN/pair_smd_ulsph.cpp
%                       lammps-2022-10-04/src/MACHDYN/pair_smd_tlsph.cpp
%   See also: interp3SPH, interp2SPH, packSPH


% 2023-02-20 | INRAE\Olivier Vitrac | rev.

% Revision history
% 2023-04-03 WJ. addition of the `poly6kernel', the `cubicsplinekernel' and the `spikykernel' as set in the SMD source code of LAMMPS:
%            lammps-2022-10-04/src/MACHDYN/smdkernel.cpp



% arg check
if nargin<1, h = []; end
if nargin<2, type = ''; end
if nargin<3, d = []; end
if isempty(h), error('Supply a value for h'), end
if isempty(type), type = 'lucy'; end
if ~ischar(type), error('type must be a char array'), end
if isempty(d), d = 3; end
if (d<2) || (d>3), error('d must be equal to 1, 2 or 3'), end

% main
switch lower(type)
    case 'lucy'
        if d==3
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                W(r) = piecewise(r<h,(1/s)*(1+3*r/h)*(1-r/h)^3,r>=h,0); % kernel definition
                s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
                assume(R<h)
                matlabFunction((subs(W3(R),R,r)))
            %}
            W = @(r) (r<h) .* ( 1.0./h.^3.*(r./h-1.0).^3.*((r.*3.0)./h+1.0).*(-1.05e+2./1.6e+1) )./pi;
        elseif d==2
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                W(r) = piecewise(r<h,(1/s)*(1+3*r/h)*(1-r/h)^3,r>=h,0); % kernel definition
                s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
                assume(R<h)
                matlabFunction((subs(W2(R),R,r)))
            %}
            W = @(r) (r<h) .* ( 1.0./h.^2.*(r./h-1.0).^3.*((r.*3.0)./h+1.0).*-5.0 )./pi;
        end
    case 'lucyder'
        if d==3
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                W(r) = piecewise(r<h,(1/s)*(1+3*r/h)*(1-r/h)^3,r>=h,0); % kernel definition
                s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
                assume(R<h)
                matlabFunction((subs(diff(W3(R),R,1),R,r)))
            %}
            W = @(r) (r<h) .* ( (1.0./h.^4.*(r./h-1.0).^3.*(-3.15e+2./1.6e+1))./pi-(1.0./h.^4.*(r./h-1.0).^2.*((r.*3.0)./h+1.0).*(3.15e+2./1.6e+1))./pi );
        elseif d==2
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                W(r) = piecewise(r<h,(1/s)*(1+3*r/h)*(1-r/h)^3,r>=h,0); % kernel definition
                s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 2D
                W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
                assume(R<h)
                matlabFunction((subs(diff(W2(R),R,1),R,r)))
            %}
            W = @(r) (r<h) .* ( (1.0./h.^3.*(r./h-1.0).^3.*-1.5e+1)./pi-(1.0./h.^3.*(r./h-1.0).^2.*((r.*3.0)./h+1.0).*1.5e+1)./pi );
        end
    case 'poly6kernel'        
        if d==3
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                W(r) = piecewise(r<h,(1/s)*((h^2 - r^2)*(h^2 - r^2)*(h^2 - r^2))/((h^2)*(h^2)*(h^2)*(h^2)*(h)),r>=h,0); % kernel definition
                s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
                assume(R<h)
                matlabFunction((subs(W3(R),R,r)))
                
            %}
            W = @(r) (r<h) .* (1.0./h.^9.*(h.^2-r.^2).^3.*(3.15e+2./6.4e+1))./pi;
        elseif d==2
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                W(r) = piecewise(r<h,(1/s)*((h^2 - r^2)*(h^2 - r^2)*(h^2 - r^2))/((h^2)*(h^2)*(h^2)*(h^2)),r>=h,0)
                s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
                assume(R<h)
                matlabFunction((subs(W2(R),R,r)))
            %}
            W = @(r) (r<h) .* (1.0./h.^8.*(h.^2-r.^2).^3.*4.0)./pi;
        end
    case 'cubicsplinekernel'        
        if d==3
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                q = 2*r/h
                W(r) = piecewise(q<1,(1/s)*(2/3-q^2+0.5*q^3),(q>=1) & (q<2),(1/s)*((2-q)^3)/6,q>=2,0); % kernel definition
                s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
                assume(R<h)
                matlabFunction((subs(W3(R),R,r)))
                
            %}
            %W = @(r) (r<h) .* (1.0./h.^6.*(h-r).^3.*1.5e+1)./pi;
            error('''%s'' is not yet properly implemented',type)
        elseif d==2
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                hr = h - r
                n = h^5
                W(r) = piecewise(r<h,(1/s)*(hr*hr*hr/n),r>=h,0); % kernel definition
                s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
                assume(R<h)
                matlabFunction((subs(W2(R),R,r)))
            %}
            %W = @(r) (r<h) .* (1.0./h.^5.*(h-r).^3.*1.0e+1)./pi;
            error('''%s'' is not yet properly implemented',type)

        end
    case 'spikykernel'        
        if d==3
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                hr = h - r
                n = h^6
                W(r) = piecewise(r<h,(1/s)*(hr*hr*hr/n),r>=h,0); % kernel definition
                s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
                assume(R<h)
                matlabFunction((subs(W3(R),R,r)))
                
            %}
            W = @(r) (r<h) .* (1.0./h.^6.*(h-r).^3.*1.5e+1)./pi;
        elseif d==2
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                hr = h - r
                n = h^5
                W(r) = piecewise(r<h,(1/s)*(hr*hr*hr/n),r>=h,0); % kernel definition
                s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
                assume(R<h)
                matlabFunction((subs(W2(R),R,r)))
            %}
            W = @(r) (r<h) .* (1.0./h.^5.*(h-r).^3.*1.0e+1)./pi;
        end
    case 'spikykernelder'
        if d==3
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                hr = h - r
                n = h^6
                W(r) = piecewise(r<h,(1/s)*(hr*hr*hr/n),r>=h,0); % kernel definition
                s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
                assume(R<h)
                matlabFunction((subs(diff(W3(R),R,1),R,r)))
                
            %}
            W = @(r) (r<h) .* (1.0./h.^6.*(h-r).^2.*-4.5e+1)./pi;
        elseif d==2
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                hr = h - r
                n = h^5
                W(r) = piecewise(r<h,(1/s)*(hr*hr*hr/n),r>=h,0); % kernel definition
                s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
                assume(R<h)
                matlabFunction((subs(diff(W2(R),R,1),R,r)))
            %}
            W = @(r) (r<h) .* (1.0./h.^5.*(h-r).^2.*-3.0e+1)./pi;
        end
        
    otherwise
        error('the kernel ''%s'' is not implemented',type)
end

% --- old code --

% function W = kernelSPH(h,type,d)
% % KERNELSPH return a SPH kernel
% %
% %   Syntax:
% %       W = kernelSPH(h,type,d)
% %    Inputs:
% %           h : cutoff
% %        type : kenel name (default = Lucy)
% %           d : dimension
% %   Output:
% %           W : kernel function @(r)
% %
% %   Example:
% %       W = kernelSPH(1,'lucy',3)
% %
% %
% %   See also: interp3SPH, interp2SPH, packSPH
% 
% 
% % 2023-02-20 | INRAE\Olivier Vitrac | rev.
% 
% % arg check
% if nargin<1, h = []; end
% if nargin<2, type = ''; end
% if nargin<3, d = []; end
% if isempty(h), error('Supply a value for h'), end
% if isempty(type), type = 'lucy'; end
% if ~ischar(type), error('type must be a char array'), end
% if isempty(d), d = 3; end
% if (d<2) || (d>3), error('d must be equal to 1, 2 or 3'), end
% 
% % main
% switch lower(type)
%     case 'lucy'
%         if d==3
%             %{
%                 syms R h s W(r)
%                 assume(h,{'real','positive'})
%                 assume(r,{'real','positive'})
%                 W(r) = piecewise(r<h,(1/s)*(1+3*r/h)*(1-r/h)^3,r>=h,0); % kernel definition
%                 s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
%                 W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
%                 assume(R<h)
%                 matlabFunction((subs(W3(R),R,r)))
%             %}
%             W = @(r) (r<h) .* ( 1.0./h.^3.*(r./h-1.0).^3.*((r.*3.0)./h+1.0).*(-1.05e+2./1.6e+1) )./pi;
%         elseif d==2
%             %{
%                 syms R h s W(r)
%                 assume(h,{'real','positive'})
%                 assume(r,{'real','positive'})
%                 W(r) = piecewise(r<h,(1/s)*(1+3*r/h)*(1-r/h)^3,r>=h,0); % kernel definition
%                 s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 3D
%                 W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
%                 assume(R<h)
%                 matlabFunction((subs(W2(R),R,r)))
%             %}
%             W = @(r) (r<h) .* ( 1.0./h.^2.*(r./h-1.0).^3.*((r.*3.0)./h+1.0).*-5.0 )./pi;
%         end
%     case 'lucyder'
%         if d==3
%             %{
%                 syms R h s W(r)
%                 assume(h,{'real','positive'})
%                 assume(r,{'real','positive'})
%                 W(r) = piecewise(r<h,(1/s)*(1+3*r/h)*(1-r/h)^3,r>=h,0); % kernel definition
%                 s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
%                 W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
%                 assume(R<h)
%                 matlabFunction((subs(diff(W3(R),R,1),R,r)))
%             %}
%             W = @(r) (r<h) .* ( (1.0./h.^4.*(r./h-1.0).^3.*(-3.15e+2./1.6e+1))./pi-(1.0./h.^4.*(r./h-1.0).^2.*((r.*3.0)./h+1.0).*(3.15e+2./1.6e+1))./pi );
%         elseif d==2
%             %{
%                 syms R h s W(r)
%                 assume(h,{'real','positive'})
%                 assume(r,{'real','positive'})
%                 W(r) = piecewise(r<h,(1/s)*(1+3*r/h)*(1-r/h)^3,r>=h,0); % kernel definition
%                 s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 2D
%                 W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
%                 assume(R<h)
%                 matlabFunction((subs(diff(W2(R),R,1),R,r)))
%             %}
%             W = @(r) (r<h) .* ( (1.0./h.^3.*(r./h-1.0).^3.*-1.5e+1)./pi-(1.0./h.^3.*(r./h-1.0).^2.*((r.*3.0)./h+1.0).*1.5e+1)./pi );
%         end
%     otherwise
%         error('the kernel ''%s'' is not implemented',type)
% end
