#! /usr/bin/env python

# ------------------------ Include Packages --------------------
## External Packages
from mpi4py import MPI
import numpy
import sys
sys.path.append('..')

## Personal packages
from SL_io.vtk import *
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
myClientID = 1
myTag=myClientID + 50;
root = 0
meshes=[]

## Preallocate meshes
for i in (0,2,1):
    meshes.append(mesh())

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
nodeIDs = numpy.array([0,1,2,3,4,5])
numNodesPerElem = numpy.array([3,3,4])
elems = numpy.array([0,1,2,1,3,2,2,3,4,5])

disp1=data('displacement',numpy.array([
       0,0,0,
       0,1,0,
       1,0,0,
       1,1,0,
       2,1,0,
       2,0,0]))
       
temp1=data('temperature',numpy.array([0,1,2,3,4,5]))

data1=[temp1,disp1]

meshes[0] = mesh(name,numNodes,numElements,nodes,nodeIDs,numNodesPerElem,elems)


#mesh2file('clienta_xy',meshes[0])

data2file('clienta_xy_data',meshes[0],data1)

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
nodeIDs = numpy.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
numNodesPerElem = numpy.array([4,4,3,3,3,3,3,3,3,3,4,4])
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

meshes[1] = mesh(name,numNodes,numElements,nodes,nodeIDs,numNodesPerElem,elems)

disp2=data('displacement',numpy.array([
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
       ]))
       
temp2=data('temperature',numpy.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]))

data2=[temp2,disp2]

#mesh2file('clienta_xz',meshes[1])
data2file('clienta_xz_data',meshes[1],data2)

# --------------------------- Initialise Client ----------------------------
# Connecting to server
comm = MPI.Comm.Get_parent()
rank = comm.Get_rank()
log('Client 1 ...')
log('server connected...')
log('Sending Client ID to Server...')
comm.send(myClientID, dest=0, tag=77)


log('--------------------------------------------------------------------')
log('Initialise Client')
log('--------------------------------------------------------------------')
log('ClientID is :: %d' % myClientID)
log('Rank is :: %d' % rank)

# ------------------------ Client Operation ---------------------
log('--------------------------------------------------------------------')
log('Basic Array Communication')
log('--------------------------------------------------------------------')

# Syncing communication
#log('----Syncing Communication')
#comm.send(myClientID, dest=0, tag=77)
#comm.recv(source=0, tag=77)

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






log('--------------------------------------------------------------------')
log('Mesh Communication')
log('--------------------------------------------------------------------')

# Syncing communication
#log('----Syncing Communication')
#comm.send(myClientID, dest=0, tag=77)
#comm.recv(source=0, tag=77)

# Send client Meshes (corresponds fmi2GetMesh)
comm.send(len(meshes)-1, dest=0, tag=myTag)

for i in range(0,len(meshes)-1,1):
    log('--------------------------------------------------------------------')
    log('-- Sending mesh %d of %d' % (i+1,len(meshes)-1))
    log('--------------------------------------------------------------------')
    sendMesh(meshes[i])






# Send data on client meshes
log('--------------------------------------------------------------------')
log('Sending mesh data')
log('--------------------------------------------------------------------')

# Syncing communication
#log('----Syncing Communication')
#comm.send(myClientID, dest=0, tag=77)
#comm.recv(source=0, tag=77)

# Mesh 1
meshInd = 0
meshTag=myClientID + 50 + meshInd
log('--Sending data on mesh %d' % (meshInd+1))
for i in range(0,len(data1),1):

    log('----Sending name %d of %d' % (i+1,len(data1)))
    comm.send(data1[i].name,dest=0,tag=meshTag)
    log('----Sending values %d of %d' % (i+1,len(data1)))
    comm.send(data1[i].values,dest=0,tag=meshTag)

# Mesh 2
meshInd = 1
meshTag=myClientID + 50 + meshInd
log('--Sending data on mesh %d' % (meshInd+1))
for i in range(0,len(data1),1):
    
    log('----Sending name %d of %d' % (i+1,len(data1)))
    comm.send(data2[i].name,dest=0,tag=meshTag)
    log('----Sending values %d of %d' % (i+1,len(data1)))
    comm.send(data2[i].values,dest=0,tag=meshTag)






# Disconnect from server
log('Disconnecting server...')
comm.Disconnect()
