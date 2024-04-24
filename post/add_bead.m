% Add bead along streamlines (considering quasi steady state)
% rev. 2024/03/12
% 2024/03/12
%%
function [x,y,Vl,l] = add_bead(s,rbead,dt)
nmax = ceil(s.l(end)/(2*rbead));  % maximum number of bead along the streamline
[x,y,l,Vl] = deal(nan(nmax,1));   % creat container
l(1) = rbead; % put first bead
cn = 1; % current number of bead
while l(1)<(s.l(end)-rbead)
    x = interp1(s.l,s.x,l);
    y = interp1(s.l,s.y,l);
    Vl = interp1(s.l,s.Vl,l);
    l = l + Vl*dt; % update the positions of beads
    if l(cn)>3*rbead
        l(cn+1) = rbead;
        cn = cn+1;
    end
end
x = interp1(s.l,s.x,l);
y = interp1(s.l,s.y,l);
Vl = interp1(s.l,s.Vl,l);
end