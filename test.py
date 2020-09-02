# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;
'''
reading matrix
'''

import numpy as np
import matplotlib.pyplot as plt

path = '/gpfs/work/PHD_Summer15/dataMARSIS/'
fileName = 'convolvedDenoisedFilteredMatrix-3000-874-0708.npy'
fileNameCompare = 'zerosConvolvedDenoisedFilteredMatrix-3000-874-0708.npy'

matrix = np.load(path+fileName)
#matrix = matrix[150:350,:,:]
matrix = np.log10(matrix)

convolvedMatrix = np.load(path+fileNameCompare)

print 'Filtered matrix shape:', matrix.shape
print 'Comparison matrix shape:', convolvedMatrix.shape

plt.figure()
plt.subplot(131)
plt.imshow(matrix[50,:,:], interpolation='none', origin='upper')
plt.axis([-874,872,-874,872])
plt.title('Z plane 200')
plt.colorbar()

plt.subplot(132)
plt.imshow(matrix[:,100,:], interpolation='none', origin='upper')
plt.title('X plane 200')
plt.colorbar()

plt.subplot(133)
plt.imshow(matrix[:,:,100], interpolation='none', origin='upper')
plt.title('Y plane 200')
plt.colorbar()
plt.tight_layout()


plt.figure()
plt.subplot(131)
plt.imshow(convolvedMatrix[50,:,:], interpolation='none', origin='upper')
plt.title('Z plane 200')
plt.colorbar()

plt.subplot(132)
plt.imshow(convolvedMatrix[:,100,:], interpolation='none', origin='upper')
plt.title('X plane 200')
plt.colorbar()

plt.subplot(133)
plt.imshow(convolvedMatrix[:,:,100], interpolation='none', origin='upper')
plt.title('Y plane 200')
plt.colorbar()
plt.tight_layout()

plt.show()
