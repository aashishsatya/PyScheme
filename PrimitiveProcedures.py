"""
Created on Sun Dec 28 20:16:29 2014

@author: aashishsatya

Description: File to handle primitive procedures
"""

primitive_operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=',
                       'and', 'or', 'not']

# sorry, operations like cadddar etc. are not supported. 
primitive_list_operators = ['cons', 'car', 'cdr', 'null?', 'list?', 'list',
                            'append']

def make_list(arguments):
    return arguments
    
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
        return make_list([args[0]] + args[1])
        
    elif list_operation == 'car':
        # [<list_item>]
        # extra parens because of the [1:] from get_arguments() 
        # earlier in PyScheme.py
        return args[0][0]
        
    elif list_operation == 'cdr':
        return args[0][1:]
        
    elif list_operation == 'null?':
        return args[0] == []
        
    elif list_operation == 'list?':
        return type(args[0]) == list
        
    elif list_operation == 'list':
        return args
        
    elif list_operation == 'append':
        # [<list1>, <list2>]
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
    elif op == 'and':
        current_op = operator.and_
    elif op == 'or':
        current_op = operator.or_
    elif op == 'not':
        return operator.not_(arguments[0])
                    
    if op in ['+', '-', '*', '/']:
        return apply_arithmetic_operator(current_op, arguments)
    return apply_logic_operator(current_op, arguments)

