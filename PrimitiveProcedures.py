"""
Created on Sun Dec 28 20:16:29 2014

@author: aashishsatya

Description: File to handle primitive procedures
"""

# Classifier.py finds the type of Scheme expression 
# that was given as input
from Classifier import *
# selectors for the given Scheme expression
from Selectors import *

primitive_operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=',
                       'and', 'or', 'not', 'eq?', 'equal?']
 
primitive_list_operators = ['cons', 'car', 'cdr', 'null?', 'list?', 'list',
                            'append']

def make_list(arguments):
    return arguments
    
def convert_to_scheme_expression(val):
    
    """
    Prints Python expression val as an expression in Scheme
    """
    
    # some code taken from Peter Norvig's implementation of the same
    # thanks Mr. Norvig
    # list_repn stands for list representation
    if type(val) == list:
        list_repn = '(' + ' '.join(map(convert_to_scheme_expression, val)) + ')'
        return list_repn

    elif str(val) == 'True':
        return '#t'
    elif str(val) == 'False':
        return '#f'
    else:
        return str(val)
    
def is_shortened_list_operation(operation_name):
    
    """
    Checks if an operation is a shortened list operation such as caar, cadddr
    etc.
    Input: A string
    Output: True or False depending on whether the operation is a shortened
    list operation
    """
    
    if operation_name[0] != 'c' or operation_name[-1] != 'r':
        return False
        
    for character in operation_name[1:-1]:
        if character != 'a' and character != 'd':
            return False
     
    return True
    
def expand_list_operation(list_op, args):
    
    args = args[0]
    for index in range(len(list_op) - 2, 0, -1):
        if list_op[index] == 'a':
            args = ['car', args]
        elif list_op[index] == 'd':
            args = ['cdr', args]
            
    return args 

def raise_argument_error(function_name, error_type, error_arg):
    
    """
    Raises an error of type error_type with error_arg as the object
    being printed as responsible for the error.
    """
    
    raise error_type('The object ' + convert_to_scheme_expression(error_arg) + ', passed as an argument to ' + function_name + ', is not the correct type.')
    
def raise_argument_count_error(correct_number, error_number, procedure_name):
    
    """
    Raises an error of type TypeError with a message containing the 
    input number and the required number of arguments.
    """
    
    if type(procedure_name) == str:
        raise TypeError('The procedure ' + procedure_name + ' has been called with ' + str(error_number) + ' argument(s); it requires exactly ' + str(correct_number) + ' argument(s).')
    raise TypeError('The procedure has been called with ' + str(error_number) + ' argument(s); it requires exactly ' + str(correct_number) + ' argument(s).')    

def apply_list_procedure(list_operation, args):
    
    """
    Applies list operations to given arguments
    """
    
    if list_operation == 'cons':
        if len(args) != 2:
            raise_argument_count_error(2, len(args), 'cons')
        if type(args[0]) not in (int, float, str):
            raise_argument_error(list_operation, TypeError, convert_to_scheme_expression(args[0]))
        if not type(args[1]) == list:
            raise_argument_error(list_operation, TypeError, convert_to_scheme_expression(args[1]))
        return make_list([args[0]] + args[1])
        
    elif list_operation == 'append':
        if not type(args[0]) == list:
            raise_argument_error(list_operation, ValueError, convert_to_scheme_expression(args[0]))
        if not type(args[1]) == list:
            raise_argument_error(list_operation, ValueError, convert_to_scheme_expression(args[0]))
        appended_lists = []
        for arg in args:
            appended_lists += arg
        return appended_lists
        
    elif list_operation == 'list':
        return args
        
    if len(args) != 1:
        raise_argument_count_error(1, len(args), list_operation)
    
    if list_operation == 'list?':
        return type(args[0]) == list
        
    if type(args[0]) != list:
            raise_argument_error(list_operation, ValueError, convert_to_scheme_expression(args[0]))
        
    if list_operation == 'car':
        # [<list_item>]
        # extra parens because of the [1:] from get_arguments() 
        # earlier in PyScheme.py
        if args[0] == []:
            raise_argument_error(list_operation, ValueError, convert_to_scheme_expression(args[0]))
        return args[0][0]
        
    elif list_operation == 'cdr':
        if args[0] == []:
            raise_argument_error(list_operation, ValueError, convert_to_scheme_expression(args[0]))
        return args[0][1:]
        
    elif list_operation == 'null?':
        return args[0] == []     
        

def apply_arithmetic_operator(op, arguments):
    
    """
    Applies an arithmetic operator (+, -, /, *) to the arguments.
    Input: An operator type and arguments
    Output: Value after applying operator op to its arguments.
    """
    
    running_value = op(arguments[0], arguments[1])
    
    if len(arguments) == 2:
        return running_value
        
    # else has more than two arguments, so process them
    remaining_arguments = arguments[2:]
    for argument in remaining_arguments:
        running_value = op(running_value, argument)            
    
    return running_value
    
def apply_logic_operator(op, arguments):
    
    """
    Applies a logic operator (>, <, == etc.) to the arguments
    Input: An operator and arguments
    Output: A True or False boolean value after applying op to its arguments
    """
    
    running_value = op(arguments[0], arguments[1])
    
    if len(arguments) == 2:
        return running_value
        
    index = 2
    while running_value and index < len(arguments):
        running_value = running_value and op(arguments[index - 1], arguments[index])
        index += 1
        
    return running_value
    
def apply_operators(op, arguments):
    
    # op stands for the operator given as string
    
    """
    Applies operator to given arguments (may be more than two; see below)
    """
    
    import operator
    
    # checking error in arguments
    for arg in arguments:
        if arg not in (True, False) and op in ('and', 'or', 'not'):
            raise_argument_error(op, TypeError, arg)
        if type(arg) != int and op == 'modulo':
            raise_argument_error(op, TypeError, arg)
        if op not in ('eq?', 'and', 'or', 'not', 'modulo', 'equal?') and type(arg) not in (int, float):
            raise_argument_error(op, TypeError, arg)
    
    if op in ('modulo', 'eq?', 'equal?') and len(arguments) != 2:
        raise_argument_count_error(2, len(arguments), op)
        
    
    if op == 'and':
        current_op = operator.and_
    elif op == 'or':
        current_op = operator.or_
    elif op == 'not':
        if len(arguments) != 1:
            raise_argument_count_error(1, len(arguments), 'not')
        return operator.not_(arguments[0])
    elif op == 'modulo':            
        return operator.mod(arguments[0], arguments[1])
    elif op == 'eq?':
        if type(arguments[0]) == str and type(arguments[1]) == str:
            return arguments[0] == arguments[1]
        else:
            return id(arguments[0]) == id(arguments[1])
    elif op == 'equal?':
        if type(arguments[0]) in (int, float) and type(arguments[1]) in (int, float):                      
            if type(arguments[1]) != type(arguments[0]):
                return False
            else:
                return arguments[0] == arguments[1]
        return str(arguments[0]) == str(arguments[1])
    
    # find the type of the operator
    if op == '+':
        current_op = operator.add
    elif op == '-':
        current_op = operator.sub
    elif op == '*':
        current_op = operator.mul
    elif op == '/':
        current_op = operator.div
    elif op == '=':
        current_op = operator.eq
    elif op == '<':
        current_op = operator.lt
    elif op == '>':
        current_op = operator.gt
    elif op == '<=':
        current_op = operator.le
    elif op == '>=':
        current_op = operator.ge
                    
    if op in ['+', '-', '*', '/']:
        return apply_arithmetic_operator(current_op, arguments)
        
    return apply_logic_operator(current_op, arguments)
    