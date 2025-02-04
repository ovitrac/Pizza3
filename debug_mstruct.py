#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 21:59:06 2025

@author: olivi
"""

# import NumPy
import numpy as np
# import param from mstruct module
from pizza.private.mstruct import param


# %% bug
# evaluate all expressions and store them in s
p = param()
p.a  = [1.0, 0.2, 0.03, 0.004] # Python list
p.b  = np.array([p.a])         # Converts a as row vector

p.d = "${b[0,1]} + ${a[0]}"    # Evaluates as `0.2 + 1.0` (bug)

p.c = "${a[1]}+10"             # Retrieves `a[1]` = 0.2 and add 10 `0.2 + 10`
p.e = "${a}[1]+10"             # This notation works also (equivalent to c for the part `${a}[1]`) `0.2 + 10`
p.f = "${b}[0,1] + ${a}[0]"
p.g = "{'a': 'a', 'b': 2}"
p.h = "${g}"
p.i = "${g[a]}"

s = p() # equivalent to s = p.eval()
prettyprint = lambda var,value: print(f"{var} = {value} (type: {type(value).__name__})")
# they are equivalent
prettyprint("c",s.c)
prettyprint("e",s.e)
# they are not equivalent
prettyprint("d",s.d)
prettyprint("f",s.f)

# generator
p.generator(printout=True)

# eval
p.formateval("this is d=${d} with b=${b}")
p.formateval("${1+2}*${a[1]}")
# %% others
p = param()
p.a = [0,1,2]                   # this list is numeric and is already in Python
p.b = '[1,2,"test","${a[1]}"]'  # this list combines param expressions
p.c = '![1,2,"test","${a[1]}"]' # the `!` to force recursive evaluation of expressions in lists
p.d = "${b[3]}*10"              # the expressions can be combined together
p.e = "${c[3]}*10"              # the expressions can be combined together
p.f = ["${a[1]+a[2]}*3", 1,2,"test","${a[1]}", "${a[1]+a[2]}", "${1+2}", "b"]
p.g = "${a[1]+a[2]}"
p.h = "this is a"
p.i = "${a[1]+100}*${b[1]}"
p.j = "the result is ${a[1]+100}*${b[1]}"
p.k = "the result is ${(a[1]+100)*b[1]}"
p.units = "$si"
p.l = ["units","$lj"]
p.m = ["units","${units}"]
p.n = "the ${l[0]} are ${units} as defined with \\${units}"
p.o = 10
p.p = 100
p.q = "[${o},${p}]"
p.r = "the sum of q is ${sum(q)}"
p.s = "${max(q)}"
s = p()
p

# %% last bug
v = param()
v.l = [1e-3, 2e-3, 3e-3]    # l is defined as a list
v.a = "$[1 2 3]"            # a is defined with  Matlab notations
v.b = "$[1:3]"              # b is defined with  Matlab notations
v.c = "$[0.1:0.1:0.9]"      # c is defined with  Matlab notations
v.test = "@{l}"
v.scale = "@{l}*2*@{a}"     # l is rescaled
v.x0 = "$[[[-0.5, -0.5],[-0.5, -0.5]],[[ 0.5,  0.5],[ 0.5,  0.5]]]*${scale[0,0]}*${a[0,0]}"
v.y0 = "$[[[-0.5, -0.5],[0.5, 0.5]],[[ -0.5,  -0.5],[ 0.5,  0.5]]]*${scale[0,1]}*${a[0,1]}"
v.z0 = "$[[-0.5 0.5 ;-0.5 0.5],[ -0.5,  0.5;  -0.5,  0.5]]*${l[2]}*${a[0,2]}"
v.X0 = "@{x0}.flatten()"
v.Y0 = "@{y0}.flatten()"
v.Z0 = "@{z0}.flatten()"
s=v()
v