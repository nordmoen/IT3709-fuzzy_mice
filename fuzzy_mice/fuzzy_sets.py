#!/usr/bin/python

#All Fuzzy sets must support at least an "eval(new_value)" method
#which returns a float representing the amount of membership that
#new_value has in the set. Float should be between [0, 1]

class FuzzyTriangle(object):
    '''A fuzzy set implementation which represents a triangle on a two
    dimensional graph'''
    def __init__(self, left, top, right):
        '''Left, top and right should be tuples of type (x::int, y::int)
        representing the left most, top most and right most point of a triangle
            top
           /   \
          /     \
        left---right
        '''
        self.x1 = left[0]
        self.x2 = right[0]
        self.top_x = top[0]
        #Create needed parts here to use later in the eval method

    def eval(self, value):
        '''Calculate how much this value is within this triangle'''
        if self.x1 <= value <= self.top_x:
            pass
        elif self.top_x < value <= self.x2:
            pass
        else:
            '''Value is outside of this triangle so just return 0.0'''
            return 0.0

