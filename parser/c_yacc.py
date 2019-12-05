import c_lex
import ply.yacc as yacc
from ast import *

tokens = c_lex.tokens


#  goal : def def ... def
def p_goal_1(p):
    """goal : def"""
    p[0] = GOAL([p[1]])


def p_goal_2(p):
    """goal : def goal"""
    p[0] = GOAL([p[1]]) + p[2]


def p_def_1(p):
    """def : defv SEMICOL"""
    p[0] = p[1]


def p_def_2(p):
    """def : deff"""
    p[0] = p[1]


# type id [=value] *[,id[=value]];;
def p_defv_1(p):
    """defv : type defv_many"""
    p[0] = VDEF(p[1], p[2])


def p_defv_many_1(p):
    """defv_many : id_adv array"""
    p[0] = [(p[1], None)]


def p_defv_many_2(p):
    """defv_many : id_adv assign"""
    p[0] = [(p[1], p[2])]


def p_defv_many_3(p):
    """defv_many : id_adv array COMMA defv_many"""
    p[0] = [(p[1], None)] + p[4]


def p_defv_many_4(p):
    """defv_many : id_adv assign COMMA defv_many"""
    p[0] = [(p[1], p[2])] + p[4]


def p_id_adv_1(p):
    """id_adv : ID"""
    p[0] = p[1]


def p_id_adv_2(p):
    """id_adv : TIMES id_adv"""
    p[0] = p[2]


def p_array_1(p):
    """array : empty"""
    pass


def p_array_2(p):
    """array : LBRACK IVAL RBRACK"""
    pass


# type id([arg] *[,arg]){*[expr]}
def p_deff(p):
    """deff : type ID LPAREN s_args RPAREN LBRACE body RBRACE"""
    p[0] = FDEF(p[1], p[2], p[4], p[7])


# for special case(no argument)
def p_s_args_1(p):
    """s_args : empty"""
    p[0] = []


def p_s_args_2(p):
    """s_args : args"""
    p[0] = p[1]


# last argument
def p_args_2(p):
    """args : arg"""
    p[0] = [p[1]]


# arg, args
def p_args_3(p):
    """args : arg COMMA args"""
    p[0] = [p[1]] + p[3]


def p_arg(p):
    """arg : type ID"""
    p[0] = (p[1], p[2])


# body : *[stmt]
def p_body_1(p):
    """body : pre_stmt_many"""
    p[0] = p[1]


def p_pre_stmt_many_1(p):
    """pre_stmt_many : empty"""
    p[0] = []


def p_pre_stmt_many_2(p):
    """pre_stmt_many : stmt_many"""
    p[0] = p[1]


def p_stmt_many_1(p):
    """stmt_many : stmt"""
    p[0] = [p[1]]


def p_stmt_many_2(p):
    """stmt_many : stmt stmt_many"""
    p[0] = [p[1]] + p[2]


def p_stmt_1(p):
    """stmt : SEMICOL"""
    pass


def p_stmt_2(p):
    """stmt : LBRACE body RBRACE"""
    pass


# EXPR
def p_stmt_3(p):
    """stmt : expr_many SEMICOL"""
    pass


# WHILE
def p_stmt_4(p):
    """stmt : WHILE LPAREN expr_many RPAREN stmt"""
    pass


# FOR
def p_stmt_5(p):
    """stmt : FOR LPAREN expr_many SEMICOL expr_many SEMICOL expr_many RPAREN stmt"""
    pass


# COND, IF
def p_stmt_6(p):
    """stmt : IF LPAREN expr_many RPAREN stmt"""
    pass


# COND, IF - ELSE
def p_stmt_7(p):
    """stmt : IF LPAREN expr_many RPAREN stmt ELSE stmt"""
    pass


# primary expression
def p_priexpr_1(p):
    """priexpr : ID
                | const"""
    pass


def p_priexpr_2(p):
    """priexpr : LPAREN expr_many RPAREN"""
    pass


# postfix expression
def p_postexpr_1(p):
    """postexpr : priexpr"""
    pass


# array indexing
def p_postexpr_2(p):
    """postexpr : postexpr LBRACK expr_many RBRACK"""
    pass


# function call with void parameter
def p_postexpr_3(p):
    """postexpr : postexpr LPAREN RPAREN"""
    pass


# function call with parameters
def p_postexpr_4(p):
    """postexpr : postexpr LPAREN argexpr_list RPAREN"""
    pass


def p_postexpr_5(p):
    """postexpr : postexpr INC
                | postexpr DEC"""
    pass


def p_argexpr_list_1(p):
    """argexpr_list : expr"""
    pass


def p_argexpr_list_2(p):
    """argexpr_list : argexpr_list COMMA expr"""
    pass


# unary expression
def p_unaryexpr_1(p):
    """unaryexpr : postexpr"""
    pass


def p_unaryexpr_2(p):
    """unaryexpr : INC unaryexpr
                 | DEC unaryexpr
                 | AND unaryexpr
                 | TIMES unaryexpr
                 | PLUS unaryexpr
                 | MINUS unaryexpr
                 | NOT unaryexpr
                 | LNOT unaryexpr"""
    pass


# multiplicative_expression
def p_multexpr_1(p):
    """multexpr : unaryexpr"""
    pass


def p_multexpr_2(p):
    """multexpr : multexpr TIMES unaryexpr
                | multexpr DIVIDE unaryexpr
                | multexpr MOD unaryexpr"""
    pass


# additive_expression
def p_addexpr_1(p):
    """addexpr : multexpr"""
    pass


def p_addexpr_2(p):
    """addexpr : addexpr PLUS multexpr
               | addexpr MINUS multexpr"""
    pass


# shift_expression
def p_shiftexpr_1(p):
    """shiftexpr : addexpr"""
    pass


def p_shiftexpr_2(p):
    """shiftexpr : shiftexpr LSHIFT addexpr
                 | shiftexpr RSHIFT addexpr"""
    pass


# relational_expression
def p_relexpr_1(p):
    """relexpr : shiftexpr"""
    pass


def p_relexpr_2(p):
    """relexpr : relexpr LE shiftexpr
               | relexpr GE shiftexpr
               | relexpr LEQ shiftexpr
               | relexpr GEQ shiftexpr"""
    pass


# equality_expression
def p_eqexpr_1(p):
    """eqexpr : relexpr"""
    pass


def p_eqexpr_2(p):
    """eqexpr : eqexpr EQ relexpr
              | eqexpr NE relexpr"""
    pass


# and_expression
def p_andexpr_1(p):
    """andexpr : eqexpr"""
    pass


def p_andexpr_2(p):
    """andexpr : andexpr AND eqexpr"""
    pass


# exclusive_or_expression
def p_xorexpr_1(p):
    """xorexpr : andexpr"""
    pass


def p_xorexpr_2(p):
    """xorexpr : xorexpr XOR andexpr"""
    pass


# inclusive_or_expression
def p_orexpr_1(p):
    """orexpr : xorexpr"""
    pass


def p_orexpr_2(p):
    """orexpr : orexpr OR xorexpr"""
    pass


# logical_and_expression
def p_landexpr_1(p):
    """landexpr : orexpr"""
    pass


def p_landexpr_2(p):
    """landexpr : landexpr LAND orexpr"""
    pass


# logical_or_expression
def p_lorexpr_1(p):
    """lorexpr : landexpr"""
    pass


def p_lorexpr_2(p):
    """lorexpr : lorexpr LOR landexpr"""
    pass


# expression
def p_expr_1(p):
    """expr : lorexpr"""
    pass


def p_expr_2(p):
    """expr : postexpr assign_op expr"""
    # TODO : Handle postexpr as lvalue (ID or ID LBRACK expr_many RBRACK)
    #      : If not, throw exception
    pass


def p_expr_3(p):
    """expr : TIMES unaryexpr assign_op expr"""
    pass


# assignment_operator
def p_assign_op(p):
    """assign_op : ASSIGN
                 | PLUS_ASSIGN
                 | MINUS_ASSIGN
                 | TIMES_ASSIGN
                 | DIVIDE_ASSIGN
                 | MOD_ASSIGN
                 | AND_ASSIGN
                 | OR_ASSIGN
                 | XOR_ASSIGN
                 | LSHIFT_ASSIGN
                 | RSHIFT_ASSIGN"""
    pass


def p_expr_many_1(p):
    """expr_many : expr"""
    pass


def p_expr_many_2(p):
    """expr_many : expr_many COMMA expr"""
    pass


def p_assign_1(p):
    "assign : ASSIGN expr"
    p[0] = p[2]


def p_type(p):
    """type : INT
            | FLOAT
            | CHAR
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
        result = yacc.parse(f.read(), tracking=True)
    print(result)






