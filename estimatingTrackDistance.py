# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;
'''
This code imports reading matrix and calculates themaximum distance 
'''
import numpy as np
import math

path = '/pico/home/userexternal/lkocjanc/Documents/marsisCode/exportedReadMat-2000.npy'
matrix = np.load( path )

def readPositionMat(data, matrix):
    '''
    Data is the type of data
	0 is for index inside radargram
	1 is for x position
	2 is for y position
	3 is for datafile nameFile
    Position is number of instance in matrix
    Matrix should be loaded before function call with matrix = np.load( path )
    '''

    if data == 0:
	return matrix[:,0].astype(np.int)

    elif data == 1:
	return matrix[:,1].astype(np.float32)

    elif data == 2:
	return matrix[:,2].astype(np.float32)

    else:
	return matrix[:,3]

dataIndex = readPositionMat(0, matrix)
xDim = readPositionMat(1, matrix)
yDim = readPositionMat(2, matrix)
dataFile = readPositionMat(3, matrix)

border = 1100.0
lengthData = xDim.shape[0]
listIndex = []

if xDim[0] > border:
    listIndex.append(0)

for i in range(lengthData-1):
    dataFileThis = dataFile[i]
    dataFileNext = dataFile[i+1]

    if dataFileThis != dataFileNext:
	if xDim[i] > border and yDim[i] > 0:
	    listIndex.append(i)
	
	if xDim[i+1] > border and yDim[i+1] > 0:
	    listIndex.append(i+1)

listIndexArray = np.asarray(listIndex)
distances = np.sqrt( ( xDim[listIndexArray] - 1155.0 )**2 + yDim[listIndexArray]**2 )
distancesSorted = np.sort(distances)

distancesBetween = np.absolute(distancesSorted[0:-1] - distancesSorted[1:])

distancesBetween = np.sort(distancesBetween)

print 'max', np.amax(distancesBetween)
print 'min', np.amin(distancesBetween)
print 'average', np.average(distancesBetween)
print 'std', np.std(distancesBetween)
print 'sorted', distancesBetween[-15:]













