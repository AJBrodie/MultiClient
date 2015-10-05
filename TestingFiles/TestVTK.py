# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 23:09:27 2015

@author: andrew
"""
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from vtk import *
from fmi2 import *

mesh = fmi2Mesh()
dataSets=[]
dataSets.append(fmi2MeshData())
dataSets.append(fmi2MeshData())
filename = 'ChannelFlow_01_FinalState.vtk'

# TEST OF readVTK
readVTK(filename,mesh,dataSets)