function rpath = rootdir(pathstr)
%ROOTDIR extract the root of path using [last,root]=lastdir(pathstr)
%   syntax: root = rootdir(pathstr) 

% MS 2.1 - 09/02/08 - INRA\Olivier  - rev.
[tmp,rpath] = lastdir(pathstr);