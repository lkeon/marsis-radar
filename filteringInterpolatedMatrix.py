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
import multiprocessing as mp
from MARSIS_functions import noise_stat_MARSIS_RDR

def main():
    numberOfTimeScans = 200
    path = '/gpfs/work/PHD_Summer15/dataMARSIS/'
    fileName = 'interpolatedMatrix-QNNradius13-z150-z350-3000-874-1208.npy'
    matrix = np.load(path+fileName)

    xDim = matrix.shape[1]
    yDim = matrix.shape[2]

    # Multiprocessing parameters
    numberProc = 18
    pool = mp.Pool(processes=numberProc) # Define the number of processors to calculate

    # Start calculation of filtering negative values in parallel
    print '\n---- START FILTERING NEGATIVE VALUES ----'
    print 'Number of negative values in input matrix:', (matrix < 0).sum()

    results = []
    for calculateZ in range(numberOfTimeScans):
	results.append( pool.apply_async( filterNegativeValues, args=(matrix[calculateZ,:,:], calculateZ, xDim, yDim) ) )

    # Get the results of filtering negative values
    filteredMatrix = np.zeros( (numberOfTimeScans, xDim, yDim) )

    for r in results:
	indexResult = r.get()[1]
	planeResult = r.get()[0]

	filteredMatrix[indexResult,:,:] = planeResult

    print 'Number of negative values in filtered matrix:', (filteredMatrix < 0).sum()

    #Start calculation for noise filtering
    stDevSpan = 2.0 # Everything below avg+stDevSpan*deviation will be treated as noise
    noiseFrame = 100 # Frame for determining noise
    print '\n---- START FILTERING NOISE VALUES ----'
    print 'Using factor', stDevSpan, 'for standard deviation'
    print 'Using noise frame of length:', noiseFrame

    resultsNoise = []
    for calculateY in range (yDim):
	resultsNoise.append( pool.apply_async( filterNoiseAlongZ, args=(filteredMatrix[:,:,calculateY], calculateY, noiseFrame, stDevSpan) ) )

    # Get the results of filtering noisy values
    denoisedFilteredMatrix = np.zeros( (numberOfTimeScans, xDim, yDim) )

    for rN in resultsNoise:
	indexResult = rN.get()[1]
	planeResult = rN.get()[0]

	denoisedFilteredMatrix[:,:,indexResult] = planeResult

    # Save interpolated matrix
    print '\n--- SAVING MATRIX ---'
    savedName = 'denoisedInterpolatedMatrix-QNNradius13-z150-z350-3000-874-1208.npy'
    np.save(savedName, denoisedFilteredMatrix)
    

def filterNegativeValues( inputPlane, indexZ, xDim, yDim ):
    # Printing info
    name = mp.current_process().name
    print ' ', name, 'filtering negative values in z plane', indexZ+1
    
    for i in range(xDim):
	for j in range(yDim):

	    # Check if we are in interioir of plane
	    if inputPlane[i,j] < 0:
		if (i > 0) and (i < xDim-1):
		    if (j > 0) and (j < yDim-1):
			
			# Calculate average value of bordering points
			sumElement = np.sum( inputPlane[i-1:i+2, j-1:j+2] ) - inputPlane[i,j]
			if sumElement > 0:
			    inputPlane[i,j] = sumElement/8.0
			else:
			    inputPlane[i,j] = 0.0

		    else:
			inputPlane[i,j] = 0.0
	    
		else:
		    inputPlane[i,j] = 0.0

    return [inputPlane, indexZ]

def filterNoiseAlongZ(zxPlane, yPlaneIndex, noiseFrame, stDevSpan):
    # Define window length for averaging in z dimension.
    #windowAvg = 10
    # Printing info
    name = mp.current_process().name
    print ' ', name, 'filtering noise values in y plane', yPlaneIndex+1
    
    zDim = zxPlane.shape[0]
    xDim = zxPlane.shape[1]

    # Calculate noise and standard deviation along z axis
    for xIndex in range(xDim):
	noiseVect = noise_stat_MARSIS_RDR(zxPlane[:,xIndex], noiseFrame)
	avgNoise = noiseVect[0]
	stdvNoise = noiseVect[1]
	
	# Put value below noise treshold to 0
	for zIndex in range(zDim):
	    if (zxPlane[zIndex,xIndex] < avgNoise + stDevSpan*stdvNoise):
		zxPlane[zIndex,xIndex] = 0.0

	## Conduct window averaging anlong z
	#zVector = zxPlane[:,xIndex]
	#zVector = np.concatenate(( zVector, np.zeros(windowAvg-1) ))
	#zVectorAvg = np.zeros(zDim)
	
	#for zIndex in range(zDim):
	    #zVectorAvg[i] = np.sum(zVector[zDim:zDim+windowAvg])

	#zxPlane[:,xIndex] = zVectorAvg
	

    return [zxPlane, yPlaneIndex]


if __name__ == '__main__':
    main()