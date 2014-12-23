"""
Created on Mon Dec 22 21:10:34 2014

@author: aashishsatya

Description: Python code that classifies a given statement for eval.
Kind of like a header file in C or C++.
"""

from Housekeeping import *

# The functions are written in such a way that the name identifies the
# purpose of the function.
# For e.g. isSelfEvaluating(item) will return the answer to the question
# "Is the item self-evaluating?", i.e.
# True if it is, False if it is not.

def isSelfEvaluating(item):
    
    """
    Returns true if the item is a number (integer or a float), false otherwise.
    """
    
    try:
        tempfloat = float(item)
        return True
    except ValueError:
        return False
        
def isVariable(item):
    
    """
    Checks if an item is a variable or not.
    For now, anything that is not a number(float or double) is a variable.
    """
    
    return not isSelfEvaluating(item)
    

    
    

