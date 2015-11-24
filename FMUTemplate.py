# -*- coding: utf-8 -*-
"""

File: FMUTemplate.py
Author: Andrew Brodie
Created: 30.10.2015

Description:
Defines the FMI API functions that need to be defined for an FMU.


"""

# ------------------------ Include Packages --------------------
## External Packages
import numpy

## Personal packages
from vtk import *
from clients import *


      
# -------------------- Creation, Destruction and Logging of FMUs --------------
        
class fmi2Component():
    '''
    An instance of an FMU.
    
    '''

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
    

def fmi2FreeInstance(fmi2Component c):
    '''
    Disposes the given instance, unloads the model and frees all memory
    OUTSIDE FMU???
    '''
    return None
    
def fmi2SetDebugLogging(fmi2Component c, fmi2Boolean loggingOn, size_t nCategories, const fmi2String categories[]):
    '''
    loggingOn = fmi2True -- logging is enabled, otherwise off
    - nCategories: if not 0 debug messages defined according to categories
    - categories[]: allowed values defined by modelling environ 
    '''
    return fmi2Status

# ------------------Initialization, Termination and Resetting FMU -------------
def fmi2SetupExperiment(fmi2Component c, fmi2Boolean toleranceDefined, fmi2Real tolerance, fmi2Real startTime, fmi2Boolean stopTimeDefined, fmi2Real stopTime):
    '''
    Causes FMU to setup experiment, call after Instantiate and before
    EnterInitilization.
    
    - 
    '''
    return fmi2Status

def fmi2EnterInitializationMode(fmi2Component c):
    '''
    FMU enters initialization mode
    
    Before:
    - All variables with attribute initial = exact / approx can be set
    - Cannot set other variables
    - fmi2SetupExperiment must be called at least once to define startTime
    
    '''
    return fmi2Status
    
def fmi2ExitInitializationMode(fmi2Component c):
    '''
    FMU exits initialization mode
    
    '''
    return fmi2Status
    
def fmi2Terminate(fmi2Component c):
    '''
    FMU terminates the simulation run
    '''
    return fmi2Status
    
def fmi2Reset(fmi2Component c):
    '''
    Called by environment to reset FMU after simulation run, back to stage just
    after fmi2Instantiate is called
    '''
    return fmi2Status
    
# ---------------------- Getting and Setting Variable Values ------------------
def fmi2GetReal(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]):
    '''
    '''
    return fmi2Status
    
def fmi2GetInteger(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]):
    '''
    '''
    return fmi2Status

def fmi2GetBoolean(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]):
    '''
    '''
    return fmi2Status

def fmi2GetString(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]):
    '''
    '''
    return fmi2Status
    
def fmi2SetReal(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]):
    '''
    '''
    return fmi2Status
    
def fmi2SetInteger(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]):
    '''
    '''
    return fmi2Status

def fmi2SetBoolean(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]):
    '''
    '''
    return fmi2Status

def fmi2SetString(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]):
    '''
    '''
    return fmi2Status
    
# ------------------ Getting and Setting the Complete FMU State ---------------
'''
FMU has internal state consisting of internal values needed to continue
simulation, i.e. continuous-time states, iteration variables, parameters etc.

Functions of this section allow these states to be copied like in the cases:
- variable step-size control of co-sim where next step not accepted
- nonlinear model prediction control
'''
def fmi2GetFMUState(fmi2Component c, fmi2FMUstate* FMUstate):
    '''
    Makes copy of internal FMU state
    '''
    return fmi2Status

def fmi2SetFMUState(fmi2Component c, fmi2FMUstate* FMUstate):
    '''
    Copies content of previous FMUState back to FMU
    '''
    return fmi2Status

def fmi2FreeFMUState(fmi2Component c, fmi2FMUstate* FMUstate):
    '''
    Frees all memory and other resources allocated with fmi2GetFMUState
    '''
    return fmi2Status
    
def fmi2SerializedFMUstateSize(fmi2Component c, fmi2FMUState FMUstate, size_t *size):
    '''
    Returns the size of the byte vector in order that FMUstate can be stored in
    '''
    return fmi2Status
    
def fmi2SerializeFMUstate(fmi2Component c, fmi2FMUState FMUstate, fmi2Byte serializedState[], size_t size):
    '''
    Serializes the data which is reference by pointer FMUstate
    '''
    return fmi2Status
    
def fmi2DeSerializeFMUstate(fmi2Component c, const fmi2Byte serializedState[], size_t size, fmi2FMUState* FMUstate):
    '''
    Deserializes the byte vector, constructs copy of FMU state and returns FMUState
    '''
    return fmi2Status
    
# -------------------------- Getting Partial Derivatives ----------------------
def fmi2GetDirectionalDerivative(fmi2Component c, const fmi2ValueReference vUnknown_ref[], size_t nUnknown, const fmi2ValueReference vKnown_ref[], size_t nKnown, const fmi2Real dvKnown[], fmi2Real dvUnknown[]):
    '''
    '''
    return fmi2Status