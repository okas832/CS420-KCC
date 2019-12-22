from ast import *
from instr import *
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
        dp = glob_var.get(t, [])
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


tmp_cnt = 0
offset = 0

pre_code = []
post_code = []

def assemble_addr(code, local_var):
    global tmp_cnt
    global offset
    tmp_cnt += 1
    offset -= 4
    local_var.append(["int", "tmp%d" % (tmp_cnt), offset])
    dst = "tmp%d" % (tmp_cnt)
    if isinstance(code, ID):
        return [IDADDR(dst, code)]
    elif isinstance(code, SUBSCR):
        arr = assemble_addr(code.arrexpr, local_var)
        idx = assemble_expr(code.idxexpr, local_var)
        return arr + idx + [ARRIDX(dst, arr[-1].dst, idx[-1].dst)]
    elif isinstance(code, DEREF):
        src = assemble_expr(code.expr, local_var)
        return src + [REFER(dst, src[-1].dst)]

def assemble_expr(code, local_var):
    global tmp_cnt
    global offset
    global pre_code
    global post_code
    tmp_cnt += 1
    offset -= 4
    local_var.append(["int", "tmp%d" % (tmp_cnt), offset])
    dst = "tmp%d" % (tmp_cnt)
    print(code)
    if isinstance(code, IVAL):
        val = re.sub('[lL]', '', code.val)
        if code.val[:2] == "0x":
            return [MOV(dst, int(val[2:], 16) & 0xFFFFFFFF)]
        elif code.val[:2] == "0b":
            return [MOV(dst, int(val[2:], 2) & 0xFFFFFFFF)]
        elif len(code.val) != 1 and code.val[:1] == "0":
            return [MOV(dst, int(val[1:], 8) & 0xFFFFFFFF)]
        else:
            return [MOV(dst, int(val) & 0xFFFFFFFF)]

    elif isinstance(code, CVAL):
        if code.val[0] == "'":
            return [MOV(dst, ord(code.val[1:-1]))]
        else:
            return [MOV(dst, evaluate_val(IVAL(code.val)))]

    elif isinstance(code, SVAL):
        return [STR(dst, code.val)]

    elif isinstance(code, BINOP):
        if code.op == "+":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [ADD(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "-":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [SUB(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "*":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [MUL(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "/":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [DIV(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "%":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [MOD(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "&":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [AND(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "|":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [OR(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "^":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [XOR(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "<<":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [LSH(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == ">>":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [RSH(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "&&":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [DAND(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "||":
            lhs = assemble_expr(code.lhs, local_var)
            rhs = assemble_expr(code.rhs, local_var)
            return lhs + rhs + [DOR(dst, lhs[-1].dst, rhs[-1].dst)]
    elif isinstance(code, ID):
        return [MOV(dst, code.name)]
    elif isinstance(code, I2C):
        src = assemble_expr(code.expr, local_var)
        return src + [MOVB(dst, src[-1].dst)]
    elif isinstance(code, C2I):
        src = assemble_expr(code.expr, local_var)
        return src + [MOVE(dst, src[-1].dst)]
    elif isinstance(code, ASSIGN):
        lhs = assemble_addr(code.lhs, local_var)
        rhs = assemble_expr(code.rhs, local_var)
        return lhs + rhs + [SAVE(lhs[-1].dst, rhs[-1].dst)]
    elif isinstance(code, SUBSCR):
        tmp_cnt += 1
        offset -= 4
        local_var.append(["int", "tmp%d" % (tmp_cnt), offset])
        dst2 = "tmp%d" % (tmp_cnt)
        arr = assemble_addr(code.arrexpr, local_var)
        idx = assemble_expr(code.idxexpr, local_var)
        return arr + idx + [ARRIDX(dst, arr[-1].dst, idx[-1].dst), DEREFER(dst2, dst)]
    elif isinstance(code, PREOP):
        if code.op == "++":
            src = assemble_expr(code.expr, local_var)
            src2 = assemble_addr(code.expr, local_var)
            for code in src2:
                pre_code.append(code)
            pre_code.append(INC(src2[-1].dst))
            return src + [MOV(dst, src[-1].dst)]
        elif code.op == "--":
            src = assemble_expr(code.expr, local_var)
            src2 = assemble_addr(code.expr, local_var)
            for code in src2:
                pre_code.append(code)
            pre_code.append(DEC(src2[-1].dst))
            return src + [MOV(dst, src[-1].dst)]
        elif code.op == "+":
            src = assemble_expr(code.expr, local_var)
            return src + [MOV(dst, src[-1].dst)]
        elif code.op == "-":
            src = assemble_expr(code.expr, local_var)
            return src + [NEG(dst, src[-1].dst)]
        elif code.op == "~":
            src = assemble_expr(code.expr, local_var)
            return src + [NOT(dst, src[-1].dst)]
        elif code.op == "!":
            src = assemble_expr(code.expr, local_var)
            return src + [LNOT(dst, src[-1].dst)]
    elif isinstance(code, POSTOP):
        if code.op == "++":
            src = assemble_expr(code.expr, local_var)
            src2 = assemble_addr(code.expr, local_var)
            for code in src2:
                post_code.append(code)
            post_code.append(INC(src2[-1].dst))
            return src + [MOV(dst, src[-1].dst)]
        elif code.op == "--":
            src = assemble_expr(code.expr, local_var)
            src2 = assemble_addr(code.expr, local_var)
            for code in src2:
                post_code.append(code)
            post_code.append(DEC(src2[-1].dst))
            return src + [MOV(dst, src[-1].dst)]
    elif isinstance(code, CALL):
        arg_code = []
        push_code = []
        func_code = assemble_addr(code.funcexpr, local_var)
        for argexpr in code.argexprs:
            arg_code += assemble_expr(argexpr, local_var)
            push_code += [PUSH(arg_code[-1].dst)]
        return func_code + arg_code + push_code + [CALLINST(dst, func_code[-1].dst, len(code.argexprs) * 4)]
    elif isinstance(code, DEREF):
        src = assemble_addr(code.expr, local_var)
        return src + [REFER(dst, src[-1].dst)]
    return []

def assemble_body(func, glob_var, arg_var, fenv):
    global offset
    global pre_code
    global post_code
    local_var = []
    code = []
    for defv in func.body.defvs:
        size = 4
        for var, val in defv.pl:
            # char is 1 byte
            if defv.type == "char":
                size = 1
            # pointer size always 4
            if var.ptr_cnt != 0:
                size = 4
            # if array, multiply
            if var.array_sz:
                size *= var.array_sz

            # alloc space
            offset -= size
            local_var.append([defv.type, var.name, offset])
            # align
            offset -= offset % 4
            if val:
                res_code = assemble_expr(val, local_var)
                code += res_code
                code.append(MOV(var.name, res_code[-1].dst))
                offset = local_var[-1][2]
    for expr in func.body.stmts:
        expr_code = assemble_expr(expr, local_var)
        code += pre_code + expr_code + post_code
        pre_code = []
        post_code = []
    print(code)
    return

def assign_arg_addr(arg):
    arg_lst = []
    offset = 8
    for i in arg:
        arg_lst.append((i[0], i[1], offset))
        offset += 4
    return arg_lst

def assemble_func(func, glob_var, fenv):
    func_type = func.type
    func_label = func.name
    func_arg = assign_arg_addr(func.arg)
    func_body = assemble_body(func, glob_var, func_arg, fenv)
    return

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
    return data_section + text_section

def AST_ASM(ast):
    return hdlr_goal(ast)

if __name__ == "__main__":
    with open("input.c", "r") as f:
        result = AST_ASM(AST_TYPE(AST_YACC(f.read())))
    print(result)
