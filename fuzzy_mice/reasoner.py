#!/usr/bin/python

class FuzzyReasoner(object):
    '''A class representing a fuzzy logic reasoner. This class takes in an
    IfStatement which it uses to perform its logic. It also needs the range
    of values it should calculate with i.e. the different X values that the
    action can have'''
    def __init__(self, if_sts, action_sets, range_gen=range(101)):
        '''This class takes a list of if statements and a list of the range
        for which it should calculate the result from. Action_set is a list of
        triples where the triple consist of (action_name, action_class, action_set)
        where the action name is the name of the action e.g. "risk" or "action".
        Action_class is the type of the action, e.g. "risk" may have ["low",
        "normal", "high"] as its associated classes. And the set is the set representing
        the class within the action.'''
        self.if_sts = if_sts
        self.action_sets = action_sets
        self.gen = range_gen

    def __mamdani_eval(self, **kwargs):
        res = map(lambda x: x.eval(**kwargs), self.if_sts)
        dividence = {s:0 for (_, s, _, _) in res}
        above = 0
        for val in self.gen:
            m = -1
            m_set = None
            m_val = 0
            for (_, s, s_val, _) in res:
                v = s.eval(val)*s_val
                if v > m:
                    m = v
                    m_set = s
                    m_val = s_val
            above += val*m_val
            dividence[m_set] += 1
        below = sum([dividence[s]*s_val for (_, s, s_val, _) in res])
        if below == 0:
            raise NoConditionalFired(self.if_sts)
        return above / below

    def __sugeno_eval(self, **kwargs):
        res = map(lambda x: x.eval(**kwargs), self.if_sts)
        above = [k*my for (_, _, my, k) in res]
        below = [my for (_, _, my, _) in res]
        ret = sum(below)
        if ret == 0:
            raise NoConditionalFired(self.if_sts)
        return sum(above) / ret

    def eval(self, mamdani = True, **kwargs):
        if mamdani:
            res = self.__mamdani_eval(**kwargs)
        else:
            res = self.__sugeno_eval(**kwargs)
        best = -1
        best_str = ''
        for (action, action_class, action_set) in self.action_sets:
            r = action_set.eval(res)
            if r > best:
                best = r
                best_str = '{}.{}'.format(action, action_class)
        return best_str

class FuzzyRuntimeError(RuntimeError):
    '''An umbrella error for runtime errors in the fuzzy rezoning'''
    def __init__(self, msg):
        super(RuntimeError, self).__init__(msg)

class NoConditionalFired(FuzzyRuntimeError):
    '''An error thrown when a none of the conditionals in the reasoner fires'''
    def __inti__(self, if_conds):
        super(FuzzyRuntimeError, self).__init__('None of the conditionals fired:\n{0!s}'.format(
            map(str, if_conds)))
