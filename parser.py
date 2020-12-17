import ply.lex as lex
from lex import *

lexer = lex.lex()

t = -1
def getTemporal():
    global t 
    t += 1
    return 't' + str(t)

precedence = (
    ( 'left', 'PLUS', 'MINUS' ),
    ( 'left', 'TIMES', 'DIV' ),
    ( 'nonassoc', 'UMINUS' )
)

def p_add( p ) :
    'expr : expr PLUS expr'
    p[0] = getTemporal()
    print(p[0] + ' = ' + p[1] + ' + ' + p[3] + ';')

def p_sub( p ) :
    'expr : expr MINUS expr'
    p[0] = getTemporal()
    print(p[0] + ' = ' + p[1] + ' - ' + p[3] + ';')

def p_expr2uminus( p ) :
    'expr : MINUS expr %prec UMINUS'
    p[0] = getTemporal()
    print(p[0] + ' = -' + p[2] + ';')

def p_mult_div( p ) :
    '''expr : expr TIMES expr
            | expr DIV expr'''

    p[0] = getTemporal()

    if p[2] == '*' :
       print(p[0] + ' = ' + p[1] + ' * ' + p[3] + ';')
    else :
        if p[3] == 0 :
            print("Can't divide by 0")
            raise ZeroDivisionError('integer division by 0')
        print(p[0] + ' = ' + p[1] + ' / ' + p[3] + ';')

def p_expr2NUM( p ) :
    'expr : NUMBER'
    p[0] = str(p[1])

def p_parens( p ) :
    'expr : LPAREN expr RPAREN'
    p[0] = str(p[2])

def p_error( p ):
    print("Syntax error in input!")

import ply.yacc as yacc
parser = yacc.yacc()

res = parser.parse("5*9+10-(4/2*3)") # the input