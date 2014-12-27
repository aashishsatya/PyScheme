"""
Created on Mon Dec 22 21:10:34 2014

@author: aashishsatya

Description: Python code that classifies a given statement for eval.
Kind of like a header file in C or C++.
"""

from Housekeeping import *

# The functions are written in such a way that the name identifies the
# purpose of the function.
# For e.g. is_self_evaluating(item) will return the answer to the question
# "Is the item self-evaluating?", i.e.
# True if it is, False if it is not.

# exp stands for "expression" unless otherwise noted

def is_self_evaluating(exp):
    
    """
    Returns true if the expression is a number (integer or a float), 
    false otherwise.
    """
    
    try:
        temp_float = float(exp)
        return True
    except:
        return False
        
def is_variable(exp):
    
    """
    Checks if an item is a variable or not.
    For now, anything that is not a number(float or double) is a variable.
    """
    
    return type(exp) == str

# to ease checking predicates, we will define a template function
# which will check if the list begins with a particular keyword.

def generic_keyword_check(exp, keyword):
    
    """
    Returns true if exp is a list whose first element is the string in
    keyword, false otherwise.
    """
    
    if exp[0] == keyword:
        return True
    else:
        return False
        
def is_assignment(exp):
    
    """
    Checks if an expression is an assignment statement
    (one that uses 'set!')
    """
    
    return generic_keyword_check(exp, 'set!')
        
def is_definition(exp):
    
    """
    Checks if an expression is a definition.
    """
    
    return generic_keyword_check(exp, 'define')
        
def is_if_statement(exp):
    
    """
    Checks if the expression is an if statement
    """
    
    return generic_keyword_check(exp, 'if')
    
def is_lambda(exp):
    
    """
    Checks if the expression is a lambda statement
    """
    
    return generic_keyword_check(exp, 'lambda')
    
    
def is_begin(exp):
    
    """
    Checks if the expression is a begin statement
    """
    
    return generic_keyword_check(exp, 'begin')
    

# unfortunately Peter Norvig's implementation does not support
# the cond statement    
def is_cond(exp):
    
    """
    Checks if the expression is a begin statement
    """
    
    return generic_keyword_check(exp, 'cond')
    
def is_application(exp):
    
    """
    Checks if the expression is an application.
    Any expression that isn't one of the above (and not an error)
    is an application.
    """
    
    try:
        if type(exp) == list and len(exp) > 0:
            return True
        else:
            return False
    except:
        return False

    
    

