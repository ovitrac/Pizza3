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

s = p() # equivalent to s = p.eval()
prettyprint = lambda var,value: print(f"{var} = {value} (type: {type(value).__name__})")
# they are equivalent
prettyprint("c",s.c)
prettyprint("e",s.e)
# they are not equivalent
prettyprint("d",s.d)
prettyprint("f",s.f)


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
