from ast import *
from ctype import *
from environ import *


def id_resolve(expr, genv, lenv):
    assert isinstance(expr, ID)

    if lenv.exist_var(expr.name):
        return lenv.find_var(expr.name)

    if genv.exist_var(expr.name):
        return genv.find_var(expr.name)

    raise SyntaxError("'%s' undeclared (first use in this function)" % expr.name)


def lvalue_resolve(expr, genv, lenv):
    assert isinstance(expr, ID) or isinstance(expr, DEREF) or (isinstance(expr, SUBSCR) and isinstance(expr.arrexpr, ID))
    # TODO: int a[10]; int **b = &a; (*b)[0] = 1;

    if isinstance(expr, DEREF):
        val = exec_expr(expr.expr)
        if isinstance(val, VPTR):
            return val.deref()
        else:
            raise TypeError("invalid type argument of unary '*' (have '%s')" % val.ctype)
    if isinstance(expr, ID):
        return id_resolve(expr, genv, lenv)
    if isinstance(expr, SUBSCR) and isinstance(expr.arrexpr, ID):
        idx = exec_expr(expr.idxexpr, genv, lenv)
        if idx.ctype == TInt():
            var = id_resolve(expr.arrexpr, genv, lenv)
            return var[idx]
        raise TypeError("array subscript is not an integer")


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


def exec_preop(expr, genv, lenv):
    assert isinstance(expr, PREOP)

    val = exec_expr(expr.expr, genv, lenv)

    # TODO: INC and DEC operator
    if expr.op == "++":
        pass
    elif expr.op == "--":
        pass
    elif expr.op == "+":
        result = +val.value
    elif expr.op == "-":
        result = -val.value
    elif expr.op == "~":
        result = ~val.value
    elif expr.op == "!":
        result = not val.value
    return VALUE(result, val.ctype)


def exec_binop(expr, genv, lenv):
    assert isinstance(expr, BINOP)

    lhs = exec_expr(expr.lhs, genv, lenv)
    rhs = exec_expr(expr.rhs, genv, lenv)
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

    rhs = exec_expr(expr.rhs, genv, lenv)
    lhs = lvalue_resolve(expr.lhs, genv, lenv)
    return lhs.set_value(rhs)


def exec_expr(expr, genv, lenv):
    if isinstance(expr, IVAL):
        return VALUE(expr.val, TInt())
    elif isinstance(expr, FVAL):
        return VALUE(expr.val, TFloat())
    elif isinstance(expr, SVAL):
        pass
    elif isinstance(expr, CVAL):
        return VALUE(expr.val, TChar())
    elif isinstance(expr, TEXPR):
        return exec_cast(expr, genv, lenv)
    elif isinstance(expr, ID):
        var = id_resolve(expr, genv, lenv)
        if isinstance(var, VAR):
            return var.get_value()
        else:
            assert isinstance(var, list)
            return var
    elif isinstance(expr, SUBSCR):
        arr = exec_expr(expr.arrexpr, genv, lenv)
        idx = exec_expr(expr.idxexpr, genv, lenv)
        assert isinstance(arr, list)
        return arr[idx].get_value()
    elif isinstance(expr, CALL):
        pass
    elif isinstance(expr, POSTOP):
        # TODO: should handle ++, --
        pass
    elif isinstance(expr, ADDR):
        return VPTR(lvalue_resolve(expr, genv, lenv))
    elif isinstance(expr, DEREF):
        val = exec_expr(expr.expr, genv, lenv)
        if isinstance(val, VPTR):
            return val.deref().get_value()
        elif isinstance(val, list):
            return val[0].get_value()
        else:
            raise ValueError("Cannot dereference '%s'" % val)
    elif isinstance(expr, PREOP):
        return exec_preop(expr, genv, lenv)
    elif isinstance(expr, BINOP):
        return exec_binop(expr, genv, lenv)
    elif isinstance(expr, ASSIGN):
        return exec_assign(expr, genv, lenv)

    raise ValueError("invalid expression '%s'" % expr)


def RUN(ast):
    assert isinstance(ast, GOAL)

    genv = ENV()
