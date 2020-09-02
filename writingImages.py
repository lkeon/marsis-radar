# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;
'''
v1.0 writingimages to file
v1.1 the name of images have the same length
v1.2 images of zx-plane
'''

import numpy as np
import matplotlib.pyplot as plt

path = '/gpfs/work/PHD_Summer15/dataMARSIS/'
imagePath = '/pico/home/userexternal/lkocjanc/Documents/marsisCode/pictures_zeros/'
fileName = 'centerZerosConvolvedDenoisedFilteredMatrix-3000-874-0708.npy'

matrix = np.load(path+fileName)
yValues = matrix.shape[2]

print 'Filtered matrix shape:', matrix.shape

# Plotting
print '\n--- PLOTTING ---'
ii = 0
listPlot = range(yValues)
lengthFor = len(listPlot)
for planeIndex in listPlot:
    print 'Saving image of y plane', ii+1, 'out of', lengthFor
    interpolatedPlane = matrix[:,:,planeIndex]
    
    plt.imshow(interpolatedPlane, origin='upper', vmin=-1, vmax=2.5)
    plt.colorbar()
    
    plt.tight_layout()
    
    if planeIndex <= 9:
	figureName = imagePath + 'figureMatrixPlane-00' + str(planeIndex) + '.jpg'
    elif (planeIndex > 9) and (planeIndex <= 99):
	figureName = imagePath + 'figureMatrixPlane-0' + str(planeIndex) + '.jpg'
    else:
	figureName = imagePath + 'figureMatrixPlane-' + str(planeIndex) + '.jpg'
    
    plt.savefig(figureName, dpi=150)
    plt.clf()

    ii += 1

print '--- ALL SAVING DONE ---\n'