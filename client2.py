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
myClientID = 2;
root = 0
mesh=mesh()

# ------------------------ Client Operation ---------------------
# Connecting to server
comm = MPI.Comm.Get_parent()
rank = comm.Get_rank()
log('Client 2 ...')
log('server connected...')
log('Sending Client ID to Server...')
comm.send(myClientID, dest=0, tag=77)

data = numpy.arange(10, dtype='d')

### Receiving the data from Server
comm.Recv(data, source=0, tag=77)
log('Received data is ::')
print(data[1], data[2]);

data = data - 10;
### Sending the data to Sever
comm.Send(data, dest=0, tag=77)
log('Sent data to server is ::')
print(data[1], data[2]);

### -----  Receive mesh ----- ###
log('Receiving Mesh - Name')
mesh.name=comm.recv(source=0, tag=79)

log('Receiving Mesh - Number of nodes & Number of elements')
ints=numpy.zeros(2,dtype='int')
comm.Recv(ints, source=0, tag=79)
mesh.numNodes=ints[0]
mesh.numElems=ints[1]

log('Receiving Mesh - Nodes')
mesh.nodes=numpy.zeros(3*mesh.numNodes,dtype='d')
comm.Recv(mesh.nodes,source=0, tag=79)

log('Receiving mesh - Node IDs')
mesh.nodeIDs=numpy.zeros(mesh.numNodes,dtype='int')
comm.Recv(mesh.nodeIDs, source=0, tag=79)

log('Receiving mesh - Number of nodes per Element')
mesh.numNodesPerElem=numpy.zeros(mesh.numElems,dtype='int')
comm.Recv(mesh.numNodesPerElem, source=0, tag=79)

log('Receiving mesh - Elements')
# python for loop to sum all elements of numNodesPerElem
total = 0
for i in range(0,int(mesh.numElems),1):
    total = total + mesh.numNodesPerElem[i]
        
mesh.elems=numpy.zeros(total,dtype='int')
comm.Recv(mesh.elems, source=0, tag=79)

# ----------------------------- Disconnect from server ------------------ #
log('disconnecting server...')
comm.Disconnect()
