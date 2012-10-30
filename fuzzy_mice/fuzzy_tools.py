#!/usr/bin/python

import re
from cond_statement import CondStatement, FuzzyExpr

LINGVAR = 'lingvar'
FUZZYSET = 'fuzzyset'
AND = 'and'
OR = 'or'
TRAPEZ = 'trapez'
TRIANGLE = 'triangle'
GRADE = 'grade'
REVERSE_GRADE = 'reverse_grade'

#Regular expression compilers:
EXPR = re.compile('\([a-z ]+ (is|not) [a-z ]+\)')

def parse_file(file):
    '''Parse the given file into fuzzy rules and states,
    this method will return a class which one can use to perform
    fuzzy logic.'''
    var = {} #Variables in the rules
    sets = {} #Dict between variables in var to values
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            l = line.lower().strip()
            if l.startswith('#'):
                #Ignore comments
                continue
            elif l.startswith('define'):
                res = __parse_define_statement(l, var, sets, i)
            elif l.startswith('if'):
                res = __parse_if_statement(l, var, sets, i)

def __parse_if_statement(line, var, sets, l_numb=None):
    '''Parse an if statement in the fuzzy rules format and convert it into
    something that we can use as a fuzzy statement'''
    if_st = line.split('then')
    if len(if_st) != 2:
        __raise_parse_exp(SyntaxError, 'Encountered malformed if statement', line,
                l_numb)
    if_conds = if_st[0].lstrip('if ').strip()
    if not if_conds:
        __raise_parse_exp(SyntaxError, 'Encountered malformed if statement', line,
                l_numb)
    raise NotImplementedError('If parsing not implemented')

def __parse_if_cond(cond, var, sets):
    #convert from "((a is A) and (b is B))" to "(a is A) and (b is B)"
    #Extract the two conditions in the expression
    expr = EXPR.match(cond)
    if expr:
        expr_st = expr.group()[1:-1].split(' ')
        func = (lambda x: x) if expr_st[1] == 'is' else (lambda x: 1.0 - x)
        return FuzzyExpr(expr_st[0], sets[expr_st[2]], func)
    else:
        a, b = __parse_if_helper(cond[1:-1])
        and1 = cond[1:len(a) + 1 + 4].strip() == AND
        if and1:
            func = min
        else:
            func = max
        return CondStatement(__parse_if_cond(a.strip()),
                __parse_if_cond(b.strip()), func)

def __parse_if_helper(cond):
    res = []
    line = ''
    found = 0
    for i in cond:
        if i == '(':
            found += 1
        elif i == ')':
            found -= 1
        line += i
        if found == 0 and line:
            res.append(line)
            line = ''
    return res[0], res[-1]

def __parse_define_statement(line, var, sets, l_numb = None):
    '''Parse a define statement in the fuzzy rules format and convert it into
    some results that we can use as either variables or sets'''
    define_vars = line.split(':')
    if len(define_vars) != 2:
        __raise_parse_exp(SyntaxError, 'Encountered a problem trying to parse a define statement',
                line, l_numb)
    d_st = define_vars[0].split(' ')
    if len(d_st) != 3:
        __raise_parse_exp(SyntaxError, 'Encountered a malformed "define" statement',
                line, l_numb)
    d_type = d_st[1]
    if d_type == LINGVAR:
        var_vals = define_vars[1].split(',')
        current_var = d_st[2].strip()
        if current_var not in var:
            var[current_var] = []
        for value in var_vals:
            var[current_var].append(value.strip())
    elif d_type == FUZZYSET:
        current_var = d_st[2].strip().split('.')
        if current_var[0] not in var and current_var[1] not in var[current_var[0]]:
            __raise_parse_exp(NameError, 'Variable({}) referenced before creation'.format(current_var),
                    line, l_numb)
        set_st = define_vars[1].split('=')
        if len(set_st) != 2:
            __raise_parse_exp(SyntaxError, 'Fuzzyset definition is not ' +
                    'correctly defined, was: {}'.format(set_st),
                    line, l_numb)
        set_type = set_st[0].strip()
        set_value = eval(set_st[1].strip())
        if set_type == TRAPEZ:
            raise NotImplementedError('Meh') #TODO create proper fuzzy set values
        elif set_type == TRIANGLE:
            raise NotImplementedError('Meh') #TODO create proper fuzzy set values
        elif set_type == GRADE:
            raise NotImplementedError('Meh') #TODO create proper fuzzy set values
        elif set_type == REVERSE_GRADE:
            raise NotImplementedError('Meh') #TODO create proper fuzzy set values
        else:
            __raise_parse_exp(TypeError, 'Type for fuzzyset is wrong, was {}'.format(set_type),
                    line, l_numb)
    else:
        __raise_parse_exp(TypeError,
                'Encountered a define type of wrong format. Was: {}'.format(d_type),
                line, l_numb)

def __raise_parse_exp(ex_type, msg, line, line_numb):
    if line_numb != None:
        error = ex_type(msg +
                '\nOn line {}, line was:\n{}'.format(line_numb, line))
    else:
        error = ex_type(msg +
                '\nLine was:\n{}'.format(line))
    raise error
