function X=lamdumpread2(filename,action,molecules,itimes,iatoms)
%LAMDUMPREAD2 read on the fly LAMMPS dump files (recognized formats: TEXT='*', TEXT GZIPPED='*.gz', BINARIES='*.bin')
% LAMDUMPRREAD2 is a fork of LAMDUMPREAD (work in progress to implement standards similar to those those used in OVITO)
%
% LAMMPS FORMATS
%               TEXT: editable, readable format (default format in LAMMPS)
%                     loading time: +++++            : file size ++++++++
%       TEXT GZIPPED: as above but compressed (file size reduction 60 %, LAMMPS requires to be compiled with -DGZIP flag)
%                     loading time: ++++++++++++++++ : file size ++++
%             BINARY: proprietary format (leads to the largest files but the fastest to open)
%                     loading time: ++               : file size +++++++++++
% SYNTAX AND OUTPUTS
% ------------------
%   X = lamdumpread(dumpfilename)
%         X.KEYWORD{i} = RECORD (by default)
%         X.KEYWORD(:,:,i) = RECORD when collect is used (or when LAMDUMPSAVE is used);
%           KEYWORD = keyword (e.g. TIMESTEP NUMBEROFATOMS BOXBOUNDS ATOMS ... )
%           RECORD  = array
% OPTIONS FOR ALL FORMATS
% -----------------------
%   X = lamdumpread(dumpfilename [,action, molecules, itimes, iatoms])
%
%          action: keyword among 'collect','count','robot','split', 'default', 'search'
%
%               Actions controlling the way the file filename is read
%                  if 'collect' is used, array data are stored into a 3 dims-arrays instead of a cell array
%                  if 'count' is used, the size of each dataset is determined and not loaded
%                  For binary files, 'collect' is always applied.
%               Actions controlling batches
%                  if 'robot' or 'prefetch' is used, all files are read and a prefetch is created
%                  if 'split' is used, all files are split into small prefetch files
%                  if 'usesplit' is used, split files have higher precedence than prefetch files
%                  if 'forceprefetch' is used, it force the genration of prefetch files even if split files exist)
%                   -- notes --
%                       lampdumpread() generate all prefetch files (high memory footprint)
%                       lamdumpread2('dump.*','split') force split even if prefetch files have been generated
%                       lamdumpread('mydump','usesplit',[],[0 500]) load specifically frames 0 and 500 from split files
%               Actions giving details on dump files and their prefetches
%                   if 'default' is used (same behavior with "#prefetch" as filename), X is a structure with fields:
%                                 prefetch.file giving the prefetch file or anonymous function doing so for any filename fn
%                                 prefetch.folder idem for the prefetch folder
%                                 prefetch.frame is anonymous function @(filname,iframe) or @(itime) giving the filename of each split frame
%                   if 'search' is used the dump file is looked for inside subfolders with the following precedence : splits, prefetech and
%                   original files
%
%       molecules: cell array to build molecules according to X.ATOMS
%                  molecules{i} list all atoms belonging to the ith molecule
%                  X.ATOMS is replaced by X.MOLECULES
%                  where X.MOLECULES{molecule index}(internal atom index,coordinate index,time step index)
%
% OPTIONS FOR TEXT AND GZIPPED FORMATS
% ------------------------------------
%   X = lamdumpread(dumpfilename,[action],[molecules],[itimes],[iatoms])
%          itimes: requested timestep index (if empty, all timesteps are loadted)
%          iatoms: requested atom index; when molecules is used, index of molecules instead
%
% SIMPLE EXAMPLE: based on in.LJ
% ------------------------------
%   X=lamdumpread('dump.atom')
%   X =
%        TIMESTEP: [0 100]
%   NUMBEROFATOMS: [32000 32000]
%       BOXBOUNDS: {[3x2 single]  [3x2 single]}
%           ATOMS: {[32000x5 single]  [32000x5 single]}
%
%   >> simple 3D plot with: plot3(X.ATOMS{2}(:,3),X.ATOMS{2}(:,4),X.ATOMS{2}(:,5),'ro')
%
% ADVANCED EXAMPLES
% -----------------
%  1) Extract the coordinates of 2 molecules consisting in atoms 1:1000 and 3001:4000 respectively
%     for the timestep indices 1 and 11
%     X=lamdumpread('dump.atom.gz','collect',{1:1000 3001:4000},[1 11])
%     X =
%          TIMESTEP: [0 1000]
%     NUMBEROFATOMS: [32000 32000]
%         BOXBOUNDS: [3x2x2 single]
%             ATOMS: [32000 5 11]    << this field is only informative
%         MOLECULES: {2x1 cell}      << Molecular data are stored here ({[1000x3x2 single];[1000x3x2 single]})
%
%   2) Extract the coordinates of a group of atoms [1:1000 3001:4000] for all timesteps
%      X=lamdumpread('dump.atom.gz','collect',{},[],[1:1000 3001:4000])
%      X =
%          TIMESTEP: [0 100 200 300 400 500 600 700 800 900 1000]
%     NUMBEROFATOMS: [32000 32000 32000 32000 32000 32000 32000 32000 32000 32000 32000]
%         BOXBOUNDS: [3x2x11 single]
%             ATOMS: [2000x5x11 single]
%
%   See also: LAMDUMPSAVE, LAMMPSCHAIN, LAMPLOT, GZIPR
%
%
% -------------------------------------------------
% EXAMPLES FROM THE PHD THESIS OF WILLIAM JENKINSON
% -------------------------------------------------
%{
    cd ~/billy/matlab/sandbox/

    % == simple 2D simulation (standard nomenclature) ==
    X = lamdumpread2(fullfile('misc_dumpfiles','dump.wall.2d'))

    % == complex 3D simulation ==
    X = lamdumpread2(fullfile('misc_dumpfiles','dump.backextrusion_v3b')) % nothing inside
    TIMESTEP = X.TIMESTEP;
    A = X.ATOMS(X.ATOMS.type==1,:); % liquid
    B = X.ATOMS(X.ATOMS.type==2,:); % walls
    listidB = B.id(B.TIMESTEP==TIMESTEP(1));
    zB = B.z; idB = B.id; % to reduce memory impact when arrayfun is used
    dzB = arrayfun(@(id) sqrt(mean(diff(zB(idB==id)).^2)),listidB); % mean displacement (long calculations)
    B0 = B(ismember(B.id,listidB(dzB==0)),:); % static cylinder
    B1 = B(ismember(B.id,listidB(dzB>0)),:);  % moving cylinder
    plotback =  @(it) [
    plot3(A.x (A.TIMESTEP ==TIMESTEP(it)), A.y( A.TIMESTEP==TIMESTEP(it)),A.z( A.TIMESTEP==TIMESTEP(it)),'bo','markerfacecolor','b','markersize',5)
    plot3(B0.x(B0.TIMESTEP==TIMESTEP(it)),B0.y(B0.TIMESTEP==TIMESTEP(it)),B0.z(B0.TIMESTEP==TIMESTEP(it)),'r.')
    plot3(B1.x(B1.TIMESTEP==TIMESTEP(it)),B1.y(B1.TIMESTEP==TIMESTEP(it)),B1.z(B1.TIMESTEP==TIMESTEP(it)),'g.')
     ];
    figure, view(3), for it=1:length(TIMESTEP), cla, hold on, plotback(it); title(sprintf('t= %4g',TIMESTEP(it))), drawnow, end

    % == complex 3D simulation ==
    X = lamdumpread2('/home/olivi/billy/lammps/sandbox/dump.backextrusion_v3a');
    TIMESTEP = unique(X.ATOMS_grp01.TIMESTEP);
    A = X.ATOMS_grp01(X.ATOMS_grp01.type==1,:); % liquid
    B = X.ATOMS_grp01(X.ATOMS_grp01.type==2,:); % walls
    listidB = B.id(B.TIMESTEP==TIMESTEP(1));
    zB = B.z; idB = B.id; % to reduce memory impact when arrayfun is used
    dzB = arrayfun(@(id) sqrt(mean(diff(zB(idB==id)).^2)),listidB); % mean displacement (long calculations)
    B0 = B(ismember(B.id,listidB(dzB==0)),:); % static cylinder
    B1 = B(ismember(B.id,listidB(dzB>0)),:);  % moving cylinder
    plotback =  @(it) [
    plot3(A.x(A.TIMESTEP ==TIMESTEP(it)), A.y( A.TIMESTEP==TIMESTEP(it)),A.z( A.TIMESTEP==TIMESTEP(it)),'bo','markerfacecolor','b','markersize',5)
    plot3(B0.x(B0.TIMESTEP==TIMESTEP(it)),B0.y(B0.TIMESTEP==TIMESTEP(it)),B0.z(B0.TIMESTEP==TIMESTEP(it)),'r.')
    plot3(B1.x(B1.TIMESTEP==TIMESTEP(it)),B1.y(B1.TIMESTEP==TIMESTEP(it)),B1.z(B1.TIMESTEP==TIMESTEP(it)),'g.')
     ];
    figure, view(3), cameratoolbar('Show'), for it=1:length(TIMESTEP), cla, hold on, plotback(it); title(sprintf('t= %4g',TIMESTEP(it))), drawnow, end
    
    % profile extraction
    % bottom position of B0
    [~,ibottom] = min(B1.z(B1.TIMESTEP==TIMESTEP(1)));
    zbottom = B1.z(B1.id==B1.id(ibottom));
    figure, plot(TIMESTEP,zbottom), ylabel('z'), xlabel('t')
    % center and radius of B0
    xmean = mean(B0.x(B0.TIMESTEP==TIMESTEP(1)));
    ymean = mean(B0.y(B0.TIMESTEP==TIMESTEP(1)));
    rB0 = max( sqrt( (B0.x(B0.TIMESTEP==TIMESTEP(1)) - xmean).^2 + (B0.y(B0.TIMESTEP==TIMESTEP(1)) - ymean).^2 ) );
    % sample positions
    nr = 200; r = linspace(0,rB0,nr+1);
    rA = sqrt( (A.x - xmean).^2 + (A.y - ymean).^2 );
	nt = length(TIMESTEP);
    vz = zeros(nt,nr);
    for it=1:nt
        okt  = (A.TIMESTEP==TIMESTEP(it)) & (A.z>zbottom(it));
        if any(okt)
            vzt  = A.vz(okt);
            rAt = rA(okt); 
            for ir = 1:nr
                ind = (rAt>=r(ir)) & (rAt<r(ir+1));
                vz(it,ir) = max(0,mean(vzt(ind)));
            end
        end
    end
    itplot = find(any(abs(vz)>0,1),1,'first'):nt; nitplot = length(itplot);
    figure, colororder(jet(nitplot)); plot(r(1:end-1),vz(itplot,:),'-','linewidth',2), xlabel('r'), ylabel('vz')
    
%}    


% MS 2.1 - 22/01/08 - INRA\Olivier Vitrac rev. 2023-08-22

% Revision history
% 05/03/08 add action
% 05/03/08 convert ATOMS field into MOLECULES
% 09/03/08 add an efficient engine for binary files
% 12/03/08 add support for GZ files using gzipr and popenr
% 13/03/08 fix error index associated to matrices with a sintle timestep, impose single precision
% 14/03/08 add itimes, iatoms, generalized counter
% 15/03/08 fix numberofdims (improve rules for row and column vectors)
% 17/04/09 trim data
% 06/10/09 add excludedexpr
% 2021/02/11 implement R2020b standards
% 2021/02/15 format ATOMS as Ovito 3.x
% 2021/02/15a updated version to split automatically broken simulations (with non constant number of atoms)
% 2021/03/03 generalized ITEM: %[] ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_[]
% 2021/03/04 the rule to separate keywords (keys) and their descriptions (variable names) has been customized
%            initially it was thought that keys were uppercase and descriptions lowercase.
%            It is not the case, some variables include letters in capitals (e.g. c_S_s[1])
%            In the future, the implemented rule may suffer some flaws as not all possible variable names have not been explored.
% 2022/11/26 remove \d ([0-9]) from keywords
% 2023-03-23 add robot, prefetch management, remove [] from ITEM
% 2023-04-02 sort files by size before applying the robot (smaller files first)
% 2023-04-04 fix lampdumpread2 or files inclding one single frame
% 2023-04-11 split all dumpfiles larger than 8GB into individual frames
% 2023-04-14 set actions 'prefetch','split','usesplit'
% 2023-04-25 add forceprefetch
% 2023-04-27 add TIMESTEPS, TIMESTEPfirst, TIMESTEPlast when 'usesplit' is used
% 2023-08-22 fixes for workshop on post treatment

% KNOWN LIMITATIONS
% 'collect' works only on standard MD DUMP files, not on SMD/SMD dump files... for now

% Patterns (see textscan for details and the example provided)
% a=textscan('ITEM: NUMBER OF ATOMS',['ITEM: %[ ' 'A':'Z' ']']); a{1}
variablepattern = ['ITEM: %[] ' 'A':'Z' 'a':'z' '0':'9' '_[]'];
numsep = ' ';        % column separator    A = X.ATOMS(X.ATOMS.type==1,:);
datatype = 'single'; % single precision (replace by 'double' to force double precision)
numpattern = '%f32'; % idem (replace by '%f' to force double precision')
maxfilesize = 8e9;   % 8 GB (size before splitting)
%prefetchthreshold = 1e7; % bytes
robotdepth = 100; % maxdepth search
% excludedexpr = '\sid type xu yu zu\s$'; % regular expression % removed 02/14/2021
SPLITPREFIX = 'TIMESTEP_'; % added 2023/04/11
makeprefetch = @(fn) fullfile(rootdir(fn),['PREFETCH_' lastdir(fn) '.mat']); % added 2023/03/23
makesplitdir = @(fn) fullfile(rootdir(fn),['PREFETCH_' lastdir(fn)]); % added 2023/03/23
makesplit = @(fn,itime) fullfile(makesplitdir(fn),sprintf('%s%09d.mat',SPLITPREFIX,itime)); % added 2023/04/11

% Arg check
robot = false;
if nargin<1, robot = true; end
if nargin<2, action = ''; end
if nargin<3, molecules = {}; end
if nargin<4, itimes = []; end
if nargin<5, iatoms = []; end
collecton = strcmpi(action,'collect');
DEBUGON = true; % set DEBUGON to true for debuggind, false otherwise

% automatic robot (added 2023-03-23)
if robot, filename = 'dump.*'; end
if any(filename=='*'), robot = true; end
if strcmpi(filename,'#prefetch'), action='default'; filename=''; end
[datafolder,fn,en] = fileparts(filename);
dumpfile = [fn en];

% action on several files
switch lower(action)
    case 'prefetch'
        robot = true;
        action = '';
    case 'forceprefetch'
        robot = true;
        action = 'robotprefetch';
    case 'split'
        robot = true;
        action = 'robotsplit';
    case 'default'
        % return the default prefetch files
        if isempty(filename)
            X = struct('prefetch',struct('file',makeprefetch,'folder',makesplitdir), ...
                'frame',makesplit);
        elseif ischar(filename)
            X = struct( ...
                'source',filename,...
                'prefetch',struct('file',makeprefetch(filename),'folder',makesplitdir(filename)), ...
                'frame',@(itime) makesplit(filename,itime));
            return
        else
            error('filename should be a char or empty when action=''default''')
        end
    case 'search'
        found = false; completed = false;
        searchmode = {'splitfolder','prefetch','original'};
        isearchmode = 0;
        while ~found && ~completed
            isearchmode = isearchmode+1;
            current_searchmode = searchmode{isearchmode};
            framefolder = '';
            % search
            datafolder_bak = datafolder;
            switch current_searchmode
                case 'original'
                    % We look for the original dump files
                    foundmatchingdumps = explore(dumpfile,datafolder,[],'abbreviate');
                    found = ~isempty(foundmatchingdumps);
                    if found
                        if length(foundmatchingdumps)>1
                            warning('%d copies of the same dump file has been found in ''%s'', the first is used',length(dumpfiles),datafolder)
                            foundmatchingdumps = foundmatchingdumps(1);
                        end
                        datafolder = foundmatchingdumps.path;
                        framefolder = fullfile(datafolder,makesplitdir(dumpfile));
                    end
                case 'prefetch'
                    % We look for the prefetch dump files
                    foundmatchingdumps = explore(lastdir(makeprefetch(dumpfile)),datafolder,[],'abbreviate');
                    found = ~isempty(foundmatchingdumps);
                    if found
                        if length(foundmatchingdumps)>1
                            warning('%d copies of the same dump file has been found in ''%s'', the first is used',length(dumpfiles),datafolder)
                            foundmatchingdumps = foundmatchingdumps(1);
                        end
                        datafolder = foundmatchingdumps.path;
                        framefolder = fullfile(datafolder,makesplitdir(dumpfile));
                    end
                case 'splitfolder'
                    framefilepattern = makesplit(fullfile(datafolder,dumpfile),0);
                    if ~exist(framefilepattern,'file')
                        dispf('Look for ''%s''... (be patient)',dumpfile)
                        frameid = lastdir(framefilepattern);
                        parentframeid = lastdir(rootdir(framefilepattern));
                        foundmatchingdumps = explore(frameid,datafolder,[],'abbreviate');
                        found = ~isempty(foundmatchingdumps);
                        if found
                            foundmatchingdumps = foundmatchingdumps(strcmp(cellfun(@lastdir,{foundmatchingdumps.subpath}','UniformOutput',false),parentframeid));
                            nfoundmatchingdumps = length(foundmatchingdumps);
                            if nfoundmatchingdumps==1
                                datafolder = rootdir(foundmatchingdumps.path);
                                dispf('...found in ''%s''\n',datafolder)
                            elseif nfoundmatchingdumps>1
                                warning('%d dump files are matching, only the first is used',nfoundmatchingdumps)
                                datafolder = rootdir(foundmatchingdumps(1).path);
                            end
                        end
                    end
                    framefolder = makesplitdir(fullfile(datafolder,dumpfile));
                    framefile = makesplit(fullfile(datafolder,dumpfile),0);
                otherwise
                    error('unrecognized searchmode ''%s''',searcurrent_searchmodechmode)
            end % end switch
            if found
                firstframeok = false;
                dispf('The dumpfile ''%s'' has been found with the method ''%s''',dumpfile,current_searchmode)
                dispf('\tin the folder: %s',datafolder);
                if ~strcmp(datafolder,datafolder_bak)
                    dispf('the original search started in %s',datafolder_bak)
                end
                if exist(framefolder,'dir')
                    dispf('The frame (split) folder is: %s',framefolder)
                end
                if exist(framefile,'file')
                    dispf('The first frame (split) is located in: %s',framefile)
                    firstframeok = true;
                end
            end
            completed = strcmp(current_searchmode,searchmode{end});
        end % end while
        if ~found,
            error('the dumpfile ''%s'' does not exist in ''%s''',dumpfile,datafolder_bak)
        else
            if firstframeok % we return the first frame (default behavior)
                X = lamdumpread2(fullfile(datafolder,dumpfile),'usesplit');
            end
            X = datafolder;
            return
        end
end % swicth action

% Pseudo-recursion on many files
if robot
    if isempty(datafolder), robotpath = pwd; else, robotpath = datafolder; end
    robotfile = dumpfile;
    dumpfiles = explore(robotfile,robotpath,robotdepth,'abbreviate');
    dumpfiles = dumpfiles(cellfun(@isempty,regexp({dumpfiles.ext},'gz$','once')));
    [~,ind] = sort([dumpfiles.bytes],'ascend'); dumpfiles = dumpfiles(ind);
    nfiles = length(dumpfiles);
    for ifile = 1:nfiles
        currentdumpfile = fullfile(dumpfiles(ifile).path,dumpfiles(ifile).file);
        if ~exist(makeprefetch(currentdumpfile),'file') || strcmpi(action,'robotsplit')
            dispf('LAMPDUMPREAD AUTO %d of %d',ifile,nfiles)
            if DEBUGON
                lamdumpread2(currentdumpfile,action)
            else
                try
                    lamdumpread2(currentdumpfile,action)
                catch ME
                    warning(ME.message)
                    dispf('ERROR to read the file ''%s'' in ''%s''',dumpfiles(ifile).file,dumpfiles(ifile).path)
                end
            end
        else
            dispf('%d:%d %s',ifile,nfiles,currentdumpfile)
            fileinfo(makeprefetch(currentdumpfile))
        end
    end
    return
end

% display help
if strcmp(filename,''), error('syntax: X=lamdumpread(dumpfilename,[collect],[molecules],[itimes],[iatoms])'), end 

% Manage forcesplit and usesplit
forcesplit = strcmpi(action,'robotsplit');
forceprefetch = strcmpi(action,'robotprefetch');
usesplit = strcmpi(action,'usesplit');


% prefetch (added 2023-03-23)
prefetchfile = makeprefetch(filename);
hasprefetchfile = exist(prefetchfile,'file');
hasprefetchfolder = exist(makesplitdir(filename),'dir');

if (hasprefetchfile && ~forcesplit && ~usesplit) || (hasprefetchfile && ~hasprefetchfolder) % fixed on 2023-08-21 (hasprefetchfile added)
    dispf('Load prefetch file (instead of ''%s'')...',filename), fileinfo(prefetchfile), t0=clock;
    load(prefetchfile)
    dispf('...loaded in %0.3g s',etime(clock,t0)) %#ok<*CLOCK,*DETIM> 
    return
elseif (hasprefetchfolder && ~forcesplit && ~forceprefetch) || usesplit % prefetch dir (added 2023-03-11)
    if isempty(itimes)
        tmplist = explore([SPLITPREFIX '*.mat'],makesplitdir(filename),0,'abbreviate');
        itimes = str2double(strrep({tmplist.name},SPLITPREFIX,''))';
        ncol = 10;
        nrow = ceil(length(itimes) / ncol);
        itimes_cell = cell(nrow, ncol);
        for i = 1:length(itimes)
            [row, col] = ind2sub([nrow, ncol], i);
            itimes_cell{row, col} = sprintf('%9d', itimes(i));
        end
        dispf('The prefetch is split in several files.\n%d TIMESTEPS are availble:',length(itimes))
        for col = 1:ncol, fprintf('  Column %02d\t', col); end, fprintf('\n');
        for row = 1:nrow, for col = 1:ncol, fprintf('%s\t', itimes_cell{row, col}); end, fprintf('\n'); end
        dispf('Choose the time step you are interested in.\nOnly the first one is returned for now.')
        itimes_all = itimes;
        itimes = itimes(1);
    else
        itimes_all = [];
    end
    t0 = clock;
    for it = 1:numel(itimes)
        tmpfile = makesplit(filename,itimes(it));
        if ~exist(tmpfile,'file'), error('the time step %d does not exist (%s)',itimes(it),filename); end
        dispf('Use the prefetch (split: TIMESTEP %d) folder (instead of ''%s'')...',itimes(it), filename), fileinfo(tmpfile)
        tmp = load(tmpfile);
        if ~isfield(tmp,'X'), error('corrupted frame'), end
        if isfield(tmp.X,'description')
            ttmp = tmp.X.TIMESTEP*ones(tmp.X.NUMBER,1,class(tmp.X.ATOMS));
            vtmp = unique(strsplit(tmp.X.description.ATOMS,' '),'stable');
            if isempty(iatoms)
                tmp.X.ATOMS = array2table([ttmp tmp.X.ATOMS],'VariableNames',[{'TIMESTEP'} vtmp]);
            else
                [~,~,jatoms] = intersect(iatoms,tmp.X.ATOMS(:,ismember(vtmp,'id')),'stable');
                 tmp.X.ATOMS = array2table([ttmp(jatoms) tmp.X.ATOMS(jatoms,:)],'VariableNames',[{'TIMESTEP'} vtmp]);
            end
            oktable = true;
        else
            oktable = false;
        end
        if it==1
            X = tmp.X;
        else
            if oktable
                X.TIMESTEP(end+1) = tmp.X.TIMESTEP;
                if isfield(tmp.X,'TIME'), X.TIME(end+1) = tmp.X.TIME; end
                X.ATOMS = [X.ATOMS;tmp.X.ATOMS];
            else
                X(end+1) = tmp.X; %#ok<*AGROW>
            end
        end
    end
    dispf('...loaded in %0.3g s',etime(clock,t0))
    X.TIMESTEPS = itimes_all';
    X.TIMESTEPfirst = min(itimes_all);
    X.TIMESTEPlast = max(itimes_all);
    return    
end

% return an error if the original file does not exist
if ~exist(filename,'file'), error('the file ''%s'' does not exist',filename), end

% Check extensions: .bin (binary mode) and .gz (text mode but gzipped)
[~,~,de] = fileparts(filename);
if strcmpi(de,'.bin'), fprintf('\n>> Switch to binary <<\n\n'), X = dumpbinary(filename,1,molecules); return, end
isgz = strcmpi(de,'.gz'); if isgz, fprintf('\n>> Switch to GZIPPED text mode <<\n\n'), end
%d = dir(filename);
counton   = strcmpi(action,'count'); % || (d.bytes>prefetchthreshold);
nmol      = length(molecules);

% detect large file
if ~isgz
    nfo = dir(filename);
    islargefile = (nfo.bytes>maxfilesize) || forcesplit;
else
    islargefile = false;
end
if islargefile && ~exist(makesplitdir(filename),'dir'), mkdir(makesplitdir(filename)); end
ipartlargefile = 0;


% PREALLOCATE when collect is active
if collecton
    fprintf('Count timesteps for all fields...\nPreallocation to preserve memory usage...\nThe file will be read twice.\n')
    fprintf('DATA format: ''%s'' [%s]\n',datatype,numpattern)
    clock0 = clock;
    if isempty(itimes) || isempty(iatoms)
        X = lamdumpread(filename,'count',molecules,itimes,iatoms); % whole procedure
    else % the structure is assumed to be known (bad prediction will generate an error)
        fprintf('Assume a general DUMP format (faster)\nBad parameters for iatoms and itimes will result in an error.\n\n')
        ntimes = length(itimes); natoms = length(iatoms);
        X = struct('TIMESTEP',[1 1 ntimes],...
            'NUMBEROFATOMS',[1 1 ntimes],...
            'BOXBOUNDS',[3 2 ntimes],...
            'ATOMS',[natoms 5 11]);
    end
    if isempty(itimes), fprintf('\nFOUND records: [size]\n\n'), else fprintf('\nFOUND records: [size]\n between timesteps [%d %d]\n',min(itimes),max(itimes)), end
    disp(X)
    restart=true; iserrorgenerated = false;
    key=fieldnames(X)'; siz = X.(key{1});
    if isempty(itimes), ntimes = siz(3); else ntimes=length(itimes); end
    if isempty(iatoms), natoms = siz(1); else natoms = length(iatoms); end
    while restart
        try
            for key=fieldnames(X)'
                siz = X.(key{1});
                if isempty(itimes), ntimes = siz(3); else ntimes=length(itimes); end
                if nmol && strcmp(key{1},'ATOMS') % molecules assembling
                    if isempty(iatoms), listofmol = 1:nmol; else listofmol = iatoms; end
                    if (max(listofmol)>nmol) || (min(listofmol)<1), iserrorgenerated=true; error('invalid molecules index'), end
                    X.MOLECULES = cell(length(listofmol),1);
                    for imol=listofmol, X.MOLECULES{imol} = zeros(length(molecules{imol}),3,ntimes,datatype); end
                else
                    if strcmp(key{1},'ATOMS')
                        if isempty(iatoms), natoms = siz(1); else natoms = length(iatoms); end
                        X.(key{1}) = zeros(squeezedims([natoms siz(2) ntimes]),datatype);
                    else % other fields
                        X.(key{1}) = zeros(squeezedims([siz(1:end-1) ntimes]),datatype);
                    end
                end
            end
            restart = false;
        catch ME
            if iserrorgenerated, rethrow(ME), end
            fprintf('Insifficient memory for %d timesteps ranged between [%d %d] and %d atoms ranged between [%d %d]\n',ntimes,min(itimes),max(itimes),natoms,min(iatoms),max(iatoms))
            disp('a 1 for 2 decimation rule wil be tented')
            if length(itimes)==1 || isempty(itimes), rethrow(ME), end
            itimes = unique(round(linspace(min(itimes),max(itimes),round(ntimes/2)))); % decimation
        end % try/catch
    end % wend
    fprintf('''%s'' preallocated in %0.4g s\n\n',filename,etime(clock,clock0))
    counton = false;
else % no preallocation (efficient but less usefull for interpretation)
    X = [];
end

% fast scan file based on BLOCKS and PATTERNS (low memory usage)
disp('LAMMPS DUMP file...'), fileinfo(filename)
start = clock;
if isgz, fid = gzipr(filename); else fid = fopen(filename,'r','n','US-ASCII'); end
foundrecord = true;
eof = false;
[RAWKEYLIST,KEYLIST,DESRCLIST] = deal({}); KEYOCC  = []; %raw counters (replace pos.('key') when it is not defined)
CURRENTOCC = -Inf; % number of occurence
if isempty(itimes), itimesmax=Inf; else itimesmax = max(itimes); end
screen=''; isfirstframe = true; nodisplay = false; tsplit = clock;
while foundrecord && ~eof
    % look for the keyword ITEM (stop when it does not match, i.e. numerical data
    if isgz, [key,eof,row] = textscanp(fid,variablepattern,'delimiter','\n');
    else key = textscan(fid,variablepattern,'delimiter','\n'); end
    if ~isempty(key) && ~isempty(key{1})
        if isfirstframe && any(strcmp(key{1},{'TIME','TIMESTEP'})), keyforfirstframe = key{1}; isfirstframe = false; end
        if islargefile && strcmp(key{1},keyforfirstframe) && ~isempty(X) && isfield(X,keyforfirstframe)
            X.description = cell2struct(DESRCLIST',KEYLIST');
            X.nfo = nfo; ipartlargefile = ipartlargefile +1;
            save(makesplit(filename,X.TIMESTEP),'X')
            [~,nfotxt] = fileinfo(makesplit(filename,X.TIMESTEP),'',false);
            screen = dispb(screen,'[%d:%d] split in %0.3g s ==> %s',ipartlargefile,X.TIMESTEP,etime(clock,tsplit),nfotxt);
            X = []; nodisplay = true; tsplit = clock;
        end
        %key{1}{1} = regexprep(key{1}{1},excludedexpr,''); % remove undesirable set of characters (for new version of LAMMPS may 2009)
        % counters based on raw names
        if ~ismember(key{1}{1},RAWKEYLIST)
            RAWKEYLIST{end+1} = key{1}{1}; %#ok<AGROW>
            KEYLIST{end+1} = regexprep(key{1}{1},{'[a-z_]','\d','\s*$','\s+','_[A-Z]?\[\d+\]','_','[\[\]]'},{'','','','_','',' ',''}); %#ok<AGROW> % only A-Z characters are kept
            DESRCLIST{end+1} = regexprep(key{1}{1},{'^[A-Z\s]*([a-z])','^\s*','\s*$',KEYLIST{end}},{'$1','','',''}); %#ok<AGROW> % '[A-Z]', the remaining characters are kept for description
            KEYLIST{end} = regexprep(KEYLIST{end},{'\s+','_[A-Z]*'},{'_',''}); % remove residual _XX names (e.g., _VM)
            KEYOCC(end+1)=0; %#ok<AGROW>
        end % create the counter if it does not exist
        ikey = find(ismember(RAWKEYLIST,key{1}{1})); %key index
        KEYOCC(ikey)=KEYOCC(ikey)+1; %#ok<AGROW> % increment the counter (not order dependent)
        % keyname standardization
        %key = strrep(key{1}{1},' ','_');        % remove all spaces
        key = KEYLIST{ikey};
        if ~isgz                                % read the next line
            row = '';
            while isempty(row) && ~feof(fid)    % while the current line is not valid
                currentpos = ftell(fid);        % current position in the file
                row = fgetl(fid);               % read a single line/row to identify the pattern
            end
        end
        n = length(find(strtrim(row)==numsep)); % number of data per row
        if ~isempty(row)                        % records were found
            % Read values
            if ~counton && ~nodisplay, display(1.001,'[%d] %s reading...',KEYOCC(ikey),KEYLIST{ikey}); end
            clock1 = clock;
            if isgz
                [val,eof] = textscanp(fid,[repmat([numpattern numsep],1,n) numpattern],'delimiter','\n','CollectOutput', 1);
            else
                fseek(fid,currentpos,'bof');    % go back to the last position
                val = textscan(fid,[repmat([numpattern numsep],1,n) numpattern],'delimiter','\n','CollectOutput', 1); % read the values
            end
            % Timestep counter
            if CURRENTOCC<KEYOCC(ikey), CURRENTOCC=KEYOCC(ikey); if counton, screen=dispb(screen,'Preallocate TIMESTEP index: %d ',CURRENTOCC); end, end
            if CURRENTOCC>itimesmax, eof = true; end % force end of file
            % Check validity of the current time step, sort ATOMS values, verbosity
            % Note that a robust/clean counter is used when a PREALLOCATION is performed, if not a raw counter (field order dependent) is used
            if ~counton
                if isempty(itimes), validtime = true; storeposition = KEYOCC(ikey);
                else
                    validtime = ismember(KEYOCC(ikey),itimes);
                    if validtime, storeposition = find(itimes==KEYOCC(ikey)); storeposition=storeposition(1); end
                end
                if ~nodisplay, if numel(val{1})<2, display(1.002,'= %0.6g',val{1}), else, display(1.002,'= %s%s array',sprintf('%dx',size(val{1})),char(8)),end, end
                if strcmp(key,'ATOMS') && validtime, if ~nodisplay, display(1.003,'>>sorting'), end, [~,ia] = sort(val{1}(:,1)); val{1} = val{1}(ia,:); end
                if ~nodisplay, display(1.004,'... end in %0.3g s\n',etime(clock,clock1)); end
            end
            % Assign values
            if counton                          % count values (if requested)
                if isfield(X,key), X.(key)(end)=X.(key)(end)+1; else X.(key)=[size(val{1}) 1]; end
            elseif collecton % collect
                if strcmp(key,'ATOMS') && nmol % replace ATOMS by MOLECULES
                    key = 'MOLECULES';
                    if validtime
                        if isempty(iatoms), listofmol = 1:nmol; else, listofmol = iatoms; end
                        for imol = listofmol, X.(key){imol}(:,:,storeposition)=val{1}(molecules{imol},3:5); end
                    end
                elseif validtime
                    if numberofel(X.(key),val{1})==numel(val{1})
                        switch numberofdims(val{1})
                            case 0, X.(key)(storeposition) = val{1};
                            case 1, X.(key)(:,storeposition)  = val{1}(:);
                            case 2, X.(key)(:,:,storeposition)= val{1};
                        end
                    end
                end
            elseif validtime
                if ~isfield(X,key), X.(key) = val{1}; % create a new keyword
                elseif ~iscell(X.(key))     % convert to a cell array to store results from several records
                    if numel(val{1})==1, X.(key)(end+1) = val{1};
                    else                 X.(key) = {X.(key) val{1}}; %#ok<*SEPEX>
                    end
                else                                  % append records
                    if numel(val{1})==1, X.(key)(end+1)=val{1};
                    else                 X.(key){end+1}=val{1};
                    end
                end
            end % count on
        else                                % likely corrupted file
            foundrecord = false;
        end
    else
        foundrecord = false;
    end
end
if isgz, try textscanp(fid); catch ME, fprintf('*-*- ERROR -*-*'), rethrow(ME), end, gzipr(fid); else fclose(fid); end
fprintf('... end in %0.3g s\n',etime(clock,start))
if isempty(X), disp('It seems not to be a valid file'), return, end

% last frame for large file
if islargefile && ~isempty(X)
    X.description = cell2struct(DESRCLIST',KEYLIST');
    X.nfo = nfo;
    save(makesplit(filename,X.TIMESTEP),'X')
    nfotxt = fileinfo(makesplit(filename,X.TIMESTEP),'',false);
    dispb(screen,'[last=%d] %d split files completed in %0.3g s\n in\t%s\n',X.TIMESTEP,ipartlargefile+1,etime(clock,start),nfotxt.path);
    return
end

%% rearrangement of outputs to match description, when possible
% added INRAE\Olivier Vitrac, 2021-02-15 (RC)
X.description=cell2struct(DESRCLIST',KEYLIST');

if length(X.TIMESTEP)>1 % more than one frame
    iseries = find(~cellfun(@isempty,DESRCLIST));
    if isempty(iseries), return; end
    nseries = length(iseries);
    
    for j=1:nseries        
        
        tmp = unique(strsplit(DESRCLIST{iseries(j)},' '),'stable');
        siz = size(X.(KEYLIST{iseries(j)}){1});
        if (siz(2)==length(tmp)) && strcmpi(KEYLIST{iseries(j)},'ATOMS') % === ATOMS ===
            nt = length(X.(KEYLIST{iseries(j)}));
            na = zeros(nt,1);
            for it=1:nt, na(it) = size(X.(KEYLIST{iseries(j)}){it},1); end
            grps = unique(na,'stable'); ngrps = length(grps);
            for igrp = 1:ngrps
                jgrp = find(na==grps(igrp)); njgrp = length(jgrp);
                tmp2 = reshape(permute(cat(length(siz)+1,X.(KEYLIST{iseries(j)}){jgrp}),[1 3 2]),[grps(igrp)*njgrp siz(2)]);
                t = ones(grps(igrp),1,'single')*X.TIMESTEP(jgrp); % time steps
                tmp2 = [t(:) tmp2]; %#ok<AGROW>
                if ngrps==1, suffix=''; else, suffix=sprintf('_grp%02d',igrp); end
                X.([KEYLIST{iseries(j)} suffix]) = array2table(tmp2,'VariableNames',[{'TIMESTEP'} tmp]);
            end
            if ngrps>1, X = rmfield(X,'ATOMS'); end
        elseif prod(siz)>max(siz) && strcmpi(KEYLIST{iseries(j)},'BOX') % array %% === BOX_BOUNDS ===
            try
                X.(KEYLIST{iseries(j)}) = cat(length(siz)+1,X.(KEYLIST{iseries(j)}){:});
                siz = size(X.(KEYLIST{iseries(j)}));
                if ndims(X.(KEYLIST{iseries(j)}))==3
                    X.(KEYLIST{iseries(j)}) = reshape(permute(X.(KEYLIST{iseries(j)}),[3 2 1]),[siz(3) siz(1)*siz(2)]);
                end
            catch
                fprintf('\nWARNING: unable to collect all data for ''%s''\n\t The likely cause is incompatible size.\n',KEYLIST{iseries(j)});
            end
        end
        
        
    end % next j (series)
    
elseif isfield(X,'ATOMS')
    
    
end % if nframes > 1

% save prefetch - added 2023-03-23
dispf('save prefetch file (for ''%s'')...',filename), t0=clock;
save(prefetchfile,'X','filename')
if ~exist(prefetchfile,'file')
    switch73 = true;
else
    details = dir(prefetchfile);
    switch73 = details.bytes<1000;
end
if switch73
    dispf('--> too large file for default save format, switch to v7.3 (HDF5) format')
    save(prefetchfile,'X','filename','-v7.3');
end
fileinfo(prefetchfile)
dispf('...saved in %0.3g s',etime(clock,t0))




end % ENDFUNCTION

%% =====================================================
% PRIVATE FUNCTIONS
% ====================================================

% Display function with id manager
function display(id,varargin)
    % manage display at prescribed intervals with an id manager
    % id = 2.001 means event=2, message instance = 1;
    persistent TDISP
    if isempty(TDISP), TDISP = struct('t',clock,'updateinterval',0.5,'idevent',NaN,'idinstance',NaN); end
    t = clock; dt = etime(t,TDISP.t);
    idevent = floor(id); idinstance = round(1000*(id-idevent));
    if TDISP.idevent==idevent                % same event 
        forced = (idinstance>TDISP.idinstance);% the instances are assumed linked if incremented
    else
        forced = false;
    end
    if ((dt>TDISP.updateinterval) && (idinstance==1)) || forced
        TDISP.t = t;
        TDISP.idevent = idevent;
        TDISP.idinstance = idinstance;
        fprintf(varargin{:});
    end
end % ENDFUNCTION

% BASIC FUNCTIONS to work multidimensional arrays (replace SQUEEZE, NUMEL, NDIMS)
function d=squeezedims(d1)
% move singleton dimension
d = d1(d1>1);
if (length(d)==1), if d<20, d = [1 d]; else d = [d 1]; end, end %% [1 d] improve the readability of small vectors
end % ENDFUNCTION

function ne=numberofel(x,ref)
% return the expected number of elements
dref = numberofdims(ref);
ne = size(x);
ne = prod(ne(1:min(length(ne),dref)));
end % ENDFUNCTION

function d=numberofdims(x)
% returns the expected number of dimension of x (0=scalar, 1=vector, 2=matrix)
d = length(find(size(x)>1));
end % ENDFUNCTION

%% CODE FOR BINARY DUMP ===============================
% TO DO LIST: to implement: itimes and imolecules
function X=dumpbinary(filename,colsort,molecules)
%READ BINARY DUMP FILES based on tools/binary2txt.cpp (Matlab comment is given as comment)
% Field names are a priori set since this information is not available in the binary files
%'collect' is always applied in this optimized version
% Definitions
colsort_default = 1;
% arg check
if nargin<2, colsort = []; end
if nargin<3, molecules = {}; end
if isempty(colsort), colsort=colsort_default; end
if isempty(molecules), molecules = {}; end
nmol = length(molecules);
% 2 steps reading
clock0 = clock;
fp = fopen(filename,'r'); % use fopen(filename,'r','b') if any problem in future Matlab versions
for do={'prealloc' 'load'}
    switch do{1}
        case 'prealloc'
            disp('BINARY Memory preallocation...')
            X = struct('TIMESTEP',[],'NUMBEROFATOMS',[],'BOXBOUNDS',[],'ATOMS',[]);
            [ncol,nproc,nbuff] = deal([]);
        case 'load'
            disp('BINARY reading...');
            X.BOXBOUNDS = zeros(3,2,numel(X.TIMESTEP)); % 3 dim array
            if nmol
                X.MOLECULES = cell(nmol,1);
                for imol=1:nmol, X.MOLECULES{imol}=zeros(length(molecules{imol}),3,numel(X.TIMESTEP)); end
                X.ATOMS = zeros(max(sum(nbuff,2))/min(ncol),max(ncol)); % only used as a buffer
            else
                X.ATOMS  = zeros(max(sum(nbuff,2))/min(ncol),max(ncol),numel(X.TIMESTEP)); % 3 dim array
            end
    end
    [u,v]=deal(0); % u=low cost index, v=expensive index (to be used only with LOAD)
    while ~feof(fp)
        switch do{1}, case 'prealloc', v=1; case 'load', v=v+1; end
        u = u+1;
        tmp = fread(fp,1,'int');
        if ~isempty(tmp) || ~feof(fp)
            clock1   = clock;
            X.TIMESTEP(u)      = tmp;
            X.NUMBEROFATOMS(u) = fread(fp,1,'int');
            X.BOXBOUNDS(:,:,v) = fread(fp,[2 3],'double')';
            ncol(u)  = fread(fp,1,'int');
            nproc(u) = fread(fp,1,'int');
            k = 1;
            iatomtime = min(v,size(X.ATOMS,3));
            for  i=1:nproc(u)
                nbuff(u,i) = fread(fp,1,'int');
                switch do{1}
                    case 'prealloc', fseek(fp,8*nbuff(end,i),'cof');
                    case 'load'
                        if i==1; display(10.001,'time step = %d\n',tmp), end
                        nlig = nbuff(u,i)/ncol(u);
                        X.ATOMS(k:(k+nlig-1),:,iatomtime)= fread(fp,[ncol(u) nlig],'double')';
                        k = k + nlig;
                end
            end
            switch do{1}
                case 'load'
                    display(10.002,'%s >>sorting')
                    [~,is] = sort(X.ATOMS(:,colsort,iatomtime));
                    X.ATOMS(:,:,iatomtime) = X.ATOMS(is,:,iatomtime);
                    if nmol, for imol=1:nmol, X.MOLECULES{imol}(:,:,v)=X.ATOMS(molecules{imol},3:5); end, end
                    display(10.003,'... end in %0.3g s\n',etime(clock,clock1))
            end
        end
    end
    fseek(fp,0,'bof');
end
fclose(fp);
fprintf('''%s'' loaded in %0.3g s\n',filename,etime(clock,clock0))

end %ENDFUNCTION ===============================

% INITIAL PROTOTYPE BASED ON BINARY2TXT
% filename = 'dump.atom.bin';
% fp = fopen(filename,'r');
% while ~feof(fp)
%     ntimestep = fread(fp,1,'int');
%     natoms    = fread(fp,1,'int');
%     bounds    = fread(fp,[2 3],'double');
%     size_one = fread(fp,1,'int');
%     nchunk = fread(fp,1,'int');
%     for  i=1:nchunk
%         n = fread(fp,1,'int');
%         buf = fread(fp,[size_one n/size_one],'double');
%     end
% end
% fclose(fp);