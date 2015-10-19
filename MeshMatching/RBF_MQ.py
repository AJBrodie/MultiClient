# -*- coding: utf-8 -*-
"""
File: /MeshMatching/RBF_MQ.py
Author: Andrew Brodie
Date: 11.10.15

DESCRIPTION
Part of MeshMatching packaging, defines the multi quadratic basis function for 
use with the RBF meshmatching

"""

## External Packages
#from abc import ABCMeta
import math
import numpy


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
        return numpy.sqrt(numpy.power(r,2) + r02)
        
#RBF_func.register(RBF_MQ)