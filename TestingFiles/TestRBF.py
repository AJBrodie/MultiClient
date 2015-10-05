# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 23:09:27 2015

@author: andrew
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
vals = mesh.dataLst[1].values
norm = 0

interpSystem = RBF_system(dim, pts, vals, RBF_fn, norm)

interpPoint = numpy.array(-8,0,0)

val = interpSystem.interp(interpPoint)