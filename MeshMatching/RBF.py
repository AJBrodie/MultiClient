#! /usr/bin/env python
"""
File: /MeshMatching/RBF.py
Author: Andrew Brodie
Date: 27.07.15

Description
Part of MeshMatching packaging, used for defining mesh matching using radial
basis function method. Main function is defined as interp with individual 
radial basis functions defined as sub classes of the virtual class RBF_func,
these are individually defined in separate files.
---------------------------------------------------------------------------
Formulation of this method taken from the paper:
de Boer A., van Zuijlen A.H., Bijl H., Comparison of conservative and 
consistent approaches for the coupling of non-mathing meshes, Computational
Methods of Applied Mechanical Engineering 2008
---------------------------------------------------------------------------

FUNCTIONS
interp
    Function to interpolate at provided values (values are provided in an array)

CLASSES
RBF_func (abstract)
    Abstract base class from which all radial basis functions should be derived

"""

## External Packages
from abc import ABCMeta
import math
import numpy


## ------------------------ Define the main system ------------------------- ##
class RBF_system():
    
    def __init__(self, dim = None, pts = None, vals = None, RBF_fn = None):
    
        # -------------------- SETUP DEFAULT VALUES ------------------------- #
        if dim is None:
            self.dim = 3
        else:
            self.dim = dim
        
        if pts is None:
            self.pts = numpy.zeros(3)
        else:
            self.pts = pts
            
        if vals is None:
            self.vals = numpy.zeros(1)
        else:
            self.vals = vals
        
        if RBF_fn is None:
            self.RBF_fn = RBF_MQ
        else:
            self.RBF_fn = RBF_fn

        # -------------------------- CALCULATE SYSTEM ----------------------- #
        # Define sizes
        nAPts = int(len(self.pts)/self.dim)
        
        # Preallocate matrices
        phiAA = numpy.zeros((nAPts,nAPts))
        QA = numpy.zeros((nAPts,self.dim+1))
        hA = numpy.zeros((nAPts+self.dim+1,nAPts+self.dim+1))
        rhs = numpy.zeros(nAPts+self.dim+1)
        self.mappingConstants = numpy.zeros(nAPts+self.dim+1)
        zeroMatrix = numpy.zeros((self.dim+1,self.dim+1))
        
        for j in range(0,nAPts):
            for i in range(0,nAPts):
                
                # Calculate the radius
                r_coord = numpy.zeros(dim)
                r = 0
                for k in range(0,self.dim-1,1):
                    r_coord[k] = (self.pts[j*self.dim+k]-self.pts[i*self.dim+k]) ** 2
                
                r = numpy.sum(r_coord)
                r = numpy.sqrt(r)
                    
                # Build matrix phiAA
                phiAA[j,i] = self.RBF_fn.rbf(r)
                
            # Build matrix QA
            QA[j,0] = 1
            for k in range(0,self.dim):
                QA[j,k+1] = self.pts[j+k]
                
        # Build RHS matrix
        rhs = numpy.concatenate((self.vals,numpy.zeros((self.dim+1,1))))
            
        # ---------------------- COMBINE MATRICES --------------------------- #
        hAtop = numpy.concatenate((phiAA,QA),1)
        hAbottom = numpy.concatenate((QA.T,zeroMatrix),1)
        hA = numpy.concatenate((hAtop,hAbottom),0)
        
        # ------------------- SOLVE MATRIX SYSTEM --------------------------- #
        self.mappingConstants = numpy.linalg.solve(hA,rhs)

    def interp(self,Bpts = None):
        if Bpts is None:
            print('Point not defined')
            return 'E1'
        # ---------------------- Initialise Matrices -------------------------#
        nBPts = int(len(Bpts)/self.dim)
        nAPts = int(len(self.pts)/self.dim)
        
        phiBA = numpy.zeros((nBPts,nAPts))
        QB = numpy.zeros((nBPts,self.dim+1))
        hBA = numpy.zeros((nBPts,nAPts+self.dim+1))
                
        
        # ---------------------- Setup Matrices to interpolate ---------------#    
        for j in range(0,nBPts):
            for i in range(0,nAPts):
                
                # Calculate the radius
                r_coord = numpy.zeros(self.dim)
                r = 0
                for k in range(0,self.dim-1,1):
                    r_coord[k] = (Bpts[j*self.dim+k]-self.pts[i*self.dim+k]) ** 2
                
                r = numpy.sum(r_coord)
                r = numpy.sqrt(r)
                    
                # Build matrix phiBA
                phiBA[j,i] = self.RBF_fn.rbf(r)
                
            # Build matrix QAB
            QB[j,0] = 1
            for k in range(0,self.dim):
                QB[j,k+1] = Bpts[j+k]        
        
        # Combine to form hBA
        hBA = numpy.concatenate((phiBA,QB),1)
        
        # -------------------- CALCULATE THE SYSTEM ------------------------- #
        val = numpy.dot(hBA,self.mappingConstants)
        

        # Return value
        return val

## -------------------------- Define the RBF's ----------------------------- ##

# Abstract Base Class
class RBF_func(metaclass = ABCMeta):
    
    def rbf(self,r):
        return 0;