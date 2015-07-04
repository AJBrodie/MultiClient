# -*- coding: utf-8 -*-
"""
fmi2.py
Created on Tue Apr 28 16:00:13 2015
@author: andrew

- Package to define fmi2 functions for implimentation by the server
"""
from mpi4py import MPI
import numpy

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

class fmi2Component:
    # Definition for a class to store information about the clients
    def __init__(self,clientid,comm):
        self.clientid = clientid
        self.comm = comm
        self.meshLst = [fmi2Mesh('',-1)]
        
    def fmi2GetReal(self,data):
        self.comm.Recv(data, source=0, tag=77)
        
    def fmi2SetReal(self,data):
        self.comm.Send(data, dest=0, tag=77)
        
    def fmi2GetMesh(self):
        
        myTag = self.clientid + 50        
        
        meshSize=self.comm.recv(source=0, tag=myTag)
        
        
        if meshSize > 1:
            for k in range(1,meshSize,1):
                self.meshLst.append(fmi2Mesh())
        
        for i in range(0,meshSize,1):

    
            fmi2Logger('Receiving mesh name')
            self.meshLst[i].name=self.comm.recv(source=0, tag=myTag)
            
            fmi2Logger('Receiving mesh integers')            
            ints = self.comm.recv(source=0, tag=myTag)          
            self.meshLst[i].numNodes=ints[0]
            self.meshLst[i].numElems=ints[1]
                        
            fmi2Logger('Receiving mesh nodes')
            self.meshLst[i].nodes=self.comm.recv(source=0, tag=myTag)            
            
            fmi2Logger('Receiving mesh nodeIDs')
            self.meshLst[i].nodeIDs = self.comm.recv(source=0, tag=myTag)
            
            fmi2Logger('Receiving mesh nodes per element') 
            self.meshLst[i].numNodesPerElem = self.comm.recv(source=0, tag=myTag)

            fmi2Logger('Receiving mesh elements')
            self.meshLst[i].elems = self.comm.recv(source=0, tag=myTag)
        
    def fmi2GetMeshData(self,meshInd,numDataSets):
        # meshInd: indicy of the mesh on which data is mapped
        # numDataSets: size of list of data components being received
        myTag = self.clientid + 50 + meshInd
        
        if numDataSets > 1:
            for k in range(1,numDataSets,1):
                self.meshLst[meshInd].dataLst.append(fmi2MeshData())
        
        for i in range(0,numDataSets,1):
                        
            fmi2Logger('---------------fmi2GetMeshData( %d , %d )--------------' % (meshInd, numDataSets))
            fmi2Logger('Receiving meshdataset %d of %d (on mesh:: %d)...' % (i+1,numDataSets,meshInd+1))
            name = self.comm.recv(source=0, tag = myTag)
            values = self.comm.recv(source=0, tag = myTag)
            fmi2Logger('Received')
            
            if i > 0:
                self.meshLst[meshInd].dataLst.append(fmi2MeshData(name,values))
            else:
                self.meshLst[meshInd].dataLst[i] = fmi2MeshData(name,values)
                
            fmi2Logger('Stored')
 
    def fmi2SetMeshdata(self,meshInd,dataLst):
        myTag = self.clientid+meshInd+50
        
        for i in range(0,len(dataLst),1):
            self.comm.send(dataLst[i].name,dest=0,tag=myTag)
            self.comm.send(dataLst[i].values,dest=0,tag=myTag)
        
    def fmi2FreeInstance(self):
        self.comm.Disconnect()
        
    

def fmi2Logger(msg, *args):
    rank = MPI.COMM_WORLD.Get_rank()    
    if rank == 0:
        print(msg % args)
          
def fmi2Instantiate(clientFile):
    # Run Client
    comm = MPI.COMM_SELF.Spawn('xterm', args=['-hold','-e','python3',clientFile],maxprocs=1)
    #comm = MPI.COMM_SELF.Spawn('xterm', args=['-hold','-e','python3','-m','pdb',clientFile],maxprocs=1)
    
    # As soon a client connects add a dictionary entry for that client with its communicator.     
    clientID = -1
    fmi2Logger('Receiving clientID')
    clientID = comm.recv(source=0, tag= 77)
    if clientID == 0:
        fmi2Logger('Wrong Client ID received .... terminating server !')
        exit();
    fmi2Logger('client %i connected...', clientID)
    
    return fmi2Component(clientID,comm)
    
