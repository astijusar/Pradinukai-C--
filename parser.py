# type: ignore
from sly import Parser
from lexer import Lex

class Parser(Parser):
    debugfile = 'parser.out'

    tokens = Lex.tokens

    precedence = (
        ('nonassoc', '>', '<'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = { }
  
    @_('')
    def statement(self, p):
        pass

    @_('out')
    def statement(self, p):
        return (p.out)

    @_('ifstmt')
    def statement(self, p):
        return (p.ifstmt)

    @_('ENDIF')
    def statement(self, p):
        return(p.ENDIF)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign
  
    @_('VAR "=" expr ";"')
    def var_assign(self, p):
        return ('var_assign', p.VAR, p.expr)
  
    @_('VAR "=" STRING ";"')
    def var_assign(self, p):
        return ('var_assign', p.VAR, p.STRING)

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)
  
    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)
  
    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('expr ">" expr')
    def expr(self, p):
        return ('greater', p.expr0, p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
        return ('less', p.expr0, p.expr1)
  
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return (p.expr[0], -p.expr[1])

    @_('OUT "(" expr ")" ";"')
    def out(self, p):
        return('out', p.expr)

    @_('IF "(" expr ")" ":"')
    def ifstmt(self, p):
        return('ifstmt', p.expr)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('STRING')
    def expr(self, p):
        return ('str', p.STRING)

    @_('BOOL')
    def expr(self, p):
        return ('bool', p.BOOL)

    @_('VAR')
    def expr(self, p):
        return ('var', p.VAR)