# -*- coding: utf-8 -*-
"""
vtk.py
Created on Wed Jun 10 09:26:05 2015
@author: andrew

Package to define how to write a legacy vtk unstructured mesh file based on an
input mesh defined as per suggested fmi2 standard

> <
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
        
        if len(d)-mesh.numNodes<1e-6:
            if dtype==0:
                fid.write('SCALARS %s double\n' % datalist[i].name)
                fid.write('LOOKUP_TABLE default\n')
                
                for j in range(0,mesh.numNodes,1):
                    fid.write('  %f\n' % (d[j] ))
            elif dtype==1:
                print('Please group scalar data together before vector data for output')
        
        elif len(d)-2*mesh.numNodes<1e-6:
            print('2D problem with vectors not implemented - ignoring')
            return
        elif len(d)-3*mesh.numNodes<1e-6:
            fid.write('VECTORS %s double\n' % datalist[i].name)
            if i==0: fid.write('LOOKUP_TABLE default\n')
            
            for j in range(0,mesh.numNodes,1):
                fid.write('  %f  %f  %f\n' % (d[j*3], d[j*3+1], d[j*3+2] ))
            dtype=1

        else:
            print('Unknown datatype (scalar/vector/etc)')
            
    fid.close()
    
    
def readVTK(filename, mesh, dataList=None):
    
    # OPEN FILE
    fid=open(filename,'r')
    lineInd = 1
    
    if dataList  is None:
        readData = 0;
    else:
        readData = 1;
            
    
    # DECLARE VARIABLES
    pointsSection = 0
    polygonsSection = 0
    dataSection = 0
    pointsCnt = 0
    dataCnt = 0
    elemCnt = 0
    elemNodesCnt = 0
    dataSetCnt = 0
    
    for line in fid:
        part = line.split(  )        
        
        # CHECK IF IN A SECTION
        if pointsSection == 1:
            # Check for first line of Points section
            if part[0] == 'POINTS':
                npoints = int(part[1])
                mesh.numNodes = npoints
                mesh.nodes = numpy.zeros(npoints*3)
                pointType = part[2]
                #break
            # Otherwise in main part of points section
            else:
                pointsInLine = int(len(part) / 3)
                # For each point in the line there are 3 ordinates to store
                for i in range(0,pointsInLine):
                    mesh.nodes[(pointsCnt+i)*3] = float(part[i*3])
                    mesh.nodes[(pointsCnt+i)*3 + 1] = float(part[i*3 + 1])
                    mesh.nodes[(pointsCnt+i)*3 + 2] = float(part[i*3 + 2])
                # Progress points counter by number of points in the line
                pointsCnt += pointsInLine
            # If the points counter reaches the number of points, section should end
            if pointsCnt >= npoints:
                pointsSection = 0
            #break

        
        elif polygonsSection == 1:
            # Polygon section only has 1 part, no header line
            # Take number of points in element and store in mesh
            points = int(part[0])
            mesh.numNodesPerElem[elemCnt] = points
            # Read through the point indicies
            for i in range(0,points):
                mesh.elems[elemNodesCnt] = int(part[i+1])
                elemNodesCnt += 1
            # Progress number of elements by 1
            elemCnt += 1
            # Check if at the end of polygon section
            if elemCnt >= nPolygons:
                polygonsSection = 0
            #break
        
        elif dataSection != 0:
            # Skip blank lines
            if len(part) != 0:
                if part[0] == 'FIELD':
                    dataSets = int(part[2])
                    dataSection = 2
                elif part[0] == 'LOOKUP_TABLE':
                    dataSets = len(dataList)
                    dataSize = int(1)
                    dataLength = nPoints
                    dataList[dataSetCnt].values = numpy.zeros(dataLength * dataSize)                    
                    dataSection = 3
                elif dataSection == 2:
                    dataName = part[0]
                    dataList[dataSetCnt].name = dataName
                    dataSize = int(part[1])
                    dataLength = int(part[2])
                    dataList[dataSetCnt].values = numpy.zeros(dataLength * dataSize)
                    dataType = part[3]
                    dataSection = 3
                elif dataSection == 3:
                    lineLength = len(part)
                    for i in range(0,lineLength):
                        dataList[dataSetCnt].values[dataCnt] = float(part[i])
                        dataCnt += 1
                
                    if dataCnt >= dataSize*dataLength:
                        dataSection = 1
                        dataSetCnt += 1
                        dataCnt = 0
                    
                    if dataSetCnt >= dataSets:
                        dataSection = 0
                    #break
        
                    

        
        # SEARCH FOR KEY TERMS
        # Skip blank lines
        if len(part) != 0:
            if part[0] == 'DATASET':
                if part[1] == 'POLYDATA':
                    pointsSection = 1
                    
                elif part[1] == 'UNSTRUCTURED_GRID':
                    pointsSection = 1
                    
                
            elif part[0] == 'POLYGONS':
                nPolygons = int(part[1])
                mesh.numElems = nPolygons
                mesh.numNodesPerElem = numpy.zeros(nPolygons)
                totalIntegers = int(part[2])
                mesh.elems = numpy.zeros(totalIntegers - nPolygons)
                polygonsSection = 1
                
            elif part[0] == 'CELLS':
                nPolygons = int(part[1])
                mesh.numElems = nPolygons
                mesh.numNodesPerElem = numpy.zeros(nPolygons)
                totalIntegers = int(part[2])
                mesh.elems = numpy.zeros(totalIntegers - nPolygons)
                polygonsSection = 1
                
                
            elif part[0] == 'POINT_DATA':
                nPoints = int(part[1])
                dataSection = 1
                if readData == 0:
                    dataSection = 0
                    print('WARNING: There is data in this file that is not being read in')
                    
        
        #print(lineInd)
        lineInd+=1
            

    fid.close()
     