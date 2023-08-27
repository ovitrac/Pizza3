function [verletList,cutoffout,dminout,config,distout] = buildVerletList(X, cutoff, sorton, nblocks, verbose, excludedfromsearch, excludedneighbors)
%BUILDVERLETLIST build the Verlet list of X
%
%   USAGE: verletList = buildVerletList(X [, cutoff, sorton, nblocks, verbose])
%           [verletList,cutoff,dmin,config,distances] = buildVerletList(...)
%           verletList =  buildVerletList(X,config)
%
%   WARNING use selfVerletList to add self in the list
%           verletList =  selfVerletlist(buildVerletList(...))
%
%
%    Inputs:
%                    X: n x 3 matrix containing the coordinates of particles
%                       a table with columns 'x' 'y' 'z'
%                       a cell {Xgrid X} to search the neighbors X around Xgrid
%               cutoff: the cutoff distance for building the Verlet list
%                       by default: cutoff = distribution mode (1000 classes)
%               sorton: flag to force the VerletList to be sorted in the increasing order
%                        by default: sorton = true
%              nblocks: number of blocks to reduce the amount memory required (typically max 8 GB)
%              verbose: set it to false to remove messages
%   excludedfromsearch: nx1 logical array (true if the coordinate does not need to be included in the search).
%    excludedneighbors: nx1 logical array (true if the coordinate is not a possible neihgborà
%
%   Outputs:
%           verletList: n x 1 cell coding for the Verlet list
%                       verletList{i} list all indices j wihtin the cutoff distance
%                       if sorton is used, verletList{i}(1) is the closest neighbor
%               cutoff: cutoff distance as provided or estimated
%                 dmin: minimum distance (off-diagonal term)
%               config: configuration structure to be used with updateVerletList()
%            distances: pair distance matrix (=NaN if nblocks>1)
%
%
%   See also: updateVerletList, partitionVerletList, selfVerletList, interp3SPHVerlet


% MS 3.0 | 2023-03-25 | INRAE\Olivier.vitrac@agroparistech.fr | rev. 2023-05-17


% Revision history
% 2023-03-29 add nblocks and verbose
% 2023-03-31 improved code with validation
% 2023-04-01 return and accept config, accept X as a table
% 2023-05-16 accept {Xgrid X} as input #1 to list neigbors X around a grid (Xgrid)
% 2023-05-17 updated help

%% Constants
targetedNumberOfNeighbors = 100; % number of maximum neighbors expected (it is a maximum guess to be used to estimate a cutoff)
bytes = struct('single',4,'double',8);
DEBUGON = false; % set it to true to activate the debugging mode
tolerance = 0.1; % to be used by updateVerletList

%% Default
sorton_default = true; % default sorton value
verbose_default = true; % default verbosity
memoryloadGB = 8;      % maximum GB to be used

%% Check arguments
if nargin<1, error('one argument is required'); end
if istable(X), X = table2array(X(:,{'x','y','z'})); end % table2array used for safety
if iscell(X)
    if length(X)~=2, error('the first argument should be {Xgrid Xpart}'), end
    Xgrid = X{1};
    X = X{2};
    hasgrid = true;
else
    Xgrid = [];
    hasgrid = false;
end
[n,d] = size(X); % number of particless
typ = class(X);  % class of coordinates
if nargin<2, cutoff   = []; end
if nargin<3, sorton   = []; end
if nargin<4, nblocks  = []; end
if nargin<5, verbose  = []; end
if nargin<6, excludedfromsearch = []; end
if nargin<7, excludedneighbors = []; end
% reuse a previous configuration
if isstruct(cutoff)
    config = cutoff;
    if isfield(config,'engine') && strcmp(config.engine,'buildVerletList')
        if (config.natoms ~= n) || (config.dimensions~=d)
            error('the number of atoms (%d) or/and dimensions (%d) have changed, expected %d x %d',...
                n,d,config.natoms,confif.dimensions)
        end
        cutoff = config.cutoff;
        sorton = config.sorton;
        nblocks = config.nblocks;
        verbose = config.verbose;
      tolerance = config.tolerance;
    else
        error('unrecognized configuration structure')
    end
end
% assign default values if needed
if isempty(cutoff) || cutoff<=0, cutoff = NaN; end
if isempty(sorton), sorton = sorton_default; end
if isempty(verbose), verbose = verbose_default; end
if isempty(nblocks), nblocks = ceil((bytes.(typ) * d * n).^2 / (memoryloadGB*1e9)); end

%% Grid management (look for neighbors around grid points)
if hasgrid
    ngrid = size(Xgrid,1);
    [excludedfromsearch,excludedneighbors] = deal(false(n+ngrid,1));
    excludedfromsearch(1:n) = true;
    excludedneighbors(n+1:end) = true;
    [verletList,cutoffout_,dminout_,config_,distout_] = ...
        buildVerletList([X;Xgrid], cutoff, sorton, nblocks, verbose, excludedfromsearch, excludedneighbors);
    verletList = verletList(n+1:end);
    distout_ = distout_(n+1:end);
    if nargout>1, cutoffout = cutoffout_; end
    if nargout>2, dminout = dminout_; end
    if nargout>3, config = config_; end
    if nargout>4, distout = distout_; end
    return
else
    if isempty(excludedfromsearch), excludedfromsearch = false(n,1); end
    if isempty(excludedneighbors), excludedneighbors = false(n,1); end
    hasexclusions = any(excludedfromsearch) || any(excludedneighbors);
end
if hasexclusions
    ivalid = find(~excludedfromsearch);
    jvalid = find(~excludedneighbors);
    jvalidreverse(jvalid) = 1:length(jvalid); % reverse operator
else
    [ivalid,jvalid] = deal([]); % not used
end

%% main()
% Allocate
verletList = cell(n, 1); % pre-allocate the Verlet list
t__ = clock; t_ = t__;

% Pseudo recursion if nblocks > 1
if (nblocks > 1) && (d == 3) % block splitting limited to 3D

    range = [min(X,[],1); max(X,[],1)]; % [mins;maxs]
    drange = diff(range, 1, 1);
    nBmax = max(2, floor(drange / (2 * cutoff)));
    [~, is] = sort(drange, 'ascend');
    nB = zeros(1, d);
    nB(is(1)) = 1 + min(nBmax(is(1)), floor(nblocks^(1/3))); % number of blocks along the smallest dimension
    nB(is(2)) = 1 + min(nBmax(is(2)), floor(sqrt(nblocks / nB(is(1))))); % idem along the intermediate dimension
    nB(is(3)) = 1 + min(nBmax(is(3)), ceil(nblocks / (nB(is(1)) * nB(is(2))))); % along the longest one
    xB = linspace(range(1, 1) - drange(1) / 20, range(2, 1) + drange(1) / 20, nB(1));
    yB = linspace(range(1, 2) - drange(2) / 20, range(2, 2) + drange(2) / 20, nB(2));
    zB = linspace(range(1, 3) - drange(3) / 20, range(2, 3) + drange(3) / 20, nB(3));
    
    % create meshgrid for block indices
    [ix, iy, iz] = meshgrid(1:nB(1)-1, 1:nB(2)-1, 1:nB(3)-1);
    ix = ix(:); iy = iy(:); iz = iz(:);
    nBall = numel(ix); dist = cell(n, 1); dmin = NaN; cutoffsafe = 1.1 * cutoff; screen = '';

    % for each block
    wasempty = true;
    if verbose, dispf('Build Verlet list by searching in blocks...'), end
    for iBall = 1:nBall
        % points mask of considered entities/particles/beads
        okxyz = (X(:, 1) > (xB(ix(iBall)) - cutoffsafe)) & (X(:, 1) < (xB(ix(iBall)+1) + cutoffsafe)) & ...
                (X(:, 2) > (yB(iy(iBall)) - cutoffsafe)) & (X(:, 2) < (yB(iy(iBall)+1) + cutoffsafe)) & ...
                (X(:, 3) > (zB(iz(iBall)) - cutoffsafe)) & (X(:, 3) < (zB(iz(iBall)+1) + cutoffsafe)); % box + margins
        ind = find(okxyz)';       % their indices (to be used for conversion)
        nind = numel(ind);        % number of entities
        narein = 0;               % default value (to be updated)
        nneighborsforthosein = 0; % counter for their neighbors
        if nind               % some neighbors found
            arein = find(...  % relative indices of those inside the box
                        (X(ind, 1) >= xB(ix(iBall))) & (X(ind, 1) <= xB(ix(iBall)+1)) & ...
                        (X(ind, 2) >= yB(iy(iBall))) & (X(ind, 2) <= yB(iy(iBall)+1)) & ...
                        (X(ind, 3) >= zB(iz(iBall))) & (X(ind, 3) <= zB(iz(iBall)+1)) ...
                    );
            narein = length(arein);   % number of entities in the box
            [verletListtmp, cutoff, dmintmp, ~, disttmp] = buildVerletList(X(ind, :), cutoff, false, 0, false, excludedfromsearch(ind), excludedneighbors(ind));
            dmin = min(dmin,dmintmp);
            for eachin = 1:narein     % for all elements in the temporary Verlet list
                ind_current   = ind(arein(eachin));                % scalar index if the current entity
                ind_neighbors = ind(verletListtmp{arein(eachin)}); % vector of neighbor indices
                nneighborsforthosein = nneighborsforthosein + length(ind_neighbors); % counter of neighbors
                verletList{ind_current} = ind_neighbors;           % update the verlet list
                dist{ind_current} = disttmp{arein(eachin)};        % update the distance matrix
            end % next eachin
        end % if nind
        if verbose
            done = iBall/nBall; currenttime = clock; dt = etime(currenttime,t_);
            if (dt>0.5) || wasempty
                screen = dispb(screen,'[BLOCK %d/%d] %d particles with %d neighbors (%0.1f %% of total considered) | min dist l:%0.3g g:%0.3g | elapsed %0.1f s | done %0.1f %% | remaining %0.1f s',...
                    iBall,nBall,narein,nneighborsforthosein,nind/n*100,dmintmp,dmin,dt,100*done,(1/done-1)*dt);
                wasempty = (nneighborsforthosein==0); t_ = currenttime;
            end
        end


    end % next iBall
    if verbose, dispb(screen,'... done in %0.4g s with %d search blocks | minimum distance %0.4g',dt,nBall,dmin); end

    % DEBUG MODE (comparison without blocks, for internal validation)
    if DEBUGON
        V = verletList; %#ok<UNRCH> 
        V0 = buildVerletList(X, cutoff, sorton, 0, true);
        figure, hold on
        [YB,ZB] = meshgrid(yB,zB); for x=xB, mesh(YB*0+x,YB,ZB,'facecolor','none','edgecolor','r'); end
        [XB,ZB] = meshgrid(xB,zB); for y=yB, mesh(XB,ZB*0+y,ZB,'facecolor','none','edgecolor','r'); end
        [XB,YB] = meshgrid(xB,yB); for z=zB, mesh(XB,YB,XB*0+z,'facecolor','none','edgecolor','r'); end
        plot3D(X((cellfun(@length,V0)-cellfun(@length,V))>0,:),'bs')
        xlabel('x'), ylabel('y'),zlabel('z')
        view(3), axis equal, axis tight
        dispf('if you do not see any bs, it is OK: %d',max(cellfun(@length,V0)-cellfun(@length,V)))
        disp('make a break point here')
    end


else % --------- vectorized code

    % Compute pairwise distances using the built-in pdist2 function
    if hasexclusions
        if verbose, dispf('Calculate the %d x %d pair distances...',ngrid,n), t_ = clock; end %#ok<*CLOCK>
        distances = pdist2(X(ivalid,:), X(jvalid,:));
    else
        if verbose, dispf('Calculate the %d x %d pair distances...',n,n), t_ = clock; end %#ok<*CLOCK>
        distances = pdist2(X, X);
    end
    if verbose, dispf('\t ... done in %0.3g s',etime(clock,t_)), end %#ok<*DETIM> 
    
    % Estimate cutoff if not provided (heuristic method)
    % cutoff is set to match targetedNumberOfNeighbors
    % without exceeding the mode of the distribution based on 1000 classes
    % note: if the number of pair distances is very large, subsampling is applied
    if isnan(cutoff)
        if verbose, dispf('Estimate cutoff...'), t_ = clock; end
        d = triu(distances,1); % all pair distances (can be very large)
        d = d(d>0); dmin = min(d);
        d = d(1:max(1,round(sqrt(length(d))/1000)):end); % subsampling
        [c,d] = hist(d,1000); %#ok<*HIST> 
        % Identify the mode (maximum)
        % counts are smoothed with a moving average over 10 classes
        % figure, plot(d(1:end-1),diff(filtzero(cumsum(c),10)))
        cfit = 1000 * diff(filtzero(cumsum(c),10)) / n;
        d = d(1:end-1) - d(1) + dmin;
        cfit = cfit-cfit(1); % first value (no, meaning)
        [~,imax] = max(cfit);
        % cutoff range
        cutoff_min = 2 * dmin;
        cutoff_max = d(imax);
        % estimate the number of neighbors between cutoff_min and cutoff_max
        % use nearest and cumulated cfit, discard the first 10 data (poorly estimated)
        cutoff = max(cutoff_min,min(cutoff_max,...
            d(nearestpoint(targetedNumberOfNeighbors,cumsum(cfit))+10)));
        if verbose, dispf('\t ... done in %0.3g s (cutoff = %0.6g)',etime(clock,t_),cutoff), end
    end
    
    % Find particle pairs within the cutoff distance
    if verbose, dispf('Find atoms within cuttoff...'), t_ = clock; end
    if hasexclusions
        [rowIndices, colIndices] = find(distances <= cutoff);
        rowIndices = ivalid(rowIndices);
        colIndices = jvalid(colIndices);
    else
        [rowIndices, colIndices] = find(triu(distances <= cutoff, 1));
    end
    if verbose, dispf('\t ... done in %0.3g s',etime(clock,t_)); end
    
    
    % Add the particle indices to the Verlet list
    if verbose ,dispf('Build the Verlet list...'), t_ = clock; end
    [t0,t1] = deal(clock);
    npairs = numel(rowIndices);
    screen = '';
    for idx = 1:npairs
        if mod(idx,100) == 0
            if (etime(clock,t1) > 2) && verbose % every two seconds
                dt = etime(clock,t0);
                done = idx/npairs*100;
                screen = dispb(screen,...
                    'Building the Verlet list [completed: %0.3g%% | elapsed: %0.3g s | remaining: %0.3g s]',...
                    done,dt,dt*(100/done-1));
                t1 = clock;
            end
        end
        i = rowIndices(idx);
        j = colIndices(idx);
        verletList{i}(end+1) = j;
        if ~hasexclusions
            verletList{j}(end+1) = i;
        end
    end
    if verbose
        verletCounts = cellfun(@length,verletList);
        dispf('\t ... done in %0.3g s [min=%d, median=%d, max=%d]',etime(clock,t_),min(verletCounts),round(median(verletCounts)),max(verletCounts))
    end

    % short distances list (efficient), compute the dmin here (faster) // revised 2023-03-29
    dmin = Inf;
    dist = cell(n,1);
    if hasexclusions
        if ~isempty(distances)
            for i_=1:length(ivalid)
                i = ivalid(i_);
                dist{i} = distances(i_,jvalidreverse(verletList{i}));
                dmin = min(dmin,min(dist{i}));
            end
        end
    else
        for i=1:n
            dist{i} = distances(i,verletList{i});
            dmin = min(dmin,min(dist{i}));
        end
    end

end % if nblocks > 2


%% finalization

% Sort the Verlet list if requested
if sorton
    if verbose, dispf('\t Sort the Verlet list...'), t_ = clock; end
    for i=1:n
        [~,u] = sort(dist{i},'ascend');
        j = verletList{i};
        verletList{i} = j(u);
    end
    if verbose, dispf('\t ... done in %0.3g s',etime(clock,t_)), end
end

% Final elapsed time
timerq = etime(clock,t__);

% Return cuttoff if requested
if nargout>1, cutoffout = cutoff; end

% Return dmin if requested
if nargout>2, dminout = dmin; end

if nargout>3
    config = struct( ...
            'engine','buildVerletList', ...
            'elaspedtime',timerq,...
            'natoms',n,...
            'dimensions',d,...
            'nblocks',nblocks,...
            'cutoff',cutoff,...
            'dmin',dmin,...
            'sorton',sorton, ...
            'verbose',verbose,...
            'tolerance',tolerance,...
            'nsamples',ceil(min(200,n*tolerance)) );
end

% Return distances if required
if nargout>4, distout = dist; end

% final display
if verbose, dispf('buildVerletList: all done in %0.3g s for %d atoms',timerq,n), end