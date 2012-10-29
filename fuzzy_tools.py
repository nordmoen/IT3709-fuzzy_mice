#!/usr/bin/python

LINGVAR = 'lingvar'
FUZZYSET = 'fuzzyset'
TRAPEZ = 'trapez'
TRIANGLE = 'triangle'
GRADE = 'grade'
REVERSE_GRADE = 'reverse_grade'

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
                res = __parse_if_statement(l, var, i)

def __parse_if_statement(line, var, l_numb=None):
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

def __parse_if_cond(cond):
    '''Parse an if condition of the format (a and b) where a and b be can be
    if conditions them self'''
    pass

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
