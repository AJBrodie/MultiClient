# -*- coding: utf-8 -*-
'''
File: ControlScript.py
Author: Andrew Brodie
Created: 30.10.2015

Description:
Defines the interaction between the FMUs.

Loads FMU1 and FMU2, sets up the simulation then utilises RBF mapping to map 
data between the meshes in FMU
'''

# Add current directory to library path
import os, sys, numpy
sys.path.append(os.getcwd())

# Import personal functions
#import MeshMatching as MM
from MeshMatching import RBF_MQ as RBFfunc
from MeshMatching import RBF
from FMUClasses import *
import SL_io.vtk as SLio


# Load fmu's
import FMU1
import FMU2

# Problem Variables
dt = 0.1
nTSteps = 10
tInit = 0
tFin = nTSteps * dt + tInit

fmi2True = 'fmi2True'
fmi2False = 'fmi2False'

fmu1Component = FMU1.fmi2Instantiate()
fmu2Component = FMU2.fmi2Instantiate()

## ------------------------------ Prepare FMU1 ----------------------------- ##
status = FMU1.fmi2SetupExperiment(fmu1Component, fmi2False, 0, tInit, fmi2True, tFin)

status = FMU1.fmi2EnterInitializationMode(fmu1Component)
'''
All variables that need to be initialised for model should be initialised
- Possibly implement mesh definitions here?
- Implement only mesh data initial values here?
'''
vr=[]
vr.append(fmi2Mesh())
vr.append(fmi2Mesh())
CS_fmu1Meshes = []
CS_fmu1Meshes.append(fmi2Mesh())
CS_fmu1Meshes.append(fmi2Mesh())

var = []
var.append('Boundary01')
var.append('Boundary02')
nvr = 2

status = FMU1.fmi2GetMesh(fmu1Component,var,nvr,vr)
CS_fmu1Meshes = vr
vr = None
var = None
status = FMU1.fmi2ExitInitializationMode(fmu1Component)

## ------------------------------ Prepare FMU2 ----------------------------- ##
status = FMU2.fmi2SetupExperiment(fmu2Component, fmi2False, 0, tInit, fmi2True, tFin)

status = FMU2.fmi2EnterInitializationMode(fmu2Component)
'''
All variables that need to be initialised for model should be initialised
- Possibly implement mesh definitions here?
- Implement only mesh data initial values here?
'''
vr=[]
vr.append(fmi2Mesh())
vr.append(fmi2Mesh())
CS_fmu2Meshes = []
CS_fmu2Meshes.append(fmi2Mesh())
CS_fmu2Meshes.append(fmi2Mesh())

var = []
var.append('Boundary01')
var.append('Boundary02')
nvr = 2

status = FMU2.fmi2GetMesh(fmu2Component,var,nvr,vr)
CS_fmu2Meshes = vr
vr = None
var = None
status = FMU2.fmi2ExitInitializationMode(fmu2Component)

## -------------------------- Output Initial Values ------------------------ ##
filename1M1Base ='fmu1_M1'
filename1M2Base ='fmu1_M2'
filename2M1Base ='fmu2_M1'
filename2M2Base ='fmu2_M2'

tCount = 0

filename1M1 = filename1M1Base + '.' + repr(tCount)
filename1M2 = filename1M2Base + '.' + repr(tCount)
filename2M1 = filename2M1Base + '.' + repr(tCount)
filename2M2 = filename2M2Base + '.' + repr(tCount)

SLio.data2file(filename1M1,CS_fmu1Meshes[0],CS_fmu1Meshes[0].dataLst)
SLio.data2file(filename1M2,CS_fmu1Meshes[1],CS_fmu1Meshes[1].dataLst)
SLio.data2file(filename2M1,CS_fmu2Meshes[0],CS_fmu2Meshes[0].dataLst)
SLio.data2file(filename2M2,CS_fmu2Meshes[1],CS_fmu2Meshes[1].dataLst)


## ------------------------------ Start time loop -------------------------- ##
for tStep in range(0,nTSteps):
    
    tCount +=1
    t = tStep * dt
    
    
    # ---------------------------- Advanced FMU1 ------------------------------
    FMU1.fmi2DoStep(fmu1Component, t, dt, fmi2False)
    
    # ------------------------ Get New Data from FMU1 -------------------------
    var = []
    var.append('pressure')
    var.append('displacement')
    nvr = 2
    
    # Get data from FMU1
    vr = []
    vr.append(numpy.ndarray(0))
    vr.append(numpy.ndarray(0))
    FMU1.fmi2GetMeshData(fmu1Component,0,var,nvr,vr)
    CS_fmu1Meshes[0].dataLst[0].values = vr[0]
    CS_fmu1Meshes[0].dataLst[1].values = vr[1]
    vr = None  
    vr = []
    vr.append(numpy.ndarray(0))
    vr.append(numpy.ndarray(0))
    FMU1.fmi2GetMeshData(fmu1Component,1,var,nvr,vr)
    CS_fmu1Meshes[1].dataLst[0].values = vr[0]
    CS_fmu1Meshes[1].dataLst[1].values = vr[1]
    vr = None    
    
    # ---------------------------- Map FMU1 data to Mesh 2 --------------------
    # Apply data mapping
    scale = 0.1
    rbf = RBFfunc.RBF_MQ(scale) 
    MMfmu1_mesh1_data1 = RBF.RBF_system(2,CS_fmu1Meshes[0].nodes,CS_fmu1Meshes[0].dataLst[0].values,rbf)
    MMfmu1_mesh1_data2_1 = RBF.RBF_system(2,CS_fmu1Meshes[0].nodes,CS_fmu1Meshes[0].dataLst[1].values[0::3],rbf)
    MMfmu1_mesh1_data2_2 = RBF.RBF_system(2,CS_fmu1Meshes[0].nodes,CS_fmu1Meshes[0].dataLst[1].values[1::3],rbf)
    MMfmu1_mesh1_data2_3 = RBF.RBF_system(2,CS_fmu1Meshes[0].nodes,CS_fmu1Meshes[0].dataLst[1].values[2::3],rbf)
    
    MMfmu1_mesh2_data1 = RBF.RBF_system(2,CS_fmu1Meshes[1].nodes,CS_fmu1Meshes[1].dataLst[0].values,rbf,[0,2])
    MMfmu1_mesh2_data2_1 = RBF.RBF_system(2,CS_fmu1Meshes[1].nodes,CS_fmu1Meshes[1].dataLst[1].values[0::3],rbf,[0,2])
    MMfmu1_mesh2_data2_2 = RBF.RBF_system(2,CS_fmu1Meshes[1].nodes,CS_fmu1Meshes[1].dataLst[1].values[1::3],rbf,[0,2])
    MMfmu1_mesh2_data2_3 = RBF.RBF_system(2,CS_fmu1Meshes[1].nodes,CS_fmu1Meshes[1].dataLst[1].values[2::3],rbf,[0,2])
    
    
    CS_fmu2Meshes[0].dataLst[0].values = MMfmu1_mesh1_data1.interp(CS_fmu2Meshes[0].nodes)
    CS_fmu2Meshes[0].dataLst[1].values[0::3] = MMfmu1_mesh1_data2_1.interp(CS_fmu2Meshes[0].nodes)
    CS_fmu2Meshes[0].dataLst[1].values[1::3] = MMfmu1_mesh1_data2_2.interp(CS_fmu2Meshes[0].nodes)
    CS_fmu2Meshes[0].dataLst[1].values[2::3] = MMfmu1_mesh1_data2_3.interp(CS_fmu2Meshes[0].nodes)
    
    CS_fmu2Meshes[1].dataLst[0].values = MMfmu1_mesh2_data1.interp(CS_fmu2Meshes[1].nodes)
    CS_fmu2Meshes[1].dataLst[1].values[0::3] = MMfmu1_mesh2_data2_1.interp(CS_fmu2Meshes[1].nodes)
    CS_fmu2Meshes[1].dataLst[1].values[1::3] = MMfmu1_mesh2_data2_2.interp(CS_fmu2Meshes[1].nodes)
    CS_fmu2Meshes[1].dataLst[1].values[2::3] = MMfmu1_mesh2_data2_3.interp(CS_fmu2Meshes[1].nodes)
    
    # ---------------------------- Set FMU2 Mesh Data -------------------------
    vr=[]
    vr.append(CS_fmu2Meshes[0].dataLst[0].values)
    vr.append(CS_fmu2Meshes[0].dataLst[1].values)
    FMU2.fmi2SetMeshData(fmu2Component,0,var,nvr,vr)
    vr = None
    
    vr=[]
    vr.append(CS_fmu2Meshes[1].dataLst[0].values)
    vr.append(CS_fmu2Meshes[1].dataLst[1].values)
    FMU2.fmi2SetMeshData(fmu2Component,1,var,nvr,vr)
    vr = None
    
    # ---------------------------- Advanced FMU2 ------------------------------
    FMU2.fmi2DoStep(fmu2Component, t, dt, fmi2False)
    
    
    
    # ------------------------ Get New Data from FMU2 -------------------------
    vr = []
    vr.append(numpy.ndarray(0))
    vr.append(numpy.ndarray(0))
    FMU2.fmi2GetMeshData(fmu2Component,0,var,nvr,vr)
    CS_fmu2Meshes[0].dataLst[0].values = vr[0]
    CS_fmu2Meshes[0].dataLst[1].values = vr[1]
    vr = None 
    vr = []
    vr.append(numpy.ndarray(0))
    vr.append(numpy.ndarray(0))
    FMU2.fmi2GetMeshData(fmu2Component,1,var,nvr,vr)
    CS_fmu2Meshes[1].dataLst[0].values = vr[0]
    CS_fmu2Meshes[1].dataLst[1].values = vr[1]
    vr = None
    
    
    # ---------------------------- Map FMU2 data to Mesh 1 --------------------
    scale = 0.1
    rbf = RBFfunc.RBF_MQ(scale) 
    MMfmu2_mesh1_data1 = RBF.RBF_system(2,CS_fmu2Meshes[0].nodes,CS_fmu2Meshes[0].dataLst[0].values,rbf)
    MMfmu2_mesh1_data2_1 = RBF.RBF_system(2,CS_fmu2Meshes[0].nodes,CS_fmu2Meshes[0].dataLst[1].values[0::3],rbf)
    MMfmu2_mesh1_data2_2 = RBF.RBF_system(2,CS_fmu2Meshes[0].nodes,CS_fmu2Meshes[0].dataLst[1].values[1::3],rbf)
    MMfmu2_mesh1_data2_3 = RBF.RBF_system(2,CS_fmu2Meshes[0].nodes,CS_fmu2Meshes[0].dataLst[1].values[2::3],rbf)
    
    MMfmu2_mesh2_data1 = RBF.RBF_system(2,CS_fmu2Meshes[1].nodes,CS_fmu2Meshes[1].dataLst[0].values,rbf,[0,2])
    MMfmu2_mesh2_data2_1 = RBF.RBF_system(2,CS_fmu2Meshes[1].nodes,CS_fmu2Meshes[1].dataLst[1].values[0::3],rbf,[0,2])
    MMfmu2_mesh2_data2_2 = RBF.RBF_system(2,CS_fmu2Meshes[1].nodes,CS_fmu2Meshes[1].dataLst[1].values[1::3],rbf,[0,2])
    MMfmu2_mesh2_data2_3 = RBF.RBF_system(2,CS_fmu2Meshes[1].nodes,CS_fmu2Meshes[1].dataLst[1].values[2::3],rbf,[0,2])
    
    
    CS_fmu1Meshes[0].dataLst[0].values = MMfmu2_mesh1_data1.interp(CS_fmu1Meshes[0].nodes)
    CS_fmu1Meshes[0].dataLst[1].values[0::3] = MMfmu2_mesh1_data2_1.interp(CS_fmu1Meshes[0].nodes)
    CS_fmu1Meshes[0].dataLst[1].values[1::3] = MMfmu2_mesh1_data2_2.interp(CS_fmu1Meshes[0].nodes)
    CS_fmu1Meshes[0].dataLst[1].values[2::3] = MMfmu2_mesh1_data2_3.interp(CS_fmu1Meshes[0].nodes)
    
    CS_fmu1Meshes[1].dataLst[0].values = MMfmu2_mesh2_data1.interp(CS_fmu1Meshes[1].nodes)
    CS_fmu1Meshes[1].dataLst[1].values[0::3] = MMfmu2_mesh2_data2_1.interp(CS_fmu1Meshes[1].nodes)
    CS_fmu1Meshes[1].dataLst[1].values[1::3] = MMfmu2_mesh2_data2_2.interp(CS_fmu1Meshes[1].nodes)
    CS_fmu1Meshes[1].dataLst[1].values[2::3] = MMfmu2_mesh2_data2_3.interp(CS_fmu1Meshes[1].nodes)
    
    
    # ---------------------------- Set FMU1 Mesh Data -------------------------
    vr=[]
    vr.append(CS_fmu1Meshes[0].dataLst[0].values)
    vr.append(CS_fmu1Meshes[0].dataLst[1].values)
    FMU1.fmi2SetMeshData(fmu1Component,0,var,nvr,vr)
    vr = None
    
    vr=[]
    vr.append(CS_fmu1Meshes[1].dataLst[0].values)
    vr.append(CS_fmu1Meshes[1].dataLst[1].values)
    FMU1.fmi2SetMeshData(fmu1Component,1,var,nvr,vr)
    vr = None
    
    # ----------------------------- Output Results to File --------------------
    filename1M1 = filename1M1Base + '.' + repr(tCount)
    filename1M2 = filename1M2Base + '.' + repr(tCount)
    filename2M1 = filename2M1Base + '.' + repr(tCount)
    filename2M2 = filename2M2Base + '.' + repr(tCount)
    
    SLio.data2file(filename1M1,CS_fmu1Meshes[0],CS_fmu1Meshes[0].dataLst)
    SLio.data2file(filename1M2,CS_fmu1Meshes[1],CS_fmu1Meshes[1].dataLst)
    SLio.data2file(filename2M1,CS_fmu2Meshes[0],CS_fmu2Meshes[0].dataLst)
    SLio.data2file(filename2M2,CS_fmu2Meshes[1],CS_fmu2Meshes[1].dataLst)
    