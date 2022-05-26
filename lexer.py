# type: ignore
from sly import Lexer

class Lex(Lexer):
    reserved_words = {FSTART, FSTOP}
    tokens = {
        STRING,
        OUT,
        NUMBER,
        BOOL,
        VAR,
        IF,
        ENDIF,
        FUNC,
        ENDFUNC,
        RETURN,
        EQ,
        NEQ,
        FOR,
        ENDFOR,
        TO,
        IN,
        FOUT,
        FIN
    }
    literals = {';', '=', '+', '-', '/', '*', '(', ')', '>', '<', ':', ','}

    ignore = '\t '

    STRING = r'\".*?\"'
    OUT = r'\bout\b'
    IN = r'\bin\b'
    FIN = r'\bfin\b'
    FOUT = r'\bfout\b'
    BOOL = r'\btrue\b|\bfalse\b'
    IF = r'\bif\b'
    ENDIF = r'\bendif\b'
    FUNC = r'\bfunc\b'
    ENDFUNC = r'\bendfunc\b'
    RETURN = r'\breturn\b'
    EQ = r'(?<!=)==(?!=)'
    NEQ = r'!=(?!=)'
    FOR = r'\bfor\b'
    ENDFOR = r'\bendfor\b'
    TO = r'\bto\b'

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def VAR(self, t):
        if t.value.upper() in self.reserved_words:
            pass
        else:
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
        