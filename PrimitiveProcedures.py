"""
Created on Sun Dec 28 20:16:29 2014

@author: aashishsatya

Description: File to handle primitive procedures
"""

primitive_operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=',
                       'and', 'or', 'not', 'eq?']

# sorry, operations like cadddar etc. are not supported. 
primitive_list_operators = ['cons', 'car', 'cdr', 'null?', 'list?', 'list',
                            'append']

def make_list(arguments):
    return arguments
    
def is_shortened_list_operation(operation_name):
    
    """
    Checks if an operation is a shortened list operation such as caar, cadddr
    etc.
    Input: A string
    Output: True or False depending on whether the operation is a shortened
    list operation
    """
    
#    print 'operation_name = ', operation_name
    if operation_name[0] != 'c' or operation_name[-1] != 'r':
#        print 'returning false, ends do not match'
        return False
        
#    print 'checking for', operation_name[1:-1]
    for character in operation_name[1:-1]:
#        print 'character != a: ', str(character != 'a')
#        print 'character != d: ', str(character != 'd')
        if character != 'a' and character != 'd':
            return False
    
#    print 'returning true...'        
    return True
    
def expand_list_operation(list_op, args):
    
#    print 'args =', args
    
    for index in range(len(list_op) - 2, 0, -1):
        if list_op[index] == 'a':
            args = ['car', args]
        elif list_op[index] == 'd':
            args = ['cdr', args]
            
    return args
        
    
        
    
#def get_elements_in_list(listname):
#    # [['list', <elem1>, <elem2>...]]
#    # extra square brackets again because of get_arguments() from earlier
#    return listname[1:]
    
def apply_list_procedure(list_operation, args):
    
    """
    Applies list operations to given arguments
    """
    
#    print 'applying list procedure'
#    print 'args =', args
#    print 'list operation =', list_operation
#    print 'type args == list? ', type(args) == list
    
    if list_operation == 'cons':
        # [<value>, <list_item>]
        if type(args[0]) not in (int, float, str):
            error_message = 'The object ' + str(args[0]) + ', passed as an argument to cons, is not the correct type.'
            raise TypeError(error_message)
        if not type(args[1]) == list:
            error_message = 'The object ' + str(args[0]) + ', passed as an argument to cons, is not a list.'
            raise TypeError(error_message)
        return make_list([args[0]] + args[1])
        
    elif list_operation == 'car':
        # [<list_item>]
        # extra parens because of the [1:] from get_arguments() 
        # earlier in PyScheme.py
        if args[0] == []:
            raise ValueError("The object (), passed as the first argument to car, is not the correct type.")
        return args[0][0]
        
    elif list_operation == 'cdr':
        if args[0] == []:
            raise ValueError("The object () passed as an argument to safe-cdr is not a proper list.")
        return args[0][1:]
        
    elif list_operation == 'null?':
        return args[0] == []
        
    elif list_operation == 'list?':
        return type(args[0]) == list
        
    elif list_operation == 'list':
        return args
        
    elif list_operation == 'append':
        # [<list1>, <list2>]
        if not type(args[0]) == list:
            error_message = 'The object ' + str(args[0]) + ', passed as an argument to append, is not a list.'
            raise TypeError(error_message)
        if not type(args[1]) == list:
            error_message = 'The object ' + str(args[1]) + ', passed as an argument to append, is not a list.'
            raise TypeError(error_message)
        return args[0] + args[1]
        

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
    
    # find the type of the operator
    if op == '+':
        current_op = operator.add
    elif op == '-':
        current_op = operator.sub
    elif op == '*':
        current_op = operator.mul
    elif op == '/':
        current_op = operator.div
    elif op == '=' or op == 'eq?':
        current_op = operator.eq
    elif op == '<':
        current_op = operator.lt
    elif op == '>':
        current_op = operator.gt
    elif op == '<=':
        current_op = operator.le
    elif op == '>=':
        current_op = operator.ge
    elif op == 'and':
        current_op = operator.and_
    elif op == 'or':
        current_op = operator.or_
    elif op == 'not':
        return operator.not_(arguments[0])
                    
    if op in ['+', '-', '*', '/']:
        return apply_arithmetic_operator(current_op, arguments)
    return apply_logic_operator(current_op, arguments)

