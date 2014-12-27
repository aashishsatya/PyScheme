"""
Created on Sun Dec 21 23:53:09 2014

@author: aashishsatya

Project Name: PyScheme

Description: In this project I attempt to write an implementation of a subset
of the Scheme Programming Language in Python.
"""

from Classifier import *


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
            raise ValueError('Variable not defined in the environment')
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

class Procedure(object):
    
    """
    A class to model procedures. Stores variables and body of a procedure
    """
    
    def __init__(self, parameter_names, body):
        self.parameter_names = parameter_names
        self.body = body
        
    def call(self, parameter_values, calling_environment):        
        if len(self.parameter_names) != len(parameter_values):
            raise TypeError('Procedure expects ' + len(self.parameter_names) +
                            ' arguments.')
        procedure_environment = Environment(calling_environment)
        for index in range(len(self.parameter_names)):
            procedure_environment.add(self.parameter_names[index], parameter_values[index])
        return eval(self.body, procedure_environment)
        
def apply_operators(op, arguments_as_string):
    
    # op stands for the operator given as string
    
    """
    Applies operator to given arguments (may be more than two)
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
                    
    running_value = current_op(arguments[0], arguments[1])
    
    if len(arguments) == 2:
        return running_value
        
    # else has more than two arguments, so process them
    remaining_arguments = arguments[2:]
    for argument in remaining_arguments:
        running_value = current_op(running_value, argument)
    
    return running_value
    
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
            # directly a number represented as string
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
    
    elif is_assignment(exp):        
        variable = get_assignment_variable(exp)
        new_value = get_assignment_new_value(exp)
        env.update(variable, new_value)
        return ';Value: ' + variable
        
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
            return ';Value: ' + get_definition_function_name(definition_name)
        body = eval(get_definition_body(exp), env)
        env.add(definition_name, body)
        return ';Value: ' + definition_name
        
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
        # ['begin', <list of things to do>]
        # all we need to do is evaluate the arguments
        args = evaluate_arguments(get_begin_statements(exp), env)
        return ';Value: ' + args[-1]
        
    elif is_cond(exp):
        # condition - consequent pairs
        cond_conseq_pairs = get_cond_conseq_pairs(exp) 
        for cond_cons_pair in cond_conseq_pairs:
            condition = get_condition_from_pair(cond_cons_pair)
            if condition == 'else' or eval(condition, env):
                consequent = get_consequent_from_pair(cond_cons_pair)
                return eval(consequent, env)        
    
    elif is_variable(exp):
        # may be a variable, check it
        try:
            value = env.lookup(exp)
            return value
        except:
            return exp
        
    elif get_name(exp) in ['+', '-', '*', '/', '=']:
        op = get_name(exp)
        # evaluate arguments before applying operators        
        return apply_operators(op, evaluate_arguments(get_arguments(exp), env))  
              
    # item is a procedure
    procedure_name = get_name(exp)
    # evaluate arguments as before
    args = evaluate_arguments(get_arguments(exp), env)
    required_procedure_obj = env.lookup(procedure_name)
    return required_procedure_obj.call(args, env)
    
def repl(prompt='PyScheme> '):
    "A prompt-read-eval-print loop."
    while True:
        val = eval(parse(raw_input(prompt)))
        if val != None:
            print val
            

repl()
        