
% Interpretation O. Vitrac - rev. 2024-07-12-31


clearvars -except d it forcedsave PREVIOUSdumpFile dataFile

% Definitions
switch localname
    case 'WS-OLIVIER2023'
        root = 'D:\Sensory_viscosimeter_V0';
    otherwise
        error('Set your machine ''%s'' first',localname)
end
subdatafolder = '/Production/numericalViscosimeter_reference_ulsphBulk_hertzBoundary';
datafolder = fullfile(root,subdatafolder);

% POST template
allDumpFiles = {
    'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with80SuspendedParticle_10Yparticle',
    'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with80SuspendedParticle_1000Yparticle',
    'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with80SuspendedParticle_100000Yparticle'
    };

jumps = 30000*30;
allTimesteps = {
    [0:jumps:10650000],
    [0:jumps:10500000],
    [0:jumps:10530000]
    };

D = 0.001;
BOX_DIMENSIONS = [0 2*D -0.1*D 1.1*D 0 2*D];
BOUNDARIES = [1 0 1]; % 1 if periodic
S = D / 48;
R = 0.5 * S; % radius of the particle (please, be very accurate)
E = 2000; % Hertz contact stiffness
A = 4 * D * D; % Area of the wall
H = 2 * R;
MU = 0.01;
NU = MU/1000;
U = 0.01;

%% choose file, backup file
if ~exist('PREVIOUSdumpFile','var'), PREVIOUSdumpFile = ''; end
if ~exist('dataFile','var'), dataFile = []; end
if ~exist('d','var'), d = 1; end
if ~exist('it','var'), it = 3; end
if ~exist('forcedsave','var'), forcedsave = false; end

% root folder
rootsaveresultfolder = fullfile(datafolder,'RESULTS_OV');
if ~exist(rootsaveresultfolder,'dir'), mkdir(rootsaveresultfolder); end

%% retrieve all frame results (if they exist)
if ischar(d) && strcmp(d,'all')
    fres = explore('*.mat',rootsaveresultfolder,3,'abbreviate');
    fresu = unique({fres.subpath},'stable');
    Elist = str2double(uncell(regexp(fresu,'\_(\d+)Yparticle','tokens')));
    nE = length(Elist);
    leg = arrayfun(@(e) sprintf('E=%s',formatsci(e,'eco')),Elist,'UniformOutput',false);
    formatfig(figure,'figname','resultsOV_meta','PaperPosition',[4.6933    9.2937   11.6133   11.1125]); %'Paperposition')
    hold on
    col = tooclear(parula(nE+1));
    hp = zeros(nE,1);
    nmax = 0;
    for i=1:nE
        k = find(ismember({fres.subpath},fresu(i)));
        nk = length(k);
        T = [];
        for j=1:nk
            tmp = load(fullfile(fres(k(j)).path,fres(k(j)).file));
            tmp.Rcurrent.E = Elist(i) * ones(height(tmp.Rcurrent),1);
            T = [T;tmp.Rcurrent]; %#ok<AGROW>
        end
        T = T(T.timestep>0,:);
        hp(i) = plot(T.nNodes,T.fractalDim,'o','markersize',10,'markeredgecolor',col(i,:),'markerfacecolor',col(i,:));
        nmax= max(nmax,max(T.nNodes));
    end
    n = 1:(nmax+1);
    hp(end+1) = plot(n,(n-1)./n,'k-','linewidth',1);
    uistack(hp(end),"bottom")
    formatax(gca,'fontsize',12)
    xlabel('Number of particles in the cluster')
    ylabel('Fractal dimension (-)')
    hl = legend(hp,[leg;{'linear cluster (theory)'}],'box','off','location','SouthEast');
    print_png(400,fullfile(rootsaveresultfolder,get(gcf,'filename')),'','',0,0,0)
    return
end

%% selected frame
dumpFile = allDumpFiles{d};
timesteps = allTimesteps{d};
DEBUGmode = false; % true to force intermediate plots

% results files for the selected frame
saveresultfolder = fullfile(rootsaveresultfolder,regexprep(dumpFile,'^dump\.',''));
if ~exist(saveresultfolder,'dir'), mkdir(saveresultfolder); end
saveresultfile = fullfile(saveresultfolder,sprintf('graph_it%d_T%d.mat',it,timesteps(it)));
saveresultfig2D = fullfile(saveresultfolder,sprintf('graph2D_it%d_T%d.png',it,timesteps(it)));
saveresultfig3D = fullfile(saveresultfolder,sprintf('graph3D_it%d_T%d.png',it,timesteps(it)));
if exist(saveresultfile,'file') && exist(saveresultfig2D,'file') && exist(saveresultfig3D,'file') && ~forcedsave
    warning('this iteration is discarded, set forcedsave=true or delete the file in\n %s\n\t or use\n delete(''%s'')\n delete(''%s'')\n delete(''%s'')', ...
        saveresultfolder,saveresultfile,saveresultfig2D,saveresultfig3D)
    return
end
close all
resultfigs = [figure; figure];

%% Load file
if ~strcmp(dumpFile,PREVIOUSdumpFile) || isempty(dataFile)
    dataFile = lamdumpread2(fullfile(datafolder, dumpFile), 'usesplit', [], timesteps);
    PREVIOUSdumpFile = dumpFile;
end

% Box size
coords = {'x', 'z', 'y'};
icoords = cellfun(@(c) find(ismember({'x', 'y', 'z'}, c)), coords);
box = dataFile.BOX(icoords, :); % note that the order is given by coords, here {'z'}    {'x'}    {'y'}
boxsize = diff(box, 1, 2);
PBC = [true, false, true]; % true if periodic
PBC = PBC(icoords);
PBCthickness = max(0.4 * boxsize(PBC));

%% First analysis (raw)
selection = dataFile.ATOMS(dataFile.ATOMS.TIMESTEP == timesteps(it) & dataFile.ATOMS.type >= 4, :);
XYZselection = PBCincell(selection{:, coords}, box, PBC);
[XYZimagesONLY, indXimagesONLY, copyimagesIdx] = PBCimages(XYZselection, box, PBC, PBCthickness);

if DEBUGmode
    figure, hold on, plot3D(XYZselection, 'kx'), plot3D(XYZimagesONLY, 'ro'), view(3), axis equal
end
selectionimage = selection(indXimagesONLY, :);
selectionimage{:, coords} = XYZimagesONLY;
selectionimage.type = selectionimage.type + 1000 * copyimagesIdx;
selectionwithimages = [selection; selectionimage];
selectionwithimages.isimages = selectionwithimages.type > 1000;

stypes = unique(selectionwithimages.type); 
nstypes = length(stypes);
[XYZ, stypesfull] = deal(cell(nstypes, 1));
isimages = stypes > 1000;
for i = 1:nstypes
    XYZ{i} = selectionwithimages{selectionwithimages.type == stypes(i), coords};
    stypesfull{i} = selectionwithimages.type(selectionwithimages.type == stypes(i));
end

% Control figure
if DEBUGmode
    figure, hold on, col = parula(nstypes);
    for i = 1:nstypes
        plot3D(XYZ{i}, 'o', 'color', col(i, :));
    end
    view(3), axis equal
end

%% Contact pairwise distance (based on contacts)
others = 1:nstypes;
C = repmat(struct('XYZ', [], 'i', [], 'type', NaN, 'n', NaN, 'center', [], 'jneigh', [], 'tneigh', [], 'dneigh', [], ...
    'isReunited', false, 'deleted', false, 'tobeupdated', true, 'ifull', []), nstypes, 1);
imagestoremove = [];
for i = 1:nstypes
    dispf('\n-- object %d of %d --', i, nstypes)
    j = setdiff(others, i);
    sti = stypes(i);
    stj = cat(1, stypesfull{j});
    XYZothers = cat(1, XYZ{j});
    [VXYZ, ~, ~, ~, dij] = buildVerletList({XYZ{i}, XYZothers}, 2 * H, false, 1);
    found = find(~cellfun(@isempty, VXYZ));
    currentNeigh = [VXYZ{found}];
    currenttyp = stj(currentNeigh);
    currenttypu = unique(currenttyp, 'stable')';
    currentDist = [dij{found}];
    currentDistu = arrayfun(@(t) min(currentDist(currenttyp == t)), currenttypu) / H;
    
    % Record
    C(i).i = i;
    C(i).n = size(XYZ{i}, 1);
    C(i).jneigh = j;
    C(i).type = sti;
    C(i).tneigh = currenttypu;
    C(i).jneigh = arrayfun(@(t) find(stypes == t), currenttypu);
    C(i).dneigh = currentDistu';
    C(i).XYZ = XYZ{i};
    C(i).tobeupdated = false;
end
Cbackup = C;

%% Identify split globules and reunite them
C = Cbackup;
nodes_tobeupdated = [];
for i = 1:nstypes
    dispf('object %d of %d', i, nstypes)
    if (C(i).type < 1000) ... % not an image (images of split globules are managed in the same time)
            || (~C(i).tobeupdated && ~C(i).deleted && ~C(i).isReunited) % not examined image
        [reunitedXYZ, isReunited] = PBCoutcell(XYZ{i}, box, PBC);
    else
        isReunited = false;
    end
    if isReunited
        C(i).XYZ = reunitedXYZ;
        tk = intersect(C(i).tneigh, (1:26) * 1000 + C(i).type); % for each image, we try to reunite them on the size they are
        k = arrayfun(@(t) find(stypes == t), tk);
        
        % Merge entries
        if ~isempty(k)
            XYZtmp = PBCoutcell(cat(1, C(k).XYZ), box, PBC);
            C(k(1)).XYZ = XYZtmp;
            C(k(1)).tobeupdated = true;
            [C(k(2:end)).deleted] = deal(true);
        end
        
        % Set updates
        C(i).tobeupdated = true;
        [C(C(i).jneigh).tobeupdated] = deal(true);
    elseif ~C(i).tobeupdated
        if ~C(i).deleted
            C(i).XYZ = XYZ{i};
        else
            C(i).XYZ = [];
        end
    end
    
    % Default update behavior
    if ~C(i).deleted
        C(i).n = size(C(i).XYZ, 1);
        C(i).ifull = ones(C(i).n, 1) * i;
        C(i).center = mean(C(i).XYZ, 1);
        C(i).isReunited = isReunited;
    else
        C(i).n = 0;
        C(i).center = [];
        C(i).ifull = [];
        C(i).tobeupdated = false;
    end
    
    if C(i).tobeupdated
        nodes_tobeupdated(end + 1) = i; %#ok<SAGROW>
    end
end

%% Update the nodes
for i =  1:nstypes
    if ismember(i,nodes_tobeupdated) % to be updated
        if ~C(i).deleted
            j = setdiff(others, i);
            j = j(~[C(j).deleted]);
            XYZothers = cat(1, C(j).XYZ);
            jothers = cat(1, C(j).ifull);
            [VXYZ, ~, ~, ~, dij] = buildVerletList({C(i).XYZ, XYZothers}, 2 * H, false, 1);
            found = find(~cellfun(@isempty, VXYZ));
            currentNeigh = [VXYZ{found}];
            currentjneigh = jothers(currentNeigh);
            C(i).oldjneigh = C(i).jneigh;
            C(i).jneigh = unique(currentjneigh, 'stable')';
        end
    else
        if ~isfield(C(i),'oldjneigh') || isempty(C(i).oldjneigh)
            C(i).oldjneigh = C(i).jneigh;
        end
    end
    C(i).jneigh = C(i).jneigh(~[C(C(i).jneigh).deleted]);
end


%% Result container ----------------------------
Rtemplate = table('Size',[1 10],...
    'VariableTypes',{'string'    ,'string'  ,'double'  ,'cell','double','double'    ,'cell'    ,'double','cell'       ,'cell'}, ...
    'VariableNames',{'datafolder','dumpfile','timestep','graph' ,'nNodes','fractalDim','XYZ'   ,'counts','nodeDegrees','color'});
Rtemplate.datafolder = datafolder;
Rtemplate.dumpfile = dumpFile;
Rtemplate.timestep = timesteps(it);

%% Build the contact matrix: A
nC = length(C);
A = sparse(nC, nC);
D = sparse(nC, nC);
dmax = max(boxsize);
nmax = max([C.n]);
for i = find([C.type]<1000)
    if ~C(i).deleted
        j = C(i).jneigh;
        j = j(~[C(j).deleted]);
        if any(C(i).jneigh)
            dtmp = vecnorm(cat(1,C(j).center)-C(i).center,2,2)';
            D(i,j) = dtmp;
        else
            dtmp=0;
        end
        if ~isempty(j), j = j(dtmp<=dmax/2); end
        A(i, j) = 1;
        A(j, i) = 1; % Ensure symmetry
    end
end
% Create a table for node information
nodeInfo = table((1:nC)', 'VariableNames', {'OriginalIndex'}); % Create table with original indices
% Add additional properties to the table if needed
nodeInfo.XYZ = cell(nC, 1);
nodeInfo.Degree = zeros(nC, 1);

for i = 1:nC
    nodeInfo.XYZ{i} = C(i).XYZ;
    nodeInfo.Degree(i) = numel(C(i).jneigh); % Example: store the degree (number of neighbors)
end
% Create the graph
G = graph(A);
G.Nodes = nodeInfo;

% Display the graph's nodes table
disp(G.Nodes);


% Create a table for node information
nodeInfo = table((1:nC)', 'VariableNames', {'OriginalIndex'}); % Create table with original indices

% Add additional properties to the table if needed
nodeInfo.XYZ = cell(nC, 1);
nodeInfo.Degree = zeros(nC, 1);

for i = 1:nC
    nodeInfo.XYZ{i} = C(i).XYZ;
    nodeInfo.Degree(i) = numel(C(i).jneigh); % Example: store the degree (number of neighbors)
end

% Create the graph
G = graph(A);
G.Nodes = nodeInfo;

% Display the graph's nodes table
disp(G.Nodes);

% Plot the topology
% Identify unique subgraphs
bins = conncomp(G); % Find connected components
uniqueSubgraphs = containers.Map;
uniqueSubgraphsCounts = containers.Map;

for i = 1:max(bins)
    subG = subgraph(G, bins == i);
    sortedEdges = sortrows(table2array(subG.Edges), 1:2);
    subgraphStr = mat2str(sortedEdges);
    
    if ~isKey(uniqueSubgraphs, subgraphStr)
        uniqueSubgraphs(subgraphStr) = subG;
        uniqueSubgraphsCounts(subgraphStr) = 0;
    end
    uniqueSubgraphsCounts(subgraphStr) = uniqueSubgraphsCounts(subgraphStr) + 1;
end

% Calculate properties
subgraphProperties = [];
subgraphList = keys(uniqueSubgraphs);

for k = 1:length(subgraphList)
    subG = uniqueSubgraphs(subgraphList{k});
    nNodes = numnodes(subG);
    fractalDim = numedges(subG) / numnodes(subG);
    count = uniqueSubgraphsCounts(subgraphList{k});
    % Store node mapping
    nodeIndices = subG.Nodes.OriginalIndex; % Use the OriginalIndex from G.Nodes
    subgraphProperties = [subgraphProperties; struct('graph', subG, 'nNodes', nNodes, 'fractalDim', fractalDim, 'count', count, 'NodeMapping', nodeIndices)];
end

% Sort subgraphs by number of nodes and remove duplicates
[~, sortIdx] = sort([subgraphProperties.nNodes], 'descend');
sortedSubgraphProperties = subgraphProperties(sortIdx);

% Remove duplicates based on fractalDim and structure
uniqueSubgraphProperties = [];
uniqueKeys = containers.Map;

for i = 1:length(sortedSubgraphProperties)
    subG = sortedSubgraphProperties(i).graph;
    fractalDim = sortedSubgraphProperties(i).fractalDim;
    nNodes = sortedSubgraphProperties(i).nNodes;
    uniqueKey = sprintf('%.2f-%d', fractalDim, nNodes); % Unique key based on fractal dimension and number of nodes
    
    if ~isKey(uniqueKeys, uniqueKey)
        uniqueKeys(uniqueKey) = true;
        uniqueSubgraphProperties = [uniqueSubgraphProperties; sortedSubgraphProperties(i)];
    end
end

% Plot unique subgraphs
figure(resultfigs(1))
formatfig(resultfigs(1),'figname',lastdir(saveresultfig2D),'PaperPosition',[-0.3939    3.6647   21.7719   22.393]);
clf(resultfigs(1))
nUnique = length(uniqueSubgraphProperties);
nCols = floor(sqrt(nUnique));
nRows = ceil(nUnique / nCols);
Rcurrent = repmat(Rtemplate,nUnique,1);

% Choose color
cmap = colormap(jet);
normDegree = @(nodeDegrees) (nodeDegrees - min(nodeDegrees)) / (max(nodeDegrees) - min(nodeDegrees)); % Normalize degree
colorDegree = @(nodeDegrees) interp1(linspace(0, 1, size(cmap, 1)), cmap, normDegree(nodeDegrees));

% for each unique case
for idx = 1:nUnique
    subGData = uniqueSubgraphProperties(idx);
    subGData.NodeDetails = G.Nodes(subGData.NodeMapping,:);
    subplot(nRows, nCols, idx);
    
    % Get node degrees
    nodeDegrees = degree(subGData.graph);
    
    % Plot the graph with nodes colored according to their degrees
    Nodelabel = cell(subGData.nNodes,1);
    if DEBUGmode
        for inl = 1:subGData.nNodes
            Nodelabel{inl} = sprintf('\\bf%d\\rm: %d-%d-%d-%d',subGData.graph.Nodes.OriginalIndex(inl), ...
                C(subGData.graph.Nodes.OriginalIndex(inl)).n,...
                C(subGData.graph.Nodes.OriginalIndex(inl)).deleted,...
                C(subGData.graph.Nodes.OriginalIndex(inl)).isReunited,...
                C(subGData.graph.Nodes.OriginalIndex(inl)).tobeupdated);
        end
    else
        Nodelabel = {};
    end

    p = plot(subGData.graph, 'Layout', 'force', 'NodeLabel', Nodelabel);
    p.NodeCData = nodeDegrees;
    
    % Adjust colorbar
    colormap(jet)
    cb = colorbar('eastoutside');
    cb.Label.String = 'Node Degree';
    pos = cb.Position;
    cb.Position = [pos(1) + 4*pos(3), pos(2) + 0.25 * pos(4), 0.25 * pos(3), 0.5 * pos(4)];
    
    % Set color limits ensuring valid range
    if max(nodeDegrees) > 1
        clim([1, max(nodeDegrees)]);
    else
        clim([1, 2]); % Set a default valid range if max degree is 1
    end

    title(sprintf('Nodes: %d, Fractal Dim: %.2f, Count: %d', subGData.nNodes, subGData.fractalDim, subGData.count));

    % store results
    Rcurrent.graph{idx} = subGData.graph;
    Rcurrent.nNodes(idx) = subGData.nNodes;
    Rcurrent.fractalDim(idx) = subGData.fractalDim;
    Rcurrent.count(idx) = subGData.count;
    Rcurrent.nodeDegrees{idx} = nodeDegrees;
    Rcurrent.XYZ{idx} = subGData.NodeDetails.XYZ;
    Rcurrent.color{idx} = colorDegree(nodeDegrees);

end

% global title
sgtitle(sprintf('Time Step: %d',timesteps(it)))

% Save results and print figure
save(saveresultfile,'Rcurrent')
print_png(400,fullfile(saveresultfolder,get(resultfigs(1),'filename')),'','',0,0,0)



%% Identify unique subgraphs
% bins = conncomp(G); % Find connected components
% uniqueSubgraphs = containers.Map;
% uniqueSubgraphsCounts = containers.Map;
% 
% for i = 1:max(bins)
%     subG = subgraph(G, bins == i);
%     sortedEdges = sortrows(table2array(subG.Edges), 1:2);
%     subgraphStr = mat2str(sortedEdges);
% 
%     if ~isKey(uniqueSubgraphs, subgraphStr)
%         uniqueSubgraphs(subgraphStr) = subG;
%         uniqueSubgraphsCounts(subgraphStr) = 0;
%     end
%     uniqueSubgraphsCounts(subgraphStr) = uniqueSubgraphsCounts(subgraphStr) + 1;
% end
% 
% %%Calculate properties
% subgraphProperties = [];
% subgraphList = keys(uniqueSubgraphs);
% 
% for k = 1:length(subgraphList)
%     subG = uniqueSubgraphs(subgraphList{k});
%     nNodes = numnodes(subG);
%     fractalDim = numedges(subG) / numnodes(subG);
%     count = uniqueSubgraphsCounts(subgraphList{k});
% 
%     % Store node mapping
%     nodeIndices = subG.Nodes.OriginalIndex; % Use the OriginalIndex from G.Nodes
%     subgraphProperties = [subgraphProperties; struct('graph', subG, 'nNodes', nNodes, 'fractalDim', fractalDim, 'count', count, 'NodeMapping', nodeIndices)];
% end

% Filter subgraphs with fractal dimension >= 1
filteredSubgraphProperties = subgraphProperties([subgraphProperties.fractalDim] > 0.6);

% Plot filtered subgraphs in 3D
figure(resultfigs(2))
formatfig(resultfigs(2),'figname',lastdir(saveresultfig3D),'PaperPosition',[-0.0000    0.3500   21.0000   29.0000]);
clf(resultfigs(2))
nFiltered = length(filteredSubgraphProperties);
nCols = floor(sqrt(nFiltered));
nRows = ceil(nFiltered / nCols);

for idx = 1:nFiltered
    subGData = filteredSubgraphProperties(idx);
    subplot(nRows, nCols, idx);
    
    % Get node degrees
    nodeDegrees = subGData.graph.Nodes.Degree;
    
    % Plot each globule in the subgraph
    hold on;
    for j = 1:numel(subGData.NodeMapping)
        nodeIdx = subGData.NodeMapping(j);
        if nodeIdx > 0 % Ensure valid index
            globuleXYZ = G.Nodes.XYZ{nodeIdx};
            globuleDegree = nodeDegrees(j);
            
            % Map degree to color
            cmap = colormap(jet);
            clim([1 max(nodeDegrees)]);
            normDegree = (globuleDegree - min(nodeDegrees)) / (max(nodeDegrees) - min(nodeDegrees)); % Normalize degree
            color = interp1(linspace(0, 1, size(cmap, 1)), cmap, normDegree);
            
            % Plot the 3D scatter plot for the globule
            if ~isempty(globuleXYZ)
                scatter3(globuleXYZ(:, 1), globuleXYZ(:, 2), globuleXYZ(:, 3), 36, repmat(color, size(globuleXYZ, 1), 1), 'filled');
            end
        end
    end
    hold off;
    
    % Add colorbar and set limits
    cb = colorbar('eastoutside');
    cb.Label.String = 'Node Degree';
    pos = cb.Position;
    cb.Position = [pos(1) + 5*pos(3), pos(2) + 0.25 * pos(4), pos(3) * 0.25, pos(4) * 0.5];
    
    % Set color limits ensuring valid range
    if max(nodeDegrees) > 1
        clim([1, max(nodeDegrees)]);
    else
        clim([1, 2]); % Set a default valid range if max degree is 1
    end
    axis equal, axis tight, view(3)

    % Title for the plot
    title(sprintf('Nodes: %d, Fractal Dim: %.2f, Count: %d', subGData.nNodes, subGData.fractalDim, subGData.count));

end
% global title
sgtitle(sprintf('Time Step: %d',timesteps(it)))


% Save results and print figure
print_png(400,fullfile(saveresultfolder,get(resultfigs(2),'filename')),'','',0,0,0)

% My old code
% % Interpretation O. Vitrac - rev. 2024-07-12
% 
% % Definitions
% switch localname
%     case 'WS-OLIVIER2023'
%         root = 'D:\Sensory_viscosimeter_V0';
%     otherwise
%         error('Set your machine ''%s'' first',localname)
% end
% subdatafolder = '/Production/numericalViscosimeter_reference_ulsphBulk_hertzBoundary';
% datafolder = fullfile(root,subdatafolder);
% 
% % POST template
% allDumpFiles = {
%     %'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with40SuspendedParticle_10Yparticle',
%     %'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with40SuspendedParticle_1000Yparticle',
%     %'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with40SuspendedParticle_100000Yparticle',
%     'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with80SuspendedParticle_10Yparticle',
%     'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with80SuspendedParticle_1000Yparticle',
%     'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with80SuspendedParticle_100000Yparticle'
%     };
% 
% jumps = 30000*30;
% allTimesteps = {
%     %[0:jumps:10080000],
%     %[0:jumps:9990000],
%     %[0:jumps:10170000],
%     [0:jumps:10650000],
%     [0:jumps:10500000],
%     [0:jumps:10530000]
%     };
% 
% D = 0.001;
% BOX_DIMENSIONS = [0 2*D -0.1*D 1.1*D 0 2*D];
% BOUNDARIES = [1 0 1]; % 1 if periodic
% S = D / 48;
% R = 0.5 * S; % radius of the particle (please, be very accurate)
% E = 2000; % Hertz contact stiffness
% A = 4 * D * D; % Area of the wall
% H = 2 * R;
% MU = 0.01;
% NU = MU/1000;
% U= 0.01;
% 
% % load file
% d = 1;
% dumpFile = allDumpFiles{d};
% timesteps = allTimesteps{d};
% dataFile=lamdumpread2(fullfile(datafolder,dumpFile),'usesplit',[], timesteps);
% 
% % box size
% coords = {'x','y','z'};
% icoords = cellfun(@(c) find(ismember({'x','y','z'},c)),coords);
% box = dataFile.BOX(icoords,:); % note that the order is given by coords, here {'z'}    {'x'}    {'y'}
% boxsize = diff(box,1,2);
% PBC = [true,false,true]; % true if periodic
% PBCthickness = max(0.4*boxsize(PBC));
% 
% %% First analysis (raw)
% it = 3;
% selection = dataFile.ATOMS(dataFile.ATOMS.TIMESTEP==timesteps(it) & dataFile.ATOMS.type>=4,:);
% XYZselection = PBCincell(selection{:,coords},box,PBC);
% [XYZimagesONLY ,indXimagesONLY,copyimagesIdx]= PBCimages(XYZselection,box,PBC,PBCthickness);
% figure, hold on, plot3D(XYZselection,'kx'), plot3D(XYZimagesONLY,'ro'), view(3), axis equal
% selectionimage = selection(indXimagesONLY,:);
% selectionimage{:,coords} = XYZimagesONLY;
% selectionimage.type = selectionimage.type+1000*copyimagesIdx;
% selectionwithimages = [selection;selectionimage];
% selectionwithimages.isimages = selectionwithimages.type>1000;
% 
% stypes = unique(selectionwithimages.type); nstypes = length(stypes);
% [XYZ,stypesfull] = deal(cell(nstypes,1));
% isimages = stypes>1000;
% for i = 1:nstypes
%     XYZ{i} = selectionwithimages{selectionwithimages.type == stypes(i),coords};
%     stypesfull{i} = selectionwithimages.type(selectionwithimages.type == stypes(i));
% end
% % control figure
% figure, hold on, col = parula(nstypes); for i=1:nstypes, plot3D(XYZ{i},'o','color',col(i,:)), end, view(3), axis equal
% 
% 
% %% Contact pair wise distance (based on contacts)
% % i = 45, j = 125
% others = 1:nstypes;
% C = repmat(struct('XYZ',[],'i',[],'type',NaN,'n',NaN,'center',[],'jneigh',[],'tneigh',[],'dneigh',[],...
%     'isReunited',false,'deleted',false,'tobeupdated',true,'ifull',[]),nstypes,1);
% imagestoremove = [];
% for i=1:nstypes
%     dispf('\n-- object %d of %d --',i,nstypes)
%     j = setdiff(others,i);
%     sti = stypes(i);
%     stj = cat(1,stypesfull{j});
%     XYZothers = cat(1,XYZ{j});
%     [VXYZ,~,~,~,dij]  = buildVerletList({XYZ{i} XYZothers},2*H,false,1);
%     found = find(~cellfun(@isempty,VXYZ));
%     currentNeigh = [VXYZ{found}];
%     currenttyp = stj(currentNeigh);
%     currenttypu = unique(currenttyp,'stable')';
%     currentDist = [dij{found}];
%     currentDistu = arrayfun(@(t) min(currentDist(currenttyp==t)),currenttypu)/H;
%     % record
%     C(i).i = i;
%     C(i).n = size(XYZ{i},1);
%     C(i).jneigh = j;
%     C(i).type = sti;
%     C(i).tneigh = currenttypu;
%     C(i).jneigh = arrayfun(@(t) find(stypes==t), currenttypu);
%     C(i).dneigh = currentDistu';
%     C(i).XYZ = XYZ{i};
%     C(i).tobeupdated = false;
% end
% Cbackup = C;
% 
% %% Identify split globules and reunite them
% C = Cbackup;
% nodes_tobeupdated = [];
% for i=1:nstypes
%     dispf('object %d of %d',i,nstypes)
%     if C(i).type<1000
%         [reunitedXYZ, isReunited] = PBCoutcell(XYZ{i}, box, PBC);
%     else
%         isReunited = false;
%     end
%     if isReunited
%         C(i).XYZ = reunitedXYZ;
%         tk = intersect(C(i).tneigh,(1:26)*1000+C(i).type); % for each image, we try to reunite them on the size they are
%         k = arrayfun(@(t)find(stypes==t),tk);
%         % merge entries
%         XYZtmp = PBCoutcell(cat(1,C(k).XYZ),box,PBC);
%         C(k(1)).XYZ = XYZtmp;
%         C(k(1)).tobeupdated = true;
%         [C(k(2:end)).deleted] = deal(true);
%         % set updates
%         C(i).tobeupdated = true;
%         [C(C(i).jneigh).tobeupdated] = deal(true);
%     else
%         if ~C(i).deleted
%             C(i).XYZ = XYZ{i};
%         else
%             C(i).XYZ = [];
%         end
%     end
%     % default update behavior
%     if ~C(i).deleted
%         C(i).n = size(C(i).XYZ,1);
%         C(i).ifull = ones(C(i).n,1)*i;
%         C(i).center = mean(C(i).XYZ,1);
%         C(i).isReunited = isReunited;
%     else
%         C(i).n = [];
%         C(i).center = [];
%         C(i).ifull = [];
%         C(i).tobeupdated = false;
%     end
%     if C(i).tobeupdated
%         nodes_tobeupdated(end+1) = i; %#ok<SAGROW>
%     end
% end
% 
% %% Update the nodes
% for i = nodes_tobeupdated
%     j = setdiff(others,i);
%     XYZothers = cat(1,C(j).XYZ);
%     jothers = cat(1,C(j).ifull);
%     [VXYZ,~,~,~,dij]  = buildVerletList({C(i).XYZ XYZothers},2*H,false,1);
%     found = find(~cellfun(@isempty,VXYZ));
%     currentNeigh = [VXYZ{found}];
%     currentjneigh = jothers(currentNeigh);
%     C(i).oldjneigh = C(i).jneigh;
%     C(i).jneigh = unique(currentjneigh,'stable')';
% end
% 
% %% Build the contact matrix: A
% nC = length(C);
% A = zeros(nC,nC);
% for i=1:length(C)
%     A(i,C(i).jneigh) = 1;
%     A(C(i).jneigh,i) = 1;
% end
% G = graph(A);
% 
