# type: ignore
import re
from sly import Parser
from lexer import Lex

class Parser(Parser):
    tokens = Lex.tokens

    precedence = (
        ('nonassoc', '>', '<', 'EQ', 'NEQ', '(', ')'),
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
        return (p.ENDIF)

    @_('ENDFUNC')
    def statement(self, p):
        return (p.ENDFUNC)

    @_('ENDFOR')
    def statement(self, p):
        return (p.ENDFOR)

    @_('ret')
    def statement(self, p):
        return (p.ret)

    @_('function')
    def statement(self, p):
        return (p.function)

    @_('loop')
    def statement(self, p):
        return (p.loop)

    @_('params')
    def statement(self, p):
        return (p.params)

    @_('param')
    def statement(self, p):
        return (p.param)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign
  
    @_('VAR "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.VAR, p.expr)
  
    @_('VAR "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.VAR, p.STRING)

    @_('VAR "=" VAR "(" ")"')
    def function(self, p):
        return ('var_function_decl', p.VAR0, p.VAR1, "")

    @_('VAR "=" VAR "(" params ")"')
    def function(self, p):
        return ('var_function_decl', p.VAR0, p.VAR1, p.params)

    @_('VAR "=" VAR "(" expr ")"')
    def function(self, p):
        return ('var_function_decl', p.VAR0, p.VAR1, p.expr)

    @_('VAR "=" VAR "(" var_assign ")"')
    def function(self, p):
        return ('var_function_decl', p.VAR0, p.VAR1, p.var_assign)

    @_('FOR expr TO expr ":"')
    def loop(self, p):
        return ('loop', p.expr0, p.expr1)

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

    @_('expr EQ expr')
    def expr(self, p):
        return ('equal', p.expr0, p.expr1)

    @_('expr NEQ expr')
    def expr(self, p):
        return ('not_equal', p.expr0, p.expr1)
  
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('OUT "(" expr ")"')
    def out(self, p):
        return ('out', p.expr)

    @_('IF "(" expr ")" ":"')
    def ifstmt(self, p):
        return ('ifstmt', p.expr)

    @_('FUNC VAR "(" ")" ":"')
    def function(self, p):
        return ('function', p.VAR)

    @_('FUNC VAR "(" params ")" ":"')
    def function(self, p):
        return ('function', p.VAR, p.params)

    @_('RETURN VAR')
    def ret(self, p):
        return ('return', p.VAR)

    @_('RETURN')
    def ret(self, p):
        return ('return')

    @_('RETURN expr')
    def ret(self, p):
        return ('return', p.expr)

    @_('params "," param')
    def params(self, p):
        return str(p.params) + ',' + str(p.param)

    @_('param')
    def params(self, p):
        return (p.param)

    @_('VAR')
    def param(self, p):
        return p.VAR

    @_('NUMBER')
    def param(self, p):
        return p.NUMBER

    @_('VAR "(" ")"')
    def function(self, p):
        return ('function_decl', p.VAR)
        
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