# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;
"""
Script for populating 3D matrix with MARSIS data
"""
import getopt
import sys

def usage():
    print 'Use -r or --resolution to define the resolution of surface matrix. Use -l or --latitude to define latitude border of the matrix.'

def main():
    try:
	opts, args = getopt.getopt(sys.argv[1:], 'r:l:')
    except getopt.GetoptError as err:
	print 'Error reading parameters.'
	usage()
	sys.exit()

    for o,a in opts:
	if o in ( '-r', '--resolution' ):
	    resolutionMatrix = float(a)
	elif o in ( '-l', '--latitude' ):
	    maxLatitude = float(a)

    import numpy as np
    import os

    libraryPath = '/pico/home/userexternal/lkocjanc/Documents/marsisCode'
    sys.path.append(libraryPath)
    import MARSIS_functions as mar

    # Calculation parameters
    rSphere = 3376.2 # Mars polar radius
    #maxLatitude = -70.0 #Border value of latitude that will be projected - imported as argument
    #resolutionMatrix = 1.0 # Resolution of terrain matrix in km - imported as argument

    # Data parameters
    numberOfTimeScans = 512
    dataPath = '/pico/work/PHD_Summer15/MARSIS_DATA/L2/' # begin and finish path with '/'

    print '\n--- CALCULATION SETTINGS ---'
    print 'Using polar radius:', rSphere, 'km'
    print 'Using latitude border:', maxLatitude, 'deg'
    print 'Using matrix resolution', resolutionMatrix, 'km'
    print '\n--- DATA SETTINGS ---'
    print 'Library path:', libraryPath
    print 'Data path:', dataPath
    print 'Number of time samples in radargram:', numberOfTimeScans
    print '\n--- CALCULATION ---'
    
    # Calculate maximal value of projected cartesian coordinate system
    borderCoordinates = mar.orto_proj_MARSIS(0.0, maxLatitude, 0.0, -90.0, rSphere )
    borderValue = round( borderCoordinates[1] )

    # Define size of a surface array
    sizeMatrix = round( 2*borderValue/resolutionMatrix + 1 )
    sizeMatrix = int(sizeMatrix)

    surfaceMatrix = np.zeros( [numberOfTimeScans, sizeMatrix, sizeMatrix] )

    # Import datafiles from folder
    importLongitude = 'SUB_SC_LONGITUDE'
    importLatitude = 'SUB_SC_LATITUDE'
    importRadar_ZERO_F1 = 'ECHO_MODULUS_ZERO_F1_DIP'

    # Loop between datafiles in folder
    filesList = os.listdir(dataPath)
    numberDatafiles = len(filesList)
    counterDataFile = 0

    for dataFile in filesList:
	dataFilePath = dataPath + dataFile
	counterDataFile += 1

	#if counterDataFile == 10:
	    #break

	print 'Analysing ' + dataFile + ' | ' + str(counterDataFile)+' out of ' + str(numberDatafiles)
	
	# Import position data
	longitudeMat = mar.read_MARSIS_RDR( dataFilePath, importLongitude )
	latitudeMat = mar.read_MARSIS_RDR( dataFilePath, importLatitude )
	
	longitudeMatSize = longitudeMat.shape[0]
	
	if longitudeMatSize > 1:
	    # Import radargram data
	    radargram = mar.read_MARSIS_RDR( dataFilePath, importRadar_ZERO_F1 )
	    
	    # Apply spherical to planar transformation
	    for i in range(longitudeMatSize):
		# Check if the point is on southern hemisphere
		if latitudeMat[i] < 0:
		    xyVect = mar.orto_proj_MARSIS(longitudeMat[i], latitudeMat[i], 0.0, -90.0, rSphere )
		    
		    # Check if loaded position is in border range
		    if ( abs( xyVect[0] ) <= borderValue ) and ( abs( xyVect[1] ) <= borderValue ):
			XpositionInMatrix = int( round(xyVect[0]) )
			YpositionInMatrix = int( round(xyVect[1]) )
			
			#print 'Adding echo No: ' + str(i) + ' at position ( '+ str(XpositionInMatrix) + ', ' + str(YpositionInMatrix) + ' )'
			
			surfaceMatrix[:,XpositionInMatrix, YpositionInMatrix] = radargram[i, :]
		    

    print 'end'

if __name__ == "__main__":
    main()