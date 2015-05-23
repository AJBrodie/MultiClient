# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:00:13 2015

@author: andrew
"""
from mpi4py import MPI
from subprocess import call
import os

class fmi2Component:
    # Definition for a class to store information about the clients
    def __init__(self,clientid,comm):
        self.clientid = clientid
        self.comm = comm
        
    def fmi2GetReal(self,data):
        self.comm.Recv([data, MPI.INT], source=0, tag=77)
        
    def fmi2SetReal(self,data):
        self.comm.Send([data, MPI.INT], dest=0, tag=77)
        
    def fmi2FreeInstance(self):
        self.comm.Disconnect()

def fmi2Logger(msg, *args):
    rank = MPI.COMM_WORLD.Get_rank()    
    if rank == 0:
        print(msg % args)
          
def fmi2Instantiate(port,info,service,clientFile):
    # Run Client
    fmi2Logger('Please Run Clients')
    cmd = 'xterm -hold -e mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python client1.py'
    #call(['mpiexec', '--ompi-server', 'file:/tmp/ompi-server.txt', '-n', '1', 'python', clientFile]) 
    #call(['bash'])
    #os.execlp(['xterm', '-hold', '-e', 'mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python client1.py']) 
    #os.execlp('xterm', '-hold', '-e', 'mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python client1.py') 
    os.system(cmd)
    root = 0
    # As soon a client connects add a dictionary entry for that client with its communicator.
    comm = MPI.COMM_WORLD.Accept(port, info, root)
    
    #comm = MPI.COMM_WORLD.Spawn(sys.executable,[clientFile], maxprocs=1)
       
    clientID = -1
    fmi2Logger('Receiving clientID')
    clientID = comm.recv(source=0, tag= 77)
    if clientID == 0:
        fmi2Logger('Wrong Client ID received .... terminating server !')
        exit();
    fmi2Logger('client %i connected...', clientID)
    
    return fmi2Component(clientID,comm)
    