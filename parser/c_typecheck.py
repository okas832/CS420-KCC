from ast import *
from ctype import *
from c_yacc import AST_YACC


def find_id(name, env):
    # search evironment, inner to outer scope
    for scope in reversed(env):
        if name in scope:
            return scope[name]
    else:
        raise SyntaxError("'%s' undeclared (first use in this function)" % name)


def type_resolve(expr, env):
    if isinstance(expr, ID):
        expr.type = find_id(expr.name, env)
    elif isinstance(expr, SUBSCR):
        arr_type = type_resolve(expr.arrexpr, env)
        if type(arr_type) not in [TPtr, TArr]:
            raise TypeError("subscripted value is neither array nor pointer")
        idx_type = type_resolve(expr.idxexpr, env)
        if type(arr_type) not in [TChar, TInt]:
            raise TypeError("array subscript is not an integer")
        if type(arr_type) is TPtr:
            expr.type = arr_type.deref_type
        else:
            expr.type = arr_type.elem_type
    elif isinstance(expr, CALL):
        # printf as keyword, exceptional call w/ variadic arguments & no argument type casting
        if isinstance(expr.funcexpr, ID) and expr.funcexpr.name == "printf":
            if len(expr.argexprs) < 1:
                raise SyntaxError("too few arguments to function")
            type_resolve(expr.argexprs[0], env)
            expr.argexprs[0] = cast(expr.argexprs[0], TPtr(TChar()))
            for argexpr in expr.argexprs[1:]:
                arg_type = type_resolve(argexpr, env)
            expr.type = TInt()
        else:
            func_type = type_resolve(expr.funcexpr, env)
            if not isinstance(func_type, TFunc):
                raise TypeError("called object is not a function or function pointer")
            if len(expr.argexprs) != len(func_type.arg_types):
                raise SyntaxError("too %s arguments to function" % ("few" if len(expr.argexprs) < len(func_type.arg_types) else "many"))
            for ae_idx, argexpr in enumerate(expr.argexprs):
                arg_type = type_resolve(argexpr, env)
                expr.argexprs[ae_idx] = cast(argexpr, func_type.arg_types[ae_idx])
            expr.type = func_type.ret_type
    elif isinstance(expr, ADDR):
        lvalue_type = type_resolve(expr.expr, env)
        if not (isinstance(expr.expr, ID) or isinstance(expr.expr, DEREF) or \
            (isinstance(expr.expr, SUBSCR) and isinstance(expr.expr.arrexpr, ID))):  # all possible forms of lvalue
            raise TypeError("lvalue required as unary '&' operand")
        expr.type = TPtr(lvalue_type)
    elif isinstance(expr, DEREF):
        ptr_type = type_resolve(expr.expr, env)
        if isinstance(ptr_type, TArr):
            expr.expr = cast(expr.expr, TPtr(ptr_type.elem_type))
            ptr_type = expr.expr.type
        elif not isinstance(ptr_type, TPtr):
            raise TypeError("invalid type argument of unary '*' (have '%s')" % ptr_type)
        if isinstance(ptr_type.deref_type, TVoid):
            raise TypeError("attempting to derefence void*")
        expr.type = ptr_type.deref_type
    elif isinstance(expr, PREOP) or isinstance(expr, POSTOP):
        expr_type = type_resolve(expr.expr, env)
        expr.type = cast_unop(expr.expr, expr.op)
    elif isinstance(expr, BINOP):
        lhs_type = type_resolve(expr.lhs, env)
        rhs_type = type_resolve(expr.rhs, env)
        expr.lhs, expr.rhs, expr.type = cast_binop(expr.lhs, expr.rhs, expr.op)
    elif isinstance(expr, ASSIGN):
        lhs_type = type_resolve(expr.lhs, env)
        rhs_type = type_resolve(expr.rhs, env)
        if isinstance(lhs_type, TArr):
            raise TypeError("assignment to expression with array type")
        expr.rhs = cast(expr.rhs, lhs_type)
        expr.type = lhs_type
    elif isinstance(expr, IVAL):
        expr.type = TInt()
    elif isinstance(expr, FVAL):
        expr.type = TFloat()
    elif isinstance(expr, SVAL):
        expr.type = TPtr(TChar())
    elif isinstance(expr, CVAL):
        expr.type = TChar()

    return expr.type


# resolve & apply VDEF into target_env
# target_env is element of env
def VDEF_resolve(vdef, env, target_env):
    base_type = typestr_map[vdef.type]
            
    for def_i, vp in enumerate(vdef.pl):
        vdefid, val = vp
        
        var_type = base_type  # resolve var_type (VDEFID -> CType)
        for _ in range(vdefid.ptr_cnt):
            var_type = TPtr(var_type)
        if vdefid.array_sz is not None:
            var_type = TArr(var_type, vdefid.array_sz)

        if val is not None:
            val_type = type_resolve(val, env)  # resolve val_type
            vdef.pl[def_i] = (vdefid, cast(val, var_type))
        
        if vdefid.name in target_env:
            raise SyntaxError("redefinition of '%s'" % vdefid.name)
        target_env[vdefid.name] = var_type


def STMT_resolve(stmt, env):
    if isinstance(stmt, BODY):
        body_resolve(stmt, env)
    elif isinstance(stmt, EMPTY_STMT):
        pass
    elif isinstance(stmt, EXPR_MANY):
        for expr in stmt.exprs:
            type_resolve(expr, env)
        stmt.type = stmt.exprs[-1].type
    elif isinstance(stmt, WHILE):
        STMT_resolve(stmt.cond, env)  ## TODO: cast conditionals to int?
        STMT_resolve(stmt.body, env)
    elif isinstance(stmt, FOR):
        STMT_resolve(stmt.init, env)
        STMT_resolve(stmt.cond, env)
        STMT_resolve(stmt.update, env)
        STMT_resolve(stmt.body, env)
    elif isinstance(stmt, IFELSE):
        STMT_resolve(stmt.cond, env)
        STMT_resolve(stmt.if_stmt, env)
        if stmt.else_stmt is not None:
            STMT_resolve(stmt.else_stmt, env)
    else:
        type_resolve(stmt, env)


def body_resolve(body, env, func_body = False):
    if not func_body:
        env.append({})  # scope of current body
    
    # resolve VDEFs
    for vdef in body.defvs:
        VDEF_resolve(vdef, env, env[-1])

    # resolve STMTs
    for stmt in body.stmts:
        STMT_resolve(stmt, env)
    
    del env[-1]


def AST_TYPE(ast):
    assert isinstance(ast, GOAL)
    
    genv = {}

    for define in ast.defs:
        if isinstance(define, VDEF):
            VDEF_resolve(define, [genv], genv)

        else:  # isinstance(define, FDEF)
            args_env = {}

            ret_type = typestr_map[define.type]
            
            arg_types = []
            for type_name, vdefid in define.arg:
                arg_type = typestr_map[type_name]
                for _ in range(vdefid.ptr_cnt):
                    arg_type = TPtr(arg_type)
                if vdefid.array_sz is not None:
                    arg_type = TPtr(arg_type)  # pointer decay
                arg_types.append(arg_type)
                args_env[vdefid.name] = arg_type

            if define.name in genv:
                raise SyntaxError("redefinition of '%s'" % define.name)
            genv[define.name] = TFunc(ret_type, arg_types)

            body_resolve(define.body, [genv, args_env], True)
    
    return ast


if __name__ == "__main__":
    with open("input.c", "r") as f:
        result = AST_TYPE(AST_YACC(f.read()))
    print(result)