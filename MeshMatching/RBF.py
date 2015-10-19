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
CLASSES
RBF_system 
    Class that describes the system of equations used for RBF mesh matching, 
    includes the function interp to solve the system of equations.    
    
RBF_func (abstract)
    Abstract base class from which all radial basis functions should be derived

"""

## External Packages
#from abc import ABCMeta
import math
import numpy


## ------------------------ Define the main system ------------------------- ##
class RBF_system():
    
    def __init__(self, dim = None, pts = None, vals = None, RBF_fn = None):
    
        # -------------------- SETUP DEFAULT VALUES ------------------------- #
        # dim is the number of dimensions used in the problem (not stated)
        # i.e. points should be given (x,y,z) however if z always equals 0, 
        # then dim = 2        
        if dim is None:
            self.dim = 3
        else:
            self.dim = dim
        
        # pts is an array of length nPts * 3
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
            
        # ------------------------- OTHER VARIABLES ------------------------- #
        # Number of dimensions defined for each point
        self.defineddim = 3

        # -------------------------- CALCULATE SYSTEM ----------------------- #
        # Define sizes
        nAPts = int(len(self.pts)/self.defineddim)
        
        # Preallocate matrices
        phiAA = numpy.zeros((nAPts,nAPts))
        QA = numpy.zeros((nAPts,self.dim+1))
        hA = numpy.zeros((nAPts+self.dim+1,nAPts+self.dim+1))
        rhs = numpy.zeros(nAPts+self.dim+1)
        self.mappingConstants = numpy.zeros(nAPts+self.dim+1)
        zeroMatrix = numpy.zeros((self.dim+1,self.dim+1))
        
        '''# Sped up even more version
        for j in range(0,nAPts):
            print(j)
            for i in range(j+1,nAPts):
                
                # Calculate the radius
                r_coord = numpy.zeros(dim)
                r = 0
                for k in range(0,self.dim-1,1):
                    r_coord[k] = (self.pts[j*self.dim+k]-self.pts[i*self.dim+k]) ** 2
                
                r = numpy.sum(r_coord)
                r = numpy.sqrt(r)
                    
                # Build matrix phiAA
                rbf = self.RBF_fn.rbf(r)
                phiAA[j,i] = rbf
                phiAA[i,j] = rbf
                
            # Build matrix QA
            QA[j,0] = 1
            for k in range(0,self.dim):
                QA[j,k+1] = self.pts[j+k]
        
                
        '''        
        # Fastest matrix construction 
        pts = numpy.zeros((self.dim,nAPts))
        pts[0,:] = self.pts[0::self.defineddim]
        if self.dim > 1:
            pts[1,:] = self.pts[1::self.defineddim]
            if self.dim > 2:
                pts[2,:] = self.pts[2::self.defineddim]

        for j in range(0,nAPts):
            rcoord = numpy.zeros((self.dim,nAPts-j-1))
            rcoord = numpy.add(pts[:,j+1::1].T,-pts[:,j].T)
            rcoord = numpy.power(rcoord,2)
            
            r = numpy.zeros((1,nAPts-j-1))
            r = numpy.sum(rcoord,1)
            r = numpy.sqrt(r)
            r = numpy.insert(r,0,0)
            
            rbf = self.RBF_fn.rbf(r)
            phiAA[j,j::1] = rbf
            phiAA[j::1,j] = rbf
            
            # Build matrix QA
            QA[j,0] = 1
            QA[j,1::] = pts[:,j].T
            
            print(j)
        '''    
        # Functiong but slow - Need to speed up this loop!!!
        for j in range(0,nAPts):
            print(j)
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
                QA[j,k+1] = self.pts[j*3+k]
        '''
        rcoord = None
        r = None
        rbf = None
        pts = None
                
        # Build RHS matrix
        #self.vals = numpy.reshape(self.vals,(len(self.vals),1))
        rhs = numpy.concatenate((self.vals,numpy.zeros((self.dim+1,1))))
            
        # ---------------------- COMBINE MATRICES --------------------------- #
        hAtop = numpy.concatenate((phiAA,QA),1)
        phiAA = None
                
        hAbottom = numpy.concatenate((QA.T,zeroMatrix),1)
        QA = None
        zeroMatrix = None        
        
        hA = numpy.concatenate((hAtop,hAbottom),0)
        hAtop = None
        hAbottom = None
        
        # ------------------- SOLVE MATRIX SYSTEM --------------------------- #
        print('Solving the matrix system')        
        self.mappingConstants = numpy.linalg.solve(hA,rhs)





    def interp(self,Bpts = None):
        # ----------------------- CHECK VARIABLES --------------------------- #
        # Was an input defined        
        if Bpts is None:
            print('Point not defined')
            return 'E1'
        
        '''# Are the points defined similar to original points (NOT COMPLETE)
        Ax = self.pts[0::self.defineddim]
        Ay = self.pts[1::self.defineddim]
        Az = self.pts[2::self.defineddim]
        A = numpy.zeros((3,2))
        A[0,0] = Ax.min(0)  
        A[0,1] = Ax.max(0)
        A[1,0] = Ay.min(0)
        A[1,1] = Ay.max(0)
        A[2,0] = Az.min(0)
        A[2,1] = Az.max(0)  
        
        
        Bx = Bpts[0::self.defineddim]
        By = Bpts[1::self.defineddim]
        Bz = Bpts[2::self.defineddim]
        B = numpy.zeros((3,2))
        B[0,0] = Bx.min(0)  
        B[0,1] = Bx.max(0)
        B[1,0] = By.min(0)
        B[1,1] = By.max(0)
        B[2,0] = Bz.min(0)
        B[2,1] = Bz.max(0)   
        
        tolerance = 1e-1 * ()
        '''
        
        # ---------------------- Initialise Matrices -------------------------#
        nBPts = int(len(Bpts)/self.defineddim)
        nAPts = int(len(self.pts)/self.defineddim)
        
        phiBA = numpy.zeros((nBPts,nAPts))
        QB = numpy.zeros((nBPts,self.dim+1))
        hBA = numpy.zeros((nBPts,nAPts+self.dim+1))
                
        
        # ---------------------- Setup Matrices to interpolate ---------------#    
        ''' # Slow Method        
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
        '''
        # Faster Method
        ptsA = numpy.zeros((self.dim,nAPts))
        ptsA[0,:] = self.pts[0::self.defineddim]
        if self.dim > 1:
            ptsA[1,:] = self.pts[1::self.defineddim]
            if self.dim > 2:
                ptsA[2,:] = self.pts[2::self.defineddim]
                
        ptsB = numpy.zeros((self.dim,nBPts))
        ptsB[0,:] = Bpts[0::self.defineddim]
        if self.dim > 1:
            ptsB[1,:] = Bpts[1::self.defineddim]
            if self.dim > 2:
                ptsB[2,:] = Bpts[2::self.defineddim]

        for j in range(0,nBPts):
            rcoord = numpy.zeros((self.dim,nAPts))
            rcoord = numpy.add(ptsB[:,j].T,-ptsA[:,:].T)
            rcoord = numpy.power(rcoord,2)
            
            r = numpy.zeros((1,nAPts))
            r = numpy.sum(rcoord,1)
            r = numpy.sqrt(r)
                        
            rbf = self.RBF_fn.rbf(r)
            phiBA[j,:] = rbf
            
            # Build matrix QB
            QB[j,0] = 1
            QB[j,1::] = ptsB[:,j].T
            
        # Combine to form hBA
        hBA = numpy.concatenate((phiBA,QB),1)
        
        # -------------------- CALCULATE THE SYSTEM ------------------------- #
        val = numpy.dot(hBA,self.mappingConstants)
        

        # Return value
        return val

## -------------------------- Define the RBF's ----------------------------- ##

# Abstract Base Class
#class RBF_func(metaclass = ABCMeta):
    
#     def rbf(self,r):
#        return 0;