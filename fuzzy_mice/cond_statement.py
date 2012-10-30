#!/usr/bin/python

class CondStatement(object):
    '''Class representing a conditional statement of the form
    "(a and|or b)" where a and b are either a conditional statement
    or a fuzzy expression'''

    def __init__(self, left_cond, right_cond, func):
        self.func = func
        self.left = left_cond
        self.right = right_cond

    def calc(self):
        return self.func(self.left.calc(), self.right.calc())

    def set_value(self, **kwargs):
        self.left.set_value(kwargs)
        self.right.set_value(kwargs)

    def reset(self):
        self.left.reset()
        self.right.reset()

    def __str__(self):
        return '(Conditional statement: {0!s} {1!s} {2!s})'.format(self.left, self.func, self.right)

class FuzzyExpr(object):
    '''A class representing a fuzzy expression of the form "health is good"'''

    def __init__(self, var_name, value, func):
        self.var = var_name
        self.value = value
        self.func = None
        self.new_value = None

    def set_value(self, **kwargs):
        if self.var in kwargs:
            self.new_value = kwargs[self.var]

    def reset(self):
        self.new_value = None

    def calc(self):
        if self.new_value == None:
            raise RuntimeError('Calc() called on expression without a new_value set')
        return self.func(self.value.eval(self.new_value))

    def __str__(self):
        func_str = 'is' if not self.func else 'not'
        return '(Fuzzy expression: {0!s} {1!s} {2!s})'.format(self.var, func_str, self.value)

class IfStatement(object):
    '''A class representing a fuzzy if statement of the form "if (a and|or b)
    action is act", all fuzzy if statements fire to some degree so every if statement
    will return some degree of truth for its condition. It can return a value between
    [0, 1]'''
    def __init__(self, cond, action):
        self.cond = cond
        self.action = action

    def set_value(self, **kwargs):
        self.cond.set_value(kwargs)

    def eval(self):
        return (self.action, self.cond.calc())

    def reset(self):
        self.cond.reset()

    def __str__(self):
        return 'IF {0!s} THEN action is {1!s}'.format(self.cond, self.action)
