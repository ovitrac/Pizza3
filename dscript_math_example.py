#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pizza.dscript import dscript
from pizza.private.mstruct import param

D = dscript(name="math example")
D.DEFINITIONS.l = [1e-3, 2e-3, 3e-3]
D.DEFINITIONS.scale = "@{l}*2"
D.DEFINITIONS.x0 = "$[[[-0.5, -0.5],[-0.5, -0.5]],[[ 0.5,  0.5],[ 0.5,  0.5]]]*${scale[0,0]}"
D.DEFINITIONS.y0 = "$[[[-0.5, -0.5],[0.5, 0.5]],[[ -0.5,  -0.5],[ 0.5,  0.5]]]*${scale[0,1]}"
D.DEFINITIONS.z0 = "$[[[-0.5, 0.5],[-0.5, 0.5]],[[ -0.5,  0.5],[ -0.5,  0.5]]]*${l[2]}"
D.DEFINITIONS.X0 = "@{x0}.flatten()"
D.DEFINITIONS.Y0 = "@{y0}.flatten()"
D.DEFINITIONS.Z0 = "@{z0}.flatten()"
T = D.DEFINITIONS.eval()
D.DEFINITIONS.x0
T.x0
