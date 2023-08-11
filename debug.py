#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 10:56:21 2023

@author: olivi
"""

from pizza.region import *


# --- do not look at this code, it is for me (Olivier)
# a=LammpsSpacefilling(style="$block",width=100,height=100,depth=100,units="",beadtype=1)
# inputs = a.DEFINITIONS+a.USER
# inputs.formateval("${width}=${style}+3")
# print(a.do)


# check here if you want a spacefilling model or not
spacefilling = True
beadtype_forglob = 2 if spacefilling else 1

mag = 1
e = emulsion(xmin=-5*mag, ymin=-5*mag, zmin=-5*mag,xmax=5*mag, ymax=5*mag, zmax=5*mag)
e.insertion([2,2,2],beadtype=beadtype_forglob)
C = region(name='debug',width=11*mag,height=11*mag,depth=11*mag,spacefilling=spacefilling)
C.scatter(e)
C.emulsion.glob00.creategroup()
C.emulsion.creategroup()
liste = C.emulsion.list()

C.script()
g = C.emulsion.group()
C.dolive()
