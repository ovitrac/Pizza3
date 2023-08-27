% KE_t for post-treatment of Billy' dump files (3D viscosimeter)
% INRAE\Olivier Vitrac - rev. 2023-03-26
% INRAE\William Jenkinson

% Dependencies (not included in MS, at least not yet)
%   lamdumpread2()    version 2023-03-23 or later
%   buildVerletList() version 2023-03-25 or later
%
% note: be sure Olivier/INRA/Codes/MS is in your Path (MS=Molecular Studio)

% Revision history
% 2023-03-23 RC, early design based on dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_Hertzdiv100_lite
% 2023-03-24 first interaction with Billy
%            the file for design was shifted to dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_Hertzdiv10_lite
% 2023-03-25 implementation of a full Verletlist, automatic identification of fluid-solid contacts without using any
%            particular topology, the template is fully operational and used to plot the number of contacts with time
% 2023-03-06 first implementation of Hertz contacts (to be validated and extended)
%            better figure management (previous results can be reloaded)
% 2023-03-29 [BRANCH - WJ] script taken to template the kinetic energy vs time
% 2023-03-31 WJ - meta data and script are up-to-date for the calculation of Kinetic Energy

%% read datafile

% path definitions (please add your machine name by typing localname in your command window)
switch localname
    case 'LP-OLIVIER2022'
        local = 'C:\Users\olivi\OneDrive - agroparistech.fr\Billy\ProductionSandbox_toOV_23-03-2023';
    case 'LX-Willy2021'
        local = '/Data/billy/Results/Viscosimeter_SMJ_V6/ProductionSandbox_toOV_23-03-2023';
    case 'YOUR MACHINE'
        local = 'it is the path where the dump file is located, results are stored at the sample place';
    otherwise
        error('add a case with your machine name, which is ''%s''',localname)
end
datafile = 'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1_Hertzdiv100_lite';
%datafile = 'dump.ulsphBulk_hertzBoundary_referenceParameterExponent+1';
fulldatafile = fullfile(local,datafile); % concatenate path (local) and data filename
X = lamdumpread2(fulldatafile); % be sure the last version of lamdumpread2() is in the same folder as this script

% result file (to store results)
resultfile = fullfile(local,['RESULT_' datafile '.mat']);

%% Region-based definitions:  Wall and fluid regions
% note that the interface between regions is defined from pair-distances
types = struct('wall',1,'fluid',2);
X.ATOMS.iswall = X.ATOMS.type==types.wall;  % add the column iswall to the table X.ATOMS
X.ATOMS.isfluid = X.ATOMS.type==types.fluid;% add the column isfluid to the table X.ATOMS
X.ATOMS.isundef = ~X.ATOMS.iswall & ~X.ATOMS.isfluid; % add the column isundef to the table X.ATOMS

%% Control frame
% note that the data are stored in data.ATOMS, which is a table with named colums allowing hybrid indexing
nsteps = length(X.TIMESTEP);
icurrenttime = ceil(0.5*nsteps); % index of the control frame (used to set basic definitions before more advanced interpretation)
currenttime = X.TIMESTEP(icurrenttime);
rawframe = X.ATOMS(X.ATOMS.TIMESTEP==currenttime,{'id','type','x','y','z','iswall','isfluid','isundef'});
frame = table2array(rawframe(:,{'x','y','z'})); % generate an array of coordinates

% Build the main Verlet list (for all particles)
% V use the natural indexing instead of rawframe.id
cutoff = 60e-6; % empty or NaN value will force an automatic estimation of cutoff
[V,cutoff,dmin] = buildVerletList(frame,cutoff); % cutoff can be omitted
 
% Build the secondary Verlet lists (highly vectorized code)
% V1 the neighbors of type 2 (fluid) for type 1 atoms (1..n1)
% V2 the neighbors of type 1 (wall) for type 2 atoms (1..n2)
idx1 = find(rawframe.type==1); n1 = length(idx1); % indices of the wall particles in the current frame
idx2 = find(rawframe.type==2); n2 = length(idx2); % indices of the fluid particles in the current frame
V1 = cellfun(@(v) v(rawframe.type(v)==2),V(idx1),'UniformOutput',false); % Verlet list for type 1 in contact with type 2
V2 = cellfun(@(v) v(rawframe.type(v)==1),V(idx2),'UniformOutput',false); % Verlet list for type 1 in contact with type 2
% corresponding distances d1,d2
% some distances can be empty for d2
d1 = arrayfun(@(i) pdist2(frame(idx1(i),:),frame(V1{i},:)),(1:n1)','UniformOutput',false); % evaluate the distance for each idx1(i)
d2 = arrayfun(@(i) pdist2(frame(idx2(i),:),frame(V2{i},:)),(1:n2)','UniformOutput',false); % evaluate the distance for each idx2(i)
d1min = cellfun(@min,d1); % minimum distance for each idx1()
d2min = cellfun(@min,d2,'UniformOutput',false); % minimum distance for each idx2()
[d2min{cellfun(@isempty,d2)}] = deal(NaN); % populate empty distances with NaN
d2min = cat(1,d2min{:}); % we collect all now all distances (since the fluid is moving with respect with the wall)
 
% Identify beads of type 1 (wall) directly in contact with fluids
% this method is general and relies only on pair distances
% the term "contact" is general (vincinity) not a "real" contact as set later
iswallcontact = d1min < 1.5 * dmin;  % condition for a wall particle to be considered possibly in contact with the fluid
isfluidcontact = ~isnan(d2min);      % the condition is less restrictive for the fluid, based on the cutoff distance
V1contact = V1(iswallcontact);       % "contact" Verlet list corresponding to V1
V2contact = V2(isfluidcontact);      % "contact" Verlet list corresponding to V1
iwallcontact = idx1(iswallcontact);
ifluidcontact = unique(cat(2,V1contact{:})); % within cutoff
% 
% control plot
% one color is assigned to each phase
% symbols are filled if they are included in the contact Verlet list
% type figure, rgb() to list all available colors
colors = struct('wall',rgb('Crimson'),'fluid',rgb('DeepSkyBlue'),'none','None');
figure, hold on
plot3D(frame(rawframe.isundef,:),'ko');
plot3D(frame(rawframe.iswall,:),'o','MarkerEdgeColor',colors.wall,'MarkerFaceColor',colors.none);
plot3D(frame(iwallcontact,:),'o','MarkerEdgeColor',colors.none,'MarkerFaceColor',colors.wall);
plot3D(frame(rawframe.isfluid,:),'o','MarkerEdgeColor',colors.fluid,'MarkerFaceColor',colors.none);
plot3D(frame(ifluidcontact,:),'o','MarkerEdgeColor',colors.none,'MarkerFaceColor',colors.fluid);
axis equal, axis tight, view(3)

%% [1:X] INTERPRETATION: counting the number of contact with time
% count the number of fluid beads in contact with wall (within 2*R)
R = 0.5*0.001/48; % radius of the particle (please, be very accurate)
dbond = 2*R; % bond = link between 2 atoms
wall_id  = rawframe.id(iwallcontact);   % extract the ids matching the contact condition in the reference frame
fluid_id = rawframe.id(ifluidcontact);  % idem for the fluid particles within the contact Verlet list
% config setup
E = 2e4 ; % ref:2e6, Hertzdiv10:2e5, Hertzdiv100:2e4
Hertzconfig = struct('name',{'wall','fluid'},'R',R,'E',E); % entries are duplicated if not mentioned

% prepare to calculate pair distances between different beads
pairdist = @(X,Y) triu(pdist2(X,Y),0); % note that the diagonal is included here (since X and Y are different)
ncontacts = zeros(nsteps,1);
KEnergy = zeros(nsteps,1);
[t_,t__] = deal(clock); %#ok<*CLOCK> 
screen = '';
for icurrenttime = 1:nsteps
    currenttime = X.TIMESTEP(icurrenttime);
    % --- some display, to encourage the user to be patient
    if mod(icurrenttime,5)
        if etime(clock,t__)>2 %#ok<*DETIM>
            t__ = clock; dt = etime(t__,t_); done = 100*(icurrenttime-1)/nsteps;
            screen = dispb(screen,'[%d/%d] interpretation [ done %0.3g %% | elapsed %0.3g s | remaining %0.3g s ] ...', ...
                icurrenttime,nsteps,done,dt,dt*(100/done-1));
        end
    end % --- end of display
    Vel = table2array(X.ATOMS((X.ATOMS.TIMESTEP==currenttime) & (X.ATOMS.type==1),{'vx','vy','vz','mass'})); % raw data for the current frame
    V_mag_sq = Vel(:,1).^2 + Vel(:,2).^2 + Vel(:,3).^2;
    KEnergy(icurrenttime) = sum(0.5*Vel(:,4).*V_mag_sq); % sum forces along x
end

% save the data to enable a refresh of the figure without restarting this block
timesteps = X.TIMESTEP;
save(resultfile,'datafile','KEnergy','ncontacts','timesteps','Hertzconfig')
dispf('Results saved (%s):',datafile), fileinfo(resultfile)

%% PLots and figure management

% reload the data
if exist(resultfile,'file'), load(resultfile), end

% plot number of contacts vs. time
contactfigure = figure;
formatfig(contactfigure,'figname',['NumberContact' datafile],'PaperPosition',[1.5000    9.2937   18.0000   11.1125])
plot(timesteps,ncontacts,'linewidth',0.5,'Color',rgb('Crimson'))
formatax(gca,'fontsize',14)
xlabel('time (units)','fontsize',16)
ylabel('Kinetic energy of particles ()','fontsize',16)
wtitle = textwrap({'\bfdump file:\rm';datafile},40);
title(regexprep(wtitle,'_','\\_'),'fontsize',10)

% plot number of Hertz projection along x vs. time
hertzfigure = figure;
formatfig(hertzfigure,'figname',['KineticEnergy' datafile],'PaperPosition',[1.5000    9.2937   18.0000   11.1125])
plot(timesteps,KEnergy,'linewidth',0.5,'Color',rgb('Teal'))
formatax(gca,'fontsize',14)
xlabel('Frame (-)','fontsize',16)
ylabel('Kinetic energy (J)','fontsize',16)
wtitle = textwrap({'\bfdump file:\rm';datafile},40);
title(regexprep(wtitle,'_','\\_'),'fontsize',10)

% save images in all valid formats (including Matlab one, the data can be extracted with this format)
% filenames are identical to the dump file with the proper extension: fig, pdf, png
for myfig = [contactfigure,hertzfigure] % loop over all figures to print
    figure(myfig)
    saveas(gcf,fullfile(local,[get(gcf,'filename') '.fig']),'fig') % fig can be open without restarting the code
    print_pdf(600,[get(gcf,'filename') '.pdf'],local,'nocheck') % PDF 600 dpi
    print_png(600,[get(gcf,'filename') '.png'],local,'',0,0,0)  % PNG 600 dpi
end

