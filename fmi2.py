# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:00:13 2015

@author: andrew
"""
from mpi4py import MPI
import numpy

class fmi2Mesh:
    def __init__(self,numNodes=0,numElems=0,nodes=numpy.zeros(1),
                 nodeIDs=numpy.zeros(1),numNodesPerElem=numpy.zeros(1)
                 ,elems=numpy.zeros(1)):
        #string        
        #self.name=name
        # Int        
        self.numNodes=numNodes
        self.numElems=numElems
        #Array 3n        
        self.nodes=nodes
        #Array n
        self.nodeIDs=nodeIDs
        #Array ne
        self.numNodesPerElem=numNodesPerElem
        # Array unknown size (array containing node IDs)
        self.elems=elems

class fmi2Component:
    # Definition for a class to store information about the clients
    def __init__(self,clientid,comm):
        self.clientid = clientid
        self.comm = comm
        
    def fmi2GetReal(self,data):
        self.comm.Recv([data, MPI.INT], source=0, tag=77)
        
    def fmi2SetReal(self,data):
        self.comm.Send([data, MPI.INT], dest=0, tag=77)
        
    def fmi2GetMesh(self,mesh):
        #self.comm.Send([mesh.name, MPI.CHAR], dest=0, tag=77)
        self.comm.Send(mesh.numNodes, dest=0, tag=77)
        self.comm.Send(mesh.numElems, dest=0, tag=77)
        self.comm.Send(mesh.nodes, dest=0, tag=77)
        self.comm.Send(mesh.nodeIDs, dest=0, tag=77)
        self.comm.Send(mesh.numNodesPerElem, dest=0, tag=77)
        self.comm.Send(mesh.elems, dest=0, tag=77)

    def fmi2SetMesh(self,mesh):
        #self.comm.Recv(mesh.name, source=0, tag=77)
        self.comm.Recv(mesh.numNodes, source=0, tag=77)
        self.comm.Recv(mesh.numElems, source=0, tag=77)
        self.comm.Recv(mesh.nodes, source=0, tag=77)
        self.comm.Recv(mesh.nodeIDs, source=0, tag=77)
        self.comm.Recv(mesh.numNodesPerElem, source=0, tag=77)
        self.comm.Recv(mesh.elems, source=0, tag=77)     
        
    def fmi2FreeInstance(self):
        self.comm.Disconnect()
        
    

def fmi2Logger(msg, *args):
    rank = MPI.COMM_WORLD.Get_rank()    
    if rank == 0:
        print(msg % args)
          
def fmi2Instantiate(clientFile):
    # Run Client
    comm = MPI.COMM_SELF.Spawn('xterm', args=['-hold','-e','python3',clientFile],maxprocs=1)
    
    # As soon a client connects add a dictionary entry for that client with its communicator.     
    clientID = -1
    fmi2Logger('Receiving clientID')
    clientID = comm.recv(source=0, tag= 77)
    if clientID == 0:
        fmi2Logger('Wrong Client ID received .... terminating server !')
        exit();
    fmi2Logger('client %i connected...', clientID)
    
    return fmi2Component(clientID,comm)
    
