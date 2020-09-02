# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;

'''
v1.0 Put values to 0 which have z index lower than maximum value
'''

import numpy as np
import multiprocessing as mp

def main():
    path = '/gpfs/work/PHD_Summer15/dataMARSIS/'
    fileName = 'convolvedDenoisedFilteredMatrix-3000-874-0708.npy'
    matrix = np.load(path+fileName)

    numberOfTimeScans = matrix.shape[0]
    xDim = matrix.shape[1]
    yDim = matrix.shape[2]

    # Multiprocessing parameters
    numberProc = 18
    pool = mp.Pool(processes=numberProc) # Define the number of processors to calculate

    # Start calculation of filtering negative values in parallel
    print '\n---- START FILTERING ----'

    resultsNoise = []
    for calculateY in range (yDim):
	resultsNoise.append( pool.apply_async( filterPutZero, args=(matrix[:,:,calculateY], calculateY) ) )

    # Get the results of filtering noisy values
    denoisedFilteredMatrix = np.zeros( (numberOfTimeScans, xDim, yDim) )

    for rN in resultsNoise:
	indexResult = rN.get()[1]
	planeResult = rN.get()[0]

	denoisedFilteredMatrix[:,:,indexResult] = planeResult

    # Save interpolated matrix
    print '\n--- SAVING MATRIX ---'
    savedName = 'zerosConvolvedDenoisedFilteredMatrix-3000-874-0708.npy'
    np.save(path+savedName, denoisedFilteredMatrix)

def filterPutZero(zxPlane, yPlaneIndex):
    # Printing info
    name = mp.current_process().name
    print ' ', name, 'replacing with zeros on y plane', yPlaneIndex+1
    
    zDim = zxPlane.shape[0]
    xDim = zxPlane.shape[1]
    zxPlaneZero = np.zeros((zDim, xDim))
    
    for xIndex in range(xDim):
	zVect = zxPlane[:,xIndex]
	maxIndex = np.argmax(zVect)
	zxPlaneZero[maxIndex:,xIndex] = zVect[maxIndex:]

    return [zxPlaneZero, yPlaneIndex]


if __name__ == '__main__':
    main()