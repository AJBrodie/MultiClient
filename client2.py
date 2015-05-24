#! /usr/bin/env python

from mpi4py import MPI
import numpy
import time



myClientID = 2;

def log(msg, *args):
    if rank == 0:
        print msg % args

root = 0

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

# Sending data after modification back to the server
comm.Send(data, dest=0, tag=77)

log('disconnecting server...')
comm.Disconnect()
