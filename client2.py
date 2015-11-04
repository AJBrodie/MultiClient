#! /usr/bin/env python

# ------------------------ Include Packages --------------------
## External Packages
from mpi4py import MPI
import numpy

## Personal packages
from vtk import *
from clients import *

# ----------------------- Client Header -------------------------
def log(msg, *args):
    if rank == 0:
        print(msg % args)
        
def sendMesh(mesh):
    log('Sending Mesh - Name')
    comm.send(mesh.name, dest=0, tag=myTag)
    log('Sending Mesh - Number of nodes & Number of elements')
    ints=numpy.zeros(2,dtype='int')
    ints[0]=mesh.numNodes
    ints[1]=mesh.numElems
    comm.send(ints, dest=0, tag=myTag)
    log('Sending Mesh - Nodes')
    comm.send(mesh.nodes, dest=0, tag=myTag)
    log('Sending mesh - Node IDs')
    comm.send(mesh.nodeIDs, dest=0, tag=myTag)
    log('Sending mesh - Number of nodes per Element')
    comm.send(mesh.numNodesPerElem, dest=0, tag=myTag)
    log('Sending mesh - Elements')
    comm.send(mesh.elems, dest=0, tag=myTag)


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
myTag=myClientID + 50;
root = 0
meshes=[]

## Preallocate meshes
for i in (0,2,1):
    meshes.append(mesh())

## First Mesh Definition
name='Mesh03'
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

meshes[0] = mesh(name,numNodes,numElements,nodes,nodeIDs,numNodesPerElem,elems)

# Data on mesh 1
disp1=data('displacement',numpy.array([
        0,0,0,
        0,1,0,
        1,0,0,
        1,1,0,
        2,0,0,
        2,1,0]))
temp1=data('temperature',numpy.array([0,1,2,3,4,5]))

data1=[temp1,disp1]
# Write mesh to file
#mesh2file('clientb_xy',meshes[0])

## Second Mesh Definition
name='Mesh05'
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

meshes[1] = mesh(name,numNodes,numElements,nodes,nodeIDs,numNodesPerElem,elems)

# Data on mesh 2
disp2 = data('displacement',numpy.array([
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
       ]))
temp2 = data('temperature',numpy.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]))

data2=[temp2,disp2]
# Write mesh to file
#mesh2file('clientb_xz',meshes[1])

# ------------------------ Client Initialisation ---------------------
# Connecting to server
comm = MPI.Comm.Get_parent()
rank = comm.Get_rank()
log('Client 2 ...')
log('server connected...')
log('Sending Client ID to Server...')
comm.send(myClientID, dest=0, tag=77)


log('--------------------------------------------------------------------')
log('Initialise Client')
log('--------------------------------------------------------------------')
log('')
log('ClientID is :: %d' % myClientID)
log('Rank is :: %d' % rank)

# ------------------------ Client Operation ---------------------
log('--------------------------------------------------------------------')
log('Basic Array Communication')
log('--------------------------------------------------------------------')

# Syncing communication
#log('----Syncing Communication')
#comm.send(myClientID, dest=0, tag=78)
#comm.recv(source=0, tag=78)

data = numpy.arange(10, dtype='d')

### Receiving the data from Server
comm.Recv(data, source=0, tag=77)
log('Received data is ::')
print(data[1], data[2]);

data = data - 10;
### Sending the data to Server
comm.Send(data, dest=0, tag=77)
log('Sent data to server is ::')
print(data[1], data[2]);






### -----  Send mesh ----- ###
log('--------------------------------------------------------------------')
log('Mesh Communication')
log('--------------------------------------------------------------------')

# Syncing communication
#log('----Syncing Communication')
#comm.send(myClientID, dest=0, tag=78)
#comm.recv(source=0, tag=78)

# Send client Meshes
comm.send(len(meshes)-1, dest=0, tag=myTag)

for i in range(0,len(meshes)-1,1):
    log('--------------------------------------------------------------------')
    log('Sending mesh %d of %d' % (i+1,len(meshes)-1))
    log('--------------------------------------------------------------------')
    sendMesh(meshes[i])






# Send data on client meshes
log('--------------------------------------------------------------------')
log('Sending mesh data')
log('--------------------------------------------------------------------')

# Syncing communication
#log('----Syncing Communication')
#comm.send(myClientID, dest=0, tag=78)
#comm.recv(source=0, tag=78)

# Mesh 1
meshInd = 0
meshTag=myClientID + 50 + meshInd
log('--Sending data on mesh %d' % (meshInd+1))
for i in range(0,len(data1),1):    
    log('----Sending name %d of %d' % (i,len(data1)))
    comm.send(data1[i].name,dest=0,tag=meshTag)
    log('----Sending values %d of %d' % (i,len(data1)))
    comm.send(data1[i].values,dest=0,tag=meshTag)

# Mesh 2
meshInd = 1
meshTag=myClientID + 50 + meshInd
log('--Sending data on mesh %d' % (meshInd+1))
for i in range(0,len(data1),1):    
    log('----Sending name %d of %d' % (i,len(data1)))
    comm.send(data2[i].name,dest=0,tag=meshTag)
    log('----Sending values %d of %d' % (i,len(data1)))
    comm.send(data2[i].values,dest=0,tag=meshTag)
 



   
# ----------------------------- Disconnect from server ------------------ #
log('disconnecting server...')
comm.Disconnect()
