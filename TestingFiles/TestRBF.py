# -*- coding: utf-8 -*-
"""
File: /TestingFiles/TestRBF2.py
Author: Andrew Brodie
Date: 20.08.15

DESCRIPTION
File to test the implementation of the radial basis function mapping. A real 
flow field is read in and then a value is interpolated from this data at a 
single point.

"""
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from vtk import *
from fmi2 import *
from MeshMatching.RBF import *

mesh = fmi2Mesh()
dataSets=[]
dataSets.append(fmi2MeshData())
dataSets.append(fmi2MeshData())
filename = 'ChannelFlow_01_FinalState.vtk'

## ------------------------------- TEST OF readVTK ------------------------- ##
readVTK(filename,mesh,dataSets)

mesh.dataLst = dataSets


## --------------------------------- TEST of RBF --------------------------- ##
# 
scale = 0.2         # Scale is larger than point separation, smaller than solution scale
RBF_fn = RBF_MQ(scale)

dim = 3
pts = mesh.nodes
vals = mesh.dataLst[0].values
norm = 0

interpSystem = RBF_system(dim, pts, vals, RBF_fn)

interpPoint = numpy.array((-8,0,0))

val = interpSystem.interp(interpPoint)

print(val)