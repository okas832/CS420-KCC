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
        return 'GOAL(%s)' % self.defs


# Variable DEFine
# type : define type
# pl : pair list (name, value)
#      value is None if not exist
class VDEF(AST):
    def __init__(self, type, pl):
        self.type = type
        self.pl = pl

    def __repr__(self):
        return 'VDEF(%s, %s)' % (self.type, self.pl)


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
        return 'FDEF(%s, %s, %s, %s)' % (self.type, self.name, self.arg, self.body)


# STateMenT
class STMT(AST):
    pass


# EXPRession
class EXPR(AST):
    pass


# BODY
# defvs: defv*
# stmts: stmt*
class BODY(STMT):
    def __init__(self, defvs, stmts):
        self.defvs = defvs
        self.stmts = stmts
    
    def __repr__(self):
        return 'BODY(%s, %s)' % (self.defvs, self.stmts)


# EMPTY STateMenT
class EMPTY_STMT(STMT):
    def __init__(self):
        pass

    def __repr__(self):
        return 'EMPTY_STMT()'


# EXPRessions MANY
# exprs: expr*
class EXPR_MANY(STMT, EXPR):
    def __init__(self, exprs):
        self.exprs = exprs
    
    def __add__(self, rhs):
        if not isinstance(rhs, EXPR_MANY):
            raise TypeError('Expected EXPR_MANY, but %s comes.' % (type(rhs)))
        return EXPR_MANY(self.exprs + rhs.exprs)
    
    def __repr__(self):
        return 'EXPR_MANY(%s)' % self.exprs


# WHILE loop
# cond: conditional
# body: body of while loop
class WHILE(STMT):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    
    def __repr__(self):
        return 'WHILE(%s, %s)' % (self.cond, self.body)


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
        return 'FOR(%s, %s, %s, %s)' % (self.init, self.cond, self.update, self.body)


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
        return 'IFELSE(%s, %s, %s)' % (self.cond, self.if_stmt, self.else_stmt)


# Viable DEFinition ID (id_adv [+ array])
# name : variable name
# ptr_cnt : number of '*'s, int
# array_sz : array size, IVAL. None for non-array variable
class VDEFID(AST):
    def __init__(self, name, ptr_cnt, array_sz):
        self.name = name
        self.ptr_cnt = ptr_cnt
        self.array_sz = array_sz  # None for non-array
    
    def __repr__(self):
        return 'LVALUE(%s, %d, %s)' % (self.name, self.ptr_cnt, self.array_sz)


class ID(EXPR):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return 'ID(%s)' % self.name


class SUBSCR(EXPR):
    def __init__(self, arrexpr, idxexpr):
        self.arrexpr = arrexpr
        self.idxexpr = idxexpr
    
    def __repr__(self):
        return 'SUBSCR(%s, %s)' % (self.arrexpr, self.idxexpr)


class CALL(EXPR):
    def __init__(self, funcexpr, argexprs):
        self.funcexpr = funcexpr
        self.argexprs = argexprs
    
    def __repr__(self):
        return 'CALL(%s, %s)' % (self.funcexpr, self.argexprs)


class POST_INC(EXPR):
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return 'POST_INC(%s)' % self.expr


class POST_DEC(EXPR):
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return 'POST_DEC(%s)' % self.expr


class PRE_INC(EXPR):
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return 'PRE_INC(%s)' % self.expr


class PRE_DEC(EXPR):
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return 'PRE_DEC(%s)' % self.expr


class ADDR(EXPR):
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return 'ADDR(%s)' % self.expr


class DEREF(EXPR):
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return 'DEREF(%s)' % self.expr


class UNOP(EXPR):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    
    def __repr__(self):
        return 'UNOP(%s, %s)' % (self.op, self.expr)


class BINOP(EXPR):
    def __init__(self, lexpr, op, rexpr):
        self.lexpr = lexpr
        self.op = op
        self.rexpr = rexpr
    
    def __repr__(self):
        return 'BINOP(%s, %s, %s)' % (self.lexpr, self.op, self.rexpr)


class ASSIGN(EXPR):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
    
    def __repr__(self):
        return 'ASSIGN(%s, %s, %s)' % (self.lhs, self.op, self.rhs)


# CONSTant values
# val: value, string
class CONST(EXPR):
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