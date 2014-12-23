# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 21:21:26 2014

@author: aashishsatya

Description: Performs basic housekeeping functions like removing parens and 
nesting instructions within instructions as lists.

Modeled after Peter Norvig's implementation of the same.

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

