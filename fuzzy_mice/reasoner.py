#!/usr/bin/python

class FuzzyReasoner(object):
    '''A class representing a fuzzy logic reasoner. This class takes in an
    IfStatement which it uses to perform its logic. It also needs the range
    of values it should calculate with i.e. the different X values that the
    action can have'''
    def __init__(self, if_sts, range_list):
        '''This class takes a list of if statements and a list of the range
        for which it should calculate the result from'''
        self.if_sts = if_sts
        self.gen = range_list

    def mamdani_eval(self, **kwargs):
        res = map(lambda x: x.eval(**kwargs), self.if_sts)
        dividence = {s:0 for (_, s, _) in res}
        above = 0
        for val in self.gen:
            m = -1
            m_set = None
            m_val = 0
            for (_, s, s_val) in res:
                v = s.eval(val)
                if v > m:
                    m = v
                    m_set = s
                    m_val = s_val
            above += val*m_val
            dividence[m_set] += 1
        return above / sum([dividence[s]*s_val for (_, s, s_val) in res])

    def sugeno_eval(self, **kwargs):
        raise NotImplementedError('Sugeno inference not implemented yet')
