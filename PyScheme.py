"""
Created on Sun Dec 21 23:53:09 2014

@author: aashishsatya

Project Name: PyScheme

Description: In this project I attempt to write an implementation of a subset
of the Scheme Programming Language in Python.
"""

from PrimitiveProcedures import *
from Parser import *


# to implement the environment model of evaluation in Scheme, 
# we need environments. 
class Environment(object):
    
    """
    An environment is simply a dict of variable-value pairs, and some
    predefined mappings.
    """
    
    def __init__(self, enclosing_environment = None):
        self.frame = {}
        self.enclosing_environment = enclosing_environment
        
    def lookup(self, variable):
        if variable in self.frame.keys():
            return self.frame[variable]
        else:
            return self.enclosing_environment.lookup(variable)
    
    def update(self, variable, new_value):
        """
        Update the variable to the new value
        """
        if variable not in self.frame.keys() and self.enclosing_environment == None:
            raise ValueError("Unbound variable: " + variable)
        elif variable not in self.frame.keys():
            self.enclosing_environment.update(variable, new_value)
        self.frame[variable] = new_value
        
    def add(self, variable, new_value):
        """
        Adds variable and new_value to the current frame
        """
        self.frame[variable] = new_value

# defining a global environment
global_env = Environment()
global_env.add('#t', True)
global_env.add('#f', False)

class Procedure(object):
    
    """
    A class to model procedures. Stores variables and body of a procedure
    """
    
    def __init__(self, parameter_names, body):
        self.parameter_names = parameter_names
        self.body = body
        
    def call(self, parameter_values, calling_environment):        
        if len(self.parameter_names) != len(parameter_values):
            raise TypeError(str(len(self.parameter_names)))
        procedure_environment = Environment(calling_environment)
        for index in range(len(self.parameter_names)):
            procedure_environment.add(self.parameter_names[index], parameter_values[index])
        return eval(self.body, procedure_environment)
        

    
def evaluate_arguments(list_of_args, env):
    
    """
    Evaluates arguments for function calls or operators.
    Input: A series of arguments as a list and an Environment env
    Returns: A list of arguments after evaluation.
    """
    
    # dereference variables
    args = []
    for var in list_of_args:
        try:
            value = eval(var, env)
            args.append(value)
        except:
            # already in simplest form, so further evaluation fails
            # so simply append
            args.append(var)
    return args


# functions use setters and getters to implement data abstraction
# if you need details of the implementation see Housekeeping.py
    
def eval(exp, env = global_env):
    
    """
    Evaluates the expression exp in the given environment env
    and returns the result
    """
    
    if is_self_evaluating(exp):
        return exp
        
    if is_quoted(exp):
        return get_text_of_quotation(exp)
    
    elif is_assignment(exp):        
        variable = get_assignment_variable(exp)
        new_value = eval(get_assignment_new_value(exp))
        previous_value = env.lookup(variable)
        env.update(variable, new_value)
        return str(previous_value)
        
    elif is_let(exp):
        # let is nothing but syntactic sugar for underlying lambda
        # expression:
        # (let ((var1 exp1) (var2 exp2) ... (varn expn)) body)
        # is ((lambda (var1 var2 ... varn) body) exp1 exp2 ... expn)
        # so we get lambda variables and expressions first
        variables = []
        expressions = []
        variable_expression_pairs = get_let_variable_expression_pairs(exp)
        for pair in variable_expression_pairs:
            variables.append(get_let_variable_from_pair(pair))
            expressions.append(get_let_expressions_from_pair(pair))
        body = get_let_body(exp)
        # make lambda function
        lambda_expression = eval(make_exp('lambda', variables, body))
        args = evaluate_arguments(expressions, env)
        return lambda_expression.call(args, env)
        
    elif is_definition(exp):        
        definition_name = get_definition_name(exp)
        if is_definition_function(definition_name):
            # means define has been used to define a function
            # send straight to lambda
            body = get_definition_body(exp)
            lambda_expression = eval(make_exp('lambda',
                                              get_definition_parameters(definition_name),
                                              body))
            env.add(get_definition_function_name(definition_name), lambda_expression)
            return get_definition_function_name(definition_name)
        body = eval(get_definition_body(exp), env)
        env.add(definition_name, body)
        return definition_name
        
    elif is_if_statement(exp):        
        condition = get_condition(exp)
        consequent = get_consequent(exp)
        # alternative is a must
        alternative = get_alternative(exp)
        if eval(condition, env) == True:
            return eval(consequent, env)
        else:
            return eval(alternative, env)
            
    elif is_lambda(exp):
        params = get_lambda_parameters(exp)
        body = get_lambda_body(exp)
        return Procedure(params, body)
        
    elif is_begin(exp):
        # all we need to do is evaluate the arguments
        args = evaluate_arguments(get_begin_statements(exp), env)
        return args[-1]
        
    elif is_cond(exp):
        # condition - consequent pairs
        cond_conseq_pairs = get_cond_conseq_pairs(exp)
        for cond_cons_pair in cond_conseq_pairs:
            condition = get_condition_from_pair(cond_cons_pair)
            if condition == 'else' or eval(condition, env):
                consequent = get_consequent_from_pair(cond_cons_pair)
                return eval(consequent, env)        
    
    elif is_variable(exp):
        # exp may be a variable name
        # so check it
        try:
            value = env.lookup(exp)
            return value
        except AttributeError:
            raise NameError("Unbound variable: " + exp)
        
    # the PrimitiveProcedures file takes care of this part
        
    elif get_name(exp) in primitive_operators:
        op = get_name(exp)
#         evaluate arguments before applying operators
        args = evaluate_arguments(get_arguments(exp), env)
        result = apply_operators(op, args)
        return result
            
    elif get_name(exp) in primitive_list_operators:
        list_operation = get_name(exp)
        args = evaluate_arguments(get_arguments(exp), env)
        return apply_list_procedure(list_operation, args)
        
    # check for shortened list operation        
    elif  is_shortened_list_operation(get_name(exp)):
        # find and convert to corresponding expanded form
        # then send back to eval
        args = evaluate_arguments(get_arguments(exp), env)
        # args[0] to remove the extra parens inserted due to get_arguments()
        expanded_expression = expand_list_operation(get_name(exp), args)
        return eval(expanded_expression)
              
    # item is a procedure
    procedure_name = get_name(exp)
    # evaluate arguments as before
    args = evaluate_arguments(get_arguments(exp), env)
    # if the procedure is already defined in the environment
    # is_variable looks it up
    # otherwise, it makes a new procedure object
    # e.g. when directly lambda is used
    required_procedure_obj = eval(procedure_name)
    try:
        return required_procedure_obj.call(args, env)
    except TypeError as incorrect_arg_count:
        correct_arg_count = int(incorrect_arg_count.message)
        raise_argument_count_error(correct_arg_count, len(args), procedure_name)

def print_help_message():

    """
    Prints a help message for the user to navigate through the program.
    """
    
    print ''
    print 'Help for navigating through PyScheme:'
    print ''
    print 'Note: Procedures work the same way they do in Scheme, unless noted otherwise.'
    print ''    
    print 'List of supported procedures:'
    print ' - define, for both variable and function definitions'
    print ' - lambda'
    print ' - if (must have an <alternative> condition)'
    print ' - cond (else is also supported)'
    print ' - set!, for assignnment'
    print ' - quote, for symbolic notation'
    print ' - begin, for sequential execution'
    print ' - primitive list operators: list, append, car, cdr, list?, null?'
    print ' - shortened list operators such as car, caddr, caar etc.'
    print ' - primitive operators: +, -, *, /, modulo (division does not give fraction though)'
    print ' - logical operators: and, or, not'
    print ' - operators for comparison: >, <, <=, >=, ='
    print ' - operators for equality comparison: eq?, equal?'
    print ''
    print 'In case of any bugs in the above procedures kindly report to ankarathaashish@gmail.com'
    print ''
    
def repl():
    
    "A prompt-read-eval-print loop."
    
    print ''
    print 'PyScheme: A Scheme-like interpreter written in Python by Aashish Satyajith.'
    print "Note: Interpreter does not support all Scheme operations, see README or enter '(help)'."
    print "Enter '(exit)' (without quotes) or Ctrl-D to exit."
    print ''
    
    while True:
        try:
            input_str = raw_input('PyScheme> ')
            if len(input_str) == 0 or input_str.isspace() or input_str.lstrip()[0] == ';':
                # whitelines and comments, continue
                continue
            while input_str.count('(') != input_str.count(')'):
                temp_input = raw_input()
                if len(temp_input) == 0 or temp_input.isspace() or temp_input.lstrip()[0] == ';':
                    continue
                input_str += ' ' + temp_input
            parsed_input = parse(input_str)
            if parsed_input == ['exit']:
                break
            if parsed_input == ['help']:
                print_help_message()
                continue
            print ''
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception:
            print ';Error in input, try again.'
        try:
            val = eval(parsed_input)
            if val != None:
                print ';Value: ' + convert_to_scheme_expression(val)
        except Exception as error:
            print ';Error: ' + error.message
        print ''
            
repl()
print ''
print 'End of input stream reached.'
print 'Moriturus te saluto.'
print ''
        