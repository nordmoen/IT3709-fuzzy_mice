#!/usr/bin/python

LINGVAR = 'lingvar'
FUZZYSET = 'fuzzyset'

def parse_file(file):
    '''Parse the given file into fuzzy rules and states,
    this method will return a class which one can use to perform
    fuzzy logic.'''
    var = [] #Variables in the rules
    sets = {} #Dict between variables in var to values
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            l = line.lower().trim()
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
    return None

def __parse_define_statement(line, var, sets, l_numb = None):
    '''Parse a define statement in the fuzzy rules format and convert it into
    some results that we can use as either variables or sets'''
    define_vars = line.split(':')
    if len(define_vars) != 2:
        __raise_parse_exp(SyntaxError, 'Encountered a problem trying to parse a define statement',
                line, l_numb)

    d_st = define_vars[0].split(' ')
    if len(d_st) != 3:
        __raise_parse_exp(SyntaxError, 'Encountered a mallformed "define" statement',
                line, l_numb)

    d_type = d_st[1]
    if d_type == LINGVAR:
        pass
    elif d_type == FUZZYSET:
        pass
    else:
        __raise_parse_exp(TypeError,
                'Encountered a define type of wrong format. Was: {}'.format(d_type),
                line, l_numb)

def __raise_parse_exp(ex_type, msg, line, line_numb):
    if line_numb:
        error = ex_type.__init__(msg +
                '\nOn line {}, line was:\n{}'.format(line_numb, line))
    else:
        error = ex_type.__init__(msg +
                '\nLine was:\n{}'.format(line))
    raise error
