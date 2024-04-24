function [traj,errout] = fillstreamline2(s,Xgrid,Ygrid,Vxgrid,Vygrid,rbead,l0,verbose)
%FILLSTREAMLINE2 fills streamline with distibuted and non-overlapping objects (beads)
%
%   USAGE: traj = fillstreamline2(s,Xgrid,Ygrid,Vxgrid,Vygrid [,dmax,l0,verbosity])
%          [traj,errout] = fillstreamline2(...)
%
%   Inputs:
%           s: n x 2 array coding for one single 2D streamline
%              1 x m cell array (output of streamline)
%       Xgrid: 2D (axb) array coding for X coordinates (output of meshgrid)
%       Ygrid: 2D (axb) array coding for Y coordinates (output of meshgrid)
%      Vxgrid: 2D (axb) array coding for x-component of velocity
%      Vygrid: 2D (axb) array coding for y-component of velocity
%       rbead: bead radius (default value = 1)
%          l0: initial position of first bead (curvilinear) (default value = 0)
%     verbose: flag to control verbosity (default = true)
%
%   Outputs:
%        traj: structure with fields (nb = number of objects/beads distributed along the streamline)

%            streamline: n×2 original streamline
%           curvilinear: n×1 curvilinear coordinate along the streamline
%            pseudotime: n×1 pseudotime to travel along the streamline
%         curv_velocity: n×1 velocity along the curvilinear coordinate
%         cart_velocity: n×2 cartesian velocity
%     curv_distribution: nb×1 distribution of beads along the curvilinear coordinate
%     cart_distribution: nb×2 corresponding cartesian coordinates
%        t_distribution: nb×1 corresponding time
%   curv_v_distribution: nb×1 corresponding velocity along the streamline
%   cart_v_distribution: nb×2 corresponding cartesian velocity 
%
%     errout: error messages


% MS 3.0 | 2024-03-13 | INRAE\han.chen@inrae.fr, INRAE\Olivier.vitrac@agroparistech.fr | rev. 2024-03-31


% Revision history
% 2024-03-17 fix help
% 2024-03-27 force nbmax to be at least one
% 2024-03-31 add verbose, errout, fix isempty(s)


%% default values
rbead_default = 1;
l0_default = 0;
verbose_default = true;

%% check arguments
if nargin<5, error('USAGE: traj = fillstreamline2(s,Xgrid,Ygrid,Vxgrid,Vygrid [,rbead,l0])'), end
if nargin<6, rbead = []; end
if nargin<7, l0 = []; end
if nargin<8, verbose = []; end
Xgridsiz = size(Xgrid);
if ~isequal(size(Ygrid),Xgridsiz),  error('Ygrid should be of the same size (%d x %d) as Xgrid',Xgridsiz(1),Xgridsiz(2)), end
if ~isequal(size(Vxgrid),Xgridsiz), error('Vxgrid should be of the same size (%d x %d) as Xgrid',Xgridsiz(1),Xgridsiz(2)), end
if ~isequal(size(Vygrid),Xgridsiz), error('Vygrid should be of the same size (%d x %d) as Xgrid',Xgridsiz(1),Xgridsiz(2)), end
if isempty(rbead), rbead = rbead_default; end
if isempty(l0), l0 = l0_default; end
if isempty(verbose), verbose = verbose_default; end
errmsg = {};
if isempty(s), error('no streamline to fill (uniform velocity field?)'), end

%% pseudo recursion
if iscell(s)
    ns = length(s);
    if ns<2 % only one streamline (no recursion)
        s = s{1};
    else % more than one streamline
        listerrmsg = [];
        screen = ''; t0_ = clock;
        for i=1:ns
            [tmp,errmsg] = fillstreamline2(s{i},Xgrid,Ygrid,Vxgrid,Vygrid,rbead,l0,false);
            dt = etime(clock,t0_); %#ok<DETIM>
            if dt>0.5
                done = 100 * i/ns;
                screen = dispb(screen,'FILLSTREAMLINE2 [%d/%d] fill 2D streamline with %d beads (resolution: %d segments) | done %0.3g %% | elapsed %0.4g s | remaining %0.4g s',...
                    i,ns,length(tmp.t_distribution),size(tmp.streamline,1),done,dt,(100/done-1)*dt);
            end
            if i==1, traj = repmat(tmp,ns,1); else, traj(i) = tmp; end
            for j = 1:length(errmsg)
                if ~ismember(errmsg{j},listerrmsg)
                    screen = ''; dispf('%s\n\t(future occurrences of the same message will not be repeated)',errmsg{j})
                    listerrmsg{end+1} = errmsg{j}; %#ok<AGROW>
                end
            end
        end % next i
        return
    end % ns>1
end

%% check argument (continued)
[n0,d] = size(s);
if d~=2, error('The streamline should be n*2 array'), end
valid = all(~isnan(s),2);
s = s(valid,:);
n = size(s,1);
if n<n0, dispf('FILTSTREAMLINE2: %d points on %d were removed from the streamline',n0-n,n0); end
if n==0, error('the streamline is empty'), end

%% curvilinear coordinate
dl = sqrt(sum(diff(s,1,1).^2,2));
l = cumsum([0;dl],1);
nbmax = max(1,l(end)/(2*rbead)); % total number of beads
%dmean = nbmax/l(end); % mean-density

%% calculate the Tangent 
T = zeros(n,d);
% first point (forward difference)
T(1,:) = s(2,:) - s(1,:);
% middle points (central differences)
T(2:end-1,:) = s(3:end,:) - s(1:end-2,:);
% end point (backward difference)
T(end,:) = s(end,:) - s(end-1,:);
%normalize the tangent
T = T./sqrt(sum(T.^2,2));

%% interpolate the velocity along the streamline
Vxy = [
  interp2(Xgrid,Ygrid,Vxgrid,s(:,1),s(:,2)),...
  interp2(Xgrid,Ygrid,Vygrid,s(:,1),s(:,2))
  ];
v = dot(Vxy,T,2);

%% reverse the streamline if the flow is in the other direction
if mean(v,1,'omitmissing')<0
    errmsg{end+1} = 'FILTSTREAMLINE2: streamline upsidedown detected';
    if verbose, dispf(errmsg{end}), end
    traj = fillstreamline2(flipud(s),Xgrid,Ygrid,Vxgrid,Vygrid,rbead,l0,verbose);
    return
end

%% fix bad v value
ibadv = find(isnan(v));
if ~isempty(ibadv)
    errmsg{end+1} = 'FILTSTREAMLINE2: bad velocity detected (fixed with extrapolation)';
    if verbose, dispf(errmsg{end}), end
    igoodv = setdiff((1:n)',ibadv);
    v(ibadv) = interp1(igoodv,v(igoodv),ibadv,'linear','extrap');
end


%% traveling time (backward: (li+1-li)/Vi) and total time
dt = diff(l)./v(1:end-1);
t = cumsum([0;dt]);

%% condition of steady-state: rate = minimum rate (e.g., # cars/beads per time unit)
% The rate is the same between all li and li+1 and it's determined by the lowest rate.
ratemin = min(1./dt);  %condition of steady state: 

%% condition of uniform density along each segment
density = ratemin*dt./dl; % # cars/beads per length
dnb = density .* dl; % # beads (not scaled)
dnb = [0;dnb/sum(dnb)] * nbmax;  % variation of the number of beads between segment
nb = cumsum(dnb);
nb = nb-interp1(l,nb,l0)+1; % first bead at l0
nb(nb<0) = 0;

%% evaluation positions
ok = nb>=1;
nbok = nb(ok);
lok = l(ok);
if any(nbok==0), error('error at least two positions are identical in the streamline'), end
pos = interp1(nbok,lok,(1:nbmax)');
pos = pos(~isnan(pos));

%% build the trajectory (fake trajectory)
traj = struct( ...
    'streamline',s,...
    'curvilinear',l,...
    'pseudotime',t,...
    'curv_velocity',v,...
    'cart_velocity',Vxy,...
    'curv_distribution',pos,...
    'cart_distribution',interp1(l,s,pos),...
    't_distribution',interp1(l,t,pos),...
    'curv_v_distribution',interp1(l,v,pos), ...
    'cart_v_distribution',interp1(l,Vxy,pos) ...
    );

if nargout>1
    errout = errmsg;
end