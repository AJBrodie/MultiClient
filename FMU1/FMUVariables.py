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

# --------------------- Variable Types --------------------------
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
            
# ---------------------- Define Model Variables -----------------
'''
This section replaces the use of other xml file to define
variables or whatever other alternative method is deemed suitable
for defining the mesh.

ModelExchange = None
CoSimulation.SourceFiles=['./FMU1.py']

UnitDefinitions=[]
# infinite list of fmi2Unit

TypeDefinitions=[]
# infinite list of fmi2SimpleType

LogCategories=[]
# infinite list of Category

DefaultExperiment = None

VendorAnnotations = []
# list of type fmi2Annotation
'''
'''
ModelVariables.ScalarVariable = []
# list of fmi2ScalarVariable
class fmi2ScalarVariable:
    
    Class for describing scalar variables, see initialiser for allowed values
    
    def __init__(name=None, valueReference=None, description=None, causality=None, variability=None, initial=None, canHandleMultipleSetPerTimeInstant=None,fmi2Type=None,annotations=None):
        
        if name is None:
            self.name = 'NA'
        else:
            self.name = name
            
        if valueReference is None:
            self.valueReference = 0
        else:
            self.valueReference = valueReference
            
        if description is None:
            self.description = ''
        else:
            self.description = description
        
        if causality is None:
            
            Valid values:
            - parameter
            - calculatedParameter
            - input/output
            - local
            - independent
            
            self.causality = ''
        else:
            self.causality = causality
        
        if variability is None:
            self.variability = ''
            
            Valid values:
            - constant
            - fixed
            - tunable
            - discrete
            - continuous
            
        else:
            self.variability = variability
            
        if initial is None:
            self.initial = ''
            
            Valid values:
            - exact
            - approx
            - calculated
            
        else:
            self.initial = initial
            
        if canHandleMultipleSetPerTimeInstant is None:
            self.canHandleMultipleSetPerTimeInstant = fmi2False
        else:
            self.canHandleMultipleSetPerTimeInstant = canHandleMultipleSetPerTimeInstant
            
        if fmi2Type is None:
            self.fmi2Type = ''
        else:
            self.fmi2Type = fmi2Type
            
        if annotations is None:
            self.annotations = []
        else:
            self.annotations = annotations

ModelVariables.VectorVariable = []
# list of fmi2VectorVariable

ModelVariables.CombinedVariable = []
# list of fmi2CombinedVariable
'''
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
        

ModelVariables = ModelVariables()
experiment = experiment()

# list of fmi2ScalarVariable
#ModelVariables.ScalarVariable.Real = []
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
name='Mesh01'
numNodes=6
numElements=3
nodes = numpy.array([
       0,0,0,
       0,1,0,
       1,0,0,
       1,1,0,
       2,1,0,
       2,0,0])
#nodes = nodes.reshape(len(nodes),1)

nodeIDs = numpy.array([0,1,2,3,4,5])
nodeIDs = nodeIDs.reshape(len(nodeIDs),1)

numNodesPerElem = numpy.array([3,3,4])
numNodesPerElem = numNodesPerElem.reshape(len(numNodesPerElem),1)

elems = numpy.array([0,1,2,1,3,2,2,3,4,5])
elems = elems.reshape(len(elems),1)


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

temp1data = numpy.array([0,1,2,3,4,5])
temp1data = temp1data.reshape(len(temp1data),1)
# DATA HAS TO BE STORED AS A 2D MATRIX (length x 1)
temp1=fmi2MeshData('temperature',temp1data)

data1=[temp1,disp1]

meshes[0] = fmi2Mesh(name,numNodes,numElements,nodes,nodeIDs,numNodesPerElem,elems)


#mesh2file('clienta_xy',meshes[0])

#data2file('clienta_xy_data',meshes[0],data1)

## Second Mesh Definition
name='Mesh02'
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
#nodes = nodes.reshape(len(nodes),1)

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
       
temp2data = numpy.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
temp2data = temp2data.reshape(len(temp2data),1)
temp2=fmi2MeshData('temperature',temp2data)

data2=[temp2,disp2]
meshes[0].dataLst = data1
meshes[1].dataLst = data2

#mesh2file('clienta_xz',meshes[1])
#data2file('clienta_xz_data',meshes[1],data2)

ModelVariables.CombinedVariable.meshes = meshes
meshes = None