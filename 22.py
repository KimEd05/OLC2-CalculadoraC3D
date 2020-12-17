# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

class Nodo():
    def __init__(self, addr = '', code = ''):
        self.addr = addr
        self.code = code

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

t = -1
def getTemporal():
    global t 
    t += 1
    return 't' + str(t)

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

def p_statement_expr(t):
    'statement : expression'
    t[0] = t[1]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    t[0] = Nodo(addr = getTemporal())
    if t[2] == '+'  : 
        t[0].code = t[1].code + t[3].code + t[0].addr + ' = ' + t[1].addr + ' + ' + t[3].addr + ';\n'
    elif t[2] == '-':
        t[0].code = t[1].code + t[3].code + t[0].addr + ' = ' + t[1].addr + ' - ' + t[3].addr + ';\n'
    elif t[2] == '*': 
        t[0].code = t[1].code + t[3].code + t[0].addr + ' = ' + t[1].addr + ' * ' + t[3].addr + ';\n'
    elif t[2] == '/': 
        if t[3].addr == 0 :
            print("Can't divide by 0")
            raise ZeroDivisionError('integer division by 0')
        t[0].code = t[1].code + t[3].code + t[0].addr + ' = ' + t[1].addr + ' / ' + t[3].addr + ';\n'

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = Nodo(addr = getTemporal())
    t[0].code = t[2].code + t[0].addr + ' = -' + t[2].addr + ';\n'

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = Nodo(t[2].addr, t[2].code)

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = Nodo(addr = str(t[1]))

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    print(parser.parse(s).code)
    t = -1
