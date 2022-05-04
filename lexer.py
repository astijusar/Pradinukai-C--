# type: ignore
from sly import Lexer

class Lex(Lexer):
    reserved_words = {}
    tokens = {
        STRING,
        OUT,
        NUMBER,
        BOOL,
        VAR,
        IF,
        ENDIF
    }
    literals = {';', '=', '+', '-', '/', '*', '(', ')', '>', '<', ':'}

    ignore = '\t '

    STRING = r'\".*?\"'
    OUT = r'\bout\b'
    BOOL = r'\btrue\b|\bfalse\b'
    IF = r'\bif\b'
    ENDIF = r'\bendif\b'

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def VAR(self, t):
        if t.value.upper() in self.reserved_words:
            t.type = t.value.upper()
        return t

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'//.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, value):
        print('Line %d: Bad character %r' % (self.lineno, value[0]))
        self.index += 1

if __name__ == '__main__':
    data = 'out "Hello world!" == true;'
    lexer = Lex()
    for tok in lexer.tokenize(data):
        print(tok)