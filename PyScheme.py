"""
Created on Sun Dec 21 23:53:09 2014

@author: aashishsatya

Project Name: PyScheme

Description: In this project I attempt to write an implementation of a subset
of the Scheme Programming Language in Python.
"""

# initially we will ignore strings and comments and will get just the core
# functionality working

# we'll need functions that perform basic housekeeping
# (removing all the parens for processing etc.)

def tokenize(string):
    
    """
    Converts a string into a list of tokens.
    """
    
    # add a space to parens so that they can be split easily
    string = string.replace('(', ' ( ')
    string = string.replace(')', ' ) ')
    
    return string.split()

# to implement the environment model of evaluation in Scheme, 
# we need environments. 
class Env(dict):
    """
    An environment is simply a dict of variable-value pairs, and some
    predefined mappings.
    """
       
def eval(exp, env):
    
    """
    Evaluates the expression exp in the given environment env
    and return the result
    """
    
    