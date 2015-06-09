# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:00:13 2015

@author: andrew
"""
from mpi4py import MPI
import numpy

class fmi2Mesh:
    def __init__(self,name='',numNodes=0,numElems=0,nodes=numpy.zeros(1),
                 nodeIDs=numpy.zeros(1),numNodesPerElem=numpy.zeros(1)
                 ,elems=numpy.zeros(1)):
        #string        
        self.name=name
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
        self.comm.Recv(data, source=0, tag=77)
        
    def fmi2SetReal(self,data):
        self.comm.Send(data, dest=0, tag=77)
        
    def fmi2GetMesh(self,mesh):
#        buf = numpy.array('c')*256
#        r = self.comm.Irecv(buf,source=0)
#        status = MPI.Status()
#        r.Wait(status)
#        n = status.Get_count(MPI.CHAR)
#        mesh.name = buf[:n].tostring()
        mesh.name=self.comm.recv(source=0, tag=78)
          
        
        ints=numpy.zeros(2,dtype='int')
        self.comm.Recv(ints, source=0, tag=78)
        mesh.numNodes=ints[0]
        mesh.numElems=ints[1]
        
        mesh.nodes=numpy.zeros(3*mesh.numNodes,dtype='d')
        self.comm.Recv(mesh.nodes,source=0, tag=78)
        
        mesh.nodeIDs=numpy.zeros(mesh.numNodes,dtype='int')
        self.comm.Recv(mesh.nodeIDs, source=0, tag=78)
        
        mesh.numNodesPerElem=numpy.zeros(mesh.numElems,dtype='int')
        self.comm.Recv(mesh.numNodesPerElem, source=0, tag=78)
        
        # python for loop to sum all elements of numNodesPerElem
        total = 0
        for i in range(0,int(mesh.numElems),1):
            total = total + mesh.numNodesPerElem[i]
            
        mesh.elems=numpy.zeros(total,dtype='int')
        self.comm.Recv(mesh.elems, source=0, tag=78)


    def fmi2SetMesh(self,mesh):
        self.comm.send(mesh.name, dest=0, tag=79)
        
        ints=numpy.zeros(2,dtype='int')
        ints[0]=mesh.numNodes
        ints[1]=mesh.numElems
        self.comm.Ssend(ints, dest=0, tag=79)
        
        self.comm.Ssend(mesh.nodes, dest=0, tag=79)
        
        self.comm.Ssend(mesh.nodeIDs, dest=0, tag=79)
        
        self.comm.Ssend(mesh.numNodesPerElem, dest=0, tag=79)
        
        self.comm.Ssend(mesh.elems, dest=0, tag=79)
   
        
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
    
