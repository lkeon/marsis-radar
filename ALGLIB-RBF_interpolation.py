# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;

'''
v1.0 Basic QNN algorithm used with default settings
v1.1 Multilayer RBF-ML algorithm used with options implemented
v1.2 Using QNN algorithm with options implemented
v2.2.0 Is parallelised version of v1.2
v2.2.1 Is for calculating all the data and saving
'''

import numpy as np
import xalglib as xl
import matplotlib.pyplot as plt
import multiprocessing as mp

def main():
    # Data parameters
    numberOfTimeScans = 200
    borderValue = 874 # +- value of calculated grid
    interpolatingREsolution = 2 # resolutin of interpolated grid
    path = '/gpfs/work/PHD_Summer15/dataMARSIS/'
    fileName = 'positionRadargramMat-z150-z300-3000-0508.npy'

    # Import .npy matrix
    print '\n--- IMPORTING DATAFILE ---'
    matrix = np.load( path + fileName )
    numberOfPoints = matrix.shape[0]

    # Multiprocessing parameters
    numberProc = 16
    numberProcAvail = mp.cpu_count()
    pool = mp.Pool(processes=numberProc) # Define the number of processors to calculate

    x = readPositionMat(1, matrix)
    y = readPositionMat(2, matrix)

    # Interpolate on selected grid using calculated weights
    xAxis = range(-1*borderValue, borderValue, interpolatingREsolution)
    xAxisLen = len(xAxis)
    gridData = [xAxis, xAxisLen]

    # Setup calculation processes
    results = []
    print '\n--- STARTING CALCULATION ---'
    for calculateZ in range(numberOfTimeScans):
	results.append( pool.apply_async( RBFinterpolate, args=(x, y, readPositionMat(0, matrix, calculateZ), calculateZ, gridData) )  )

    # Get the results
    interpolatedMatrix = np.zeros( (numberOfTimeScans, xAxisLen, xAxisLen) )

    for r in results:
	indexResult = r.get()[0]
	planeResult = r.get()[1]
	
	interpolatedMatrix[indexResult,:,:] = planeResult

    # Save interpolated matrix
    print '\n--- SAVING INTERPOLATED MATRIX ---'
    outFile = 'interpolatedMatrix-QNNradius13-z150-z350-3000-874-1208.npy'
    np.save(path+outFile, interpolatedMatrix)

def RBFinterpolate(x, y, z, zIndex, gridData):
    # ---- INTERPOLATION PARAMETERS ----
    interpolationDimension = 2 # 2 for plane interpolation, 3 for volume interpolation
    interpolationDataDimension = 1 # 1 for interplating scalar values, vector interpolation also possible

    radiusFactorQ = 1.3 # default = 1.0, Coefficient for multiplying automatically determined interpolation radius, [0.75, 1.50], bigger factor gives greater smoothness
    radiusMedianFactorZ = 5.0 # default = 5.0, each radius cannot be bigger than factorZ*median_radius, so it does not influences to many points
    # ---- INTERPOLATION PARAMETERS END ----

    # Printing info
    name = mp.current_process().name
    print ' ', name, 'interpolating plane number', zIndex+1

    xyz = np.vstack( (x, y, z) ).T # Arrange in matrix
    xyzList = xyz.tolist() # Convert from array to normal list for xalglib

    # Create interpolation object
    plane = xl.rbfcreate(interpolationDimension, interpolationDataDimension)
    xl.rbfsetpoints(plane, xyzList)

    # Calculate weights
    xl.rbfsetalgoqnn(plane, radiusFactorQ, radiusMedianFactorZ)
    xl.rbfbuildmodel(plane)

    xAxis = gridData[0]
    xAxisLen = gridData[1]
    yAxis = xAxis
    yAxisLen = xAxisLen

    interpolatedPlaneList = xl.rbfgridcalc2(plane, xAxis, xAxisLen, yAxis, yAxisLen)

    interpolatedPlane = np.asarray(interpolatedPlaneList, dtype=np.float64) # Convert to numpy array
    #interpolatedPlane = np.absolute(interpolatedPlane) # Absolute value of all datapoints

    return [zIndex, interpolatedPlane]

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

if __name__ == '__main__':
    main()
    
    


