# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;
'''
v1.0 normal import
v1.1 import with -1 in central region
v1.2 first put -1 to matrix and save then write whole matrix to csv
'''
import math
import numpy as np

path = '/gpfs/work/PHD_Summer15/dataMARSIS/'
dataMatrix = 'zerosConvolvedDenoisedFilteredMatrix-3000-874-0708.npy'
matrix = np.load(path + dataMatrix)

# Saving new matrix with -1 in the center
outputDataMatrix = 'centerZerosConvolvedDenoisedFilteredMatrix-3000-874-0708.npy'
numberOfTimeScans = matrix.shape[0]
xRange = matrix.shape[1]
yRange = matrix.shape[2]

noCoveredRadiusInPoints = 77
noCoveredRadiusInPoints2 = 77**2
centerPoint = xRange/2

ii = 0
for i in range(xRange):
    print 'Analysing x plane:', ii+1, 'out of', xRange

    for j in range(yRange):
	if (i - centerPoint)**2 + (j - centerPoint)**2 < noCoveredRadiusInPoints2:
	    matrix[:,i,j] = -1
    ii += 1

#np.save(path+outputDataMatrix, matrix)
#print 'File', outputDataMatrix, 'written!'

# Saving .csv file
outputFilePath = path
outputFileName = 'centerZerosConvolvedDenoisedFilteredMatrix-3000-874-1308.csv'
outputFileComment = 'x,y,z,value\n'

borderValue = 874 # +- value of calculated grid
interpolatingResolution = 3 # resolutin of interpolated grid

xAxis = range(-borderValue, borderValue, interpolatingResolution)
xAxisLen = len(xAxis)
yAxis = xAxis
yAxisLen = xAxisLen

print 'X length of matrix:', xRange
print 'X length of CSV file:', len(xAxis)

outputFile = open(outputFilePath + outputFileName, 'w')
outputFile.write(outputFileComment)

ii = 0
for i in range(xAxisLen):
    print 'Writing to csv x plane:', i+1, 'out of', xAxisLen
    
    for j in range(yAxisLen):
	for k in range(numberOfTimeScans):
	    outputStr = str( xAxis[i] ) + ',' + str( yAxis[j] ) + ',' + str( k ) +  ',' + str( matrix[k,i,j] ) + '\n'
	    outputFile.write(outputStr)
	    ii += 1


outputFile.close()
print 'Writing finished.'

print '\nX and Y size:', xAxisLen
print 'Z size:', numberOfTimeScans


