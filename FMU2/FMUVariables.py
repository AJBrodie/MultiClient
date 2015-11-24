# -*- coding: utf-8 -*-
"""
File: FMUVariables.py
Author: Andrew Brodie
Created: 30.10.2015

Description:
File to describe the variables present in the model.

"""
# ------------------------ Include Packages --------------------
## External Packages
import numpy

## Personal packages
from SL_io.vtk import *

           
# ---------------------- Create Variable Structure -----------------
class ModelVariables():
    def __init__(self):
        self.ScalarVariable = ScalarVariable()
        self.CombinedVariable = CombinedVariable()

class experiment():
    def __init__(self):
        self.startTime = 0
        self.stopTime = 0
        self.dt = 0
        self.tolerance = 0
        
class ScalarVariable():
    def __init__(self):
        self.Real = []
        
class RealScalarVariable():
    def __init__(self, ID = None):
        self.__name = ''
        self.__id = ID
        
class CombinedVariable():
    def __init__(self):
        self.meshes = []


class fmi2MeshData:
    def __init__(self,name=None,values=None):
        if name is None:
            self.name = ''
        else:
            self.name = name
            
        if values is None:
            self.values = numpy.zeros(1)
        else:
            self.values=values

class fmi2Mesh:
    def __init__(self,name=None,numNodes=None,numElems=None,nodes=None,
                 nodeIDs=None,numNodesPerElem=None,elems=None,dataLst=None):
        #string
        if name is None:
            self.name=''
        else:
            self.name=name
        
        # Int
        if numNodes is None:
            self.numNodes=0
        else:
            self.numNodes=numNodes
        if numElems is None:
            self.numElems=0
        else:
            self.numElems=numElems
            
        #Array 3n
        if nodes is None:
            self.nodes = numpy.zeros(1)
        else:
            self.nodes=nodes
            
        #Array n
        if nodeIDs is None:
            nodeIDs = numpy.zeros(1)
        else:
            nodeIDs = nodeIDs
            
        #Array ne
        if numNodesPerElem is None:
            self.numNodesPerElem = numpy.zeros(1)
        else:
            self.numNodesPerElem=numNodesPerElem

        # Array unknown size (array containing node IDs)
        if elems is None:
            self.elems = numpy.zeros(1)
        else:
            self.elems=elems

        # Array for storing mesh data
        if dataLst is None:
            self.dataLst = []
        else:
            self.dataLst=dataLst        

## ------------------------- Define the Model Variables -------------------- ##

ModelVariables = ModelVariables()
experiment = experiment()

# list of fmi2ScalarVariable
ModelVariables.ScalarVariable.Real.append(RealScalarVariable())

# Real - ScalarVariable with index 0 is time
ModelVariables.ScalarVariable.Real[0].__name = 'time'
ModelVariables.ScalarVariable.Real[0] = 0


meshes=[]
nMeshes = 2
## Preallocate meshes
for i in range(0,nMeshes):
    meshes.append(fmi2Mesh())

## First Mesh Definition
name='Boundary01'
numNodes=6
numElements=3
nodes = numpy.array([
       0,0,0,
       0,1,0,
       1,0,0,
       1,1,0,
       2,0,0,
       2,1,0])
       
nodeIDs = numpy.array([0,1,2,3,4,5])
numNodesPerElem = numpy.array([4,3,3])
elems = numpy.array([
        0,1,3,2,
        2,5,4,
        2,3,5])

meshes[0] = fmi2Mesh(name,numNodes,numElements,nodes,nodeIDs,numNodesPerElem,elems)

# Data on mesh 1
disp1data = numpy.array([
        0,0,0,
        0,1,0,
        1,0,0,
        1,1,0,
        2,0,0,
        2,1,0])
disp1data = disp1data.reshape(len(disp1data),1)
disp1=fmi2MeshData('displacement',disp1data)

temp1data = numpy.array([0,1,2,3,4,5])
temp1data = temp1data.reshape(len(temp1data),1)
temp1=fmi2MeshData('pressure',temp1data)

data1=[temp1,disp1]

## Second Mesh Definition
name='Boundary02'
numNodes=15
numElements=12
nodes = numpy.array([
        0,0,0,
        0,0,0.25,
        0,0,0.5,
        0,0,0.75,
        0,0,1,
        1,0,0,
        1,0,0.25,
        1,0,0.5,
        1,0,0.75,
        1,0,1,
        2,0,0,
        2,0,0.25,
        2,0,0.5,
        2,0,0.75,
        2,0,1
       ])
nodeIDs = numpy.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
numNodesPerElem = numpy.array([3,3,3,3,3,3,3,3,4,4,4,4])
elems = numpy.array([
        0,6,5,
        0,1,6,
        1,2,6,
        2,7,6,
        2,8,7,
        2,3,8,
        3,4,8,
        4,9,8,
        5,6,11,10,
        6,7,12,11,
        7,8,13,12,
        8,9,14,13
        ])

meshes[1] = fmi2Mesh(name,numNodes,numElements,nodes,nodeIDs,numNodesPerElem,elems)

# Data on mesh 2
disp2data = numpy.array([
        0,0,0,
        0,0,0.25,
        0,0,0.5,
        0,0,0.75,
        0,0,1,
        1,0,0,
        1,0,0.25,
        1,0,0.5,
        1,0,0.75,
        1,0,1,
        2,0,0,
        2,0,0.25,
        2,0,0.5,
        2,0,0.75,
        2,0,1
       ])
disp2data = disp2data.reshape(len(disp2data),1)
disp2 = fmi2MeshData('displacement',disp2data)

temp2data = numpy.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
temp2data = temp2data.reshape(len(temp2data),1)
temp2 = fmi2MeshData('pressure',temp2data)

data2=[temp2,disp2]
meshes[0].dataLst = data1
meshes[1].dataLst = data2

ModelVariables.CombinedVariable.Meshes = meshes
meshes = None