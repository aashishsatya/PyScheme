"""
Created on Sun Dec 21 23:53:09 2014

@author: aashishsatya

Project Name: PyScheme

Description: In this project I attempt to write an implementation of a subset
of the Scheme Programming Language in Python.
"""

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
    
    