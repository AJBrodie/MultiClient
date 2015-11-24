# -*- coding: utf-8 -*-
"""

File: FMU2.py
Author: Andrew Brodie
Created: 30.10.2015

Description:
Defines the FMI API functions for FMU2.


"""

# ------------------------ Include Packages --------------------
## External Packages
import numpy
from copy import deepcopy

fmi2True = 'fmi2True'
fmi2False = 'fmi2False'
fmi2OK = 'fmi2OK'
fmi2Error = 'fmi2Error'

# -------------------- Creation, Destruction and Logging of FMUs --------------
        
def fmi2Instantiate():
    '''
    Returns a new instance of an FMU.
    fmi2Component fmi2Instantiate(fmi2String  instanceName,
                                  fmi2Type    fmuType,
                                  fmi2String  fmuGUID,
                                  fmi2String  fmuResourceLocation,
                                  const fmi2CallbackFunctions*  functions
                                  fmi2Boolean visible,
                                  fmi2Boolean loggingOn)
    - Possibly should be defined outside of FMU?
    - For co-sim this function has to perform all actions of a slave
      which are necessary before a simulation run starts (load model
      file, compilation...)
    
    INPUT VARIABLES
    - instanceName has to have a value which is unique to each FMU
    - fmuType is either fmi2ModelExchange or fmi2CoSimulation
    - fmuGUID used to check if XML file compatible with C code of FMU
    - fmuResourceLocation is URI to indicate location of resources directory of unzipped FMU
    - functions provides callback functions for FMU to utilize resources from environment
    - visible if false determines interaction with user is minimum
    - loggingOn if true debug logging is enabled
    '''
    import  FMU2.FMUVariables as fmi2Component
    
    '''
    Insert here
    - checks for suitability of the model
    - imports for ResuorceLocation
    '''    
    return fmi2Component
    


def fmi2FreeInstance(c):
    '''
    Disposes the given instance, unloads the model and frees all memory
    OUTSIDE FMU???
    '''
    c = None
    
    return None

'''
NOT IMPLEMENTED
def fmi2SetDebugLogging(fmi2Component c, fmi2Boolean loggingOn, size_t nCategories, const fmi2String categories[]):
    
    loggingOn = fmi2True -- logging is enabled, otherwise off
    - nCategories: if not 0 debug messages defined according to categories
    - categories[]: allowed values defined by modelling environ 
    
    return fmi2Status
'''

# ------------------Initialization, Termination and Resetting FMU -------------
def fmi2SetupExperiment(fmi2Component, toleranceDefined, tolerance, startTime, stopTimeDefined, stopTime):
    '''
    Causes FMU to setup experiment, call after Instantiate and before
    EnterInitilization.
    '''
    if toleranceDefined is fmi2True:
        fmi2Component.experiment.tolerance = tolerance
    
    if stopTimeDefined is fmi2True:
        fmi2Component.experiment.stopTime = stopTime
        
    fmi2Component.experiment.startTime = startTime
        
    fmi2Status = 'fmi2OK'
    
    return fmi2Status

def fmi2EnterInitializationMode(fmi2Component):
    '''
    FMU enters initialization mode
    
    Before:
    - All variables with attribute initial = exact / approx can be set
    - Cannot set other variables
    - fmi2SetupExperiment must be called at least once to define startTime
    
    '''
    
    fmi2Component.fmuMode = 'InitializationMode'    
    fmi2Status = 'OK'    
    
    return fmi2Status
    
def fmi2ExitInitializationMode(fmi2Component):
    '''
    FMU exits initialization mode
    
    '''
    fmi2Component.fmuMode = ''    
    fmi2Status = 'OK'

    return fmi2Status
    
def fmi2Terminate(fmi2Component):
    '''
    FMU terminates the simulation run
    '''
    fmi2Component.fmuMode = 'Terminated'
    fmi2Status = 'OK'    
    
    return fmi2Status
    
def fmi2Reset(fmi2Component):
    '''
    Called by environment to reset FMU after simulation run, back to stage just
    after fmi2Instantiate is called
    '''
    
    fmi2Component = None
    fmi2Component = fmi2Instantiate()
    
    fmi2Status = 'OK'
    
    return fmi2Status
    
# ---------------------- Getting and Setting Variable Values ------------------
'''
def fmi2GetReal(fmi2Component, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]):
    
    
    return fmi2Status
    
def fmi2GetInteger(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]):
    
    
    return fmi2Status

def fmi2GetBoolean(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]):
    
    
    return fmi2Status

def fmi2GetString(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]):
    
    
    return fmi2Status
    
def fmi2SetReal(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]):
    
    
    return fmi2Status
    
def fmi2SetInteger(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]):
    
    
    return fmi2Status

def fmi2SetBoolean(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]):
    
    
    return fmi2Status

def fmi2SetString(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]):


    return fmi2Status
'''
'''
Newly created get/set functions 
'''

def fmi2GetMesh(fmi2Component=None, var=None, nvr=None, value=None):
    '''
    
    '''
    fmi2Status = 'fmi2OK'    
    
    if fmi2Component is None:
        fmi2Status = 'fmi2Error'
    elif var is None:
        fmi2Status = 'fmi2Error'
    elif nvr is None:
        nvr = len(var)
    elif value is None:
        value = []
        for i in range(0,nvr):
            value.append(fmi2Component.fmi2Mesh)
            
    if fmi2Status is 'fmi2OK':
        temp = []
        for i in range(0,nvr):
            temp.append(fmi2Component.fmi2Mesh)
            
        for i in range(0,nvr):
            j=0
            while fmi2Component.ModelVariables.CombinedVariable.Meshes[j].name is not var[i]:
                j+=1
                         
            value[i] = deepcopy(fmi2Component.ModelVariables.CombinedVariable.Meshes[j])
            
    return fmi2Status



    
def fmi2SetMesh(fmi2Component=None, var=None, nvr=None, value=None):
    '''
    
    '''
    fmi2Status = 'fmi2OK'    
    
    if fmi2Component is None:
        fmi2Status = 'fmi2Error'
    elif value is None:
        fmi2Status = 'fmi2Error'
    elif nvr is None:
        nvr = len(value)
    elif var is None:
        fmi2Status = 'fmi2Error'

            
    if fmi2Status is 'fmi2OK':
        for i in range(0,nvr):
            j=0
            while fmi2Component.ModelVariables.CombinedVariable.Meshes[j].name is not var[i]:
                j+=1
                
            fmi2Component.ModelVariables.CombinedVariable.Meshes[j] = deepcopy(value[i])
            
    return fmi2Status



    
def fmi2GetMeshData(fmi2Component=None, meshID=None, var=None, nvr=None, value=None):
    '''
    var defines a list of strings, the data names to be set
    
    value defines a list of numpy arrays, each array defines the values for the
        corresponding variable name in vr
    
    '''
    fmi2Status = 'fmi2OK'    
    
    if fmi2Component is None:
        fmi2Status = 'fmi2Error'
    elif var is None:
        fmi2Status = 'fmi2Error'
    elif nvr is None:
        nvr = len(var)
    elif value is None:
        value = []
        for i in range(0,nvr):
            value.append(numpy.ndarray())
    

    if fmi2Status is 'fmi2OK':
        data = fmi2Component.ModelVariables.CombinedVariable.Meshes[meshID].dataLst
        
        #temp = []            
        for i in range(0,nvr):
            #name = var[i]
            for j in range(0,len(data)):
                if data[j].name is var[i]:
                    value[i] = deepcopy(data[j].values)
        

    return fmi2Status



    
def fmi2SetMeshData(fmi2Component=None, meshID=None, var=None, nvr=None, value=None):
    '''
    var defines a list of strings, the data names to be set
    
    value defines a list of numpy arrays, each array defines the values for the
        corresponding variable name in var
    '''
    fmi2Status = 'fmi2OK'    
    
    if fmi2Component is None:
        fmi2Status = 'fmi2Error'
    elif value is None:
        fmi2Status = 'fmi2Error'
    elif nvr is None:
        nvr = len(value)
    elif var is None:
        fmi2Status = 'fmi2Error'
        
    data = fmi2Component.ModelVariables.CombinedVariable.Meshes[meshID].dataLst
    if fmi2Status is 'fmi2OK':
        for i in range(0,nvr):
            for j in range(0,len(data)):
                if data[j].name is var[i]:
                    data[j].values=value[i]
            
    return fmi2Status
    
# ------------------ Getting and Setting the Complete FMU State ---------------
'''
FMU has internal state consisting of internal values needed to continue
simulation, i.e. continuous-time states, iteration variables, parameters etc.

Functions of this section allow these states to be copied like in the cases:
- variable step-size control of co-sim where next step not accepted
- nonlinear model prediction control

def fmi2GetFMUState(fmi2Component c, fmi2FMUstate* FMUstate):
    
    Makes copy of internal FMU state
    
    return fmi2Status

def fmi2SetFMUState(fmi2Component c, fmi2FMUstate* FMUstate):
    
    Copies content of previous FMUState back to FMU
    
    return fmi2Status

def fmi2FreeFMUState(fmi2Component c, fmi2FMUstate* FMUstate):
    
    Frees all memory and other resources allocated with fmi2GetFMUState
    
    return fmi2Status
    
def fmi2SerializedFMUstateSize(fmi2Component c, fmi2FMUState FMUstate, size_t *size):
    
    Returns the size of the byte vector in order that FMUstate can be stored in
    
    return fmi2Status
    
def fmi2SerializeFMUstate(fmi2Component c, fmi2FMUState FMUstate, fmi2Byte serializedState[], size_t size):
    
    Serializes the data which is reference by pointer FMUstate
    
    return fmi2Status
    
def fmi2DeSerializeFMUstate(fmi2Component c, const fmi2Byte serializedState[], size_t size, fmi2FMUState* FMUstate):
    
    Deserializes the byte vector, constructs copy of FMU state and returns FMUState
    
    return fmi2Status
    
# -------------------------- Getting Partial Derivatives ----------------------
def fmi2GetDirectionalDerivative(fmi2Component c, const fmi2ValueReference vUnknown_ref[], size_t nUnknown, const fmi2ValueReference vKnown_ref[], size_t nKnown, const fmi2Real dvKnown[], fmi2Real dvUnknown[]):
    
    Computes the directional derivatives of an FMU
    
    return fmi2Status
'''

#--------------------------- CoSimulation Functions ---------------------------
def fmi2DoStep(fmi2Component, currentCommunicationPoint, communicationStepSize, noSetFMUStatePriorToCurrentPoint):
    
    tolerance = 1e-10    
    
    if abs(currentCommunicationPoint - fmi2Component.ModelVariables.ScalarVariable.Real[0]) >= tolerance:
        fmi2Status = 'fmi2Error'
        return fmi2Status
    
    meshes = fmi2Component.ModelVariables.CombinedVariable.Meshes
        
    for mesh in meshes:
        mesh.dataLst[0].values-=5
        mesh.dataLst[1].values/=5
        
    fmi2Component.ModelVariables.ScalarVariable.Real[0] += communicationStepSize
        
    fmi2Status = 'fmi2OK'        
        
    return fmi2Status