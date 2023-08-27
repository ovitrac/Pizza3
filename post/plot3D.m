function ho=plot3D(X,varargin)
%PLOT3D wrapper of plot3(X(:,1),X(:,2),X(:,3),'property','value')
%   syntax: h=plot3D(X,property,value...)
%   NB: works also on cell array

% MS 2.1 - 30/03/08 - INRA\Olivier Vitrac rev.

% default

% arg check
if nargin<1, error('h=plot3D(X,property,value...)'), end
options = varargin;
if iscell(X)
    nX = length(X);
    h = [];
    if ~iscell(X{1}) % new molecule
        pos=1; ntot = sum(cellfun('length',X));
        for i=1:nX
            h =[h;plot3D(X{i},'colrange',[pos ntot],options{:})];
            pos = pos+length(X{i});
        end
    else
        if isempty(options)
            col = jet(nX);
            for i=1:nX, h= [h;plot3D(X{i},'-o','color',col(i,:),'markeredgecolor',col(i,:),'markerfacecolor',col(i,:),'linewidth',2,'markersize',12)]; end
        else
            for i=1:nX, h= [h;plot3D(X{i},options{:})]; end
        end
    end
    if nargout, ho = h; end
    return
elseif size(X,3)>1
    nX = size(X,3);
    col = jet(nX); h = [];
    for i=1:nX, h=[h;plot3D(X(:,:,i),'-','color',col(i,:))]; end
    if nargout, ho = h; end
    return
end     
if size(X,2)~=3 && size(X,1)==3, X=X'; end
[m,n] = size(X); if n~=3, error('X must be a mx3 array'), end

% non standard options
ikw = find(cellfun('isclass',options,'char'));
if ismember('colrange',options(ikw))
    iopt = ikw(find(ismember(options(ikw),'colrange'),1,'first'));
    colrange = options{iopt+1};
    options = options(setdiff(1:length(options),[0 1]+iopt));
 else
    colrange = [];
end
ikw = find(cellfun('isclass',options,'char'));
if ismember('autocol',options(ikw))
    iopt = ikw(find(ismember(options(ikw),'autocol'),1,'first'));
    options = options(setdiff(1:length(options),iopt));
    autocol = true;
    if isempty(colrange)
        collist = jet(m);
        colstart = 0;
    else
        collist = jet(colrange(2));
        colstart = colrange(1);
    end
else
    autocol = false;
    collist = [];
end

% plots
hold on
if autocol && m>1
    h = zeros(m-1,1);
    for i=1:m-1
        h(i) = plot3(X(i:i+1,1),X(i:i+1,2),X(i:i+1,3),options{:});
        set(h(i),'color',collist(colstart+i,:),'markerfacecolor',collist(colstart+i,:),'markeredgecolor',collist(colstart+i,:))
    end
else
    h = plot3(X(:,1),X(:,2),X(:,3),options{:});
end
if nargout, ho = h; end