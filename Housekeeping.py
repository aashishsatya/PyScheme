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
        # so try to find the matching data type, and return
        return find_best_data_type(first_token)
        
def find_best_data_type(data_obj):
    
    """
    Finds the best possible data type for an object
    Input: a string
    Output: an int, float or a string depending on the input string
    """
    
    try:
        return int(data_obj)
    except ValueError:
        try:
            return float(data_obj)
        except ValueError:
            # string
            return data_obj

# most of these functions are implemented for data abstraction 

def make_exp(keyword, *args):
    
    """
    Used to make a new expression to pass to eval
    Input: A scheme keyword and a variable number of arguments
    Output: A parsed-form expression of the above mentioned scheme keyword
    """
    
#    print 'makeexp: keyword =', keyword
#    print 'makeexp: args =', args
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
# they're simply strings with "'" (apostrophe) inserted at the front

def get_text_of_quotation(exp):
    return exp[1:]
    
# getters for let expressions
# internal representation:
# ['let', [[<variable1>, <value1>], [<variable2>, <value2>]...], <body>]
    
def get_let_variable_expression_pairs(exp):
    return exp[1]
    
def get_let_body(exp):
    return exp[2]
    
# [<variable>, <value>]
def get_let_variable_from_pair(pair):
    return pair[0]
def get_let_expressions_from_pair(pair):
    return pair[1]

    
                
        


