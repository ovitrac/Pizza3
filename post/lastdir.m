function [rep,root] = lastdir(chemin)
% LASTDIR extrait le nom du dernier répertoire du chemin (et la racine correspondante)
%		ex. rep = last_dir(chemin)
%		options : [rep,root] = last_dir(chemin)

% Woodox 1.0 - 27/02/01 - Olivier Vitrac - rev.  02/02/08

% Revision history
% 24/01/08 optimization, filesep instead of '\'
% 02/02/08 Unix compatibility
% 07/02/2019 fix lastdir(filesep)

% arg check
if nargin<1, chemin = ''; end
if isempty(chemin), chemin = pwd; end
if ~ischar('the argument must be a string'), end

if isunix 
    if (length(chemin)<1), warning('''%s'' does not seem to be a valid path',chemin), rep = ''; end
else
    if (length(chemin)==1) && (chemin==filesep), warning('''%s'' does not seem to be a valid path',chemin), rep = ''; end
end

chemin = remove_slash(chemin);
ind = find(chemin == filesep);

if any(ind) && ind(end)<length(chemin)
   rep = chemin(ind(end)+1:end);
   if nargout>1, root = remove_slash(chemin(1:ind(end))); end
else
   rep = chemin;
   if nargout>1, root = ''; end
end


function chemin = remove_slash(chemin_sl)
if isempty(chemin_sl) || (length(chemin_sl)==1 && (chemin_sl(end)==filesep) )
    chemin = '';
elseif chemin_sl(end)==filesep && (isunix || (chemin_sl(end-1)~=':') )
   chemin = chemin_sl(1:end-1);
else
   chemin = chemin_sl;
end