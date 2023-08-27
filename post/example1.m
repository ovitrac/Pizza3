% WORKSHOP built on Billy production file (suspended particle in a fluid)
% This example takes the benefit of a Lagrangian description

% INRAE\Olivier Vitrac, Han Chen - rev. 2023-08-25

% MATLAB FILES included in this distribution (either from INRAE/MS or Pizza3 project)

% Main file
% ├── example1.m

% Main features demonstrated
% ├── lamdumpread2.m     ==> the Swiss knife for the manipulating HUGE dump files (version 2 as it is the fork for Pizza3)
% ├── buildVerletList.m  --> the basic tool for statistical physics, it implement an efficient grid search method

% Other dependencies and future workshop extensions (from Pizza3)
% ├── checkfiles.m
% ├── forceHertzAB.m
% ├── forceHertz.m
% ├── forceLandshoff.m
% ├── interp2SPH.m
% ├── interp3SPH.m
% ├── interp3SPHVerlet.m
% ├── kernelSPH.m
% ├── packing.m
% ├── packing_WJbranch.m
% ├── packSPH.m
% ├── partitionVerletList.m
% ├── selfVerletList.m
% ├── updateVerletList.m

% Advanced scripts written for INRAE\William Jenkinson
% ├── KE_t.m
% ├── particle_flux.m
% └── wallstress.m

% Dependencies from MS (INRAE/Molecular Studio) 
% ├── color_line3.m
% ├── dispb.m
% ├── dispf.m
% ├── explore.m
% ├── fileinfo.m
% ├── lastdir.m
% ├── MDunidrnd.m
% ├── plot3D.m
% ├── rootdir.m

% DUMP FILES included in this workshop
% ├── dumps
% │   └── hertz
% │       ├── dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle             <== it is the original dump file
% │       └── PREFETCH_dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle    <-- the split folder
% │           ├── TIMESTEP_000000000.mat                                                                   <-- a split file
% │           ├── TIMESTEP_000050000.mat                                                                   <-- 158 splits (frames)
% │           ├── TIMESTEP_000100000.mat                                                                   <-- the value represent time
%             ... 

%% STEP 1 - PREPROCESSING
% preprocess all the dumps (no need to precise the filenames, only the pattern)
% lamdumpread2 include two PREPROCESSORS 'prefetch' and 'split'
%   prefetch should be preferred for 2D files (relatively smaller number of particles and many time frames)
%       Usage: lamdumpread2('dump.*','prefetch');
%   split should be preferred for large 3D files (large number of particles and a relatively smaller number of time frames)
%       Usage: lamdumpread2('dump.*','split');
%
% note: this step should be used ONLY once, applying again will overwrite the previous splits (frames)

PREPROCESS_FLAG = false; % set it to true to preprocess your data
if PREPROCESS_FLAG
    datafolder = './dumps/';
    lamdumpread2(fullfile(datafolder,'dump.*'),'split'); % for large 3D
end


%% STEP 2 - PROCESS SPECIFICALLY ONE FILE
% we do work with one dump file
datafolder = './dumps/';
dumpfile = 'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_with1SuspendedParticle';
datafolder = lamdumpread2(fullfile(datafolder,dumpfile),'search'); % fix datafolder based on initial guess
defaultfiles = lamdumpread2(fullfile(datafolder,dumpfile),'default'); % default folder (just for check)


%% Extract the types of atoms and the list of available frames
X0 = lamdumpread2(fullfile(datafolder,dumpfile)); % default frame
natoms = X0.NUMBER;
timesteps = X0.TIMESTEPS;
atomtypes = unique(X0.ATOMS.type);
ntimesteps = length(timesteps);

%% Extract the middle frame (i.e. in the middle of the simulation duration)
% X0 is too far from steady state for advanced analysis
Xmiddle = lamdumpread2(fullfile(datafolder,dumpfile),'usesplit',[],timesteps(ceil(ntimesteps/2))); % middle frame

%% Extract the number of beads for each type
% guess the bead type for the fluid (the most populated)
% same guess for the particle (the less populated)
T = X0.ATOMS.type;
natomspertype = arrayfun(@(t) length(find(T==t)),atomtypes);
[~,fluidtype] = max(natomspertype);
[~,solidtype] = min(natomspertype);
walltypes = setdiff(atomtypes,[fluidtype,solidtype]);

%% Estimate the fluid bead size
% This step uses for more accuracy the buildVerletList()
fluidxyz = X0.ATOMS{T==fluidtype,{'x','y','z'}};
fluidid = X0.ATOMS{T==fluidtype,'id'};
nfluidatoms = length(fluidid);
nsolidatoms = natomspertype(solidtype);
% first estimate assuming that the bead is a cube
boxdims = X0.BOX(:,2) - X0.BOX(:,1);
Vbead_guess = prod(boxdims)/natoms;
rbead_guess = (3/(4*pi)*Vbead_guess)^(1/3);
cutoff = 3*rbead_guess;
[verletList,cutoff,dmin,config,dist] = buildVerletList(fluidxyz,cutoff);
rbead = dmin/2;

%% find the direction of the flow (largest dimension)
[~,iflow] = max(boxdims);
iothers = setdiff(1:size(X0.BOX,1),iflow);

%% separate top and bottom walls
vel = {'vx','vy','vz'};
wall1vel = Xmiddle.ATOMS{Xmiddle.ATOMS.type==walltypes(1),vel{iflow}}; wall1vel = wall1vel(1);
wall2vel = Xmiddle.ATOMS{Xmiddle.ATOMS.type==walltypes(2),vel{iflow}}; wall2vel = wall2vel(1);
[wallvel,iwall] = sort([wall1vel,wall2vel],'descend'); % 1 is top (>0), 2 is bottom;
walltypes = walltypes(iwall);

%% find the position of the particle (i.e., obstacle) placed in the flow (from the middle frame)
solidxyz = Xmiddle.ATOMS{T==solidtype,{'x','y','z'}};
solidid = Xmiddle.ATOMS{T==solidtype,'id'};
solidbox = [min(solidxyz);max(solidxyz)]';

%% Pick n particles randomly from the left inlet and included in the mask of the solid (initial frame)
n = 300;
tol = 0.5; % add 40% particles around
selectionbox = NaN(3,2);
selectionbox(iflow,:) = [X0.BOX(iflow,1), X0.BOX(iflow,1)+2*rbead];
selectionbox(iothers,:) =  (1+tol)*(solidbox(iothers,2)-solidbox(iothers,1))*[-1 1]/2 ...
    + (solidbox(iothers,1)+solidbox(iothers,2)) * [1 1]/2;
ok = true(nfluidatoms,1);
for c = 1:3
    ok = ok & (fluidxyz(:,c)>=selectionbox(c,1)) & (fluidxyz(:,c)<=selectionbox(c,2));
end
icandidates = find(ok);
iselected = icandidates(MDunidrnd(length(icandidates),n));
selectedid = fluidid(iselected); % ID to be used
% plot selected particles and other ones
figure, hold on
plot3D(fluidxyz,'b.')
plot3D(fluidxyz(iselected,:),'ro','markerfacecolor','r')
plot3D(solidxyz,'ks','markerfacecolor','k')
view(3), axis equal

%% Generate the trajectory for the selected particles (for all frames)
% All data are loaded with Lamdumpread2() with a single call using 'usesplit'
% each split is loaded individually and only atoms matching selectedid are stored
% all atoms are sorted as selectedid (no need to sort them)
Xselection = lamdumpread2(fullfile(datafolder,dumpfile),'usesplit',[],timesteps,selectedid);

%% Collect the trajectory of the solid particle for all frames
Xsolid = lamdumpread2(fullfile(datafolder,dumpfile),'usesplit',[],timesteps,solidid);

%% Store the trajectories stored in a ntimesteps x 3 x n matrix
% missing data will
[seltraj,selveloc] = deal(NaN(ntimesteps,3,n,'single'));
solidtraj = NaN(ntimesteps,3,nsolidatoms,'double');
goodframes = true(ntimesteps,1);
for it = 1:ntimesteps
    % read fluid atoms
    selframe = Xselection.ATOMS(Xselection.ATOMS{:,'TIMESTEP'} == timesteps(it),:);
    nfoundatoms = size(selframe,1);
    if nfoundatoms<n % incomplete dumped frame (it may happen in LAMMPS)
        dispf('incomplete frame %d/%d (t=%0.4g): %d of %d fluid atoms missing',it,ntimesteps,timesteps(it),n-nfoundatoms,n)
        [~,iatoms,jatoms] = intersect(selectedid,selframe.id,'stable');
        seltraj(it,:,iatoms) = permute(selframe{jatoms,{'x','y','z'}},[3 2 1]);
        goodframes(it) = false;
    else
        seltraj(it,:,:) = permute(selframe{:,{'x','y','z'}},[3 2 1]);
        selveloc(it,:,:) = permute(selframe{:,{'vx','vy','vz'}},[3 2 1]);
    end
    % read solid atoms
    solidframe = Xsolid.ATOMS(Xsolid.ATOMS{:,'TIMESTEP'} == timesteps(it),:);
    nfoundatoms = size(solidframe,1);
    if nfoundatoms<nsolidatoms % incomplete dumped frame (it may happen in LAMMPS)
        dispf('incomplete frame %d/%d (t=%0.4g): %d of %d solid atoms missing',it,ntimesteps,timesteps(it),nsolidatoms-nfoundatoms,nsolidatoms)
        [~,iatoms,jatoms] = intersect(solidid,solidframe.id,'stable');
        solidtraj(it,:,iatoms) = permute(solidframe{jatoms,{'x','y','z'}},[3 2 1]);
        goodframes(it) = false;
    else
        solidtraj(it,:,:) = permute(solidframe{:,{'x','y','z'}},[3 2 1]);
    end
end
% velocity magnitude for the fluid particles
selveloc_magnitude = squeeze(sqrt(sum(selveloc.^2, 2)));

% Interpertation of the solid deformation via Ixx, Iyy, Izz and D
centeredsolidtraj = solidtraj - repmat(nanmean(solidtraj,3),1,1,nsolidatoms);


%% Calculate the approximate major and minor axes (assuming an ellipsoidal shape)

% Building the inertia tensor

% Initialize moments of inertia
Ixx = zeros(ntimesteps, 1);
Iyy = zeros(ntimesteps, 1);
Izz = zeros(ntimesteps, 1);

for it = 1:ntimesteps
    % Extract the 3 x natoms matrix for the current timestep
    coordinates = squeeze(centeredsolidtraj(it, :, :))';
    
    % Compute the covariance matrix
    C = coordinates' * coordinates / nsolidatoms;
    
    % Perform Singular Value Decomposition
    [U, S, ~] = svd(C);
    
    % The principal moments of inertia are on the diagonal of S
    Ixx(it) = S(1, 1);
    Iyy(it) = S(2, 2);
    Izz(it) = S(3, 3);
end
% Calculate the approximate major and minor axes (assuming an ellipsoidal shape)
L = sqrt(5 * (Ixx + Iyy - Izz) / 2); % Major axis (approximation)
B = sqrt(5 * (Ixx - Iyy + Izz) / 2); % Minor axis (approximation)
% Calculate the Taylor deformation 
D = (L - B) ./ (L + B);

figure;
plot(timesteps, D,'-','linewidth',2);
xlabel('Time'); ylabel('D: Taylor deformation');
title({'\rm{' strrep(dumpfile, '_', '\_') '}:' '\bf{Taylor Deformation Over Times}'}, 'Interpreter', 'tex')


%% Plot the trajectories for the selected particles
% streamlines with color representing velocity magnitude
figure, hold on
col = parula(n);
for i=1:n
    jumps = [1;ntimesteps+1];
    for d=1:3
        jumps = unique([jumps;find(abs(diff(seltraj(:,d,i)))>boxdims(d)/2)+1]);
    end
    for j=1:length(jumps)-1
        u = jumps(j):jumps(j+1)-1;
        streamline = seltraj(u, :, i);
        color_line3(streamline(:, 1), streamline(:, 2), streamline(:, 3), selveloc_magnitude(u, i), 'linewidth', 3);
        % faster method but without streamline
        %plot3(traj(u,1,i),traj(u,2,i),traj(u,3,i),'-','linewidth',3,'color',col(i,:))
    end
end
plot3D(solidxyz,'ko','markerfacecolor','k','markersize',5)
view(3), axis equal
title({'\rm{' strrep(dumpfile, '_', '\_') '}:' '\bf{Velocity of Selected Particles Along Streamlines}'}, 'Interpreter', 'tex')
xlabel('x (m)'), ylabel('Y (m)'), zlabel('z (m)')
hc = colorbar; hc.Label.String = 'velocity (m/s)';

