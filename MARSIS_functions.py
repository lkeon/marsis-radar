# -*- coding: utf-8 -*-
# Function ibrary for MARSIS project.
# kate: indent-pasted-text false; indent-width 4;

# Function to import MARSIS data
# Library MARSIS_R_SS3_TRK_CMP is imported automatically within this function but has to be present in the folder
def read_MARSIS_RDR( RdrFile, ParameterName = 'notSet', StartRecord = 'notSet', StopRecord = 'notSet', SkipRecords = 'notSet' ):
    if ('_SS1_TRK_CMP_' in RdrFile) and ('R_' in RdrFile):
        print 'This type of file cannot be read yet'
        return
    
    elif ('_SS3_TRK_CMP_' in RdrFile) and ('R_' in RdrFile):
        import MARSIS_R_SS3_TRK_CMP as mar
        import numpy as np

    elif ('_SS4_TRK_CMP_' in RdrFile) and ('R_' in RdrFile):
        print 'This type of file cannot be read yet'
        return
    
    elif ('_SS5_TRK_CMP_' in RdrFile) and ('R_' in RdrFile):
        print 'This type of file cannot be read yet'
        return
    
    else:
        print 'File ', RdrFile, 'does not follow standard naming conventions, file type could not be determined.'
        
    # The data product file is opened.
    try:
        fid = open(RdrFile, 'r')
    except IOError:
        print 'read_MARSIS_RDR:MissingInputFile, The required data product file', RdrFile, 'could not be opened'
    #fid = open(RdrFile, 'r')
        
    # The length in bytes of the data product file is retrieved, and divided by
    # the length of a file record in bytes to obtain the number of records in
    # the file.
    fid.seek(0, 2)
    FileBytes = fid.tell()
    FileRecords = FileBytes/mar.RecordBytes
    
    if round(FileRecords) != FileRecords:
        fid.close()
        print 'read_MARSIS_RDR:FractionalNumberOfRecords, The data product file', RdrFile, 'cotains', FileRecords, 'records, a non integer number of records'
    
    # If the only input argument is the name of a data product file, the
    # function returns the number of records contained in that file.
    if (ParameterName == 'notSet') and (StartRecord == 'notSet') and (StopRecord == 'notSet') and (SkipRecords == 'notSet'):
        MarsisRdr = FileRecords
        fid.close()
        return MarsisRdr
        
    # The name of the parameter to be extracted from the data product file is
    # compared to the list of parameters in the data product, to determine its
    # position in the list.
    try:
        ParameterIndex = mar.Parameter.index(ParameterName)
    except ValueError:
        fid.close()
        print 'read_MARSIS_RDR:ParameterNotFound, The parameter', ParameterName, 'is not listed among those contained in a MARSIS RDR FRM data product.'

    # If input values are not provided, default values are assigned to
    # StartRecord, StopRecord and SkipRecords
    if StartRecord == 'notSet':
        StartRecord = 1
        
    if StopRecord == 'notSet':
        StopRecord = FileRecords
        
    if SkipRecords == 'notSet':
        SkipRecords = 1
        
    # StartRecord, StopRecord and SkipRecords are checked for consistency.
    if (StartRecord < 1) or (StartRecord > FileRecords):
        fid.close()
        print 'read_MARSIS_RDR:InvalidValueForStartRecord, The last record to be extracted is record', SkipRecords, ', which is outside the valid interval [ 1,', FileRecords, ']'
        
    if (StopRecord < 1) or (StopRecord > FileRecords):
        fid.close()
        print 'read_MARSIS_RDR:InvalidValueForStopRecord, The last record to be extracted is record', StopRecord, ', which is outside the valid interval [ 1,', FileRecords, ']'
        
    if (SkipRecords < 1) or (SkipRecords > FileRecords):
        fid.close()
        print 'read_MARSIS_RDR:InvalidValueForSkipRecords, The number of records to be skipped is', SkipRecords, ', which is outside the valid interval [ 1,', FileRecords, ']'
        
    if StopRecord < StartRecord:
        fid.close()
        print 'read_MARSIS_RDR:StopRecordBeforeStartRecord, The first record to be extracted is record', StartRecord, 'and is greater than last record to be extracted, which is record', StopRecord, '.'
        
    # the number of records to be extracted from the data product file is
    # determined.
    Records = len( range(StartRecord - 1, StopRecord + 1, SkipRecords) )
    
    if Records == 0:
        fid.close()
        print 'read_MARSIS_RDR:NoRecordsExtracted, The combination of StartRecord =', StartRecord, ', StopRecord =', StopRecord, ', SkipRecords =', SkipRecords, 'does not allow the extraction of records from this data product file.'
        
    #The requested parameter is extracted from the data product file.
    
    offset = (StartRecord - 1)*mar.RecordBytes + mar.OffsetBytes[ParameterIndex]
    fid.seek(offset, 0)
    
    dataType = getattr(np, mar.Precision[ParameterIndex])
    itemsImport = mar.Items[ParameterIndex]
    
    MarsisRdr = np.fromfile( fid, dtype = dataType, count = itemsImport )
    
    
    if (mar.ItemBytes[ParameterIndex] >= 1) and (mar.ItemBits[ParameterIndex] == 0):
        skip = (SkipRecords - 1)*mar.RecordBytes + mar.RecordBytes
        
    elif (mar.ItemBytes[ParameterIndex] == 0) and (mar.ItemBits[ParameterIndex] >= 1):
        skip = (SkipRecords - 1)*8*mar.RecordBytes + 8*mar.RecordBytes
    
    else:
        print 'read_MARSIS_RDR:WrongParameterFormat, The parameter', mar.Parameter[ParameterIndex], 'is described as being', mar.ItemBytes[ParameterIndex], 'bytes long and', mar.ItemBits[ParameterIndex], 'bits long.'
        
    for i in range(Records - 2):
        fid.seek(offset + (i + 1)*skip, 0)
        MarsisRdrRow = np.fromfile( fid, dtype = dataType, count = itemsImport )
        MarsisRdr = np.vstack( [MarsisRdr, MarsisRdrRow] )
    
    return MarsisRdr

# Function create_MARSIS_MAP creates specifications for polar mapping matrix with the biggest element size maxDimension
# assuming that Mars is a sphere with polar radius. Output list contains maximal values of phi and radius and their minimal
# step in the projected plane.
def dimensions_MARSIS_MAP( maxDimension = -1, latitudeToMap = 70.0 ):
    if maxDimension < 0:
        print 'create_MARSIS_MAP:ERROR, First argument for maximum dimension is not defined or is smaller than 0.'
        
    import math
    maxDimension = float(maxDimension)
    latitudeToMap = abs(latitudeToMap)
        
    polarRadius = 3376.2 #km
    
    # Compute the arc length from the latitude and specify the number of divisions (dimensionRadius) of the arc length
    angle = math.radians( 90.0 - latitudeToMap )
    radiusToPlot = angle*polarRadius
    dimensionRadius = math.ceil( radiusToPlot/maxDimension )
    
    # Compute the circumference of the bordering latitude and determine number of divisions and delta step
    radiusParallelPhi = polarRadius*math.cos( math.radians(latitudeToMap) )
    circumferenceParallel = 2*math.pi*radiusParallelPhi
    dimensionPhi = math.ceil( circumferenceParallel/maxDimension )
    
    deltaRadius = radiusToPlot/dimensionRadius
    deltaPhi = 360.0/dimensionPhi
    
    dimensionsList = [dimensionRadius, deltaRadius, dimensionPhi, deltaPhi]
    
    return dimensionsList
    
# Function for mapping spherical LAT/LON coordinates to planar polar coordinates assuming that Mars is a sphere
# with polar radius. Input is in DEG and latitudes are treaded equally for N and S pole.
def polar_transform_MARSIS_MAP( longitude, latitude ):
    import math
    longitude = abs(longitude)
    latitude = abs(latitude)
    
    # Compute the arc distance from the pole
    arcAngleRad = math.radians( 90 - float(latitude) )
    polarRadius = 3376.2 #km
    arcDistance = arcAngleRad*polarRadius
    
    listOut = [ float(longitude), arcDistance ]
    
    return listOut
    
# Function that finds the closest point in the mapping matrix. Input and output is in DEG. Function returns negative
# values in the list, if the input values are out of bounds.
def find_nearest_MARSIS_MAP( phi, radius, dimensionsList ):
    dimensionPhi = dimensionsList[2]
    dimensionRadius = dimensionsList[0]
    if phi > dimensionPhi and radius <= dimensionRadius:
        return [-1, 0]
    elif phi <= dimensionPhi and radius > dimensionRadius:
        return [0, -1]
    elif phi > dimensionPhi and radius > dimensionRadius:
        return [-1, -1]
    
    deltaPhi = dimensionsList[3]
    deltaRadius = dimensionsList[1]
    
    phi = float(phi)
    radius = float(radius)
    
    phiIndex = int( round( phi/deltaPhi ) )
    radiusIndex = int( round( radius/deltaRadius ) )
    
    indexList = [phiIndex, radiusIndex]    
    
    return indexList
    
# Function that determines noise statistics for an array of echoes. First argument is the array of the
# samples and second argument is the size of the window that is used to compute statistics. Samples are
# in columns, different frames are in different columns. If we have different looks of satellite, they are
# in third dimension.
def noise_stat_MARSIS_RDR( echo, nnoise ):
    import numpy as np
    import math    
    
    echoArray = np.asarray(echo)
    test = np.isfinite(echoArray)
    
    if False in test:
        print 'There are invalid values in the input matrix.'
        #return
    
    # Case for a row    
    if len(echoArray.shape) == 1:
        samples = echoArray.shape[0]
        
        boxf = np.zeros((1, samples))
        boxf[0, 0:nnoise] = 1
        ftboxf = np.conjugate( np.fft.fft(boxf) )
        
        convf = np.fft.ifft( np.fft.fft(echoArray)*ftboxf)
        istart = np.argmin(convf)
        istop = istart + nnoise - 1
        
        if istop <= samples:
            noise = echoArray[istart:istop + 1]
        else:
            noise = np.concatenate( (echoArray[istart:samples], echoArray[0:istop - samples + 1]) )
            
        avg = np.mean(noise)
        stdev = math.sqrt( np.var(noise, ddof = 1) )
        
    # Case of an array in shape of matrix
    elif len(echoArray.shape) == 2:
        samples = echoArray.shape[1]
        frames = echoArray.shape[0]
        
        avg = np.zeros(frames)
        stdev = np.zeros(frames)
        
        boxf = np.zeros((1, samples))
        boxf[0, 0:nnoise] = 1
        ftboxf = np.conjugate( np.fft.fft(boxf) )
        
        for i in range(frames):
            
            convf = np.fft.ifft( np.fft.fft(echoArray[i,:])*ftboxf)
            istart = np.argmin(convf)
            istop = istart + nnoise - 1
            
            if istop <= samples:
                noise = echoArray[i, istart:istop + 1]
            else:
                noise = np.concatenate( (echoArray[i, istart:samples], echoArray[i, 0:istop - samples + 1]) )
                
            avg[i] = np.mean(noise)
            stdev[i] = math.sqrt( np.var(noise, ddof = 1) )    
    
    # Case of an array in shape of multiple matrices    
    else:
        samples = echoArray.shape[2]
        frames = echoArray.shape[1]
        looks = echoArray.shape[0]
        
        avg = np.zeros((frames, looks))
        stdev = np.zeros((frames, looks))
        
        boxf = np.zeros((1, samples))
        boxf[0, 0:nnoise] = 1
        ftboxf = np.conjugate( np.fft.fft(boxf) )
        
        for j in range(looks):
            
            for i in range(frames):
            
                convf = np.fft.ifft( np.fft.fft(echoArray[j, i, :])*ftboxf)
                istart = np.argmin(convf)
                istop = istart + nnoise - 1
                
                if istop <= samples:
                    noise = echoArray[j, i, istart:istop + 1]
                else:
                    noise = np.concatenate( (echoArray[j, i, istart:samples], echoArray[j, i, 0:istop - samples + 1]) )
                    
                avg[i, j] = np.mean(noise)
                stdev[i, j] = math.sqrt( np.var(noise, ddof = 1) )

    return (avg, stdev)
                
# Fuction to extract data from the simulation file. Radargrams should be extracted in Fourier
# transform as separated RE and IM components. Input is a list of text parameters and output is
# a list of matrices in the same order as parameters. input = ('fileToRead', ['par1', 'par2', ...])
def simulation_read_MARSIS_RDR( RdrFile, ParametersToExtract ):
    import numpy as np

    # Number of bytes
    RecordBytes = 49312
    
    #Open the file
    fid = open(RdrFile, 'rb')
    
    fid.seek(0, 2)
    FileBytes = fid.tell()
    FileRecords = FileBytes/RecordBytes
    
    if round(FileRecords) != FileRecords:
        fid.close()
        print 'read_MARSIS_RDR:FractionalNumberOfRecords, The data product file', RdrFile, 'cotains', FileRecords, 'records, a non integer number of records'
        
    # Create specifications for parameters
    ParameterName = ['ostline', 'f0', 'theta_s', 'frameid', 'scetfw', 'scetff', 'Vt', 'Vr', 'NA', 'x0', 'y0', 'z0', 'alt0', 'Vx0', 'Vy0', 'Vz0', 'lon_0', 'lat_0', 'esm1f1r', 'esm1f1i', 'es00f1r', 'es00f1i', 'esp1f1r', 'esp1f1i', 'esm1f2r', 'esm1f2i', 'es00f2r', 'es00f2i', 'esp1f2r', 'esp1f2i']
    OffsetBytes = [0, 8, 24, 32, 40, 48, 56, 64, 72, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 4256, 8352, 12448, 16544, 20640, 24736, 28832, 32928, 37024, 41120, 45216]
    Items = [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512]
    
    outList = []
        
    for j in range( len(ParametersToExtract) ):
        ParameterIndex = ParameterName.index( ParametersToExtract[j] )
        
        ItemsImport = Items[ParameterIndex]
        offset = OffsetBytes[ParameterIndex]
        fid.seek(offset, 0)
        SimulationRdr = np.fromfile(fid, dtype = np.float64, count = ItemsImport)
        
        skip = RecordBytes
        
        for i in range(FileRecords - 1):
            fid.seek(offset + (i + 1)*skip, 0)
            SimulationRdrRow = np.fromfile( fid, dtype = np.float64, count = ItemsImport )
            SimulationRdr = np.vstack( (SimulationRdr, SimulationRdrRow) )
            
        outList.append(SimulationRdr)
        
    return outList
    
# Function to join RE and IM component and return inverse FFT
def ifft_sim_MARSIS_RDR( inputList ):
    import numpy.fft as fft    
    
    realArray = inputList[0]
    imagArray = inputList[1]
    
    # Frames should be arranged along the lines, because ifft operates along the lines.
    complexArray = realArray + 1j*imagArray
    timeDomainMat = abs( fft.ifft(complexArray) )
                                                                                                                                                                            
    return timeDomainMat
    
# Function for orthographic projection of a set of planetocentric coordiates
# to a plane. Angles should be entered in DEG. Type can be 'cartesian' or 'polar', default is 'cartesian'.
# Use rSphere = 3376.2 for pole radius on Mars.
def orto_proj_MARSIS( longitude, latitude, longitudePlaneCenter, latitudePlaneCenter, rSphere, type = 'cartesian' ):
    import math
    import numpy as np
    
    latitudePlaneCenterDEG = latitudePlaneCenter
    longitude = math.radians( float(longitude) )
    latitude = math.radians( float(latitude) )
    longitudePlaneCenter = math.radians( float(longitudePlaneCenter) )
    latitudePlaneCenter = math.radians( float(latitudePlaneCenter) )
    
    Xsphere = rSphere*math.cos(latitude)*math.cos(longitude)
    Ysphere = rSphere*math.cos(latitude)*math.sin(longitude)
    Zsphere = rSphere*math.sin(latitude)
    
    Xplane = rSphere*math.cos(latitudePlaneCenter)*math.cos(longitudePlaneCenter)
    Yplane = rSphere*math.cos(latitudePlaneCenter)*math.sin(longitudePlaneCenter)
    Zplane = rSphere*math.sin(latitudePlaneCenter)
    
    # Now a new reference frame must be built, in which the z axis is pointing
    # to the central point in the real mars, the x axis is in the equatorial plane
    # and the y axis is obtained as the vector forming a right-handed frame.
    if latitudePlaneCenterDEG == 90:
        Xaxis = np.array( [0, 1, 0] )
        Yaxis = np.array( [-1, 0, 0] )
        Zaxis = np.array( [0, 0, 1] )
        
    elif latitudePlaneCenterDEG == -90:
        Xaxis = np.array( [0, 1, 0] )
        Yaxis = np.array( [1, 0, 0] )
        Zaxis = np.array( [0, 0, -1] )
        
    else:
        Xaxis = np.array( [-Yplane, Xplane, 0] )   
        Zaxis = np.array( [Xplane, Yplane, Zplane] )
        Yaxis = np.cross( Zaxis, Xaxis )
        
        Xaxis = Xaxis/np.linalg.norm(Xaxis)
        Yaxis = Yaxis/np.linalg.norm(Yaxis)
        Zaxis = Zaxis/np.linalg.norm(Zaxis)
    
    # The map grid is rotated to new reference frame    
    x = Xaxis[0]*Xsphere + Xaxis[1]*Ysphere + Xaxis[2]*Zsphere
    y = Yaxis[0]*Xsphere + Yaxis[1]*Ysphere + Yaxis[2]*Zsphere
    z = Zaxis[0]*Xsphere + Zaxis[1]*Ysphere + Zaxis[2]*Zsphere
    
    if z < 0:
        print 'Ortographproj:NegativeHeights - They are on the opposite hemisphere w.r.t. the central point of the projection.'
        
    if type == 'polar':
        r = math.sqrt( x**2 + y**2 )
        phi = np.degrees( math.atan2(y, x) )
        
        arrayOut = np.array( [r, phi] )
        
    else:
        arrayOut = np.array( [x, y] )
    
    return arrayOut

# Function to read from saved .npy matrix with datastructure in columns as
# follows indexInDatagram, xPositionCartesian, yPositionCartesian, nameOfDataFile
def readPositionMat(data, matrix):
    import numpy as np
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

# Function to read single radargram in satellite path from datafile
# Library MARSIS_R_SS3_TRK_CMP is imported automatically within this function but has to be present in the folder
def read_oneDatagram_MARSIS_RDR( RdrFile, ParameterName = 'notSet', datagramNumber = 'notSet', StartRecord = 'notSet', StopRecord = 'notSet', SkipRecords = 'notSet' ):
    if ('_SS1_TRK_CMP_' in RdrFile) and ('R_' in RdrFile):
        print 'This type of file cannot be read yet'
        return
    
    elif ('_SS3_TRK_CMP_' in RdrFile) and ('R_' in RdrFile):
        import MARSIS_R_SS3_TRK_CMP as mar
        import numpy as np

    elif ('_SS4_TRK_CMP_' in RdrFile) and ('R_' in RdrFile):
        print 'This type of file cannot be read yet'
        return
    
    elif ('_SS5_TRK_CMP_' in RdrFile) and ('R_' in RdrFile):
        print 'This type of file cannot be read yet'
        return
    
    else:
        print 'File ', RdrFile, 'does not follow standard naming conventions, file type could not be determined.'
        
    # The data product file is opened.
    try:
        fid = open(RdrFile, 'r')
    except IOError:
        print 'read_MARSIS_RDR:MissingInputFile, The required data product file', RdrFile, 'could not be opened'
    fid = open(RdrFile, 'r')
        
    # The length in bytes of the data product file is retrieved, and divided by
    # the length of a file record in bytes to obtain the number of records in
    # the file.
    fid.seek(0, 2)
    FileBytes = fid.tell()
    FileRecords = FileBytes/mar.RecordBytes
    
    if round(FileRecords) != FileRecords:
        fid.close()
        print 'read_MARSIS_RDR:FractionalNumberOfRecords, The data product file', RdrFile, 'cotains', FileRecords, 'records, a non integer number of records'
    
    # If the only input argument is the name of a data product file, the
    # function returns the number of records contained in that file.
    if (ParameterName == 'notSet') and (StartRecord == 'notSet') and (StopRecord == 'notSet') and (SkipRecords == 'notSet') and (datagramNumber == 'notSet'):
        MarsisRdr = FileRecords
        fid.close()
        return MarsisRdr
        
    # The name of the parameter to be extracted from the data product file is
    # compared to the list of parameters in the data product, to determine its
    # position in the list.
    try:
        ParameterIndex = mar.Parameter.index(ParameterName)
    except ValueError:
        fid.close()
        print 'read_MARSIS_RDR:ParameterNotFound, The parameter', ParameterName, 'is not listed among those contained in a MARSIS RDR FRM data product.'

    # If input values are not provided, default values are assigned to
    # StartRecord, StopRecord and SkipRecords
    if StartRecord == 'notSet':
        StartRecord = 1
        
    if StopRecord == 'notSet':
        StopRecord = FileRecords
        
    if SkipRecords == 'notSet':
        SkipRecords = 1
        
    # StartRecord, StopRecord and SkipRecords are checked for consistency.
    if (StartRecord < 1) or (StartRecord > FileRecords):
        fid.close()
        print 'read_MARSIS_RDR:InvalidValueForStartRecord, The last record to be extracted is record', SkipRecords, ', which is outside the valid interval [ 1,', FileRecords, ']'
        
    if (StopRecord < 1) or (StopRecord > FileRecords):
        fid.close()
        print 'read_MARSIS_RDR:InvalidValueForStopRecord, The last record to be extracted is record', StopRecord, ', which is outside the valid interval [ 1,', FileRecords, ']'
        
    if (SkipRecords < 1) or (SkipRecords > FileRecords):
        fid.close()
        print 'read_MARSIS_RDR:InvalidValueForSkipRecords, The number of records to be skipped is', SkipRecords, ', which is outside the valid interval [ 1,', FileRecords, ']'
        
    if StopRecord < StartRecord:
        fid.close()
        print 'read_MARSIS_RDR:StopRecordBeforeStartRecord, The first record to be extracted is record', StartRecord, 'and is greater than last record to be extracted, which is record', StopRecord, '.'
        
    # the number of records to be extracted from the data product file is
    # determined.
    Records = len( range(StartRecord - 1, StopRecord + 1, SkipRecords) )
    
    if Records == 0:
        fid.close()
        print 'read_MARSIS_RDR:NoRecordsExtracted, The combination of StartRecord =', StartRecord, ', StopRecord =', StopRecord, ', SkipRecords =', SkipRecords, 'does not allow the extraction of records from this data product file.'
        
    #The requested parameter is extracted from the data product file.
    
    offset = (StartRecord - 1)*mar.RecordBytes + mar.OffsetBytes[ParameterIndex]
    fid.seek(offset, 0)
    
    dataType = getattr(np, mar.Precision[ParameterIndex])
    itemsImport = mar.Items[ParameterIndex]
    
    
    if (mar.ItemBytes[ParameterIndex] >= 1) and (mar.ItemBits[ParameterIndex] == 0):
        skip = (SkipRecords - 1)*mar.RecordBytes + mar.RecordBytes
        
    elif (mar.ItemBytes[ParameterIndex] == 0) and (mar.ItemBits[ParameterIndex] >= 1):
        skip = (SkipRecords - 1)*8*mar.RecordBytes + 8*mar.RecordBytes
    
    else:
        print 'read_MARSIS_RDR:WrongParameterFormat, The parameter', mar.Parameter[ParameterIndex], 'is described as being', mar.ItemBytes[ParameterIndex], 'bytes long and', mar.ItemBits[ParameterIndex], 'bits long.'
        
    i = datagramNumber-1
    fid.seek(offset + (i + 1)*skip, 0)
    MarsisRdrRow = np.fromfile( fid, dtype = dataType, count = itemsImport )
    
    return MarsisRdrRow

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
