# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;

import numpy as np
from scipy.interpolate import Rbf
import MARSIS_functions as mar
import matplotlib.pyplot as plt

rSphere = 3376.2 # Mars polar radius
maxLatitude = -75.0 #Border value of latitude that will be projected
resolutionMatrix = 3.0 # Resolution of terrain matrix in km
numberOfTimeScans = 512 # Number of time scans in radargram

# Calculate maximal value of projected cartesian coordinate system
borderCoordinates = mar.orto_proj_MARSIS(0.0, maxLatitude, 0.0, -90.0, rSphere )
borderValue = round( borderCoordinates[1] )

# Define size of a surface array
sizeMatrix = round( 2*borderValue/resolutionMatrix + 1 )
sizeMatrix = int(sizeMatrix)

print sizeMatrix

# Define matrix for interpolation
XinterpolationGrid , YinterpolationGrid = np.mgrid[-borderValue:borderValue:sizeMatrix*1j, -borderValue:borderValue:sizeMatrix*1j]

# Initialize interpolation matrix
interpolatedMatrix = np.zeros( [numberOfTimeScans, sizeMatrix, sizeMatrix] )

# Load data
print '\n--- LOADING DATA ---'
matrix = np.load('/pico/home/userexternal/lkocjanc/Documents/marsisCode/data/positionRadargramMat-1000-0308.npy')

numberOfPoints = matrix.shape[0]
useNumberOfoints = numberOfPoints/30

print 'Using',useNumberOfoints, 'for interpolation'

positionMat = matrix[0:useNumberOfoints,0:2]
radargramMat = matrix[0:useNumberOfoints,2:]

# Interpolation
for iTimeScan in range(numberOfTimeScans):
    radargramVect = radargramMat[:,iTimeScan]

    print 'Interpolating plane ' + str(iTimeScan+1) + ' out of ' + str(numberOfTimeScans)

    interpObj = Rbf(positionMat[:,0], positionMat[:,1], radargramVect, function='linear')

    xi = XinterpolationGrid.flatten()
    yi = YinterpolationGrid.flatten()
    interpolatedPlane2 = interpObj(xi, yi)
    interpolatedMatrix[iTimeScan,:,:] = interpolatedPlane2.reshape( (sizeMatrix,sizeMatrix) )

    '''
    plt.imshow(interpolatedPlane2.reshape( (sizeMatrix,sizeMatrix) ), origin='lower')
    plt.title('Interpolated plane')
    plt.colorbar()
    plt.show()
    '''

# Save interpolated matrix to binary file .npy
print '\n--- WRITING FILE ---'
np.save('interpolatedMatrix-RBF-1000-0408.npy', interpolatedMatrix)