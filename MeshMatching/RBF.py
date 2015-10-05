#! /usr/bin/env python

## File: /MeshMatching/RBF.py
## Author: Andrew Brodie
## Date: 27.07.15
##
## Description
## Part of MeshMatching packaging, used for defining mesh matching using radial
## basis function method. Main function is defined as interp with individual 
## radial basis functions defined as sub classes of the virtual class RBF_func
##
## Functions
## interp
##
## 


## External Packages
from abc import ABCMeta
import math
import numpy


## ------------------------ Define the main system ------------------------- ##
class RBF_system():
    
    def __init__(self, dim = None, pts = None, vals = None, RBF_fn = None, norm = None):
    
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
            
        if norm is None:
            self.norm = 0
        else:
            self.norm = norm

        # -------------------------- CALCULATE SYSTEM ----------------------- #
        # Preallocate matrices
        RBF = numpy.zeros((len(self.vals),len(self.vals)))
        y = numpy.zeros(len(self.vals))
        self.w = numpy.zeros(len(self.vals))
        
        for j in range(0,len(self.pts)-1,self.dim):
            for i in range(0,len(self.pts)-1,self.dim):
                
                # Calculate the radius
                r_coord = numpy.zeros(dim)
                r = 0
                for k in range(0,self.dim-1,1):
                    r_coord[k] = (self.pts[j+k]-self.pts[i+k]) ** 2
                
                r = numpy.sum(r_coord)
                r = numpy.sqrt(r)
                    
                # Build the matrices
                RBF[j,i] = self.RBF_fn.rbf(r)
                
            if norm is 1:
                y[j] = self.vals[j] * numpy.sum(RBF[j,:])
            else:
                y[j] = self.vals[j]
            
        # ------------------- SOLVE MATRIX SYSTEM --------------------------- #
        self.w = numpy.linalg.solve(RBF,y)

    def interp(self,pt = None):
        if pt is None:
            print('Point not defined')
            return 'E1'
        
        RBF = numpy.zeros(self.vals)
        for i in range(0,len(self.pts)-1,self.dim):
            r_coord = numpy.zeros(self.dim)
            r = 0
            for k in range(0,self.dim-1,1):
                r_coord[k] = (pt[k]-self.pts[i+k]) ** 2
            
            r = numpy.sum(r_coord)
            r = numpy.sqrt(r)
            
            RBF[i] = self.RBF_fn.rbf(r)
            
            val = numpy.vdot(RBF.transpose(),self.w)
            
        return val

## -------------------------- Define the RBF's ----------------------------- ##

# Abstract Base Class
class RBF_func(metaclass = ABCMeta):
    
    def rbf(self):
        return 0;

# ---------------- Define individual radial basis functions ----------------- #

## Multi quadric basis function
class RBF_MQ():
    
    def __init__(self,scale=None):
        
        # Define default values
        if scale is None:
            self.scale=1
            # Scale should be larger than typical separation points but smaller 
            # than the problem length                                                       ! Look at implementing better default definition
        else:
            self.scale=scale
            
        # Caclulate the RBF
    def rbf(self,r):
        r02 = self.scale**2
        return math.sqrt(r**2 + r02)
        
RBF_func.register(RBF_MQ)
        
    
## Inverse Multi quadric basis function
class RBF_IMQ():
    
    def __init__(self,scale=None):
        
        # Define default values
        if scale is None:
            self.scale=1
            # Scale should be larger than typical separation points but smaller 
            # than the problem length                                                       ! Look at implementing better default definition
        else:
            self.scale=scale
            
        # Caclulate the RBF
    def rbf(self,r):
        r02 = self.scale**2
        return 1/math.sqrt(r**2 + r02)
    
RBF_func.register(RBF_IMQ)