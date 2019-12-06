from ast import *
from ctype import *
from c_yacc import AST_YACC


def find_id(name, genv, lenv):
    for local_scope in reversed(lenv):
        if name in local_scope:
            return local_scope[name]
    if name in genv:
        return genv[name]
    else:
        raise SyntaxError("'%s' undeclared (first use in this function)" % name)


def type_resolve(expr, genv, lenv):
    if isinstance(expr, ID):
        expr.type = find_id(expr.name, genv, lenv)
    elif isinstance(expr, SUBSCR):
        arr_type = type_resolve(expr.arrexpr, genv, lenv)
        if type(arr_type) not in [TPtr, TArr]:
            raise TypeError("subscripted value is neither array nor pointer")
        idx_type = type_resolve(expr.idxexpr, genv, lenv)
        if type(arr_type) not in [TChar, TInt]:
            raise TypeError("array subscript is not an integer")
        if type(arr_type) is TPtr:
            expr.type = arr_type.deref_type
        else:
            expr.type = arr_type.elem_type
    elif isinstance(expr, CALL):
        func_type = type_resolve(expr.funcexpr, genv, lenv)
        if not isinstance(func_type, TFunc):
            raise TypeError("called object is not a function or function pointer")
        if len(expr.argexprs) != len(func_type.arg_types):
            raise TypeError("too %s arguments to function" % ("few" if len(expr.argexprs) < len(func_type.arg_types) else "many"))
        for ae_idx, argexpr in enumerate(expr.argexprs):
            arg_type = type_resolve(argexpr, genv, lenv)
            expr.argexprs[ae_idx] = cast(argexpr, func_type.arg_types[ae_idx])
        expr.type = func_type.ret_type
    elif isinstance(expr, ADDR):
        lvalue_type = type_resolve(expr.expr, genv, lenv)
        if not (isinstance(expr.expr, ID) or isinstance(expr.expr, DEREF) or \
            (isinstance(expr.expr, SUBSCR) and isinstance(expr.expr.arrexpr, ID))):  # all possible forms of lvalue
            raise TypeError("lvalue required as unary '&' operand")
        expr.type = TPtr(lvalue_type)
    elif isinstance(expr, DEREF):
        ptr_type = type_resolve(expr.expr, genv, lenv)
        if not isinstance(ptr_type, TPtr):
            raise TypeError("invalid type argument of unary '*' (have '%s')" % ptr_type)
        expr.type = ptr_type.deref_type
    elif isinstance(expr, PREOP) or isinstance(expr, POSTOP):
        expr_type = type_resolve(expr.expr, genv, lenv)
        expr.type = cast_unop(expr.expr, expr.op)
    elif isinstance(expr, BINOP):
        lhs_type = type_resolve(expr.lhs, genv, lenv)
        rhs_type = type_resolve(expr.rhs, genv, lenv)
        expr.lhs, expr.rhs, expr.type = cast_binop(expr.lhs, expr.rhs, expr.op)
    elif isinstance(expr, ASSIGN):
        lhs_type = type_resolve(expr.lhs, genv, lenv)
        rhs_type = type_resolve(expr.rhs, genv, lenv)
        expr.rhs = cast(expr.rhs, lhs_type)
    elif isinstance(expr, IVAL):
        expr.type = TInt()
    elif isinstance(expr, FVAL):
        expr.type = TFloat()
    elif isinstance(expr, SVAL):
        expr.type = TPtr(TChar())
    elif isinstance(expr, CVAL):
        expr.type = TChar()

    return expr.type


def AST_TYPE(ast, genv):
    assert isinstance(ast, GOAL)
    
    genv = {}

    for define in ast.defs:
        if isinstance(define, VDEF):
            base_type = typestr_map[define.type]
            
            for def_i, vp in enumerate(define.pl):
                vdefid, val = vp
                
                var_type = base_type  # resolve var_type (VDEFID -> CType)
                for _ in range(vdefid.ptr_cnt):
                    var_type = TPtr(var_type)
                if vdefid.array_sz is not None:
                    var_type = TArr(var_type, vdefid.array_sz)

                if val is not None:
                    val_type = type_resolve(val, genv, {})  # resolve val_type
                    define.pl[def_i] = (vdefid, cast(val, var_type))
                
                if vdefid.name in genv:
                    raise SyntaxError("redefinition of '%s'" % vdefid.name)
                genv[vdefid.name] = var_type

        else:  # isinstance(define, FDEF)
            pass  ## TODO ##
    
    return ast


if __name__ == "__main__":
    with open("input.c", "r") as f:
        result = AST_TYPE(AST_YACC(f.read()), {})
    print(result)