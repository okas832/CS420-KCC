import c_lex
import ply.yacc as yacc
from ast import *

tokens = c_lex.tokens


#  goal : def def ... def
def p_goal_1(p):
    "goal : def"
    p[0] = GOAL([p[1]])

def p_goal_2(p):
    "goal : def goal"
    p[0] = GOAL([p[1]]) + p[2]


# type id [=value] *[,id[=value]];;

def p_def_1(p):
    "def : type def_many"
    p[0] = VDEF(p[1], p[2])

def p_def_many_1(p):
    "def_many : ID SEMICOL"
    p[0] = [(p[1], None)]

def p_def_many_2(p):
    "def_many : ID assign SEMICOL"
    p[0] = [(p[1], p[2])]

def p_def_many_3(p):
    "def_many : ID COMMA def_many"
    p[0] = [(p[1], None)] + p[3]

def p_def_many_4(p):
    "def_many : ID assign COMMA def_many"
    p[0] = [(p[1], p[2])] + p[4]


# type id([arg] *[,arg]){*[expr]}

def p_def_2(p):
    "def : type ID LPAREN s_args RPAREN LBRACE body RBRACE"
    p[0] = FDEF(p[1], p[2], p[4], p[7])


# for special case(no argument)
def p_s_args_1(p):
    "s_args : empty"
    p[0] = []

def p_s_args_2(p):
    "s_args : args"
    p[0] = p[1]

# last argument
def p_args_2(p):
    "args : arg"
    p[0] = [p[1]]

# arg, args
def p_args_3(p):
    "args : arg COMMA args"
    p[0] = [p[1]] + p[3]

def p_arg(p):
    "arg : type ID"
    p[0] = (p[1], p[2])


# body : *[stmt]
def p_body_1(p):
    "body : pre_stmt_many"
    p[0] = p[1]

def p_pre_stmt_many_1(p):
    "pre_stmt_many : empty"
    p[0] = []

def p_pre_stmt_many_2(p):
    "pre_stmt_many : stmt_many"
    p[0] = p[1]

def p_stmt_many_1(p):
    "stmt_many : stmt"
    p[0] = [p[1]]

def p_stmt_many_2(p):
    "stmt_many : stmt stmt_many"
    p[0] = [p[1]] + p[2]


def p_stmt_1(p):
    "stmt : LBRACE body RBRACE"
    pass

# EXPR
def p_stmt_2(p):
    "stmt : expr SEMICOL"
    pass

# WHILE
def p_stmt_3(p):
    "stmt : WHILE LPAREN expr RPAREN stmt"
    pass

# FOR
def p_stmt_4(p):
    "stmt : FOR LPAREN expr SEMICOL expr SEMICOL expr RPAREN stmt"
    pass

# COND, IF
def p_stmt_5(p):
    "stmt : IF LPAREN expr RPAREN stmt"
    pass

# COND, IF - ELSE
def p_stmt_6(p):
    "stmt : IF LPAREN expr RPAREN stmt ELSE stmt"
    pass



def p_assign_1(p):
    "assign : ASSIGN const"
    p[0] = p[2]

def p_assign_2(p):
    "assign : ASSIGN ID"
    p[0] = p[2]

def p_type(p):
    """type : INT
            | FLOAT
            | VOID"""
    p[0] = p[1]

def p_const(p):
    """const : IVAL
             | FVAL
             | SVAL
             | CVAL"""
    p[0] = p[1]

def p_empty(p):
    """empty :"""
    pass

yacc.yacc()
if __name__ == "__main__":
    with open("input.c", "r") as f:
        result = yacc.parse(f.read(), tracking = True)
    print(result)






