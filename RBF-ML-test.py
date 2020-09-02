# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;

"""
Test of RBF-ML algorithm (multilayer algorithm)
"""

import xalglib as xl

model = xl.rbfcreate(2, 1)
xy0 = [[-2,0,1],[-1,0,0],[0,0,1],[+1,0,-1],[+2,0,1]]
xl.rbfsetpoints(model, xy0)

xl.rbfsetalgomultilayer(model, 5.0, 4, 1.0e-3)
rep = xl.rbfbuildmodel(model)
xAxis = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
v = xl.rbfgridcalc2(model, xAxis, 9, [0.0], 1)

print v