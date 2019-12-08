from ast import *
from ctype import *


class VALUE(object):
    def __init__(self, addr, value, ctype):
        assert isinstance(ctype, CType)
        self.addr = addr
        self.value = value
        self.ctype = ctype

    def __repr__(self):
        if isinstance(self.ctype, TVoid):
            return "(void)"
        elif isinstance(self.ctype, TInt):
            return "(int) %d" % self.value
        elif isinstance(self.ctype, TFloat):
            return "(float) %f" % self.value
        elif isinstance(self.ctype, TChar):
            return "(char) %d" % self.value

        raise TypeError("Not Implemented")


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


def calc_binop(expr, genv, lenv):
    assert isinstance(expr, BINOP)

    lhs = calc_expr(expr.lhs)
    rhs = calc_expr(expr.rhs)
    assert lhs.ctype == rhs.ctype
    ctype = lhs.ctype

    if expr.op == "+":
        result = lhs.value + rhs.value
    elif expr.op == "-":
        result = lhs.value - rhs.value
    elif expr.op == "*":
        result = lhs.value * rhs.value
    elif expr.op == "/":
        if isinstance(ctype, TFloat):
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


    return VALUE()


def calc_expr(expr, genv, lenv):
    if isinstance(expr, ID):
        return id_resolve(expr, genv, lenv)
    elif isinstance(expr, 
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
