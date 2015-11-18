# -*- coding: utf-8 -*-
import os
os.chdir('..')


import SL_io.vtk as SLio
import FMUClasses
import numpy

def L2Norm(A):
    norm = 0
    for (value) in A:
        norm += abs(value)**2
        norm = numpy.sqrt(norm)
    return norm


file='Results/CoarseMesh(interp)_scale.vtk'
mesh = FMUClasses.fmi2Mesh()
dataLst = []
dataLst.append(FMUClasses.fmi2MeshData())
dataLst.append(FMUClasses.fmi2MeshData())
dataLst.append(FMUClasses.fmi2MeshData())
dataLst.append(FMUClasses.fmi2MeshData())

SLio.readVTK(file,mesh,dataLst)

norm1 = L2Norm(dataLst[0].values)
norm2 = L2Norm(dataLst[1].values)
norm3 = L2Norm(dataLst[2].values)
norm4 = L2Norm(dataLst[3].values)