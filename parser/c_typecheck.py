from ast import *
from ctype import *
from c_yacc import AST_YACC

# TODO: Traverse AST, check EXPRs type & attach appropriate type casting expressions as necessary
#       If no type cast rule exist, raise TypeError.
#       If non-pointers are DEREFed or rvalues are ADDRed, raise TypeError.
#       Assume that SVAL string literals are char[], since we don't have const.


def type_resolve(expr, env):
    if isinstance(expr, IVAL):
        expr.type = TInt()
    elif isinstance(expr, FVAL):
        expr.type = TFloat()
    elif isinstance(expr, CVAL):
        expr.type = TChar()
    elif isinstance(expr, SVAL):
        expr.type = TPtr(TChar())

    return expr.type


def AST_TYPE(ast, env):
    assert isinstance(ast, GOAL)
    
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
                    val_type = type_resolve(val, env)  # resolve val_type
                    define.pl[def_i] = (vdefid, cast(val, var_type))
                    
        else:  # isinstance(define, FDEF)
            pass
    
    return ast


if __name__ == "__main__":
    with open("input.c", "r") as f:
        result = AST_TYPE(AST_YACC(f.read()), {})
    print(result)