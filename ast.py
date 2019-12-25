class Ln:
    def __init__(self, linespan):
        self.start, self.end = linespan
    def __repr__(self):
        return "%d-%d" % (self.start, self.end)

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
    def __init__(self, type, pl, lineno):
        self.type = type
        self.pl = pl
        self.lineno = lineno

    def __repr__(self):
        return '%s:VDEF("%s", %s)' % (self.lineno, self.type, self.pl)


# Function DEFine
# type : return type
# name : function name
# arg : argument (type_name, vdefid) pair
# body : statements
class FDEF(AST):
    def __init__(self, type, name, arg, body, lineno):
        self.type = type
        self.name = name
        self.arg = arg
        self.body = body
        self.lineno = lineno
        self.func_type = None  # type annotation added by AST_TYPE

    def __repr__(self):
        return '%s:FDEF("%s", %s, %s, %s)' % (self.lineno, self.type, self.name, self.arg, self.body)


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
    def __init__(self, defvs, stmts, lineno):
        self.defvs = defvs
        self.stmts = stmts
        self.lineno = lineno

    def __repr__(self):
        return '%s:BODY(%s, %s)' % (self.lineno, self.defvs, self.stmts)


# EMPTY STateMenT
class EMPTY_STMT(STMT):
    def __init__(self, lineno):
        self.lineno = lineno

    def __repr__(self):
        return '%s:EMPTY_STMT()' % self.lineno


# EXPRessions MANY
# exprs: expr*
class EXPR_MANY(STMT, EXPR):
    def __init__(self, exprs):
        self.exprs = exprs
        self.lineno = Ln((self.exprs[0].lineno.start, self.exprs[-1].lineno.end))

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
    def __init__(self, cond, body, lineno):
        self.cond = cond
        self.body = body
        self.lineno = lineno

    def __repr__(self):
        return '%s:WHILE(%s, %s)' % (self.lineno, self.cond, self.body)


# FOR loop
# init: initialization expr
# cond: conditional expr
# update: update exopr
# body: body of for loop
class FOR(STMT):
    def __init__(self, init, cond, update, body, lineno):
        self.init = init
        self.cond = cond
        self.update = update
        self.body = body
        self.lineno = lineno

    def __repr__(self):
        return '%s:FOR(%s, %s, %s, %s)' % (self.lineno, self.init, self.cond, self.update, self.body)


# IF-ELSE statement
# cond: conditional expr
# if_stmt: statement taken if true
# else_stmt: statement taken if false (None if ELSE nonexistent)
class IFELSE(STMT):
    def __init__(self, cond, if_stmt, else_stmt, lineno):
        self.cond = cond
        self.if_stmt = if_stmt
        self.else_stmt = else_stmt
        self.lineno = lineno

    def __repr__(self):
        return '%s:IFELSE(%s, %s, %s)' % (self.lineno, self.cond, self.if_stmt, self.else_stmt)


# CONTINUE statement
class CONTINUE(STMT):
    def __init__(self, lineno):
        self.lineno = lineno

    def __repr__(self):
        return '%s:CONTINUE()' % (self.lineno)


# BREAK statement
class BREAK(STMT):
    def __init__(self, lineno):
        self.lineno = lineno

    def __repr__(self):
        return '%s:BREAK()' % (self.lineno)


# RETURN statement
# expr: return value (None if return void)
class RETURN(STMT):
    def __init__(self, lineno, expr=None):
        self.lineno = lineno
        self.expr = expr

    def __repr__(self):
        return '%s:RETURN(%s)' % (self.lineno, self.expr)


# Varible DEFinition ID (id_adv [+ array])
# name : variable name
# ptr_cnt : number of '*'s, int
# array_sz : array size, int >= 0. None for non-array variable
class VDEFID(AST):
    def __init__(self, name, ptr_cnt, array_sz, lineno):
        self.name = name
        self.ptr_cnt = ptr_cnt
        self.array_sz = array_sz
        self.lineno = lineno
        self.var_type = None  # type annotated added by VDEF_RESOLVE

    def __repr__(self):
        return '%s:VDEFID("%s", %d, %s)' % (self.lineno, self.name, self.ptr_cnt, self.array_sz)


class ID(EXPR):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno

    def __repr__(self):
        return '%s:ID("%s")' % (self.lineno, self.name)


class SUBSCR(EXPR):
    def __init__(self, arrexpr, idxexpr, lineno):
        self.arrexpr = arrexpr
        self.idxexpr = idxexpr
        self.lineno = lineno

    def __repr__(self):
        return '%s:SUBSCR(%s, %s)' % (self.lineno, self.arrexpr, self.idxexpr)


class CALL(EXPR):
    def __init__(self, funcexpr, argexprs, lineno):
        self.funcexpr = funcexpr
        self.argexprs = argexprs
        self.lineno = lineno

    def __repr__(self):
        return '%s:CALL(%s, %s)' % (self.lineno, self.funcexpr, self.argexprs)


# Unary postfix operator
class POSTOP(EXPR):
    def __init__(self, expr, op, lineno):
        self.expr = expr
        self.op = op
        self.lineno = lineno

    def __repr__(self):
        return '%s:POSTOP(%s, "%s")' % (self.lineno, self.expr, self.op)


class ADDR(EXPR):
    def __init__(self, expr, lineno):
        self.expr = expr
        self.lineno = lineno

    def __repr__(self):
        return '%s:ADDR(%s)' % (self.lineno, self.expr)


class DEREF(EXPR):
    def __init__(self, expr, lineno):
        self.expr = expr
        self.lineno = lineno

    def __repr__(self):
        return '%s:DEREF(%s)' % (self.lineno, self.expr)


# Unary prefix operators
class PREOP(EXPR):
    def __init__(self, op, expr, lineno):
        self.op = op
        self.expr = expr
        self.lineno = lineno

    def __repr__(self):
        return '%s:PREOP("%s", %s)' % (self.lineno, self.op, self.expr)


class BINOP(EXPR):
    def __init__(self, lhs, op, rhs, lineno):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
        self.lineno = lineno

    def __repr__(self):
        return '%s:BINOP(%s, "%s", %s)' % (self.lineno, self.lhs, self.op, self.rhs)


class ASSIGN(EXPR):
    def __init__(self, lhs, rhs, lineno):
        self.lhs = lhs
        self.rhs = rhs
        self.lineno = lineno

    def __repr__(self):
        return '%s:ASSIGN(%s, %s)' % (self.lineno, self.lhs, self.rhs)


# CONSTant values
# val: value, string
class CONST(EXPR):
    def __init__(self, val, lineno):
        self.val = val
        self.lineno = lineno


# Integer VALue
class IVAL(CONST):
    def __repr__(self):
        return '%s:IVAL("%s")' % (self.lineno, self.val)


# Float VALue
class FVAL(CONST):
    def __repr__(self):
        return '%s:FVAL("%s")' % (self.lineno, self.val)


# String VALue
class SVAL(CONST):
    def __repr__(self):
        return '%s:SVAL("%s")' % (self.lineno, self.val)


# Char VALue
class CVAL(CONST):
    def __repr__(self):
        return '%s:CVAL("%s")' % (self.lineno, self.val)
