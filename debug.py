#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 10:56:21 2023

@author: olivi
"""

from pizza.region import *

mag = 1
e = emulsion(xmin=-5*mag, ymin=-5*mag, zmin=-5*mag,xmax=5*mag, ymax=5*mag, zmax=5*mag)
e.insertion([2,2,2],beadtype=1)
C = region(name='debug',width=11*mag,height=11*mag,depth=11*mag)
C.scatter(e)
C.emulsion.glob00.creategroup()
C.emulsion.creategroup()
liste = C.emulsion.list()

C.script()
g = C.emulsion.group()
C.dolive()
