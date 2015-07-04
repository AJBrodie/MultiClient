# -*- coding: utf-8 -*-
"""
vtk.py
Created on Wed Jun 10 09:26:05 2015
@author: andrew

Package to define how to write a legacy vtk unstructured mesh file based on an
input mesh defined as per suggested fmi2 standard
"""
import numpy
import os

# ------------------------------- Header Definitions ------------------------
        
class data:
    def __init__(self,name='',values=numpy.zeros(1)):
        self.name=name
        self.values=values
        
# ---------------------------------------------------------------------------

def mesh2file(filename,mesh,closefile=1):
    
    directory = '../Results/'    
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    fid=open('%s%s.vtk' % (directory,filename),'w')
    
    ###### VTK HEADER ######
    fid.write('# vtk DataFile Version 2.0\n')
    fid.write('%s\n' % mesh.name)
    fid.write('ASCII\n')
    fid.write('\n')
    
    ##### VTK MESH #####
    fid.write('DATASET UNSTRUCTURED_GRID\n')
    
    ## Points
    fid.write('POINTS %d double\n' % mesh.numNodes)
    for i in range(0,mesh.numNodes,1):
        fid.write('  %f  %f  %f\n' % (mesh.nodes[i*3], mesh.nodes[i*3+1], mesh.nodes[i*3+2]) )
    
    ## Cells
    cellsSize=numpy.size(mesh.numNodesPerElem)+numpy.size(mesh.elems)
    fid.write('\n')
    fid.write('CELLS %d %d\n' % (mesh.numElems, cellsSize))
    
    nodeCount=0
    for i in range (0,mesh.numElems,1):
        if mesh.numNodesPerElem[i]==3:
            fid.write('  %d  %d  %d  %d\n' % (mesh.numNodesPerElem[i], mesh.elems[nodeCount], mesh.elems[nodeCount+1], mesh.elems[nodeCount+2]))
        elif mesh.numNodesPerElem[i]==4:
            fid.write('  %d  %d  %d  %d  %d\n' % (mesh.numNodesPerElem[i], mesh.elems[nodeCount], mesh.elems[nodeCount+1], mesh.elems[nodeCount+2], mesh.elems[nodeCount+3]))
        else:
            print('Unknown number of nodes per element')
            return
        
        nodeCount=nodeCount+mesh.numNodesPerElem[i]
        
    ## Cell types
    fid.write('\n')
    fid.write('CELL_TYPES %d\n' % mesh.numElems)
    for i in range (0,mesh.numElems,1):
        if mesh.numNodesPerElem[i]==3:
            fid.write('5\n')
        elif mesh.numNodesPerElem[i]==4:
            fid.write('9\n')
        else:
            print('Unknown number of nodes per element')
            
    if closefile==1:
        fid.close()
        fid=0

    return fid

def data2file(filename,mesh,datalist):
    
    fid = mesh2file(filename,mesh,0)
    fid.write('\n')
    fid.write('POINT_DATA %d\n' % mesh.numNodes)
    
    ## Write Node Data
    dtype=0             # initialise dtype, if dtype = 0 (scalar) if dtype = 1 (vector)
    for i in range(0,len(datalist),1):
        d=datalist[i].values
        
        if len(d)/mesh.numNodes==1:
            if dtype==0:
                fid.write('SCALARS %s double\n' % datalist[i].name)
                if i==0: fid.write('LOOKUP_TABLE default\n')
                
                for j in range(0,mesh.numNodes,1):
                    fid.write('  %f\n' % (d[j] ))
            elif dtype==1:
                print('Please group scalar data together before vector data for output')
        
        elif len(d)/mesh.numNodes==2:
            print('2D problem with vectors not implemented - ignoring')
            return
        elif len(d)/mesh.numNodes==3:
            fid.write('VECTORS %s double\n' % datalist[i].name)
            if i==0: fid.write('LOOKUP_TABLE default\n')
            
            for j in range(0,mesh.numNodes,1):
                fid.write('  %f  %f  %f\n' % (d[j*3], d[j*3+1], d[j*3+2] ))
            dtype=1

        else:
            print('Unknown datatype (scalar/vector/etc')
            
    fid.close()
    
    
            