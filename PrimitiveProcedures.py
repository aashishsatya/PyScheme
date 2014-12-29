"""
Created on Sun Dec 28 20:16:29 2014

@author: aashishsatya

Description: File to handle primitive procedures
"""

primitive_operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=']

# sorry, operations like cadddar etc. are not supported. 
primitive_list_operators = ['cons', 'car', 'cdr', 'null?', 'list?', 'list',
                            'append']

def make_list(arguments):
    return ['list'] + arguments
    
def get_elements_in_list(listname):
    # [['list', <elem1>, <elem2>...]]
    # extra square brackets again because of get_arguments() from earlier
    return listname[1:]
    
def apply_list_procedure(list_operation, args):
    
    """
    Applies list operations to given arguments
    """
    
#    print 'applying list procedure'
#    print 'args =', args
#    print 'list operation =', list_operation
    
    if list_operation == 'cons':
        # [<value>, <list_item>]
        return make_list([args[0]] + get_elements_in_list(args[1]))
        
    elif list_operation == 'car':
        # [0] index because of extra square brackets
        # from get_arguments earlier
        list_args = get_elements_in_list(args[0])
        return list_args[0]
        
    elif list_operation == 'cdr':
        list_args = get_elements_in_list(args[0])
        return make_list(list_args[1:])
        
    elif list_operation == 'null?':
        list_args = get_elements_in_list(args[0])
        return list_args == []
        
    elif list_operation == 'list?':
        return args[0][0] == 'list'
        
    elif list_operation == 'list':
        return make_list(args)
        
    elif list_operation == 'append':
        # [<list1>, <list2>]
        return make_list(get_elements_in_list(args[0]) + 
                         get_elements_in_list(args[1]))
        

def apply_operators(op, arguments_as_string):
    
    # op stands for the operator given as string
    
    """
    Applies operator to given arguments (may be more than two; see below)
    """
    
    import operator
    
    # convert all arguments to floats
    arguments = []
    for arg in arguments_as_string:
        arguments.append(float(arg))
    
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
                    
    running_value = current_op(arguments[0], arguments[1])
    
    if len(arguments) == 2:
        return running_value
        
    # else has more than two arguments, so process them
    remaining_arguments = arguments[2:]
    for argument in remaining_arguments:
        running_value = current_op(running_value, argument)
    
    return running_value

