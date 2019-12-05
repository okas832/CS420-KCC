class AST():
    pass


# goal : [def, def, ... , def]
class GOAL(AST):
    def __init__(self, defs):
        self.defs = defs

    def __add__(self, rhs):
        if not isinstance(rhs, GOAL):
            raise TypeError('Expected GOAL, but %s comes.' % (type(rhs)))
        return GOAL(self.defs + rhs.defs)

    def __repr__(self):
        return 'GOAL(%s)' % (str(self.defs))


# Variable DEFine
# type : define type
# pl : pair list (name, value)
#      value is None if not exist
class VDEF(AST):
    def __init__(self, type, pl):
        self.type = type
        self.pl = pl

    def __repr__(self):
        return 'VDEF(%s, %s)' % (self.type, str(self.pl))


# Function DEFine
# type : return type
# name : function name
# arg : argument (name, type) pair
# body : statements
class FDEF(AST):
    def __init__(self, type, name, arg, body):
        self.type = type
        self.name = name
        self.arg = arg
        self.body = body

    def __repr__(self):
        return 'FDEF(%s, %s, %s, %s)' % (self.type, self.name, self.arg, str(self.body))


# EXPRession
# ast : ast of expression
class EXPR(AST):
    def __init__(self, ast):
        self.ast = ast
    
    def __repr__(self):
        return 'EXPR(%s)' % (str(self.ast))


# STateMenT
class STMT(AST):
    pass


# BODY
# defvs: defv*
# stmts: stmt*
class BODY(STMT):
    def __init__(self, defvs, stmts):
        self.defvs = defvs
        self.stmts = stmts
    
    def __repr__(self):
        return 'BODY(%s, %s)' % (str(self.defvs), str(self.stmts))


# EMPTY STateMenT
class EMPTY_STMT(STMT):
    def __init__(self):
        pass

    def __repr__(self):
        return 'EMPTY_STMT()'


# EXPRessions MANY
# exprs: expr*
class EXPR_MANY(STMT):
    def __init__(self, exprs):
        self.exprs = exprs
    
    def __add__(self, rhs):
        if not isinstance(rhs, EXPR_MANY):
            raise TypeError('Expected EXPR_MANY, but %s comes.' % (type(rhs)))
        return EXPR_MANY(self.exprs + rhs.exprs)
    
    def __repr__(self):
        return 'EXPR_MANY(%s)' % (str(self.exprs))


# WHILE loop
# cond: conditional
# body: body of while loop
class WHILE(STMT):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    
    def __repr__(self):
        return 'WHILE(%s, %s)' % (str(self.cond), str(self.body))


# FOR loop
# init: initialization expr
# cond: conditional expr
# update: update exopr
# body: body of for loop
class FOR(STMT):
    def __init__(self, init, cond, update, body):
        self.init = init
        self.cond = cond
        self.update = update
        self.body = body
    
    def __repr__(self):
        return 'FOR(%s, %s, %s, %s)' % (str(self.init), str(self.cond), str(self.update), str(self.body))


# IF-ELSE statement
# cond: conditional expr
# if_stmt: statement taken if true
# else_stmt: statement taken if false (None if ELSE nonexistent)
class IFELSE(STMT):
    def __init__(self, cond, if_stmt, else_stmt):
        self.cond = cond
        self.if_stmt = if_stmt
        self.else_stmt = else_stmt
    
    def __repr__(self):
        return 'IFELSE(%s, %s, %s)' % (str(self.cond), str(self.if_stmt), str(self.else_stmt))


# ID VARiable (id_adv [+ array])
# name : variable name
# ptr_cnt : number of '*'s, int
# array_sz : array size, IVAL. None for non-array variable
class IDVAR(AST):
    def __init__(self, name, ptr_cnt, array_sz):
        self.name = name
        self.ptr_cnt = ptr_cnt
        self.array_sz = array_sz  # None for non-array
    
    def __repr__(self):
        return 'LVALUE(%s, %d, %s)' % (self.name, self.ptr_cnt, str(self.array_sz))


# CONSTant values
# val: value, string
class CONST(AST):
    def __init__(self, val):
        self.val = val


# Integer VALue
class IVAL(CONST):
    def __repr__(self):
        return 'IVAL(%s)' % self.val


# Float VALue
class FVAL(CONST):
    def __repr__(self):
        return 'FVAL(%s)' % self.val


# String VALue
class SVAL(CONST):
    def __repr__(self):
        return 'SVAL(%s)' % self.val


# Char VALue
class CVAL(CONST):
    def __repr__(self):
        return 'CVAL(%s)' % self.val