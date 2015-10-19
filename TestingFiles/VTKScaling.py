# -*- coding: utf-8 -*-
"""
File: /TestingFiles/VTKScaling.py
Author: Andrew Brodie
Date: 19.10.15

DESCRIPTION
File to read in VTK files and rescale them accordingly.
Coarse: 0.5 - 0.75
Fine: 0.075 - 0.75

>  <  ^

"""
import numpy
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from vtk import *
from fmi2 import *

meshFine = fmi2Mesh()

meshCoarse = fmi2Mesh()

filenameFine = 'interface2_fine.vtk'
filenameCoarse = 'interface2_coarse.vtk'

## ------------------------------- READ IN MESHES -------------------------- ##
print('Reading in fine mesh')
readVTK(filenameFine,meshFine)

print('Reading in coarse mesh')
readVTK(filenameCoarse,meshCoarse)

## -------------------------------- SCALE MESHES --------------------------- ##
coarseScaling = 1.5
fineScaling = 10

meshFine.nodes = meshFine.nodes * fineScaling
meshCoarse.nodes = meshCoarse.nodes * coarseScaling

## ------------------------------ OUTPUT MESHES ---------------------------- ##
filenameFine = 'interface2_fine_scale.vtk'
filenameCoarse = 'interface2_coarse_scale.vtk'
mesh2file(filenameFine,meshFine)
mesh2file(filenameCoarse,meshCoarse)