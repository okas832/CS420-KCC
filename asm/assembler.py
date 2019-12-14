from ast import *
from ctype import *
from c_typecheck import AST_TYPE
from c_yacc import AST_YACC
import re

GLOBAL_ID_PREFIX = "__"

def evaluate_val(v):
    if isinstance(v, IVAL):
        val = re.sub('[lL]', '', v.val)
        if v.val[:2] == "0x":
            return int(val[2:], 16) & 0xFFFFFFFF
        elif v.val[:2] == "0b":
            return int(val[2:], 2) & 0xFFFFFFFF
        elif len(v.val) != 1 and v.val[:1] == "0":
            return int(val[1:], 8) & 0xFFFFFFFF
        else:
            return int(val) & 0xFFFFFFFF
    if isinstance(v, FVAL):
        val = re.sub('[fF]', '', v.val)
        return float(val)
    if isinstance(v, CVAL):
        if v.val[0] == "'":
            return ord(v.val[1:-1])
        else:
            return evaluate_val(IVAL(v.val))
    if isinstance(v, I2F):
        return float(evaluate_val(v.expr))
    if isinstance(v, F2I):
        return int(evaluate_val(v.expr))
    if isinstance(v, C2I):
        return int(evaluate_val(v.expr))
    if isinstance(v, I2C):
        return int(evaluate_val(v.expr)) & 0xFF
    if isinstance(v, BINOP):
        if v.op == "+":
            return evaluate_val(v.lhs) + evaluate_val(v.rhs)
        elif v.op == "-":
            return evaluate_val(v.lhs) - evaluate_val(v.rhs)
        elif v.op == "*":
            return evaluate_val(v.lhs) * evaluate_val(v.rhs)
        elif v.op == "/":
            lhs = evaluate_val(v.lhs)
            rhs = evaluate_val(v.rhs)
            if isinstance(lhs, int) and isinstance(rhs, int):
                return int(lhs / rhs)
            else:
                return lhs / rhs
        elif v.op == "%":
            return evaluate_val(v.lhs) % evaluate_val(v.rhs)
        elif v.op == "&":
            return evaluate_val(v.lhs) & evaluate_val(v.rhs)
        elif v.op == "|":
            return evaluate_val(v.lhs) | evaluate_val(v.rhs)
        elif v.op == "^":
            return evaluate_val(v.lhs) ^ evaluate_val(v.rhs)
        elif v.op == "<<":
            return evaluate_val(v.lhs) << evaluate_val(v.rhs)
        elif v.op == ">>":
            return evaluate_val(v.lhs) >> evaluate_val(v.rhs)
        elif v.op == "&&":
            return int(bool(evaluate_val(v.lhs) and evaluate_val(v.rhs)))
        elif v.op == "||":
            return int(bool(evaluate_val(v.lhs) or evaluate_val(v.rhs)))
    if isinstance(v, PREOP):
        if v.op == "!":
            return int(not evaluate_val(v.expr))
        elif v.op == "~":
            return ~evaluate_val(v.expr)


def emit_data_section(glob_var):
    exist_type = [("int", 4), ("float", 4), ("char", 1)]
    res = "section .data\n"
    for t, size in exist_type:
        dp = glob_var[t]
        for id, val in dp:
            name, ptr_cnt, array_sz = id.name, id.ptr_cnt, id.array_sz

            name = GLOBAL_ID_PREFIX + name
            # change value's expression to asm
            if val != None:
                val = str(evaluate_val(val))
            else:
                val = "0"

            if ptr_cnt != 0: # pointer size is 4
                size = 4

            if array_sz == None:
                if size == 4:
                    res += "\t%s: dd %s\n" % (name, val)
                elif size == 1:
                    res += "\t%s: db %s\n" % (name, val)
            else:
                if size == 4:
                    res += "\t%s: times %d dd 0\n" % (name, array_sz)
                elif size == 1:
                    res += "\t%s: times %d db 0\n" % (name, array_sz)

    return res

def emit_text_section(func):
    return ""

def assemble_func(func, glob_var, fenv):
    pass

def hdlr_goal(ast):
    assert isinstance(ast, GOAL)

    glob_var = {}
    func = []
    for d in ast.defs:
        if isinstance(d, VDEF):
            var_type = d.type
            vdef_lst = glob_var.get(var_type, [])
            for i in d.pl:
                vdef_lst.append(i)
            glob_var[var_type] = vdef_lst
        elif isinstance(d, FDEF):
            func.append(assemble_func(d, glob_var, func))
        else:
            raise TypeError("Cannot handle %s" % (d))
    data_section = emit_data_section(glob_var)
    text_section = emit_text_section(func)
    return data_section + "\n" + text_section

def AST_ASM(ast):
    return hdlr_goal(ast)

if __name__ == "__main__":
    with open("input.c", "r") as f:
        result = AST_ASM(AST_TYPE(AST_YACC(f.read())))
    print(result)
