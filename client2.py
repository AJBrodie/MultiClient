#! /usr/bin/env python

# ------------------------ Include Packages --------------------
from mpi4py import MPI
import numpy
import time

# ------------------------ Header Definitions ------------------
def log(msg, *args):
    if rank == 0:
        print(msg % args)

class mesh:
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

# ------------------------ Client Variables ---------------------
myClientID = 2;
root = 0
mesh=mesh()

# ------------------------ Client Operation ---------------------
# Connecting to server
comm = MPI.Comm.Get_parent()
rank = comm.Get_rank()
log('server connected...')
log('Sending Client ID to Server...')
comm.send(myClientID, dest=0, tag=77)

data = numpy.arange(10, dtype='d')
# Receiving the data from Server
comm.Recv(data, source=0, tag=77)
log('Received data is ::')
print(data[1], data[2]);

data = data - 10;
# Sending the data to Sever
comm.Send(data, dest=0, tag=77)
log('Sent data to server is ::')
print(data[1], data[2]);

time.sleep(5)
#Receive mesh
#log('Receiving Mesh - Name')
#comm.Recv(mesh.name, source=0, tag=77)
log('Receiving Mesh - Number of nodes')
comm.Recv(mesh.numNodes, source=0, tag=77)
log('Receiving Mesh - Number of elements')
comm.Recv(mesh.numElems, source=0, tag=77)
log('Receiving Mesh - Nodes')
comm.Recv(mesh.nodes, source=0, tag=77)
log('Receiving mesh - Node IDs')
comm.Recv(mesh.nodeIDs, source=0, tag=77)
log('Receiving mesh - Number of nodes per Element')
comm.Recv(mesh.numNodesPerElem, source=0, tag=77)
log('Receiving mesh - Elements')
comm.Recv(mesh.elems, source=0, tag=77)

# Disconnect from server
log('disconnecting server...')
comm.Disconnect()
