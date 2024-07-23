% Script to manage results
% 20240517Yao
% INRAE\Olivier Vitrac

% Comments
% Series 1 difficult to inteerpret but principles are there between frames 1à-14
% Series 2 nothing changed
% Series 3 

%% Definitions
switch localname
    case 'WS-OLIVIER2023'
        root = 'C:\Users\olivi\Seafile\Han\Experiments\Yao';
    otherwise
        root = pwd;
end
result_folder = '20240517Yao';
local = fullfile(root,result_folder);
if ~exist(local,'dir'), error('the folder ''%s'' does not exist'), end

%% load data
if ~exist('raw','var')
    f = explore('*.tif',local,[],'abbreviate');
    nf = length(f);
    raw = repmat(struct('im',[],'finfo',[],'iminfo',[]),nf,1);
    screen = '';
    for i = 1:nf
        raw(i).iminfo = imfinfo(fullfile(f(i).path,f(i).file));
        raw(i).finfo = f(i);
        npages = length(raw(i).iminfo);
        raw(i).im = zeros(raw(i).iminfo(1).Height,raw(i).iminfo(1).Width,raw(i).iminfo(1).BitDepth/8,npages,'uint8');
        for j = 1:npages
            screen = dispb(screen,'[im: %d/%d] load frame %d of %d',i,nf,j,npages);
            raw(i).im(:,:,:,j) = imread(fullfile(f(i).path,f(i).file),j);
        end
    end
end

%% Series 1 
% control
i = 1;
selection = 10:14;
figure, montage(raw(i).im(:,:,:,selection))
title(sprintf('Series %d | frame %d-->%d',i,selection(1),selection(end)))

close all
for j=selection
    figure, imagesc(double(raw(i).im(:,:,2,j))), colorbar
    title(sprintf('Series %d | frame %d',i,j))
end

% select the image
% Summary of results
% frame 10:  r=49.94  r=52.55 (metric = 0.63)
% frame 11:  r=61.78  r=33.85 (metric = 0.33)
% frame 12:  r=59.02  r=54.27 (metric = 0.63)
% frame 13:  r=59.02  r=54.27 (metric = 0.40)
% frame 14:  r=68.6 r=59.27 (metric = 0.86)
nselection = length(selection);
nr = 301; cutoff = 2;
R = repmat(struct('Icrop',[],'xmin',NaN,'xmax',NaN,'ymin',NaN,'ymax',NaN,...
    'r0',NaN,'r1',NaN,'metric',NaN,'r',[],'intensity',zeros(nr-1,1)),nselection,1);
for iselection = 1:nselection
    I = raw(i).im(:,:,2,selection(iselection));      % to show it: figure, imshow(imadjust(rescale(I)))
    % find the sphere (assuming only one)
    filtwidth = 2;                          % default filter width
    found = false; niter = 0;
    while ~found && niter<5
        niter = niter +1;                   % next iteration
        filtwidth = 2 * filtwidth;          % double filter width
        If_ = imgaussfilt(I, filtwidth);    % Apply Gaussian filter
        [centers,radii,metric] = imfindcircles(If_,round([0.3 2]*sqrt(numel(I))/6));
        found = ~isempty(centers);
    end
    [~,ibest] = max(metric);
    dispf('frame %d: %d particles have been found',selection(iselection),length(radii));
    dispf('\t best candidate has a radius of %0.4g pixels (metric=%0.4g)',radii(ibest),metric(ibest));
    If2 = imgaussfilt(I, 2);            % Apply Gaussian filter
    [Gmag, Gdir] = imgradient(If2);     % Calculate gradient, figure, imagesc(Gmag)
    objectiveFunction = @(params) sphereObjective(params, Gmag);      % Define objective function for optimization
    initialGuess = [centers(ibest,:), radii(ibest)]; % Initial guess for [center_x, center_y, radius]
    OptOptions = optimoptions(@lsqnonlin, 'Display', 'iter','MaxFunctionEvaluations',1000);      % Optimization options
    paramsOptimized = lsqnonlin(objectiveFunction, initialGuess, [], [], OptOptions); % Perform optimization
    % paramsOptimized = fminsearch(objectiveFunction, initialGuess); % Perform optimization
    % Extract optimized center and radius
    center_x = paramsOptimized(1);
    center_y = paramsOptimized(2);
    radius = paramsOptimized(3);
    dispf('\t optimized search found %0.4g pixels',radius);
    % Display results
    figure, hold on, imshow(imadjust(rescale(I)));
    viscircles([center_x, center_y], radius, 'EdgeColor', 'r');
    title(sprintf('Series %d, Frame %d of %d (%d): Detected Sphere',i, iselection, nselection, selection(iselection)));
    drawnow
    % store results
    R(iselection).r0 = radii(ibest);
    R(iselection).r1 = radius;
    R(iselection).metric = metric;
    r01 = max(R(iselection).r0,R(iselection).r1);
    R(iselection).xmin = max(1,floor(center_x-cutoff*r01));
    R(iselection).ymin = max(1,floor(center_y-cutoff*r01));
    R(iselection).xmax = min(size(I,2),ceil(center_x+cutoff*r01));
    R(iselection).ymax = min(size(I,1),ceil(center_y+cutoff*r01));
    R(iselection).Icrop = double(I(R(iselection).ymin:R(iselection).ymax,R(iselection).xmin:R(iselection).xmax));
    R(iselection).r = linspace(0,cutoff*r01,nr)';
    [X_,Y_] = meshgrid(R(iselection).xmin:R(iselection).xmax,R(iselection).ymin:R(iselection).ymax);
    R_ = sqrt((X_-center_x).^2 + (Y_-center_y).^2);
    for ir = 1:nr-1
        if ir<nr-1
            ok = (R_>=R(iselection).r(ir)) & (R_<R(iselection).r(ir+1));
        else
            ok = (R_>=R(iselection).r(ir)) & (R_<=R(iselection).r(ir+1));
        end
        R(iselection).intensity(ir) = mean(R(iselection).Icrop(ok),'all');
    end
    R(iselection).intensity(isnan(R(iselection).intensity))=0;
end

figure, hold on
for i=1:length(R)
    stairs(R(i).r(1:end-1)+diff(R(i).r)/2,R(i).intensity)
end

%% Series 3
i = 3;
selection = 56:68;
close all
figure, montage(raw(i).im(:,:,:,selection))
title(sprintf('Series %d | frame %d-->%d',i,selection(1),selection(end)))
for j=selection
    I = raw(i).im(:,:,2,j);
    If = imgaussfilt(I,5);
    figure, imagesc(double(If)), colorbar
    title(sprintf('Series %d | frame %d',i,j))
end


nselection = length(selection);
nr = 301; cutoff = 2;
R = repmat(struct('Icrop',[],'xmin',NaN,'xmax',NaN,'ymin',NaN,'ymax',NaN,...
    'r0',NaN,'r1',NaN,'metric',NaN,'r',[],'intensity',zeros(nr-1,1)),nselection,1);
for iselection = 1:nselection
    I = raw(i).im(:,:,2,selection(iselection));      % to show it: figure, imshow(imadjust(rescale(I)))
    % find the sphere (assuming only one)
    filtwidth = 2;                          % default filter width
    found = false; niter = 0;
    while ~found && niter<5
        niter = niter +1;                   % next iteration
        filtwidth = 2 * filtwidth;          % double filter width
        If_ = imgaussfilt(I, filtwidth);    % Apply Gaussian filter
        [centers,radii,metric] = imfindcircles(If_,round([0.3 2]*sqrt(numel(I))/6));
        found = ~isempty(centers);
    end
    [~,ibest] = max(metric);
    dispf('frame %d: %d particles have been found',selection(iselection),length(radii));
    dispf('\t best candidate has a radius of %0.4g pixels (metric=%0.4g)',radii(ibest),metric(ibest));
    If2 = imgaussfilt(I, 2);            % Apply Gaussian filter
    [Gmag, Gdir] = imgradient(If2);     % Calculate gradient, figure, imagesc(Gmag)
    objectiveFunction = @(params) sphereObjective(params, Gmag);      % Define objective function for optimization
    initialGuess = [centers(ibest,:), radii(ibest)]; % Initial guess for [center_x, center_y, radius]
    OptOptions = optimoptions(@lsqnonlin, 'Display', 'iter','MaxFunctionEvaluations',1000);      % Optimization options
    paramsOptimized = lsqnonlin(objectiveFunction, initialGuess, [], [], OptOptions); % Perform optimization
    % paramsOptimized = fminsearch(objectiveFunction, initialGuess); % Perform optimization
    % Extract optimized center and radius
    center_x = paramsOptimized(1);
    center_y = paramsOptimized(2);
    radius = paramsOptimized(3);
    dispf('\t optimized search found %0.4g pixels',radius);
    % Display results
    figure, hold on, imshow(imadjust(rescale(I)));
    viscircles([center_x, center_y], radius, 'EdgeColor', 'r');
    title(sprintf('Series %d, Frame %d of %d (%d): Detected Sphere',i, iselection, nselection, selection(iselection)));
    drawnow
    % store results
    R(iselection).r0 = radii(ibest);
    R(iselection).r1 = radius;
    R(iselection).metric = metric;
    r01 = max(R(iselection).r0,R(iselection).r1);
    R(iselection).xmin = max(1,floor(center_x-cutoff*r01));
    R(iselection).ymin = max(1,floor(center_y-cutoff*r01));
    R(iselection).xmax = min(size(I,2),ceil(center_x+cutoff*r01));
    R(iselection).ymax = min(size(I,1),ceil(center_y+cutoff*r01));
    R(iselection).Icrop = double(I(R(iselection).ymin:R(iselection).ymax,R(iselection).xmin:R(iselection).xmax));
    R(iselection).r = linspace(0,cutoff*r01,nr)';
    [X_,Y_] = meshgrid(R(iselection).xmin:R(iselection).xmax,R(iselection).ymin:R(iselection).ymax);
    R_ = sqrt((X_-center_x).^2 + (Y_-center_y).^2);
    for ir = 1:nr-1
        if ir<nr-1
            ok = (R_>=R(iselection).r(ir)) & (R_<R(iselection).r(ir+1));
        else
            ok = (R_>=R(iselection).r(ir)) & (R_<=R(iselection).r(ir+1));
        end
        R(iselection).intensity(ir) = mean(R(iselection).Icrop(ok),'all');
    end
    R(iselection).intensity(isnan(R(iselection).intensity))=0;
end

figure, hold on
for i=1:length(R)
    stairs(R(i).r(1:end-1)+diff(R(i).r)/2,R(i).intensity)
end

%% =================================================================
%   the last part of the code is to define functions in a script
%
% =================================================================

function criterion = sphereObjective(params, img)
    sgrad = 8;
    center_x = params(1);
    center_y = params(2);
    radius = params(3);
    [X, Y] = meshgrid(1:size(img,2), 1:size(img,1));
    distFromCenter = sqrt((X - center_x).^2 + (Y - center_y).^2);
    sphereProfile = exp(-((distFromCenter - radius).^2)/(2*(radius/sgrad)^2)); % Example halo profile
    xmin = max(1,floor(center_x - radius - 3 * sgrad));
    xmax = min(size(img,1),ceil(center_x + radius + 3 * sgrad));
    ymin = max(1,floor(center_y - radius - 3 * sgrad));
    ymax = min(size(img,1),ceil(center_y + radius + 3 * sgrad));

    imgd = double(img(ymin:ymax,xmin:xmax));
    %error = imgd/max(imgd,[],'all') - sphereProfile/max(sphereProfile,[],'all');
    %error = sum(error(:).^2);
    localerr = imgd/prctile(imgd(:),95) - sphereProfile(ymin:ymax,xmin:xmax);
    criterion = zeros(size(img));
    criterion(ymin:ymax,xmin:xmax) = localerr;
    criterion = criterion(:);
end