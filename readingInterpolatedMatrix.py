# -*- coding: utf-8 -*-
# kate: indent-pasted-text false; indent-width 4;
'''
v1.1 Reading one plane of interpolated matrix
'''

import numpy as np
import os
import sys
import matplotlib.pyplot as plt

path = '/gpfs/work/PHD_Summer15/dataMARSIS/'
data = 'denoisedFilteredMatrix-3000-874-0708.npy'
interpolatedMatrix = np.load(path+data)

interpolatedPlane = interpolatedMatrix[200,:,:]

plt.imshow(np.log10(interpolatedPlane), origin='lower')
plt.title('Interpolated plane')
plt.colorbar()

plt.show()

