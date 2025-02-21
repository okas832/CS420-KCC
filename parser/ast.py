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
        return 'VDEF("%s", %s)' % (self.type, self.pl)


# Function DEFine
# type : return type
# name : function name
# arg : argument (type_name, vdefid) pair
# body : statements
class FDEF(AST):
    def __init__(self, type, name, arg, body):
        self.type = type
        self.name = name
        self.arg = arg
        self.body = body

    def __repr__(self):
        return 'FDEF("%s", %s, %s, %s)' % (self.type, self.name, self.arg, self.body)


# STateMenT
class STMT(AST):
    pass


# EXPRession
class EXPR(AST):
    def __init__(self, type=None):
        self.type = type  # set at AST_TYPE() -> type_resolve()

    def __add__(self, rhs):
        if not isinstance(rhs, EXPR):
            raise TypeError('Expected EXPR, but %s comes.' % (type(rhs)))
        if isinstance(rhs, EXPR_MANY):
            return EXPR_MANY([self] + rhs.exprs)
        else:
            return EXPR_MANY([self, rhs])


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
        if not isinstance(rhs, EXPR):
            raise TypeError('Expected EXPR, but %s comes.' % (type(rhs)))
        if isinstance(rhs, EXPR_MANY):
            return EXPR_MANY(self.exprs + rhs.exprs)
        else:
            return EXPR_MANY(self.exprs + [rhs])

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


# CONTINUE statement
class CONTINUE(STMT):
    def __init__(self):
        pass

    def __repr__(self):
        return 'CONTINUE()'


# BREAK statement
class BREAK(STMT):
    def __init__(self):
        pass

    def __repr__(self):
        return 'BREAK()'


# RETURN statement
# expr: return value (None if return void)
class RETURN(STMT):
    def __init__(self, expr=None):
        self.expr = expr

    def __repr__(self):
        return 'RETURN(%s)' % self.expr


# Varible DEFinition ID (id_adv [+ array])
# name : variable name
# ptr_cnt : number of '*'s, int
# array_sz : array size, int >= 0. None for non-array variable
class VDEFID(AST):
    def __init__(self, name, ptr_cnt, array_sz):
        self.name = name
        self.ptr_cnt = ptr_cnt
        self.array_sz = array_sz

    def __repr__(self):
        return 'VDEFID("%s", %d, %s)' % (self.name, self.ptr_cnt, self.array_sz)


class ID(EXPR):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'ID("%s")' % self.name


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


# Unary postfix operator
class POSTOP(EXPR):
    def __init__(self, expr, op):
        self.expr = expr
        self.op = op

    def __repr__(self):
        return 'POSTOP(%s, "%s")' % (self.expr, self.op)


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


# Unary prefix operators
class PREOP(EXPR):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return 'PREOP("%s", %s)' % (self.op, self.expr)


class BINOP(EXPR):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __repr__(self):
        return 'BINOP(%s, "%s", %s)' % (self.lhs, self.op, self.rhs)


class ASSIGN(EXPR):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return 'ASSIGN(%s, %s)' % (self.lhs, self.rhs)


# CONSTant values
# val: value, string
class CONST(EXPR):
    def __init__(self, val):
        self.val = val


# Integer VALue
class IVAL(CONST):
    def __repr__(self):
        return 'IVAL("%s")' % self.val


# Float VALue
class FVAL(CONST):
    def __repr__(self):
        return 'FVAL("%s")' % self.val


# String VALue
class SVAL(CONST):
    def __repr__(self):
        return 'SVAL("%s")' % self.val


# Char VALue
class CVAL(CONST):
    def __repr__(self):
        return 'CVAL("%s")' % self.val
