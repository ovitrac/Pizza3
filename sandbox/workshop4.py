#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ideas for the region workshop

Created on Fri Jul  7 13:22:02 2023

@author: olivi, han
"""



#variable        l0 equal 0.05 # initial particle lattice spacing
#region          box block 0 12 0 8 -0.01 0.01 units box
#create_box      5 box
R = region(name="cavity",width=12,height=8,depth=1)
# saliva 1 and 2
#   region          saliva1 block 0.25 1.8 1.25 3.5 EDGE EDGE units box
#   region          saliva2 block 10 11.65 1.25 4 EDGE EDGE units box
R.block(name = "saliva1",xlo=0.25,xhi=1.8,ylo= 1.25,yhi=3.5,zlo="EDGE",zhi="EDGE",units="box",beadtype=1)
R.block(name = "saliva2",xlo=10,xhi=11.65,ylo= 1.25,yhi=4,zlo="EDGE",zhi="EDGE",units="box",beadtype=1)
# mouth
#   region          mouth block 0.15 11.85 0.15 8 -0.01 0.01 units box side out # mouth
R.block(name = "mouth",xlo=0.15,xhi=11.65,ylo= 1.25,yhi=4,zlo="EDGE",zhi="EDGE",units="box",beadtype=3)

# create a "tongue" (with two parts; tongue and palate)
# objects are positionned on floors (yfloor1, yfloor2, yfloor3)
# default size
hgap=0.25        # gap to prevent direct contact at t=0 (too much enery)
hsmallgap = 0.1   # gap to prevent direct contact at t=0 (too much enery)
hto1 = 0.8         # height of to1 (the tongue to1, note 1 not l)
hto2 = 0.5         # height of to2 (the tongue to2)
rsph = 0.3         # radius of spherical food particles
lpar = 0.6         # size of prismatic particles
# floor1/roof1: 1st floor and roof
yfloor1 = hgap  # bottom position of to1, position of the first floor
yroof1 = yfloor1 + hto1
yfloor2a = yroof1 + hsmallgap  # position of the second floor / level a
yroof2a = yfloor2a + lpar      # position of the second floor / level a
yfloor2b = yroof2a + hsmallgap # position of the second floor / level b
yroof2b = yfloor2b+ lpar      # position of the second floor / level b
yfloor2c = yfloor2a + rsph     # position of the second floor / level c
yroof2c  = yfloor2c + rsph      # position of the second floor / level c
yfloor2d  = yroof2c + rsph + hsmallgap # position of the second floor / level d
yroof2d  = yfloor2d + rsph      # position of the second floor / level d
yfloor3 = 5.0      # third floor
yroof3 = yfloor3 + hto2 # bottom position of to1
yfloor3a  = yfloor3 - 0.6
yroof3a = yfloor3

# crunch distance: crunchl, period: crunchp, velocity: crunchv
# using the shortcurts l,P,v and assuming v = v0 sin(wt)
# the distance D visited during P/2 (which should be equal to l) reads:
#   D = integrate (v0*sin (w*t)*dt) from t=0 to P/2
#   D = (2*v0*sin^2((P*w)/4))/w
# see: https://www.wolframalpha.com/input/?i=integrate+%28v0*sin+%28w*t%29*dt%29+from+t%3D0+to+P%2F2
crunchl  = yfloor3 - yfloor2a -0.8
crunchp = 3   # real time (time are not time steps)
crunchw = 2*pi/crunchp
crunchd = 2*(sin((crunchp*crunchw)/4)**2)/crunchw
crunchv = crunchl/crunchd
print(f"Crunch distance:{crunchl}")  # 3.65
print(f"Crunch distance:{crunchv}")  # 0.1147

# bottom part of the tongue: to1 (real tongue)
# warning: all displacements are relative to the bottom part
# region          to1 block 1 11 ${yfloor1} ${yroof1} EDGE EDGE units box
# region          to2part1 block 0.5 11.5 ${yfloor3} ${yroof3} EDGE EDGE units box
# region          to2part2 block 5.5 6 ${yfloor3a} ${yroof3a} EDGE EDGE units box
# region          to2 union 2 to2part1 to2part2
R.block(name = "to1",xlo=1,xhi=11,ylo=yfloor1,yhi=yroof1,zlo="EDGE",zhi="EDGE",units="box",beadtype=4)
R.block(name = "to2part1",xlo=0.5,xhi=11.5,ylo=yfloor3,yhi=yroof3,zlo="EDGE",zhi="EDGE",units="box")
R.block(name = "to2part2",xlo=5.5,xhi=6,ylo=yfloor3a,yhi=yroof3a,zlo="EDGE",zhi="EDGE",units="box")
R.union("to2part1","to2part2",name="to2",beadtype=5)

# create some solid objects to be pushed around
# region          pr1 prism 2 2.6 ${yfloor2a} ${yroof2a} EDGE EDGE 0.3 0 0 units box
# region          bl1 block 3 3.6 ${yfloor2a} ${yroof2a} EDGE EDGE units box
# region          sp1 sphere 4.3 ${yfloor2c} 0 ${rsph} units box
# region          sp2 sphere 5 ${yfloor2c} 0 ${rsph} units box
# region          sp3 sphere 5.7 ${yfloor2c} 0 ${rsph} units box
# region          sp4 sphere 6.4 ${yfloor2c} 0 ${rsph} units box
# region          sp5 sphere 7.1 ${yfloor2c} 0 ${rsph} units box
# region          sp6 sphere 6.05 ${yfloor2d} 0 ${rsph} units box
# region          br2 block 3 3.6 ${yfloor2b} ${yroof2b} EDGE EDGE units box
# create some solid objects to be pushed around
R.prism(name = "pr1", xlo=2, xhi=2.6, ylo=yfloor2a, yhi=yroof2a, zlo="EDGE", zhi="EDGE", xy=0.3, xz=0, yz=0, units="box",beadtype=2)
R.block(name = "bl1", xlo=3, xhi=3.6, ylo=yfloor2a, yhi=yroof2a, zlo="EDGE", zhi="EDGE", units="box",beadtype=2)
R.sphere(name = "sp1", x=4.3, y=yfloor2c, z=0, radius=rsph, units="box",beadtype=2)
R.sphere(name = "sp2", x=5, y=yfloor2c, z=0, radius=rsph, units="box",beadtype=2)
R.sphere(name = "sp3", x=5.7, y=yfloor2c, z=0, radius=rsph, units="box",beadtype=2)
R.sphere(name = "sp4", x=6.4, y=yfloor2c, z=0, radius=rsph, units="box",beadtype=2)
R.sphere(name = "sp5", x=7.1, y=yfloor2c, z=0, radius=rsph, units="box",beadtype=2)
R.sphere(name = "sp6", x=6.05, y=yfloor2d, z=0, radius=rsph, units="box",beadtype=2)
R.block(name = "br2", xlo=3, xhi=3.6, ylo=yfloor2b, yhi=yroof2b, zlo="EDGE", zhi="EDGE", units="box",beadtype=2)
R.dolive()
