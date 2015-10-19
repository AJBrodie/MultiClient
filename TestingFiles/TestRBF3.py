# -*- coding: utf-8 -*-
"""
File: /TestingFiles/TestRBF3.py
Author: Andrew Brodie
Date: 18.10.15

DESCRIPTION
File to test the implementation of the radial basis function mapping. Two real
meshes are read in from a previous study. A solution is plotted to the finer
mesh and then mapped to the coarser mesh

>  <  ^

"""
import numpy
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from vtk import *
from fmi2 import *
import MeshMatching.RBF
import MeshMatching.RBF_MQ

meshFine = fmi2Mesh()
dataSetsFine=[]
dataSetsFine.append(fmi2MeshData())

meshCoarse = fmi2Mesh()
dataSetsCoarse=[]
dataSetsCoarse.append(fmi2MeshData())
dataSetsCoarse.append(fmi2MeshData())
dataSetsCoarse.append(fmi2MeshData())

filenameFine = 'interface2_fine_scale.vtk'
filenameCoarse = 'interface2_coarse_scale.vtk'

## ------------------------------- READ IN MESHES -------------------------- ##
print('Reading in fine mesh')
readVTK(filenameFine,meshFine)
meshFine.dataLst = dataSetsFine
meshFine.dataLst[0].name = 'Data'
meshFine.dataLst[0].values = numpy.zeros((meshFine.numNodes,1))

print('Reading in coarse mesh')
readVTK(filenameCoarse,meshCoarse)
meshCoarse.dataLst = dataSetsCoarse
meshCoarse.dataLst[0].name = 'DataInterp'
meshCoarse.dataLst[0].values = numpy.zeros((meshCoarse.numNodes,1))
meshCoarse.dataLst[1].name = 'DataPlot'
meshCoarse.dataLst[1].values = numpy.zeros((meshCoarse.numNodes,1))
meshCoarse.dataLst[2].name = 'DataDiff'
meshCoarse.dataLst[2].values = numpy.zeros((meshCoarse.numNodes,1))


## ------------------------- PLOT DATA ON FINE MESH ------------------------ ##
print('Generating values on fine mesh')

for i in range(0,meshFine.numNodes):
    x = meshFine.nodes[i*3]
    y = meshFine.nodes[i*3+1]
    z = meshFine.nodes[i*3+2]
    
    meshFine.dataLst[0].values[i,0]=numpy.sin(3*(numpy.sin(5*(x**2)) + z**2 - numpy.sin(2*(z**2))))


## ------------------------ MAP DATA TO COARSE MESH ------------------------ ## 
print('Mapping values to coarse mesh')

scale = 0.1         # Scale is larger than point separation, smaller than solution scale
RBF_fn = MeshMatching.RBF_MQ.RBF_MQ(scale)

dim = 3
pts = meshFine.nodes
vals = meshFine.dataLst[0].values

interpSystem = MeshMatching.RBF.RBF_system(dim, pts, vals, RBF_fn)

interpPoints = meshCoarse.nodes

meshCoarse.dataLst[0].values = interpSystem.interp(interpPoints)

## ----------------------- PLOT DATA ON COARSE MESH ------------------------ ##
print('Generating values on fine mesh')

for i in range(0,meshCoarse.numNodes):
    x = meshCoarse.nodes[i*3]
    y = meshCoarse.nodes[i*3+1]
    z = meshCoarse.nodes[i*3+2]
    
    meshCoarse.dataLst[1].values[i,0]=numpy.sin(3*(numpy.sin(5*(x**2)) + z**2 - numpy.sin(2*(z**2))))
    
## ----------- CALCULATE DIFFERENCE BETWEEN PLOTTED AND INTERP ------------- ##
meshCoarse.dataLst[2].values = meshCoarse.dataLst[1].values-meshCoarse.dataLst[0].values

## ------------------------ OUTPUT TO VTK FILE ----------------------------- ##
print('Outputing meshes and values to files')
data2file('CoarseMesh(interp)_scale',meshCoarse,meshCoarse.dataLst)
data2file('FineMesh(Orig)_scale',meshFine,meshFine.dataLst)