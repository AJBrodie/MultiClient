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
       2,1,0,
       2,0,0])

nodeIDs = numpy.array([0,1,2,3,4,5])
nodeIDs = nodeIDs.reshape(len(nodeIDs),1)

numNodesPerElem = numpy.array([3,3,4])
numNodesPerElem = numNodesPerElem.reshape(len(numNodesPerElem),1)

elems = numpy.array([0,1,2,1,3,2,2,3,4,5])
elems = elems.reshape(len(elems),1)

x = nodes[0::3]
y = nodes[1::3]
z = nodes[2::3]

disp1data=numpy.zeros((numNodes*3))
#scale = 0.01
#disp1data[0::3]=scale*numpy.sin(x*numpy.pi)*numpy.sin(y*numpy.pi)*numpy.sin(z*numpy.pi)

disp1data = numpy.array([
       0,0,0,
       0,1,0,
       1,0,0,
       1,1,0,
       2,1,0,
       2,0,0])
disp1data = disp1data.reshape(len(disp1data),1)
# DATA HAS TO BE STORED AS A 2D MATRIX (length x 1)
disp1=fmi2MeshData('displacement',disp1data)

#press1data = 5*numpy.cos(x*numpy.pi)*numpy.sin(y*numpy.pi)*numpy.sin(z*numpy.pi)
press1data = numpy.array([0,1,2,3,4,5])
press1data = press1data.reshape(len(press1data),1)

# DATA HAS TO BE STORED AS A 2D MATRIX (length x 1)
press1=fmi2MeshData('pressure',press1data)

data1=[press1,disp1]

meshes[0] = fmi2Mesh(name,numNodes,numElements,nodes,nodeIDs,numNodesPerElem,elems)


## Second Mesh Definition
name='Boundary02'
numNodes=15
numElements=12
nodes = numpy.array([
        0,0,0,
        0,0,0.5,
        0,0,1,
        0.5,0,0,
        0.5,0,0.5,
        0.5,0,1,
        1,0,0,
        1,0,0.5,
        1,0,1,
        1.5,0,0,
        1.5,0,0.5,
        1.5,0,1,
        2,0,0,
        2,0,0.5,
        2,0,1
       ])

nodeIDs = numpy.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
nodeIDs = nodeIDs.reshape(len(nodeIDs),1)

numNodesPerElem = numpy.array([4,4,3,3,3,3,3,3,3,3,4,4])
numNodesPerElem = numNodesPerElem.reshape(len(numNodesPerElem),1)

elems = numpy.array([
        0,1,4,3,
        1,2,5,4,
        3,4,6,
        4,7,6,
        4,8,7,
        4,5,8,
        6,10,9,
        6,7,10,
        7,8,10,
        8,11,10,
        9,10,13,12,
        10,11,14,13
        ])
elems = elems.reshape(len(elems),1)

meshes[1] = fmi2Mesh(name,numNodes,numElements,nodes,nodeIDs,numNodesPerElem,elems)

disp2data = numpy.array([
        0,0,0,
        0,0,0.5,
        0,0,1,
        0.5,0,0,
        0.5,0,0.5,
        0.5,0,1,
        1,0,0,
        1,0,0.5,
        1,0,1,
        1.5,0,0,
        1.5,0,0.5,
        1.5,0,1,
        2,0,0,
        2,0,0.5,
        2,0,1
       ])
disp2data = disp2data.reshape(len(disp2data),1)
disp2=fmi2MeshData('displacement',disp2data)
       
press2data = numpy.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
press2data = press2data.reshape(len(press2data),1)
press2=fmi2MeshData('pressure',press2data)

data2=[press2,disp2]
meshes[0].dataLst = data1
meshes[1].dataLst = data2


ModelVariables.CombinedVariable.Meshes = meshes
meshes = None