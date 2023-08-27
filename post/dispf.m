function out = dispf(varargin)
%DISPF fast wrapper of disp(sprintf(...))
% see help on SPRINTF
% see also FPRINTF (the main difference is that LF is used after disp)

% MS 2.1 - 16/03/08 - INRA\Olivier Vitrac rev. 14/09/19

% Revision history
% 29/12/12 updated help
% 19/08/18 implement varargin{1} as a cell
% 14/09/19 add output for vectorization

if iscell(varargin{1})
    n = 0;
    for i=1:numel(varargin{1})
        n = n+dispf(varargin{1}{i});
    end
else
    txt = sprintf(varargin{:});
    n = length(txt);
    disp(txt)
end
if nargout, out = n; end