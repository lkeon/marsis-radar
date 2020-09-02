# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;

import numpy as np

path = '/pico/home/userexternal/lkocjanc/Documents/marsisCode/data/'
fileName = 'positionRadargramMat-3000-0508.npy'

matrix = np.load( path + fileName )

def readPositionMat( data, matrix, zIndex = -1):
       '''
       Data is the type of data
           data = 0 is for echo value in radargram
           data = 1 returns x position
           data = 2 returns y position
       Matrix should be loaded before function call with matrix = np.load( path )
       '''
       if data == 0:
           return matrix[:,zIndex+2].astype(np.float32)
       elif data == 1:
           return matrix[:,0].astype(np.float32)
       elif data == 2:
           return matrix[:,1].astype(np.float32)

x = readPositionMat(1, matrix)
y = readPositionMat(2, matrix)
z = readPositionMat(0, matrix, 0)

print x,y,z