#!/usr/bin/python

import constants as const

class FuzzyExpr(object):
    '''A class representing a fuzzy expression of the form "health is good",
    is_val represents whether or not there is a NOT modifier on this expr'''
    def __init__(self, var_name, value, is_val= True, hedge = lambda x: x):
        self.var = var_name
        self.value = value
        self.is_val = is_val
        self.hedge = hedge
        if self.is_val:
            #This expression does not have a NOT modifier
            self.func = lambda x: x
        else:
            #This means the expression has a NOT modifier
            self.func = lambda x: 1.0 - x

    def eval(self, **kwargs):
        return self.func(self.hedge(self.value.eval(kwargs[self.var])))

    def __str__(self):
        is_str = const.IS if self.is_val else const.NOT
        return '(Fuzzy expression: {0!s} {1!s} {2!s})'.format(self.var, is_str, self.value)

class CondStatement(object):
    '''Class representing a conditional statement of the form
    "(a and|or b)" where a and b are either a conditional statement
    or a fuzzy expression'''
    def __init__(self, left_cond, right_cond, func):
        self.func = func
        self.left = left_cond
        self.right = right_cond

    def eval(self, **kwargs):
        return self.func(self.left.eval(**kwargs), self.right.eval(**kwargs))

    def __str__(self):
        return '(Conditional statement: {0!s} {1!s} {2!s})'.format(self.left, self.func, self.right)

class IfStatement(object):
    '''A class representing a fuzzy if statement of the form "if (a and|or b)
    action is act", all fuzzy if statements fire to some degree so every if statement
    will return some degree of truth for its condition. It can return a value between
    [0, 1]'''
    def __init__(self, cond, action_name, action_set):
        self.cond = cond
        self.action = action_name
        self.set = action_set

    def eval(self, **kwargs):
        try:
            return (self.action, self.set, self.cond.eval(**kwargs), self.set.range())
        except KeyError, e:
            raise TypeError('Not all needed arguments was supplied. The argument' +
                    ' {0!s} was needed, but not supplied'.format(e))

    def __str__(self):
        return 'IF {0!s} THEN action is {1!s}, using hedge:{2!s}'.format(self.cond,
                self.action, self.func)
