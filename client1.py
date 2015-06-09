#! /usr/bin/env python

# ------------------------ Include Packages --------------------
from mpi4py import MPI
import numpy

# ------------------------ Header Definitions ------------------
def log(msg, *args):
    if rank == 0:
        print(msg % args)

class mesh:
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


# ------------------------ Client Variables ---------------------
myClientID = 1;
root = 0

name='Mesh01'
numNodes=6
numElements=3
nodes = numpy.array([
       0,0,0,
       0,1,0,
       1,0,0,
       1,1,0,
       2,1,0,
       2,2,0],dtype='d')
nodeIDs = numpy.array([1,2,3,4,5,6])
numNodesPerElem = numpy.array([3,3,4])
elems = numpy.array([1,2,3,2,4,3,3,4,5,6])

mesh = mesh(name,numNodes,numElements,nodes,nodeIDs,numNodesPerElem,elems)


# ------------------------ Client Operation ---------------------
# Connecting to server
comm = MPI.Comm.Get_parent()
rank = comm.Get_rank()
log('Client 1 ...')
log('server connected...')
log('Sending Client ID to Server...')
comm.send(myClientID, dest=0, tag=77)


# Receiving the data from Server
data = numpy.arange(10, dtype='d')
comm.Recv(data, source=0, tag=77)
log('Received data is ::')
print(data[1], data[2]);

data = data + 10;
# Sending the data to Sever
comm.Send(data, dest=0, tag=77)
log('Sent data is ::')
print(data[1], data[2]);

# Send client Mesh
log('Sending Mesh - Name')
comm.send(mesh.name, dest=0, tag=78)

log('Sending Mesh - Number of nodes & Number of elements')
ints=numpy.zeros(2,dtype='int')
ints[0]=mesh.numNodes
ints[1]=mesh.numElems
comm.Ssend(ints, dest=0, tag=78)
log('Sending Mesh - Nodes')
comm.Ssend(mesh.nodes, dest=0, tag=78)
log('Sending mesh - Node IDs')
comm.Ssend(mesh.nodeIDs, dest=0, tag=78)
log('Sending mesh - Number of nodes per Element')
comm.Ssend(mesh.numNodesPerElem, dest=0, tag=78)
log('Sending mesh - Elements')
comm.Ssend(mesh.elems, dest=0, tag=78)


# Disconnect from server
log('Disconnecting server...')
comm.Disconnect()
