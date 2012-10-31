#!/usr/bin/python

#All Fuzzy sets must support at least an "eval(new_value)" method
#which returns a float representing the amount of membership that
#new_value has in the set. Float should be between [0, 1]

def create_line(p1, p2):
    '''Create a line equation from two points(p1, p2) and return
    a lambda function with that equation'''
    m = (p1[1] - p2[1]) / (p1[0] - p2[0])
    b = p1[1] - m*p1[0]
    assert isinstance(m, float), 'Create line got points not in float format'
    assert isinstance(b, float), 'Create line got points not in float format'
    if m == 0:
        return lambda x: b
    else:
        return lambda x: m*x + b

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
        self.l1 = create_line(left, top)
        self.l2 = create_line(top, right)
        self.left = left
        self.top = top
        self.right = right

    def eval(self, value):
        '''Calculate how much this value is within this triangle'''
        if self.left[0] <= value <= self.top[0]:
            return self.l1(value)
        elif self.top[0] < value <= self.right[0]:
            return self.l2(value)
        else:
            #Value is outside of this triangle so just return 0.0
            return 0.0
    def __str__(self):
        return 'Triangle = left:{0!s}, top:{1!s}, right:{2!s}'.format(self.left,
                self.top, self.right)

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
        self.l1 = create_line(left, top_left)
        self.l2 = create_line(top_left, top_right)
        self.l3 = create_line(top_right, right)
        self.left = left
        self.top_left = top_left
        self.top_right = top_right
        self.right = right

    def eval(self, value):
        if self.left[0] <= value <= self.top_left[0]:
            return self.l1(value)
        elif self.top_left[0] < value <= self.top_right[0]:
            return self.l2(value)
        elif self.top_right[0] < value <= self.right[0]:
            return self.l3(value)
        else:
            return 0.0

    def __str__(self):
        return 'Trapezoid = left:{0!s}, top_left:{1!s}, top_right:{2!s}, right:{3!s}'.format(
                self.left, self.top_left, self.top_right, self.right)

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
        self.top = float(left[1]) if not self.reverse else float(right[1])
        assert self.top <= 1.0, 'Gradient is larger than 1.0'
        self.line = create_line(left, right)
        self.left = left
        self.right = right

    def eval(self, value):
        if not self.reverse:
            if value <= self.left[0]:
                return self.top
            elif self.left[0] < value <= self.right[0]:
                return self.line(value)
            else:
                return 0.0
        else:
            if value >= self.right[0]:
                return self.top
            elif self.left[0] <= value < self.right[0]:
                return self.line(value)
            else:
                return 0.0

    def __str__(self):
        return 'Gradient = left:{0!s}, right{1!s}'.format(self.left, self.right)
