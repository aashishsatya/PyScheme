"""
Created on Mon Dec 22 21:21:26 2014

@author: aashishsatya

Description: Performs basic housekeeping functions like removing parens and 
nesting instructions within instructions as lists.

Modeled after Peter Norvig's implementation of the same.

"""

# most of these functions are implemented for data abstraction 

def make_exp(keyword, *args):
    
    """
    Used to make a new expression to pass to eval
    Input: A scheme keyword and a variable number of arguments
    Output: A parsed-form expression of the above mentioned scheme keyword
    """
    
    new_exp = [keyword]
    for arg in args:
        new_exp.append(arg)
    return new_exp

def get_name(exp):
    
    """
    Gets the name of the function or variable. Implemented for
    data abstraction.
    Input: a list exp after parsing a scheme expression
    Output: the name of the function or operator in the expression.
    """
    
    return exp[0]
    
def get_arguments(exp):
    
    """
    Gets the arguments of a function or operator statement. Implemented
    for data abstraction.
    Input: a list exp after parsing a scheme expression
    Output: the arguments of the function or operator in the expression.
    """
    
    return exp[1:]    

# main housekeeping; setters and getters for functions
    
# getters for assignment
# internal representation:
# ['set!', <variable name>, <new value>]
    
def get_assignment_variable(exp):
    return exp[1]    
def get_assignment_new_value(exp):
    return exp[2]

# getters for define
# internal representation:
# ['define', <variable or token>, <body>]

def get_definition_name(exp):
    return exp[1]
def get_definition_body(exp):
    return exp[2]
def is_definition_function(definition_name):
    return type(definition_name) == list
def get_definition_parameters(definition_name):
    # [<function name>, <arg1>, <arg2>...]
    return definition_name[1:]
def get_definition_function_name(definition_name):
    return definition_name[0]
    

# getters for if
# internal representation:
# ['if', <condition>, <consequent>, <alternative>]        

def get_condition(exp):
    return exp[1]
def get_consequent(exp):
    return exp[2]
def get_alternative(exp):
    return exp[3]
    
# getters for lambda
# internal representation:
# ['lambda',[<arg1>, <arg2>...], <body]
def get_lambda_parameters(exp):
    return exp[1]
def get_lambda_body(exp):
    return exp[2]
    
# getters for begin
# internal representation:
# ['begin', <item1>, <item2>...]

def get_begin_statements(exp):
    return exp[1:]

# getters for cond
#  internal representation:
# ['cond',[<condition1>, <consequent1>], [<condition2, conseq2]...]

def get_cond_conseq_pairs(exp):
    
    """
    Return a list of all the condition-consequent pairs
    """
    return exp[1:]
    
def get_condition_from_pair(pair):
    # [<condition>, <consequent>]
    return pair[0]
def get_consequent_from_pair(pair):
    # [<condition>, <consequent>]
    return pair[1]
    
# getters for quoted expressions
# either a string with "'" (apostrophe) inserted
# infront of it or of the form ['quote', <string>]

def get_text_of_quotation(exp):
    if type(exp) == list:
        return exp[1]
    return exp[1:]