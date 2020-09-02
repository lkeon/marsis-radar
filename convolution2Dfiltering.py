# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;
'''
v1.1 implementation of 3D Gaussian function
'''

import numpy as np
import matplotlib.pyplot as plt
from astropy.convolution import Gaussian2DKernel, Gaussian1DKernel, convolve_fft

path = '/gpfs/work/PHD_Summer15/dataMARSIS/'
fileName = 'denoisedFilteredMatrix-3000-874-0708.npy'
fileNameToSave = 'convolvedDenoisedFilteredMatrix-3000-874-0708.npy'

matrix = np.load(path+fileName)
matrix = matrix[150:350,:,:]
matrix = np.log10(matrix)
print 'Filtered matrix shape:', matrix.shape
stddevGauss = 3
sizeGauss = 4
size = sizeGauss*stddevGauss

gauss2d = Gaussian2DKernel(stddevGauss, x_size=sizeGauss*stddevGauss, y_size=sizeGauss*stddevGauss, factor=10) #stddev, size*stddev, size*stddev, factor of oversampling

typeFilter = 'custom_z' # Use 'gaussian_z' or 'custom_z'
if typeFilter == 'gaussian_z':
    gauss1d = Gaussian1DKernel(stddevGauss, x_size=sizeGauss*stddevGauss, factor=10)
elif typeFilter == 'custom_z':
    gauss1d = Gaussian1DKernel(0.8, x_size=5, factor=10)

gauss1dArray = gauss1d.array
gauss2dArray = gauss2d.array
gauss3dArray = np.zeros((gauss1dArray.shape[0], size, size))

ii = 0
for i in gauss1dArray:
    gauss3dArray[ii,:,:] = i*gauss2dArray
    ii += 1

print 'Gaussian 3D filter shape:', gauss3dArray.shape

convolvedMatrix = convolve_fft(matrix, gauss3dArray, interpolate_nan=True, normalize_kernel=True, allow_huge=True)

np.save(path+fileNameToSave, convolvedMatrix)

plt.figure()
plt.subplot(131)
plt.imshow(matrix[25,:,:], interpolation='none', origin='lower')
plt.title('Z plane 200')
plt.colorbar()

plt.subplot(132)
plt.imshow(matrix[:,100,:], interpolation='none', origin='lower')
plt.title('X plane 200')
plt.colorbar()

plt.subplot(133)
plt.imshow(matrix[:,:,100], interpolation='none', origin='lower')
plt.title('Y plane 200')
plt.colorbar()
plt.tight_layout()


plt.figure()
plt.subplot(131)
plt.imshow(convolvedMatrix[25,:,:], interpolation='none', origin='lower')
plt.title('Z plane 200')
plt.colorbar()

plt.subplot(132)
plt.imshow(convolvedMatrix[:,100,:], interpolation='none', origin='lower')
plt.title('X plane 200')
plt.colorbar()

plt.subplot(133)
plt.imshow(convolvedMatrix[:,:,100], interpolation='none', origin='lower')
plt.title('Y plane 200')
plt.colorbar()
plt.tight_layout()


plt.figure()
plt.imshow(gauss2d, interpolation='none', origin='lower')
plt.title('Gaussian filter')
plt.colorbar()

plt.show()
