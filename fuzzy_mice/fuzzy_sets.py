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
        assert top[1] <= 1.0, 'Triangle is higher than 1.0'
        self.x1 = left[0]
        self.x2 = right[0]
        self.top_x = top[0]
        #TODO: Create needed parts here to use later in the eval method

    def eval(self, value):
        '''Calculate how much this value is within this triangle'''
        if self.x1 <= value <= self.top_x:
            raise NotImplementedError('Triangle eval not done')
        elif self.top_x < value <= self.x2:
            raise NotImplementedError('Triangle eval not done')
        else:
            #Value is outside of this triangle so just return 0.0
            return 0.0

class FuzzyTrapeze(object):
    '''A fuzzy set implementation which represents a trapeze in a two
    dimensional graph'''
    def __init__(self, left, top_left, top_right, right):
        '''         top_left-----------top_right
                    /                          \
                   /                            \
                left---------------------------right'''
        assert top_left[1] <= 1.0, 'Trapeze is larger than 1.0 in height'
        assert top_right[1] <= 1.0, 'Trapeze is larger than 1.0 in height'
        self.x1 = left[0]
        self.x2 = top_left[0]
        self.x3 = top_right[0]
        self.x4 = right[0]
        #TODO Finish

    def eval(self, value):
        if self.x1 <= value <= self.x2:
            raise NotImplementedError('Trapeze eval not done')
        elif self.x2 < value <= self.x3:
            raise NotImplementedError('Trapeze eval not done')
        elif self.x3 < value <= self.x4:
            raise NotImplementedError('Trapeze eval not done')
        else:
            return 0.0

class FuzzyGradient(object):
    '''Fuzzy set implementation representing a gradient, everything inside the
    gradient is inside the fuzzy set'''
    def __init__(self, left, right):
        '''If reverse is true we have a line like:
             /
            / All this is within the set
        else:
                              \
        All this is within     \ '''
        self.reverse = left[1] < right[1]
        self.x1 = left[0]
        self.x2 = right[0]
        self.top = float(left[1]) if not self.reverse else float(right[1])
        assert self.top <= 1.0, 'Gradient is larger than 1.0'

    def eval(self, value):
        if not self.reverse:
            if value <= self.x1:
                return self.top
            elif self.x1 < value <= self.x2:
                #TODO fix calculation
                raise NotImplementedError('Gradient eval not done')
            else:
                return 0.0
        else:
            if value >= self.x2:
                return self.top
            elif self.x1 <= value < self.x2:
                #TODO fix calculation
                raise NotImplementedError('Gradient eval not done')
            else:
                return 0.0
