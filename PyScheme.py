"""
Created on Sun Dec 21 23:53:09 2014

@author: aashishsatya

Project Name: PyScheme

Description: In this project I attempt to write an implementation of a subset
of the Scheme Programming Language in Python.
"""

from Classifier import *


# to implement the environment model of evaluation in Scheme, 
# we need environments. 
class Env(object):
    
    """
    An environment is simply a dict of variable-value pairs, and some
    predefined mappings.
    """
    
    def __init__(self, frame = {}, enclosingEnvironment = None):
        self.frame = frame
        self.enclosingEnvironment = enclosingEnvironment
        
    def lookup(self, variable):
        if variable in self.frame.keys():
            return self.frame[variable]
        else:
            self.enclosingEnvironment.lookup(variable)
       
def eval(exp, env):
    
    """
    Evaluates the expression exp in the given environment env
    and return the result
    """
    
    