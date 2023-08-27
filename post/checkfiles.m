%checkfiles
% 2023-04-23 checkfiles: generic script to check lamdumpread prefetch and split (frame) files
% outputs in Markdown for Mermaid and Markmap


%% look for gz files
switch localname
    case 'LX-Olivier2021'
        local = '/media/olivi/MODIC4TB_WSJ2/'; %#ok<*NASGU> 
        local = '/media/olivi/MODIC4TB_WSJ1/';
    case 'LP-OLIVIER2022'
        local = 'E:\';
    otherwise
        dispf('implement you machine by adding\n\n\tCASE ''%s''\n\t\tlocal = ''this is my path''\n',localname)
        error('unknown machine and local path')
end

target = '*.tar.gz';
fgz = explore(target,local,100,'abbreviate');
ngz = length(fgz);

%% look for dump files without the extension tar.gz
% templates
makeprefetch = @(fn) char(fullfile(rootdir(fn),['PREFETCH_' lastdir(fn) '.mat'])); % added 2023/03/23
makesplitdir = @(fn) char(fullfile(rootdir(fn),['PREFETCH_' lastdir(fn)])); % added 2023/03/23
statenfo = @(done,dt) sprintf('| elapsed %0.3g s | done %0.3g %% | remaining %0.3g s |',dt,done*100,(1/done-1)*dt);
SPLITPREFIX = 'TIMESTEP_';
MB = 1024^2;
GB = 1024^3;
screen = ''; t0 = clock;
for i=1:ngz
    done = (i-1)/ngz; dt = etime(clock,t0); %#ok<*DETIM> 
    screen = dispb(screen,'[%d/%d] search for dump files and frames ... %s',i,ngz,statenfo(done,dt));
    dfi = explore('dump.*',fgz(i).path,10,'abbreviate');
    dfi=dfi(cellfun(@(e) ~any(strcmpi(e,{'gz','mat'})),{dfi.ext})); % remove gz extensions
    ndfi = length(dfi);
    % for each
    for j = 1:ndfi
        f = fullfile(dfi(j).path,dfi(j).file);
        dfi(j).hasprefetch = exist(makeprefetch(f),'file')==2;
        dfi(j).hassplitdir =  exist(makesplitdir(f),'dir')==7;
        % counts frames
        if dfi(j).hassplitdir
            dfi(j).frames = explore(sprintf('%s*.mat',SPLITPREFIX),makesplitdir(f),0,'abbreviate');
            dfi(j).nframes = length(dfi(j).frames);
            t1 = clock;
            done = (i-1+(j-1)/ndfi)/ngz; dt = etime(clock,t0);
            screen = dispb(screen,'[%d/%d] %d of %d dump files with %d frames ... %s',i,ngz,j,ndfi,dfi(j).nframes,statenfo(done,dt));
            for iframe = 1:dfi(j).nframes
                dfi(j).frames(iframe).timestep = str2double(regexprep(dfi(j).frames(iframe).name,SPLITPREFIX,''));
            end
        else
            dfi(j).nframes = 0;
            ispb(screen,'[%d/%d: %d] no frame found !',i,ngz,j); screen = '';
        end
    end
    % save
    fgz(i).ndump = ndfi;
    if ndfi
        fgz(i).dump = dfi;
        fgz(i).nprefetch = length(find([dfi.hasprefetch]));
        fgz(i).nsplitdir = length(find([dfi.hassplitdir]));
    else
        fgz(i).dump = struct([]);
        fgz(i).nprefetch = 0;
        fgz(i).nsplitdir = 0;
        dispb(screen,'[%d/%d] no dump found !',i,ngz); screen = '';
    end
end


%% Files not untar and ungzipped
untar = fgz([fgz.ndump]<1);
dispf('%d files are not untarred and ungzipped',length(untar))

%% create a database
ndumps = sum([fgz.ndump]);
dispf('%d dump filmes have been found',ndumps)
% review the tags (based on ext)
nmaxtags = 0;
idump = 0;
for i=1:length(fgz)
    for j=1:length(fgz(i).dump)
        idump = idump + 1;
        name = fgz(i).dump(j).ext;
        nmaxtags = max(nmaxtags,length(strsplit(name,'_')));
    end
end
tagfields = arrayfun(@(t) sprintf('tag%d',t),1:nmaxtags,'UniformOutput',false);
tagtypes = repmat({'categorical'},1,nmaxtags);
% preallocate the table
T = table( ...
    'Size',[ndumps,22+length(tagfields)], ...
    'VariableTypes',[{'string','datetime'} tagtypes {'logical','logical'    ,'string'      ,'double'    ,'double' ,'cell'  , 'double','double','string'    ,'string'    ,'cell'   ,'double' ,'double'  ,'string'    ,'string'  ,'string'  ,'double','string','string','double'}],...
    'VariableNames',[{'name','date'} tagfields {'hasprefetch' ,'hassplitdir','prefetchfile','prefetchMB','nframes','tframe','tfirst' ,'tlast' ,'firstframe','lastframe' ,'frames' ,'frameMB','framesGB','framespath','dumpfile','dumppath','dumpGB','gzfile','gzpath','gzGB'}]);
% fill the table
idump = 0;
for i=1:length(fgz)
    for j=1:length(fgz(i).dump)
        idump = idump + 1;
        % name
        name = fgz(i).dump(j).ext;
        T.name(idump) = name;
        % date
        T.date(idump) = datetime(fgz(i).dump(j).datenum,'ConvertFrom','datenum','format','yyyy-MM-dd');
        % add tags
        tags = strsplit(name,'_'); ntags = length(tags);
        for itag = 1:ntags
            T.(tagfields{itag})(idump) = tags(itag);
        end
        % prefetch/split flags
        T.hasprefetch(idump) = fgz(i).dump(j).hasprefetch;
        T.hassplitdir(idump) = fgz(i).dump(j).hassplitdir;
        % dump file
        T.dumppath(idump) = fgz(i).dump(j).path;
        T.dumpfile(idump) = fgz(i).dump(j).file;
        T.dumpGB(idump) = fgz(i).dump(j).bytes/GB;
        % prefetch file
        if T.hasprefetch(idump)
            T.prefetchfile(idump) = makeprefetch(char(fullfile(T.dumppath(idump),T.dumpfile(idump))));
            tmp = dir(T.prefetchfile(idump));
            T.prefetchMB(idump) = tmp.bytes/MB;
        else
            dispf('dump #%d: missing prefetch !',idump)
        end
        % frames
        timesteps = [fgz(i).dump(j).frames.timestep];
        frames = string({fgz(i).dump(j).frames.file});
        [tfirst,kfirst] = min(timesteps);
        [tlast,klast] = max(timesteps);
        T.nframes(idump) = fgz(i).dump(j).nframes;
        T.tframe{idump} = timesteps;
        T.tfirst(idump) = tfirst;
        T.tlast(idump)  = tlast;
        T.firstframe(idump) = frames(kfirst); 
        T.lastframe(idump) = frames(klast);
        T.frames{idump} = frames;
        T.framespath(idump) = fgz(i).dump(j).frames(1).path;
        T.framesGB(idump) = sum([fgz(i).dump(j).frames.bytes])/GB;
        T.frameMB(idump) = (T.framesGB(idump)/T.nframes(idump)) * (GB/MB);
        % gz info
        T.gzpath(idump) = fgz(i).path;
        T.gzfile(idump) = fgz(i).file;
        T.gzGB(idump) = fgz(i).bytes/GB;
    end
end
% remove any duplicate
idT = cellfun(@(p,f) fullfile(p,f) ,T.dumppath,T.dumpfile,'uniformoutput',false);
[~,kept] = unique(idT,'stable');
T = T(kept,:);
nT = size(T,1);

%% TAGs
ntags = length(tagfields);
for i=1:ntags
    T.(tagfields{i})(ismissing(T.(tagfields{i}))) = sprintf('UndefTag%02d',i);
end
Ttagsafe = T(:,tagfields);
tagvalues = cellfun(@(t) categories(T.(t)),tagfields,'UniformOutput',false);
tagvaluessafe = tagvalues;
taginternal = tagvalues;
repeatedtags = [];
knowntags = {};
for i=1:ntags
    for j=1:length(tagvalues{i})
        if ismember(tagvalues{i}{j},knowntags)
            k = find(ismember(knowntags,tagvalues{i}{j}));
            repeatedtags(k) = repeatedtags(k) + 1; %#ok<*SAGROW> 
            tagvaluessafe{i}{j} = sprintf('%s_%0d',tagvaluessafe{i}{j},repeatedtags(k));
            tobereplaced = T.(tagfields{i})==tagvalues{i}{j};
            Ttagsafe.(tagfields{i})(tobereplaced)=tagvaluessafe{i}{j};
        end
        knowntags{end+1} = tagvaluessafe{i}{j};
        repeatedtags(end+1) = 1;
        taginternal{i}{j} = sprintf('TAG%02d%02d',i,j);
    end
end
%% Generate the diGraph
rootnode = 'root';
nodes = arrayfun(@(n) sprintf('dump%03d',n),(1:nT)','UniformOutput',false);
tagnodes = cat(1,taginternal{:});
tagrealnodes= cat(1,tagvaluessafe{:});

% defintions (should match mermaidones)
definitions = [
    {rootnode}
    tagrealnodes
    nodes
    ];
ndefintions = length(definitions);
% mermaid defintions
mermaiddefinitions = [
    {sprintf('%s[%s]',rootnode,strrep(local,'\','_'))}
    cellfun(@(n,d) sprintf('%s[%s]',n,d),tagnodes,cat(1,tagvalues{:}),'UniformOutput',false);
    arrayfun(@(i) sprintf('%s[%d: <kbd>%s</kbd>]',nodes{i},i,T.dumpfile(i)),(1:nT)','UniformOutput',false)
    ];
mermaidnodes = [
    {rootnode}
    tagnodes
    nodes
    ];
% ID
ID = zeros(nT,ntags+1);
[~,ID(:,end)] = intersect(definitions,nodes,'stable');
for i=1:ntags
    [usetags,iusetags] = intersect(definitions,Ttagsafe.(tagfields{i}),'stable');
    for j = 1:length(usetags)
        ID(ismember(T.(tagfields{i}),usetags(j)),i) = iusetags(j);
    end
end
ID = [ones(nT,1) ID];
C = false(ndefintions,ndefintions);
for i = 1:nT
    ind = ID(i,ID(i,:)>0);
    for j=2:length(ind)
        C(ind(j-1),ind(j)) = true;
    end
end
 g = digraph(C,definitions); figure, plot(g,'nodelabel',definitions,'layout','force3');

%% Generate the Mermaid document
mermaidheader = {
'```mermaid'
'graph LR;'
'linkStyle default interpolate basis'
''
};
mermaidfooter = {'```'};
[i,j] = ind2sub(size(C),find(C));
mermaidlinks = arrayfun(@(a,b) sprintf('%s --> %s',mermaidnodes{a},mermaidnodes{b}),i,j,'UniformOutput',false);
mermaid = [mermaidheader;mermaiddefinitions;mermaidlinks;mermaidfooter];
clipboard('copy',sprintf('%s\n',mermaid{:}))


%% Generate the Markdown document
markdown = {
'---'
'markmap:'
'  colorFreezeLevel: 5'
'  initialExpandLevel: 3'
'  maxWidth: 400'
'---'
    };
level = @(position,txt) sprintf('%s [tag%0d] %s',repmat('#',position,1),position,txt);
vec = zeros(1,ntags); vec(1)=1;
lengthvec = cellfun(@length,tagvalues);
position = 1;
ok = false(nT,ntags);
finished = false;
newlevel = true;
nfound = 0;
founditems = [];
action = 'init';
DEBUGON = true; DEBUGCOMB = NaN(prod(lengthvec),ntags); DEBUGITER = 0;
isprintedT = false(nT,1);
if DEBUGON, clc, end
while (position>0) && any(vec)
    terminal = (position==ntags);
    % refresh flags
    currenttag = tagvalues{position}{vec(position)};
    ok(:,position) = (T.(tagfields{position}) == currenttag);
    currentfound = find(all(ok(:,1:position),2));
    completed = false;
    if position>1 && isempty(currentfound)
        previousfound = find(all(ok(:,1:position-1),2));
        if ~isempty(previousfound)
            completed = all(ismissing(T.(tagfields{position})(previousfound)));
            if completed
                currentfound = previousfound;
            end
        end
    end
    ncurrentfound = length(currentfound);
    
    % display (debugging purposes)
        % check duplicates with this line
        %[~,ia]=unique(DEBUGCOMB,'rows','first'); [~,ib]=unique(DEBUGCOMB,'rows','last'); [ia(find(ia-ib,1,'first')) ib(find(ia-ib,1,'first'))]
        % check missing
        %{
            arrays = arrayfun(@(i) 1:lengthvec(i), 1:ntags,'UniformOutput',false);
            [grid{1:ntags}] = ndgrid(arrays{:});
            grid_arrays = cellfun(@(x) x(:), grid, 'UniformOutput', false);
            combinations = [grid_arrays{:}]; disp(size(combinations));
            missing  = combinations(~ismember(combinations,DEBUGCOMB,'rows'),:);
            findfirst = find(sum(missing(:,1:3)-[1 1 2],2)==0)
        %}
    if DEBUGON %&& ismember(action,{'init','keep','keep+reset'})
        if terminal, DEBUGITER = DEBUGITER+1; DEBUGCOMB(DEBUGITER,:) = vec; end
        vecstr = arrayfun(@(v) num2str(v),vec,'UniformOutput',false);
        vecstr{position} = sprintf('[%s]%',vecstr{position});
        if newlevel, newstr = '*'; else newstr = '-'; end %#ok<*SEPEX> 
        if terminal, newstr = [newstr newstr]; end %#ok<*AGROW> 
        dispf('%d> %s%s <-- %s (%d found [%s], total = %d)',DEBUGITER,sprintf('%s ',vecstr{:}),newstr,action,ncurrentfound,currenttag,nfound)
    end
    

    % do
    if ncurrentfound>0
        if newlevel %(newlevel || terminal || (ncurrentfound == 1)) && ~completed
            markdown{end+1} = level(position,tagvalues{position}{vec(position)});
        end
        if terminal %(ncurrentfound < 2) %|| (ncurrentfound>1 && (terminal || completed))
            founditems = union(founditems,currentfound);
            for ifound = 1:ncurrentfound
                nfound = nfound + 1;
                mycurentnode = currentfound(ifound);
                if ~isprintedT(mycurentnode)
                    markdown{end+1} = sprintf('> **`%s`**',T.dumpfile(mycurentnode));
                    markdown{end+1} = sprintf('> ORIGINAL file size: %0.2f GB',T.dumpGB(mycurentnode));
                    if ~ismissing(T.prefetchfile(mycurentnode))
                        markdown{end+1} = sprintf('> PREFETCH file (%0.2f MB): %s',T.prefetchMB(mycurentnode),strrep(T.prefetchfile(mycurentnode),'\','/'));
                    else
                        markdown{end+1} = '> ==missing PREFETCH file==';
                    end
                    if ~ismissing(T.framespath(mycurentnode))
                        markdown{end+1} = sprintf('> FRAMES folder (%0.2f GB): %s',T.framesGB(mycurentnode),strrep(T.framespath(mycurentnode),'\','/'));
                        markdown{end+1} = sprintf('> NUMBER of frames: *%d* (%0.2f MB/frame)',T.nframes(mycurentnode),T.frameMB(mycurentnode));
                        markdown{end+1} = sprintf('> FIRST TIMESTEP: *%d*',T.tfirst(mycurentnode));
                        markdown{end+1} = sprintf('> LAST TIMESTEP: *%d*',T.tlast(mycurentnode));
                        markdown{end+1} = sprintf('> FIRST FRAME: %s',strrep(T.firstframe(mycurentnode),'\','//'));
                        markdown{end+1} = sprintf('> FIRST LAST: %s',strrep(T.lastframe(mycurentnode),'\','//'));
                    else
                        markdown{end+1} = '> ==missing  FRAMES folder==';
                    end
                    markdown{end+1} = newline;
                    isprintedT(mycurentnode)=true;
                end % already printed
            end % next found
        end
    end
    % shift operations
    if (position<ntags) && vec(position+1)<lengthvec(position+1)
        position = position +1; % descent into the next level
        vec(position) = 1;
        if position<ntags, vec(position+1) = 1; end
        newlevel = true;
        action = 'descent';
    else
        if vec(position)<lengthvec(position)
            vec(position) = vec(position)+1; % keep the same level
            if (position<ntags)
                vec(position+1) = 1;
                newlevel = true;
                action ='keep+reset';
            else
                newlevel = false;
                action = 'keep';
            end
        else
            position = position - 1; % raise the level (nothing done)
            newlevel = false;
            action = 'raise';
        end
    end
end
DEBUGCOMB(any(isnan(DEBUGCOMB),2),:) = [];
clipboard('copy',sprintf('%s\n',markdown{:}))
