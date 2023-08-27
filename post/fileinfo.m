function [rout,strout] = fileinfo(filename,ppath,dispon,stringonly,noerror)
%FILEINFO returns a structure that contains the main information of a given file
%  Syntax: info = fileinfo(filename,[path])
%  Options: [info,str] = fileinfo(filename,[path,dispon,stringonly,noerror])
%
% INPUTS
%   filename can include a full path or not
%   path is used if filename does not include it (the current path is used otherwise)
%   dispon (flag, default=true) prints on screen if true
%   stringonly (flag, default=false) returns a formated single string instead of a structure if true 
%   noerror (flag, default=false) no error message if true, corresponding files appear with sizes 0
%   
% OUTPUTS
%   info = structure matching dir/ls properties (string if stringonly is true)
%   str = formated string
%
%   See also: explore, isformat, isformat_multiple, ls, dir

% MS-MATLAB 1.0 - 20/04/04 - INRA\Olivier Vitrac - rev. 03/06/19

% revision history
% 19/08/04: display if no ouput, added str
% 11/09/07 fix filename as cell array
% 12/01/11 fix versn in FILEPARTS for Matlab later than 7.11 (not supported any more)
% 30/12/12 cosmetic modifications
% 09/02/16 improved help, add noerror
% 03/06/19 fix date format on French computers

% arg check
if nargin<2, ppath = ''; end
if nargin<3, dispon = []; end
if nargin<4, stringonly = []; end
if nargin<5, noerror = []; end
if ~nargout || isempty(dispon), dispon = true; end
if isempty(stringonly), stringonly = false; end
if isempty(noerror), noerror = false; end
oldmatlab = verLessThan('matlab','7.11');
issomethingmissing = false;

if iscell(filename)
    m = length(filename);
    str = cell(m,1);
    [r,str{1}] = fileinfo(filename{1},ppath,dispon);
    for i=2:m, [r(i),str{i}] = fileinfo(filename{i},ppath,dispon); end
    dispon = false;
else
    % other checks
    if oldmatlab
        [pathstr,name,ext,versn] = fileparts(filename);
    else
        [pathstr,name,ext] = fileparts(filename);
        versn = [];
    end
    if isempty(pathstr)
        if isempty(ppath)
            pathstr = cd;
        else
            pathstr = ppath;
        end
    end
    if ~exist(pathstr,'dir')
        if noerror
            issomethingmissing = true;
        else
            error('the directory ''%s'' does not exist',pathstr)
        end
    end
    fullfilename = fullfile(pathstr,[name ext versn]);
    if ~exist(fullfilename,'file')
        if noerror
            issomethingmissing = true;
        else
            error('the file ''%s'' does not exist in ''%s''',[name ext versn],pathstr)
        end
    end

    if issomethingmissing % faked info
        f = struct('date',datestr(now),'bytes',0);
    else % true info
        f = dir(fullfilename);
        if isfield(f,'datenum'), f.date = datestr(f.datenum); end
    end
    r =struct(   'filename', [name ext versn], ...
        'name',     name, ...
        'ext',      ext, ...
        'ver',      versn, ...
        'date',     f.date, ...
        'bytes',    f.bytes, ...
        'path',     pathstr...
        );

    if f.bytes>1024*1024
        str = sprintf('\t%s%s\t\t%s\t\t%0.1f MBytes\t\t%s',name,ext,f.date,f.bytes/(1024*1024),pathstr);
    elseif f.bytes>1024
        str = sprintf('\t%s%s\t\t%s\t\t%0.1f kBytes\t\t%s',name,ext,f.date,f.bytes/1024,pathstr);
    else
        str = sprintf('\t%s%s\t\t%s\t\t%d Bytes\t\t%s',name,ext,f.date,f.bytes,pathstr);
    end
end

% output
if nargout>0, rout = r; end
if stringonly, rout = str; return, end 
if nargout>1, strout = str; end
if dispon, disp(str), end