function W = kernelSPH(h,type,d)
% KERNELSPH return a SPH kernel as an anonymous function in 3D or 2D (kernels are zero for r>h)
%
%   Syntax:
%       W = kernelSPH(h,type,d)
%    Inputs:
%           h : cutoff (all kernels have support between 0 and h)
%        type : kenel name (default = Lucy)
%           d : dimension (3 or 2)
%   Output:
%           W : kernel function @(r)
%   Example:
%       W = kernelSPH(1,'lucy',3)
%
%
%   List of implemented Kernels (aliases can be defined)
%       Suffix der is added to first-order derivative kernels
%
%
%   lucy and lucyder:  used for the Morris calculation in the SPH source code of LAMMPS:
%                       lammps-2022-10-04/src/SPH/pair_sph_taitwater_morris.cpp ln. 138
%   poly6, polyder:       used for ULSPH density calculation in SMD source code of LAMMPS:
%                       lammps-2022-10-04/src/MACHDYN/pair_smd_ulsph.cpp
%   cubicspline, cubic:   used for ULSPH artificial pressure calculation in SMD source code of LAMMPS:
%   cubicder            lammps-2022-10-04/src/MACHDYN/pair_smd_ulsph.cpp
%                       USER-SMD/smd_kernels.h
%   spikykernel,spiky     used for ULSPH and TLSPH force calculation in SMD source code of LAMMPS:
%   spikyder            lammps-2022-10-04/src/MACHDYN/pair_smd_ulsph.cpp
%                       lammps-2022-10-04/src/MACHDYN/pair_smd_tlsph.cpp
%   gaussian, gaussiankernel
%   gaussiander

%   See also: interp3SPH, interp3SPHVerlet, interp2SPH, interp2SPHVerlet, packSPH


% 2023-02-20 | INRAE\Olivier Vitrac | rev. 2023-10-29

% Revision history
% 2023-04-03 WJ. addition of the `poly6kernel', the `cubicsplinekernel' and the `spikykernel' as set in the SMD source code of LAMMPS:
%            lammps-2022-10-04/src/MACHDYN/smdkernel.cpp
% 2023-10-29 major revision, updated and new kernels, help improvement, all kernels are zero beyond h


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
    case {'poly6kernel','poly6'}
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
    case  {'cubicsplinekernel','cubicspline','cubic'}
        if d==3
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                q = 2*r/h;
                W(r) = piecewise(q<1,(1/s)*(2/3-q^2+0.5*q^3),(q>=1) & (q<2),(1/s)*((2-q)^3)/6,q>=2,0); % kernel definition
                s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
                assume(R<h/2)
                matlabFunction(simplify(subs(W3(R),R,r)))
                assume(R,'clear')
                assume((R>h/2) & (R<h))
                matlabFunction(simplify(subs(W3(R),R,r)))           
            %}
            W = @(r) (r<h/2) .* ...
                (1.0./h.^6.*(h.*r.^2.*-4.8e+1+h.^3.*8.0+r.^3.*4.8e+1))./pi ...
                + ((r>=h/2) & (r<h)) .* ...
                (1.0./h.^6.*(h-r).^3.*1.6e+1)./pi;
        elseif d==2
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                q = 2*r/h;
                W(r) = piecewise(q<1,(1/s)*(2/3-q^2+0.5*q^3),(q>=1) & (q<2),(1/s)*((2-q)^3)/6,q>=2,0); % kernel definition
                s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 2D
                W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
                assume(R<h/2)
                matlabFunction(simplify(subs(W2(R),R,r)))
                assume(R,'clear')
                assume((R>h/2) & (R<h))
                matlabFunction(simplify(subs(W2(R),R,r))) 
            %}
            W = @(r) (r<h/2) .* ...
                (1.0./h.^5.*(h.*r.^2.*-2.4e+2+h.^3.*4.0e+1+r.^3.*2.4e+2))./(pi.*7.0) ...
                + ((r>=h/2) & (r<h)) .* ...
                (1.0./h.^5.*(h-r).^3.*(8.0e+1./7.0))./pi;
        end
    case  {'cubicsplineder','cubicder'}
        if d==3
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                q = 2*r/h;
                W(r) = piecewise(q<1,(1/s)*(2/3-q^2+0.5*q^3),(q>=1) & (q<2),(1/s)*((2-q)^3)/6,q>=2,0); % kernel definition
                s3D = solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s); % scaling factor in 3D
                W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
                assume(R<h/2)
                matlabFunction(simplify(subs(diff(W3(R),R,1),R,r)))
                assume(R,'clear')
                assume((R>h/2) & (R<h))
                matlabFunction(simplify(subs(diff(W3(R),R,1),R,r)))           
            %}
            W = @(r) (r<h/2) .* ...
                (1.0./h.^6.*r.*(h.*2.0-r.*3.0).*-4.8e+1)./pi ...
                + ((r>=h/2) & (r<h)) .* ...
                (1.0./h.^6.*(h-r).^2.*-4.8e+1)./pi;
        elseif d==2
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                q = 2*r/h;
                W(r) = piecewise(q<1,(1/s)*(2/3-q^2+0.5*q^3),(q>=1) & (q<2),(1/s)*((2-q)^3)/6,q>=2,0); % kernel definition
                s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 2D
                W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
                assume(R<h/2)
                matlabFunction(simplify(subs(diff(W2(R),R,1),R,r)))
                assume(R,'clear')
                assume((R>h/2) & (R<h))
                matlabFunction(simplify(subs(diff(W2(R),R,1),R,r))) 
            %}
            W = @(r) (r<h/2) .* ...
                (1.0./h.^5.*r.*(h.*2.0-r.*3.0).*(-2.4e+2./7.0))./pi ...
                + ((r>=h/2) & (r<h)) .* ...
                (1.0./h.^5.*(h-r).^2.*(-2.4e+2./7.0))./pi;
        end        

    case {'spikykernel' 'spiky'}        
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
    case {'spikykernelder','spikyder'}
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

    case 'gaussian'
        % M. Liu, & G. Liu, Smoothed particle hydrodynamics (SPH): an overview and recent developments, “Archives of computational methods in engineering”, 17.1 (2010), pp. 25-76.
        if d==3
            %{
                syms R h s W(r) pi
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                W(r) = piecewise(r<=h,(1/s)*(exp(-(3*r/h)^2) - exp(-(3)^2)),r>h,0); % kernel definition
                s3D = simplify(solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s)); % scaling factor in 3D
                % -pi*((2*h^3*exp(-9))/9 + (2276509072173613*h^3)/13835058055282163712 - (h^3*pi^(1/2)*erf(3))/27)
                s3D = h^3*pi^(3/2)/27;
                W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
                assume(R<=h)
                matlabFunction((subs(W3(R),R,r)))
            %}
            W = @(r) (r<h) .* 1.0./h.^3.*1.0./pi.^(3.0./2.0).*(exp(1.0./h.^2.*r.^2.*-9.0)-1.234098040866796e-4).*2.7e+1;
        elseif d==2
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                W(r) = piecewise(r<=h,(1/s)*(exp(-(3*r/h)^2) - exp(-(3)^2)),r>h,0); % kernel definition
                s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 2D
                % (h^2*pi*exp(-9)*(18426255492059989099*exp(9) - 18446744073709551616))/166020696663385964544
                s2D = pi*h^2/9; % exp(-9) is dropped
                W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
                assume(R<=h)
                matlabFunction((subs(W2(R),R,r)))
            %}
            W = @(r) (r<h) .* (1.0./h.^2.*(exp(1.0./h.^2.*r.^2.*-9.0)-1.234098040866796e-4).*9.0)./pi;
        end
    case 'gaussiander'
        % M. Liu, & G. Liu, Smoothed particle hydrodynamics (SPH): an overview and recent developments, “Archives of computational methods in engineering”, 17.1 (2010), pp. 25-76.
        if d==3
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                W(r) = piecewise(r<=h,(1/s)*(exp(-(3*r/h)^2) - exp(-(3)^2)),r>h,0); % kernel definition
                s3D = simplify(solve( int(4*pi*r^2 * W(r),r,0,Inf)==1,s)); % scaling factor in 3D
                % -pi*((2*h^3*exp(-9))/9 + (2276509072173613*h^3)/13835058055282163712 - (h^3*pi^(1/2)*erf(3))/27)
                s3D = h^3*pi^(3/2)/27;
                W3(r) = subs(W(r),s,s3D); % scaled kernel in 3D
                assume(R<=h)
                matlabFunction((subs(diff(W3(R),R,1),R,r)))
            %}
            W =  @(r) (r<h) .* 1.0./h.^5.*r.*exp(1.0./h.^2.*r.^2.*-9.0).*(-8.727934135283096e+1);
        elseif d==2
            %{
                syms R h s W(r)
                assume(h,{'real','positive'})
                assume(r,{'real','positive'})
                W(r) = piecewise(r<=h,(1/s)*(exp(-(3*r/h)^2) - exp(-(3)^2)),r>h,0); % kernel definition
                s2D = solve( int(2*pi*r * W(r),r,0,Inf)==1,s); % scaling factor in 2D
                % (h^2*pi*exp(-9)*(18426255492059989099*exp(9) - 18446744073709551616))/166020696663385964544
                s2D = pi*h^2/9; % exp(-9) is dropped
                W2(r) = subs(W(r),s,s2D); % scaled kernel in 2D
                assume(R<=h)
                matlabFunction((subs(diff(W2(R),R,1),R,r)))
            %}
            W =  @(r) (r<h) .* (1.0./h.^4.*r.*exp(1.0./h.^2.*r.^2.*-9.0).*-1.62e+2)./pi;

        end
    case {'kernelwendlandquintic' 'wendlandquintickernel' 'wendlandquintic'}
        error('the kernel ''%s'' is not implemented yet (pending)',type)
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
