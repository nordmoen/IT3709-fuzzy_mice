#!/usr/bin/python

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

class FuzzyExpr(object):
    '''A class representing a fuzzy expression of the form "health is good"'''
    def __init__(self, var_name, value, func):
        self.var = var_name
        self.value = value
        self.func = func

    def eval(self, **kwargs):
        return self.func(self.value.eval(kwargs[self.var]))

    def __str__(self):
        func_str = 'is' if not self.func else 'not'
        return '(Fuzzy expression: {0!s} {1!s} {2!s})'.format(self.var, func_str, self.value)

class IfStatement(object):
    '''A class representing a fuzzy if statement of the form "if (a and|or b)
    action is act", all fuzzy if statements fire to some degree so every if statement
    will return some degree of truth for its condition. It can return a value between
    [0, 1]'''
    def __init__(self, cond, action_name, action_set, func = lambda x: x):
        self.cond = cond
        self.action = action_name
        self.set = action_set
        self.func = func

    def eval(self, **kwargs):
        return (self.action, self.set, self.func(self.cond.eval(**kwargs)))

    def __str__(self):
        return 'IF {0!s} THEN action is {1!s}, using hedge:{2!s}'.format(self.cond,
                self.action, self.func)
