#! /usr/bin/env python

from mpi4py import MPI
import numpy
import time

# Number of Clients expected
numClients = 2
# mapp containing the communicators of clients.
clientMapp = {}
rank = MPI.COMM_WORLD.Get_rank()

def log(msg, *args):
    if rank == 0:
        print msg % args


log('')
# Data to be sent
data = numpy.arange(10, dtype='d')

info = MPI.INFO_NULL

port = MPI.Open_port(info)
log("opened port: '%s'", port)

service = 'pyeval'
MPI.Publish_name(service, info, port)
log("published service: '%s'", service)

root = 0
# As soon a client connects add a dictionary entry for that client with its communicator.
for i in range(0, numClients):
    log('waiting for client %i connection...',i+1)
    comm = MPI.COMM_WORLD.Accept(port, info, root)
    clientID=-1
    clientID = comm.recv(source=0, tag= 77)
    if clientID > 0:
        clientMapp[clientID]=comm
    else:
        log('Wrong Client ID received .... terminating server !')
        exit();
    log('client %i connected...', clientID)
    

## The following statements define the communication pattern between the clients

# Sending data to Client 1
log("Sending the data to client 1 :: ")
print(data[1], data[2])
clientMapp[1].Send([data, MPI.INT], dest=0, tag=77)

# Receive from Client 1
log("Receiving the data from client 1:: ")
clientMapp[1].Recv([data, MPI.INT], source=0, tag=77)
print(data[1], data[2])

# Dividing the data by 2
data = data * 0.5;

# Sending data to Client 2
log("Sending the data to client 2 :: ")
print(data[1], data[2])
clientMapp[2].Send([data, MPI.INT], dest=0, tag=77)

# Receive from Client 2
log("Receiving the data from client 2 :: ")
clientMapp[2].Recv([data, MPI.INT], source=0, tag=77)
print(data[1], data[2])

log('disconnecting clients...')
for i in range(0, numClients):
    clientMapp[i+1].Disconnect()

# Waiting for clients to disconnect 
time.sleep(4)

log('upublishing service...')
MPI.Unpublish_name(service, info, port)

log('closing port...')
MPI.Close_port(port)
