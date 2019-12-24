from ast import *
from ctype import *
from environ import *
from c_yacc import AST_YACC
from c_typecheck import AST_TYPE
import warnings


class VBREAK():
    pass


class VCONTINUE():
    pass


class VRETURN():
    def __init__(self, value):
        self.ret_val = value


def lvalue_resolve(expr, env):
    assert isinstance(expr, ID) or isinstance(expr, DEREF) or (isinstance(expr, SUBSCR) and isinstance(expr.arrexpr, ID))
    # TODO: int a[10]; int **b = &a; (*b)[0] = 1;

    if isinstance(expr, DEREF):
        val = exec_expr(expr.expr, env)
        if isinstance(val, VPTR):
            return val.deref()
        elif isinstance(val, VARRAY):
            return val
        else:
            raise TypeError("invalid type argument of unary '*' (have '%s')" % val.ctype)
    if isinstance(expr, ID):
        return env.id_resolve(expr.name)
    if isinstance(expr, SUBSCR) and isinstance(expr.arrexpr, ID):
        idx = exec_expr(expr.idxexpr, env)
        var = exec_expr(expr.arrexpr, env)

        if not isinstance(var, VPTR):
            raise TypeError("Cannot array subscript")

        if isinstance(var.deref(), VARRAY):
            return var.deref().subscr(idx.value)
        elif idx.value == 0:
            return var.deref()

        raise TypeError("Cannot array subscript")


def define_func(fdef, env):
    assert isinstance(fdef, FDEF)

    # type annotation exists, although it is not isinstance(fdef, EXPR)
    ctype = fdef.func_type
    arg_names = [arg[1].name for arg in fdef.arg]
    value = VFUNC(fdef.name.name, ctype, arg_names, fdef.body)
    env.add_var(fdef.name.name, ctype, value)


def define_var(vdef, env):
    assert isinstance(vdef, VDEF)

    for vdefid, assign in vdef.pl:
        val = exec_expr(assign, env) if assign is not None else None
        env.add_var(vdefid.name, vdefid.var_type, val)


def exec_cast(expr, env):
    result = exec_expr(expr.expr, env)

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
    if isinstance(expr, A2P):
        return result
    raise ValueError("Not Implemented Type Casting: %s" % result.expr)


def exec_preop(expr, env):
    assert isinstance(expr, PREOP)

    if expr.op == "++" or expr.op == "--":
        var = lvalue_resolve(expr.expr, env)
        val = var.get_value()

        if expr.op == "++":
            var.set_value(VALUE(val.value + 1, val.ctype))
        else:
            var.set_value(VALUE(val.value - 1, val.ctype))
        return var.get_value()

    val = exec_expr(expr.expr, env)

    if expr.op == "+":
        result = +val.value
    elif expr.op == "-":
        result = -val.value
    elif expr.op == "~":
        result = ~val.value
    elif expr.op == "!":
        result = not val.value
    return VALUE(result, val.ctype)


def exec_postop(expr, env):
    assert isinstance(expr, POSTOP)

    var = lvalue_resolve(expr.expr, env)
    val = var.get_value()
    if expr.op == "++":
        var.set_value(VALUE(val.value + 1, val.ctype))
    else:
        var.set_value(VALUE(val.value - 1, val.ctype))

    return val


def exec_binop(expr, env):
    assert isinstance(expr, BINOP)

    lhs = exec_expr(expr.lhs, env)
    rhs = exec_expr(expr.rhs, env)
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


def exec_assign(expr, env):
    assert isinstance(expr, ASSIGN)

    rhs = exec_expr(expr.rhs, env)
    lhs = lvalue_resolve(expr.lhs, env)
    return lhs.set_value(rhs)


def exec_expr(expr, env):
    if isinstance(expr, IVAL):
        return VALUE(expr.val, TInt())
    elif isinstance(expr, FVAL):
        return VALUE(expr.val, TFloat())
    elif isinstance(expr, SVAL):
        string = expr.val[1:-1].encode('utf-8').decode('unicode_escape')
        arr = VARRAY("", TArr(TChar(), len(string) + 1))
        for i, s in enumerate(string):
            arr.array[i].set_value(VALUE(ord(s), TChar()))
        arr.array[-1].set_value(VALUE(0, TChar()))
        return VPTR(arr)
    elif isinstance(expr, CVAL):
        char = expr.val[1:-1].encode('utf-8').decode('unicode_escape')
        return VALUE(ord(char), TChar())
    elif isinstance(expr, TEXPR):
        return exec_cast(expr, env)
    elif isinstance(expr, ID):
        var = env.id_resolve(expr.name)
        if isinstance(var, VAR):
            return var.get_value()
        return var
    elif isinstance(expr, SUBSCR):
        arr = exec_expr(expr.arrexpr, env)
        idx = exec_expr(expr.idxexpr, env)

        if not isinstance(arr, VPTR):
            raise TypeError("Cannot array subscript")

        if isinstance(arr.deref(), VARRAY):
            return arr.deref().subscr(idx.value).get_value()
        elif idx.value == 0:
            return arr.deref().get_value()

        raise TypeError("Cannot array subscript")
    elif isinstance(expr, CALL):
        func = exec_expr(expr.funcexpr, env)
        assert isinstance(func, VFUNC)
        if func.name == "printf":
            args = []
            for argexpr in expr.argexprs:
                args.append(exec_expr(argexpr, env))
            return builtin_printf(args)
        else:
            func_env = env.global_env()
            func_env.new_env()
            for argexpr, argname, argtype in zip(expr.argexprs, func.arg_names, func.ctype.arg_types):
                arg = exec_expr(argexpr, env)
                func_env.add_var(argname, argtype, arg)
            ret = exec_stmt(func.body, func_env, True)
            if isinstance(ret, VRETURN) and ret.ret_val is not None and func.ctype.ret_type != TVoid():
                return ret.ret_val
            elif (ret is None or (isinstance(ret, VRETURN) and ret.ret_val is None)) and \
                func.ctype.ret_type == TVoid():
                return None
            else:
                assert ret is None or (isinstance(ret, VRETURN) and ret.ret_val is None)
                raise RuntimeError("Missing return (expected '%s')" % func.ctype.ret_type)
    elif isinstance(expr, POSTOP):
        return exec_postop(expr, env)
    elif isinstance(expr, ADDR):
        return VPTR(lvalue_resolve(expr.expr, env))
    elif isinstance(expr, DEREF):
        val = exec_expr(expr.expr, env)
        if isinstance(val, VPTR):
            return val.deref().get_value()
        raise ValueError("Cannot dereference '%s'" % val)
    elif isinstance(expr, PREOP):
        return exec_preop(expr, env)
    elif isinstance(expr, BINOP):
        return exec_binop(expr, env)
    elif isinstance(expr, ASSIGN):
        return exec_assign(expr, env)
    elif isinstance(expr, EXPR_MANY):
        for e in expr.exprs:
            val = exec_expr(val, env)
        return val

    raise ValueError("invalid expression '%s'" % expr)


def exec_stmt(stmt, env, func_body=False):
    if isinstance(stmt, BODY):
        if not func_body:
            env.new_env()
        for defv in stmt.defvs:
            define_var(defv, env)
        for sub in stmt.stmts:
            ret = exec_stmt(sub, env)
            if isinstance(ret, VCONTINUE) or isinstance(ret, VBREAK) or isinstance(ret, VRETURN):
                env.del_env()
                return ret
        env.del_env()
    elif isinstance(stmt, EMPTY_STMT):
        pass
    elif isinstance(stmt, WHILE):
        c = exec_expr(stmt.cond, env)
        while c.value:
            ret = exec_stmt(stmt.body, env)
            if isinstance(ret, VBREAK):
                break
            elif isinstance(ret, VRETURN):
                return ret
            c = exec_expr(stmt.cond, env)
    elif isinstance(stmt, FOR):
        exec_expr(stmt.init, env)
        c = exec_expr(stmt.cond, env)
        while c.value:
            ret = exec_stmt(stmt.body, env)
            if isinstance(ret, VBREAK):
                break
            elif isinstance(ret, VRETURN):
                return ret
            exec_expr(stmt.update, env)
            c = exec_expr(stmt.cond, env)
    elif isinstance(stmt, IFELSE):
        c = exec_expr(stmt.cond, env)
        if c.value:
            ret = exec_stmt(stmt.if_stmt, env)
            if isinstance(ret, VBREAK) or isinstance(ret, VCONTINUE) or isinstance(ret, VRETURN):
                return ret
        elif stmt.else_stmt is not None:
            ret = exec_stmt(stmt.else_stmt, env)
            if isinstance(ret, VBREAK) or isinstance(ret, VCONTINUE) or isinstance(ret, VRETURN):
                return ret
    elif isinstance(stmt, CONTINUE):
        return VCONTINUE()
    elif isinstance(stmt, BREAK):
        return VBREAK()
    elif isinstance(stmt, RETURN):
        if stmt.expr is not None:
            return VRETURN(exec_expr(stmt.expr, env))
        return VRETURN(None)
    else:
        exec_expr(stmt, env)
    return None


def builtin_printf(args):
    assert len(args) >= 1
    if not isinstance(args[0], VPTR) or \
       not isinstance(args[0].deref(), VARRAY) or \
       not isinstance(args[0].deref().get_value().ctype, TChar):
       raise RuntimeError("Invalid argument given as format string in built-in function printf")

    # built format string from arg
    fmt = ""
    fmt_varr = args[0].deref()
    for i in range(fmt_varr.index, len(fmt_varr.array)):
        c = chr(fmt_varr.array[i].get_value().value & 0xFF)
        if c == '\0':
            break
        fmt += c
    else:
        raise RuntimeError("Format string with no NULL terminator in built-in printf")

    res = ""
    i, arg_idx = 0, 1
    while i < len(fmt):
        if fmt[i:i+2] == r"%d":
            if arg_idx >= len(args):
                raise RuntimeError("Insufficient variadic arguments while executing built-in printf")
            elif not isinstance(args[arg_idx].ctype, TInt) and not isinstance(args[arg_idx].ctype, TChar):
                raise RuntimeError("Invalid argument type while executing built-in printf (expected 'int'/'char', got '%s')" % type(args[arg_idx]))
            res += str(args[arg_idx].value)
            i += 2
            arg_idx += 1
        elif fmt[i:i+2] == r"%f":
            if arg_idx >= len(args):
                raise RuntimeError("Insufficient variadic arguments while executing built-in printf")
            elif not isinstance(args[arg_idx].ctype, TFloat):
                raise RuntimeError("Invalid argument type while executing built-in printf (expected 'float', got '%s')" % type(args[arg_idx]))
            res += str(args[arg_idx].value)
            i += 2
            arg_idx += 1
        else:
            res += fmt[i]
            i += 1

    print(res, end='')

    if arg_idx != len(args):
        warnings.warn("Trailing variadic arguments after executing built-in printf (%d arguments unused)" % (len(args) - arg_idx), RuntimeWarning)

    return VALUE(len(res), TInt())


def AST_INTERPRET(ast):
    assert isinstance(ast, GOAL)

    env = ENV()

    for define in ast.defs:
        if isinstance(define, VDEF):
            define_var(define, env)
        else:  # isinstance(define, FDEF)
            define_func(define, env)

    call_main = CALL(ID("main"), [])
    exec_expr(call_main, env)


if __name__ == "__main__":
    with open("../sample_input/recursive2.c", "r") as f:
        result = AST_TYPE(AST_YACC(f.read()))
    AST_INTERPRET(result)
