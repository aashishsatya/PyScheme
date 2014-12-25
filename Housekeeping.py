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
    
    # a token is the smallest individual unit of a program
    
    """
    Converts the input string into a list of tokens.
    """
    
    # add a space to parens so that they can be split easily
    string = string.replace('(', ' ( ')
    string = string.replace(')', ' ) ')
    
    return string.split()
    
# we will model things exactly as with the scheme implementation
# of the metacircular evaluator
# (define a 10) becomes ['define', 'a', '10']
# To make the concept more clear, think of a list in Scheme as a 
# list in Python!!
# this lets the classifier do its work (see Classifier.py)

# Thanks Peter Norvig for making this part easy

def parse(program):
    
    """
    Calls tokenize and read_from_tokens, cleans up the program for processing 
    as mentioned above.
    """
    
    # assumes the programmer to be correct
    
    return read_from_tokens(tokenize(program))
    
def read_from_tokens(token_list):    
    
    """
    Identifies individual expressions from a list of tokens and packages
    them as a list
    """
    
    # this is implemented as a separate function for the recursion to work
    # properly
    
    first_token = token_list.pop(0)
    
    if first_token == '(':
        # new expression in place
        # so initialize new list to package it
        new_expression = []
        while token_list[0] != ')':
            # keep appending values to the new expression list
            new_expression.append(read_from_tokens(token_list))
        # like Mr. Norvig said, remove  the ')'
        token_list.pop(0)
        return new_expression
    else:
        # token is not the start of a new expression
        # i.e. already in its smallest form
        # so simply return
        return first_token
    
    
    


