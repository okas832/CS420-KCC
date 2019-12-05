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


def p_def(p):
    """def : defv
           | deff"""
    p[0] = p[1]


# type id [=value] *[,id[=value]];
def p_defv_1(p):
    """defv : type defv_multi SEMICOL"""
    p[0] = VDEF(p[1], p[2])


def p_defv_multi_1(p):
    """defv_multi : id_adv array"""
    p[1].array_sz = p[2]
    p[0] = [(p[1], None)]


def p_defv_multi_2(p):
    """defv_multi : id_adv assign"""
    p[0] = [(p[1], p[2])]


def p_defv_multi_3(p):
    """defv_multi : id_adv array COMMA defv_multi"""
    p[1].array_sz = p[2]
    p[0] = [(p[1], None)] + p[4]


def p_defv_multi_4(p):
    """defv_multi : id_adv assign COMMA defv_multi"""
    p[0] = [(p[1], p[2])] + p[4]


def p_id_adv_1(p):
    """id_adv : ID"""
    p[0] = IDVAR(p[1], 0, None)


def p_id_adv_2(p):
    """id_adv : TIMES id_adv"""
    p[2].ptr_cnt += 1
    p[0] = p[2]


def p_array_1(p):
    """array : empty"""
    p[0] = None


def p_array_2(p):
    """array : LBRACK IVAL RBRACK"""
    p[0] = IVAL(p[2])


# type id([arg] *[,arg]){*[expr]}
def p_deff(p):
    """deff : type ID LPAREN s_args RPAREN LBRACE body RBRACE"""
    p[0] = FDEF(p[1], p[2], p[4], p[7])


# for special case(no argument)
def p_s_args_1(p):
    """s_args : empty
              | VOID"""
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
    """arg : type id_adv"""
    p[0] = (p[1], p[2])


# body : *[defv] *[stmt]
def p_body_1(p):
    """body : pre_defv_many pre_stmt_many"""
    p[0] = BODY(p[1], p[2])


def p_pre_defv_many_1(p):
    """pre_defv_many : empty"""
    p[0] = []


def p_pre_defv_many_2(p):
    """pre_defv_many : defv_many"""
    p[0] = p[1]


def p_defv_many_1(p):
    """defv_many : defv"""
    p[0] = [p[1]]


def p_defv_many_2(p):
    """defv_many : defv defv_many"""
    p[0] = [p[1]] + p[2]


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
    p[0] = EMPTY_STMT()


def p_stmt_2(p):
    """stmt : LBRACE body RBRACE"""
    p[0] = p[2]


# EXPR_MANY
def p_stmt_3(p):
    """stmt : expr_many SEMICOL"""
    p[0] = p[1]


# WHILE
def p_stmt_4(p):
    """stmt : WHILE LPAREN expr_many RPAREN stmt"""
    p[0] = WHILE(p[3], p[5])


# FOR
def p_stmt_5(p):
    """stmt : FOR LPAREN expr_many SEMICOL expr_many SEMICOL expr_many RPAREN stmt"""
    p[0] = FOR(p[3], p[5], p[7], p[9])


# COND, IF
def p_stmt_6(p):
    """stmt : IF LPAREN expr_many RPAREN stmt"""
    p[0] = IFELSE(p[3], p[5], None)


# COND, IF - ELSE
def p_stmt_7(p):
    """stmt : IF LPAREN expr_many RPAREN stmt ELSE stmt"""
    p[0] = IFELSE(p[3], p[5], p[7])


# primary expression
def p_priexpr_1(p):
    """priexpr : ID"""
    p[0] = ID(p[1])


def p_priexpr_2(p):
    """priexpr : const"""
    p[0] = p[1]


def p_priexpr_3(p):
    """priexpr : LPAREN expr_many RPAREN"""
    p[0] = p[2]


# postfix expression
def p_postexpr_1(p):
    """postexpr : priexpr"""
    p[0] = p[1]


# array indexing
def p_postexpr_2(p):
    """postexpr : postexpr LBRACK expr_many RBRACK"""
    p[0] = SUBSCR(p[1], p[3])


# function call with void parameter
def p_postexpr_3(p):
    """postexpr : postexpr LPAREN RPAREN"""
    p[0] = CALL(p[1], [])


# function call with parameters
def p_postexpr_4(p):
    """postexpr : postexpr LPAREN argexpr_list RPAREN"""
    p[0] = CALL(p[1], p[3])


def p_postexpr_5(p):
    """postexpr : postexpr INC"""
    p[0] = POST_INC(p[1])


def p_postexpr_6(p):
    """postexpr : postexpr DEC"""
    p[0] = POST_DEC(p[1])


def p_argexpr_list_1(p):
    """argexpr_list : expr"""
    p[0] = [p[1]]


def p_argexpr_list_2(p):
    """argexpr_list : argexpr_list COMMA expr"""
    p[0] = p[1] + [p[3]]


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
    p[0] = EXPR_MANY([p[1]])


def p_expr_many_2(p):
    """expr_many : expr_many COMMA expr"""
    p[0] = p[1] + EXPR_MANY([p[3]])


def p_assign_1(p):
    "assign : ASSIGN expr"
    p[0] = p[2]


def p_type(p):
    """type : INT
            | FLOAT
            | CHAR
            | VOID"""
    p[0] = p[1]


def p_const_1(p):
    """const : IVAL"""
    p[0] = IVAL(p[1])


def p_const_2(p):
    """const : FVAL"""
    p[0] = FVAL(p[1])


def p_const_3(p):
    """const : SVAL"""
    p[0] = SVAL(p[1])


def p_const_4(p):
    """const : CVAL"""
    p[0] = CVAL(p[1])


def p_empty(p):
    """empty :"""
    pass


yacc.yacc()
if __name__ == "__main__":
    with open("input.c", "r") as f:
        result = yacc.parse(f.read(), tracking=True)
    print(result)






