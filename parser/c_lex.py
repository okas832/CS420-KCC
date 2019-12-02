# Almost referenced ANSI C grammar
# Removed some code generation related reserved word

import ply.lex as lex

tokens = [
    'ID',
    'IVAL',
    'FVAL',
    'SVAL',
    'CVAL',

    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'AND',
    'OR',
    'NOT',
    'XOR',
    'LSHIFT',
    'RSHIFT',
    'LOR',
    'LAND',
    'LNOT',
    'LE',
    'LEQ',
    'GE',
    'GEQ',
    'EQ',
    'NE',

    'ASSIGN',
    'PLUS_ASSIGN',
    'MINUS_ASSIGN',
    'TIMES_ASSIGN',
    'DIVIDE_ASSIGN',
    'MOD_ASSIGN',
    'AND_ASSIGN',
    'OR_ASSIGN',
    'XOR_ASSIGN',
    'LSHIFT_ASSIGN',
    'RSHIFT_ASSIGN',

    'INC',
    'DEC',

    'TENARY',

    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'PERIOD',
    'SEMICOL',
    'COLON',

    'NEWLINE'
]

reserved = {
    'break'    : 'BREAK',
    'case'     : 'CASE',
    'char'     : 'CHAR',
    'const'    : 'CONST',
    'continue' : 'CONTINUE',
    'do'       : 'DO',
    'else'     : 'ELSE',
    'float'    : 'FLOAT',
    'for'      : 'FOR',
    'goto'     : 'GOTO',
    'if'       : 'IF',
    'int'      : 'INT',
    'return'   : 'RETURN',
    'switch'   : 'SWITCH',
    'unsigned' : 'UNSIGNED',
    'void'     : 'VOID',
    'while'    : 'WHILE'
}

tokens += reserved.values()

t_ignore = ' \t\x0c'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

t_IVAL = r'(0x[0-9a-fA-F]*|\d+)([uU]|[lL]|[uU][lL]|[lL][uU])?'
t_FVAL = r'((\d+)(\.\d+)(e(\+|-)?(\d+))?|(\d+)e(\+|-)?(\d+))([lL]|[fF])?'
t_SVAL = r'\"([^\\\n]|(\\.))*?\"'
t_CVAL = r'(L)?\'([^\\\n]|(\\.))*?\''

t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_MOD    = r'%'
t_AND    = r'&'
t_OR     = r'\|'
t_NOT    = r'~'
t_XOR    = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LOR    = r'\|\|'
t_LAND   = r'&&'
t_LNOT   = r'!'
t_LE     = r'<'
t_GE     = r'>'
t_LEQ    = r'<='
t_GEQ    = r'>='
t_EQ     = r'=='
t_NE     = r'!='

t_ASSIGN        = r'='
t_PLUS_ASSIGN   = r'\+='
t_MINUS_ASSIGN  = r'-='
t_TIMES_ASSIGN  = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MOD_ASSIGN    = r'%='
t_AND_ASSIGN    = r'^='
t_OR_ASSIGN     = r'\|='
t_XOR_ASSIGN    = r'\^='
t_LSHIFT_ASSIGN = r'<<='
t_RSHIFT_ASSIGN = r'>>='

t_INC = r'\+\+'
t_DEC = r'--'

t_TENARY = r'\?'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACK  = r'\['
t_RBRACK  = r'\]'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_COMMA   = r','
t_PERIOD  = r'\.'
t_SEMICOL = r';'
t_COLON   = r':'

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved.get(t.value, "ID")
    return t

def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__":

    with open("input.c", "r") as f:
        lexer.input(f.read())

    while True:
        token = lexer.token()
        if not token: break
        print(token)




