from ast import *
from ctype import *


class VALUE():
    def __init__(self, value, ctype):
        assert isinstance(ctype, CType)
        if ctype == TFloat():
            self.value = float(value)
        elif ctype == TInt():
            value = int(value) & 0xFFFFFFFF
            self.value = value if value < 0x80000000 else value - 0x100000000
        elif ctype == TChar():
            value = int(result) & 0xFF
            self.value = value if value < 0x80 else value - 0x100
        else:
            raise ValueError("Not Implemented Type '%s'" % ctype)
        self.ctype = ctype

    def __repr__(self):
        if self.ctype == TVoid():
            return "(void)"
        return "(%s) %d" % (self.ctype, self.value)


class VPTR(VALUE):
    def __init__(self, deref_value):
        self.deref_value = deref_value

    def __repr__(self):
        return "&%s" % self.value


def id_resolve(expr, genv, lenv):
    assert isinstance(expr, ID)

    if expr.name in lenv:
        return lenv[expr.name]

    if expr.name in genv:
        return genv[expr.name]

    raise SyntaxError("'%s' undeclared (first use in this function)" % expr.name)


def define_func(expr):
    assert isinstance(expr, FDEF)


def define_var(expr):
    assert isinstance(expr, VDEFID)


def exec_cast(expr, genv, lenv):
    result = exec_expr(expr.expr, genv, lenv)

    if isinstance(expr, C2I):
        assert result.ctype == TChar()
        return VALUE(result.value, TInt())
    elif isinstance(expr, I2C):
        assert result.ctype == TInt()
        return VALUE(result.value, TChar())
    elif isinstance(expr, I2F):
        assert result.ctype == TInt()
        return VALUE(result.value, TFloat())
    elif isinstance(expr, F2I):
        assert result.ctype == TFloat()
        return VALUE(result.value, TInt())

    raise ValueError("Not Implemented Type Casting: %s" % result.expr)


def exec_binop(expr, genv, lenv):
    assert isinstance(expr, BINOP)

    lhs = exec_expr(expr.lhs)
    rhs = exec_expr(expr.rhs)
    assert lhs.ctype == rhs.ctype
    ctype = lhs.ctype

    if expr.op == "+":
        result = lhs.value + rhs.value
    elif expr.op == "-":
        result = lhs.value - rhs.value
    elif expr.op == "*":
        result = lhs.value * rhs.value
    elif expr.op == "/":
        if ctype == TFloat():
            result = lhs.value / rhs.value
        else:
            result = lhs.value // rhs.value
    elif expr.op == "%":
        result = lhs.value % rhs.value
    elif expr.op == "&":
        result = lhs.value & rhs.value
    elif expr.op == "|":
        result = lhs.value | rhs.value
    elif expr.op == "^":
        result = lhs.value ^ rhs.value
    elif expr.op == "<<":
        result = lhs.value << rhs.value
    elif expr.op == ">>":
        result = lhs.value >> rhs.value
    elif expr.op == "&&":
        result = bool(lhs.value) and bool(rhs.value)
    elif expr.op == "||":
        result = bool(lhs.value) or bool(rhs.value)
    elif expr.op == "==":
        result = lhs.value == rhs.value
    elif expr.op == "!=":
        result = lhs.value != rhs.value
    elif expr.op == "<":
        result = lhs.value < rhs.value
    elif expr.op == ">":
        result = lhs.value > rhs.value
    elif expr.op == "<=":
        result = lhs.value <= rhs.value
    elif expr.op == ">=":
        result = lhs.value >= rhs.value

    else:
        raise ValueError("Not Implemented Operator '%s'" % expr.op)

    return VALUE(result, ctype)


def exec_assign(expr, genv, lenv):
    assert isinstance(expr, ASSIGN)

    rhs = exec_expr(expr.rhs)
    # rhs = exec_expr(expr.rhs)
    pass


def exec_expr(expr, genv, lenv):
    if isinstance(expr, IVAL):
        return VALUE(expr.val, TInt())
    elif isinstance(expr, FVAL):
        return VALUE(expr.val, TFloat())
    elif isinstance(expr, SVAL):
        pass
    elif isinstance(expr, CVAL):
        return VALUE(expr.val, TChar())
    elif isinstance(expr, ID):
        return id_resolve(expr, genv, lenv)
    elif isinstance(expr, TEXPR):
        return exec_cast(expr, genv, lenv)
    elif isinstance(expr, ADDR):
        return VPTR(exec_expr(expr, genv, lenv))
    elif isinstance(expr, DEREF):
        val = exec_expr(expr.expr, genv, lenv)
        assert isinstance(val, VPTR)
        return val.deref_value
    elif isinstance(expr, PREOP):
        pass
    elif isinstance(expr, POSTOP):
        pass
    elif isinstance(expr, BINOP):
        return calc_binop(expr, genv, lenv)
    elif isinstance(expr, ASSIGN):
        pass

    raise ValueError("invalid expression '%s'" % expr)


def RUN(ast):
    assert isinstance(ast, GOAL)

    genv = {}

    # for define in ast.defs:
