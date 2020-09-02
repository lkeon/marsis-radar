# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;

import numpy as np
import xalglib as xl
import matplotlib.pyplot as plt
import multiprocessing as mp

path = '/gpfs/work/PHD_Summer15/TMP/'
fileName = 'positionRadargramMat-3000-0508.npy'
outputFileName = 'positionRadargramMat-z150-z300-3000-0508.npy'

matrix = np.load( path + fileName )
print matrix.shape

outMatrix = matrix[:,0:2]
outMatrix = np.hstack( (outMatrix, matrix[:,152:352]) )

print outMatrix.shape
print outMatrix

np.save(outputFileName, matrix[:])

