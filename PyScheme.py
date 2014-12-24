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
    
    def __init__(self, frame = {}, enclosingEnvironment = None):
        self.frame = frame
        self.enclosingEnvironment = enclosingEnvironment
        
    def lookup(self, variable):
        if variable in self.frame.keys():
            return self.frame[variable]
        else:
            self.enclosingEnvironment.lookup(variable)
    
    def update(self, variable, newValue):
        """
        Update the variable to the new value
        """
        if variable not in self.frame.keys() and self.enclosingEnvironment == None:
            raise ValueError('Variable not defined in the environment')
        elif variable not in self.frame.keys():
            self.enclosingEnvironment.update(variable, newValue)
        self.frame[variable] = newValue
        
    def add(self, variable, newValue):
        """
        Adds variable and newValue to the current frame
        """
        self.frame[variable] = newValue

# defining a global environment
global_env = Environment()

class Procedure(object):
    
    """
    A class to model procedures. Stores variables and body of a procedure
    """
    
    def __init__(self, parameters, body):
        self.parameters = parameters
        self.body = body
       
def eval(exp, env = global_env):
    
    """
    Evaluates the expression exp in the given environment env
    and returns the result
    """
    
    if isSelfEvaluating(exp):
        return exp
    
    if isAssignment(exp):
        variable = exp[1]
        newValue = exp[2]
        env.update(variable, newValue)
        
    if isDefinition(exp):
        tokenToDefine = exp[1]
        definitionBody = eval(exp[2], env)
        env.add(tokenToDefine, definitionBody)
        
    if isIfStatement(exp):        
        condition = exp[1]
        consequent = exp[2]
        alternative = exp[3]
        if eval(condition, env) == 'True':
            return eval(consequent, env)
        elif eval(condition, env) == 'False':
            return eval(alternative, env)
        