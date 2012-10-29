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
        return 'Conditional statement: {0!s} {1!s} {2!s}'.format(self.left, self.func, self.right)

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
        try:
            return self.func(self.value.eval(self.new_value))
        except AttributeError:
            raise RuntimeError('Calc() called on expression without a new_value set')

    def __str__(self):
        func_str = 'is' if not self.func else 'not'
        return 'Fuzzy expression: {0!s} {1!s} {2!s}'.format(self.var, func_str, self.value)
