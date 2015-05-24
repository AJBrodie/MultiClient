#! /usr/bin/env python

from fmi2 import *

from mpi4py import MPI
import numpy
import time


# Number of Clients expected
numClients = 2
clientFile = ['client1.py','client2.py']

# mapp containing the communicators of clients.
clientMapp = {}
sudorank = MPI.COMM_WORLD.Get_rank()


fmi2Logger('')

# Data to be sent
data = numpy.arange(10, dtype='d')

root = 0

# As soon a client connects add a dictionary entry for that client with its communicator.
for i in range(0, numClients):
    fmi2Logger("instantiating client %i of %i", i+1, numClients)
    clientMapp[i+1] = fmi2Instantiate(clientFile[i])

## -----------------------------------------------------------------------------    
## The following statements define the communication pattern between the clients

# Sending data to Client 1
fmi2Logger("Sending the data to client 1 :: ")
print(data[1], data[2])
clientMapp[1].fmi2SetReal(data)

# Receive from Client 1
fmi2Logger("Receiving the data from client 1:: ")
clientMapp[1].fmi2GetReal(data)
print(data[1], data[2])

# Dividing the data by 2
data = data * 0.5;

# Sending data to Client 2
fmi2Logger("Sending the data to client 2 :: ")
print(data[1], data[2])
clientMapp[2].fmi2SetReal(data)

# Receive from Client 2
fmi2Logger("Receiving the data from client 2 :: ")
clientMapp[2].fmi2GetReal(data)
print(data[1], data[2])

## -------------------------------------------------------------------------
## Final cleanup of clients

fmi2Logger('disconnecting clients...')
for i in range(0, numClients):
    clientMapp[i+1].fmi2FreeInstance()

# Waiting for clients to disconnect 
time.sleep(1)

fmi2Logger('')
fmi2Logger('--------------------------------------------------')
fmi2Logger('Please close client terminals to terminate program')
