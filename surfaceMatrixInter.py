# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;
"""
Script for populating 3D matrix with MARSIS data.
v2.0 The interpolation is done first without reducing satellite datapoints.
After interpolation noise is estimated along each z axis and noisy data is
reduced.
v2.0.1 save also position and datagram matrix
v2.0.2 Operates with float32, longitude and latitude is still imported as float64
v2.4 saves a matrix with index | x | y | 'nameFile'
"""

import numpy as np
import os
import sys

libraryPath = '/pico/home/userexternal/lkocjanc/Documents/marsisCode'
sys.path.append(libraryPath)
import MARSIS_functions as mar

import matplotlib.pyplot as plt

from scipy.interpolate import griddata
#from vtk.util import numpy_support
#import vtk

# -------------------- PARAMETERS --------------------

# Calculation parameters
rSphere = 3376.2 # Mars polar radius
maxLatitude = -70.0 #Border value of latitude that will be projected
resolutionMatrix = 2 # Resolution of terrain matrix in km

# Data parameters
limitReading = 20 # Set to -1 to read all the files
numberOfTimeScans = 512
dataPath = '/pico/work/PHD_Summer15/MARSIS_DATA/L2/' # begin and finish path with '/'

# ------------------- PARAMETERS END -------------------

print '\n--- CALCULATION SETTINGS ---'
print 'Using polar radius:', rSphere, 'km'
print 'Using latitude border:', maxLatitude, 'deg'
print 'Using matrix resolution', resolutionMatrix, 'km'
print '\n--- DATA SETTINGS ---'
#print 'Library path:', libraryPath
print 'Data path:', dataPath
print 'Number of time samples in radargram:', numberOfTimeScans

if limitReading > 0:
    print 'Number of radargrams to read:', limitReading
else:
    print 'Number of radargrams to read: all in folder'

print '\n--- IMPORTING STARTED ---'

# Calculate maximal value of projected cartesian coordinate system
borderCoordinates = mar.orto_proj_MARSIS(0.0, maxLatitude, 0.0, -90.0, rSphere )
borderValue = round( borderCoordinates[1] )

# Define size of a surface array
sizeMatrix = round( 2*borderValue/resolutionMatrix + 1 )
sizeMatrix = int(sizeMatrix)

XinterpolationGrid , YinterpolationGrid = np.mgrid[-borderValue:borderValue:sizeMatrix*1j, -borderValue:borderValue:sizeMatrix*1j]
XinterpolationGrid = XinterpolationGrid.astype(np.float32, copy=False)
YinterpolationGrid = YinterpolationGrid.astype(np.float32, copy=False)

# Import datafiles from folder
importLongitude = 'SUB_SC_LONGITUDE'
importLatitude = 'SUB_SC_LATITUDE'
importRadar_ZERO_F1 = 'ECHO_MODULUS_ZERO_F1_DIP'

# Loop between datafiles in folder
filesList = os.listdir(dataPath)
numberDatafiles = len(filesList)
counterDataFile = np.uint16(0) # Count the number of datafiles to read in order to stop reading ad defined number
startSign = np.uint8(0)

for dataFile in filesList:
    dataFilePath = dataPath + dataFile
    counterDataFile += 1

    if counterDataFile > limitReading:
	break

    if (limitReading < 0) or (limitReading > numberDatafiles):
	print 'Analysing ' + dataFile + ' | ' + str(counterDataFile)+' out of ' + str(numberDatafiles)
    else:
	print 'Analysing ' + dataFile + ' | ' + str(counterDataFile)+' out of ' + str(limitReading) + ' | total: ' + str(numberDatafiles)
    
    # Import position data, two arrays of size (n, 1)
    longitudeMat = mar.read_MARSIS_RDR( dataFilePath, importLongitude )
    latitudeMat = mar.read_MARSIS_RDR( dataFilePath, importLatitude )
    
    longitudeMatSize = longitudeMat.shape[0]
    
    if longitudeMatSize > 1:
	# Import radargram data, size of array is (n, numberOfTimeScans)
	radargram = mar.read_MARSIS_RDR( dataFilePath, importRadar_ZERO_F1 )
	
	# Apply spherical to planar transformation
	for i in range(longitudeMatSize):
	    # Check if the point is on the southern hemisphere
	    if latitudeMat[i] < 0:
		xyVect = mar.orto_proj_MARSIS(longitudeMat[i], latitudeMat[i], 0.0, -90.0, rSphere )
		
		# Check if loaded position is in border range
		if ( abs( xyVect[0] ) <= borderValue ) and ( abs( xyVect[1] ) <= borderValue ):
		    positionVect = np.array( [xyVect[0], xyVect[1]], dtype=np.float32 )
		    # Initialize position and radargram matrices
		    if startSign == 0:
			startSign = 1
			positionMat = positionVect.astype(np.float32) # Copy positionVect and copy as float32
			fileMat = np.array([dataFile])
			indexMat = np.array([i])
		    # Append new values to matrices
		    else:
			positionMat = np.vstack( (positionMat, positionVect) )
			fileMat = np.vstack( (fileMat, dataFile) )
			indexMat = np.vstack( (indexMat, i) )

# Write position and radargram matrix
exportMat = np.hstack( (indexMat,positionMat, fileMat) )
np.save('exportedReadMat.npy', exportMat)

# Check if radargramMat has been populated
try:
    positionMat
except NameError:
    print '\nThe satellite orbits do not pass the defined area! \nChange value of maxLatitude, variable positionMat does not exist.\n'
    sys.exit()

