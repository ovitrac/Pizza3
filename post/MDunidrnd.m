function x = MDunidrnd(n,m)
%  MDUNIDRND generates m uniform random numbers (one appearance) ranged between 1 and n (n>m)
%
% 	Syntax:  x = MDunidrnd(n,m)
       
% MDsimple 2.0 - 21/07/03 - Olivier Vitrac - rev.

% argument check
if n<m, error('n<m'), end

% random generator
x = []; lx = 0;
while lx<m
	x(end+1:m) = unidrnd(n,m-lx,1);
	[xu,j] = unique(x);
	x = x(sort(j));
	lx = length(x);
end
