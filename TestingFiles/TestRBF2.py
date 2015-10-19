# -*- coding: utf-8 -*-
"""
File: /TestingFiles/TestRBF2.py
Author: Andrew Brodie
Date: 11.10.15

DESCRIPTION
File to test the implementation of the radial basis function. Arbitrary values 
(a parabola) are created on meshA (dx/dy = 0.25) then interpolated on meshB
(dx/dy = 0.2) using the radial basis function method and plotted using
matplotlib.

"""

import sys
sys.path.append("..") # Adds higher directory to python modules path.

import numpy
import matplotlib.pyplot as plt

from vtk import *
from fmi2 import *
import MeshMatching.RBF
import MeshMatching.RBF_MQ

meshA = fmi2Mesh()
dataSetsA=[]
dataSetsA.append(fmi2MeshData())

meshB = fmi2Mesh()
dataSetsB=[]
dataSetsB.append(fmi2MeshData())

## ------------------------------- CREATE MATRICES ------------------------- ##
nXA = int(5/0.25 + 1)
nYA = int(5/0.25 + 1)
nPtsA = nXA * nYA

ptsA = numpy.zeros(3*nPtsA)
xA = numpy.zeros((1,nPtsA))
yA = numpy.zeros((1,nPtsA))
cntA = 0
for i in range(0,nXA):
    for j in range(0,nYA):
        ptsA[cntA*3] = i*0.25
        xA[0,cntA] = i*0.25
        ptsA[cntA*3+1] = j*0.25
        yA[0,cntA] = j*0.25
        ptsA[cntA*3+2] = 0
        cntA = cntA + 1

nXB = int(5/0.2 + 1)
nYB  = int(5/0.2 + 1)       
nPtsB = nXB * nYB
ptsB = numpy.zeros(3*nPtsB)
xB = numpy.zeros((1,nPtsB))
yB = numpy.zeros((1,nPtsB))
cntB = 0
for i in range(0,nXB):
    for j in range(0,nYB):
        ptsB[cntB*3] = i*0.2
        xB[0,cntB] = i*0.2
        ptsB[cntB*3+1] = j*0.2
        yB[0,cntB] = j*0.2
        ptsB[cntB*3+2] = 0
        cntB = cntB + 1
        
## ------------------------ CALCULATE VALUES ON MATRIX A ------------------- ##        
valA = xA * (xA-5) * yA * (yA - 5)
xAPlot = numpy.reshape(xA,(nXA,nYA))
yAPlot = numpy.reshape(yA,(nXA,nYA))
zAPlot = numpy.reshape(valA,(nXA,nYA))

## ----------------------- PLOT OF INITIAL MESH VALUES --------------------- ##
plt.figure(1)
plt.contourf(xAPlot,yAPlot,zAPlot)
plt.colorbar()
plt.draw()
plt.show(block=False)


## --------------------------------- TEST of RBF --------------------------- ##

scale = 0.3         # Scale is larger than point separation, smaller than solution scale
RBF_fn = MeshMatching.RBF_MQ.RBF_MQ(scale)

dim = 2
interpSystem = MeshMatching.RBF.RBF_system(dim, ptsA, valA, RBF_fn)

valB = interpSystem.interp(ptsB)


## ---------------------------- PLOTTING OF RBF RESULT --------------------- ##

xBPlot = numpy.reshape(xB,(nXB,nYB))
yBPlot = numpy.reshape(yB,(nXB,nYB))
zBPlot = numpy.reshape(valB,(nXB,nYB))

plt.figure(2)
plt.contourf(xBPlot,yBPlot,zBPlot)
plt.colorbar()
plt.draw()
plt.show()
