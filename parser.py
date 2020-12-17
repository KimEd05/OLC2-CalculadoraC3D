import ply.lex as lex
from lex import *

lexer = lex.lex()

class Nodo():
    def __init__(self, addr = '', code = ''):
        self.addr = addr
        self.code = code

    def getAddr(self):
        return self.addr

    def getCode(self):
        return self.code

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
    p[0] = Nodo(addr = getTemporal())
    p[0].code = p[1].code + p[3].code + p[0].addr + ' = ' + p[1].addr + ' + ' + p[3].addr + ';\n'

def p_sub( p ) :
    'expr : expr MINUS expr'
    p[0] = Nodo(addr = getTemporal())
    p[0].code = p[1].code + p[3].code + p[0].addr + ' = ' + p[1].addr + ' - ' + p[3].addr + ';\n'

def p_expr2uminus( p ) :
    'expr : MINUS expr %prec UMINUS'
    p[0] = Nodo(addr = getTemporal())
    p[0].code = p[2].code + p[0].addr + ' = -' + p[2].addr + ';\n'

def p_mult_div( p ) :
    '''expr : expr TIMES expr
            | expr DIV expr'''

    p[0] = Nodo(addr = getTemporal())

    if p[2] == '*' :
       p[0].code = p[1].code + p[3].code + p[0].addr + ' = ' + p[1].addr + ' * ' + p[3].addr + ';\n'
    else :
        if p[3].addr == 0 :
            print("Can't divide by 0")
            raise ZeroDivisionError('integer division by 0')
        p[0].code = p[1].code + p[3].code + p[0].addr + ' = ' + p[1].addr + ' / ' + p[3].addr + ';\n'

def p_expr2NUM( p ) :
    'expr : NUMBER'
    p[0] = Nodo(addr = str(p[1]))

def p_parens( p ) :
    'expr : LPAREN expr RPAREN'
    p[0] = Nodo(p[2].addr, p[2].code)

def p_error( p ):
    print("Syntax error in input!")

import ply.yacc as yacc
parser = yacc.yacc()

res = parser.parse("5*9+10-(4/2*3)") # the input
print(res.code)