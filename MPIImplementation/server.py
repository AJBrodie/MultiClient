#! /usr/bin/env python

## External Packages
from mpi4py import MPI
import numpy
import time

import sys
sys.path.append('..')

## Personal Packages
from fmi2 import *
from SL_io.vtk import *
import MeshMatching.RBF

# ---------------------------------------------------------------------------
# --------------------------------- Body code -------------------------------
# ---------------------------------------------------------------------------

# ----------------------------- Declare Variables ---------------------------#

# Number of Clients expected
clientFile = ['client1.py','client2.py']
numClients = len(clientFile)

# mapp containing the communicators of clients.
clientMapp = {}
sudorank = MPI.COMM_WORLD.Get_rank()

# Data to be sent
data = numpy.arange(10, dtype='d')
mesh = []

root = 0

# Outputs from server initialization

fmi2Logger('')
fmi2Logger('Clients to be run::')
for i in range(0,numClients,1):
    fmi2Logger('%s' % clientFile[i])
fmi2Logger('Rank is:: %d' % sudorank)
fmi2Logger('Initial array:: %f - %f' % (data[1],data[9]))


# -------------------------- Instantiate Clients ----------------------------#
fmi2Logger('-----------------------------------------------------------------')
fmi2Logger('-------------------- Instantiating Clients ----------------------')
fmi2Logger('-----------------------------------------------------------------')

# As soon a client connects add a dictionary entry for that client with its communicator.
for i in range(0, numClients):
    fmi2Logger("instantiating client %i of %i", i+1, numClients)
    clientMapp[i] = fmi2Instantiate(clientFile[i])


# -------------------------- Basic Data Communication-------------------------#
fmi2Logger('-----------------------------------------------------------------')
fmi2Logger('---------------------- Basic Communication ----------------------')
fmi2Logger('-----------------------------------------------------------------')            
# Syncing client1
#fmi2Logger('Syncing Communication - Client 1')
#a=clientMapp[0].comm.recv(source = 0, tag = 77)
#clientMapp[0].comm.send(a, dest = 0, tag = 77)

# Syncing client2
#fmi2Logger('Syncing Communication - Client 2')
#a=clientMapp[1].comm.recv(source = 0, tag = 78)
#clientMapp[1].comm.send(a, dest = 0, tag = 78)

# Sending data to Client 1
fmi2Logger("Sending the data to client 1 :: ")
print(data[1], data[2])
clientMapp[0].fmi2SetReal(data)

# Receive from Client 1
fmi2Logger("Receiving the data from client 1:: ")
clientMapp[0].fmi2GetReal(data)
print(data[1], data[2])

# Dividing the data by 2
data = data * 0.5;

# Sending data to Client 2
fmi2Logger("Sending the data to client 2 :: ")
print(data[1], data[2])
clientMapp[1].fmi2SetReal(data)

# Receive from Client 2
fmi2Logger("Receiving the data from client 2 :: ")
clientMapp[1].fmi2GetReal(data)
print(data[1], data[2])


# -------------------------- Mesh Communication-------------------------#
fmi2Logger('-----------------------------------------------------------------')
fmi2Logger('------------------ Receive Mesh 1 + Meshdata1 -------------------')
fmi2Logger('-----------------------------------------------------------------')
            
# Syncing client1
#fmi2Logger('Syncing Communication - Client 1')
#a=clientMapp[0].comm.recv(source = 0, tag = 77)
#clientMapp[0].comm.send(a, dest = 0, tag = 77)

# Receive meshes from Client 1
fmi2Logger("Receiving meshes from client 1")
clientMapp[0].fmi2GetMesh()
# Print meshes from Client 1 to files
#mesh2file('servera_xy',clientMapp[0].meshLst[0])
#mesh2file('servera_xz',clientMapp[0].meshLst[1]) 

           
# Syncing client1
#fmi2Logger('Syncing Communication - Client 1')
#a=clientMapp[0].comm.recv(source = 0, tag = 77)
#clientMapp[0].comm.send(a, dest = 0, tag = 77)

# Receive data on meshes from Client 1
clientMapp[0].fmi2GetMeshData(0,2)
clientMapp[0].fmi2GetMeshData(1,2)
# Print mesh data from client 1 to file
data2file('servera_xy_data',clientMapp[0].meshLst[0],clientMapp[0].meshLst[0].dataLst)
data2file('servera_xz_data',clientMapp[0].meshLst[1],clientMapp[0].meshLst[1].dataLst)
 

fmi2Logger('-----------------------------------------------------------------')
fmi2Logger('------------------ Receive Mesh 2 + Meshdata2 -------------------')
fmi2Logger('-----------------------------------------------------------------')
            
# Syncing client2
#fmi2Logger('Syncing Communication - Client 2')
#a=clientMapp[1].comm.recv(source = 0, tag = 78)
#clientMapp[1].comm.send(a, dest = 0, tag = 78)

# Receive meshes from Client 2
fmi2Logger("Receiving mesh from client 2")
clientMapp[1].fmi2GetMesh()
# Print meshes from Client 2 to file
#mesh2file('serverb_xy',clientMapp[1].meshLst[0])
#mesh2file('serverb_xz',clientMapp[1].meshLst[1])
       

# Syncing client2
#fmi2Logger('Syncing Communication - Client 2')
#a=clientMapp[1].comm.recv(source = 0, tag = 78)
#clientMapp[1].comm.send(a, dest = 0, tag = 78)

# Receive data on client 2 meshes
clientMapp[1].fmi2GetMeshData(0,2)
clientMapp[1].fmi2GetMeshData(1,2)
# Print client 2 mesh data to files
data2file('serverb_xy_data',clientMapp[1].meshLst[0],clientMapp[1].meshLst[0].dataLst)
data2file('serverb_xz_data',clientMapp[1].meshLst[1],clientMapp[1].meshLst[1].dataLst)

# -------------------------------  Mesh Matching  ----------------------------#
fmi2Logger('-----------------------------------------------------------------')
fmi2Logger('------------------------ Mesh Matching --------------------------')
fmi2Logger('-----------------------------------------------------------------')






























# ------------------------------- Client Cleanup ----------------------------#
fmi2Logger('-----------------------------------------------------------------')
fmi2Logger('-------------------- Disconnecting Clients ----------------------')
fmi2Logger('-----------------------------------------------------------------')

fmi2Logger("disconnecting clients...")
for i in range(0, numClients):
    clientMapp[i].fmi2FreeInstance()

# Waiting for clients to disconnect 
time.sleep(1)

fmi2Logger('')
fmi2Logger('--------------------------------------------------')
fmi2Logger('Please close client terminals to terminate program')
