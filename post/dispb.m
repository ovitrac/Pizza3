function update=dispb(old,varargin)
%DISPB wrapper of disp with linefeed 
% syntax: screenline=dispb(screenline,'string with codes %s %d',value1,value2,...)
% see help on SPRINTF

% MS 2.1 - 22/03/09 - INRA\Olivier Vitrac rev.

% Revision history
update = sprintf(varargin{:});
if any(old)
    varargin{1} = [repmat('\b',1,length(old)+1) varargin{1}];
end
dispf(varargin{:})
