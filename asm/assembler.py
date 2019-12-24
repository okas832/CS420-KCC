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
        return src + [DEREFER(dst, src[-1].dst)]
    elif isinstance(code, CALL):
        src = assemble_expr(code, local_var)
        return src

JMP_LABEL_CNT = 0
IF_LABEL_CNT = 0
def assemble_expr(code,local_var):
    global tmp_cnt
    global offset
    global pre_code
    global post_code
    global JMP_LABEL_CNT
    global IF_LABEL_CNT
    tmp_cnt += 1
    offset -= 4
    local_var.append([4, "tmp%d" % (tmp_cnt), offset])
    dst = "tmp%d" % (tmp_cnt)
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
        lhs = assemble_expr(code.lhs, local_var)
        rhs = assemble_expr(code.rhs, local_var)
        if code.op == "+":
            return lhs + rhs + [ADD(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "-":
            return lhs + rhs + [SUB(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "*":
            return lhs + rhs + [MUL(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "/":
            return lhs + rhs + [DIV(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "%":
            return lhs + rhs + [MOD(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "&":
            return lhs + rhs + [AND(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "|":
            return lhs + rhs + [OR(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "^":
            return lhs + rhs + [XOR(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "<<":
            return lhs + rhs + [LSH(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == ">>":
            return lhs + rhs + [RSH(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "&&":
            return lhs + rhs + [DAND(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "||":
            return lhs + rhs + [DOR(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "<":
            return lhs + rhs + [LC(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == ">":
            return lhs + rhs + [GC(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == "<=":
            return lhs + rhs + [LEC(dst, lhs[-1].dst, rhs[-1].dst)]
        elif code.op == ">=":
            return lhs + rhs + [GEC(dst, lhs[-1].dst, rhs[-1].dst)]

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
        return lhs + rhs + [SAVE(lhs[-1].dst, rhs[-1].dst), DEREFER(dst, lhs[-1].dst)]
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
        push_code = push_code[::-1]
        return func_code + arg_code + push_code + [CALLINST(dst, func_code[-1].dst, len(code.argexprs) * 4)]
    elif isinstance(code, DEREF):
        src = assemble_expr(code.expr, local_var)
        return src + [DEREFER(dst, src[-1].dst)]
    elif isinstance(code, ADDR):
        src = assemble_addr(code.expr, local_var)
        return src
    elif isinstance(code, A2P):
        src = assemble_addr(code.expr, local_var)
        return src
    elif isinstance(code, FOR):
        init_code = assemble_expr(code.init, local_var)
        init_code = pre_code + init_code + post_code
        pre_code = []
        post_code = []
        cond_code = assemble_expr(code.cond, local_var)
        cond_code = pre_code + cond_code + post_code
        pre_code = []
        post_code = []
        next_code = assemble_expr(code.update, local_var)
        next_code = pre_code + next_code + post_code
        pre_code = []
        post_code = []
        body_code = assemble_expr(code.body, local_var)
        JMP_LABEL_CNT += 1
        return init_code + [JMP("for_lbl%d_2"%(JMP_LABEL_CNT))]\
                         + [LABEL("for_lbl%d_1"%(JMP_LABEL_CNT))]\
                         + body_code\
                         + [LABEL("for_lbl%d_4"%(JMP_LABEL_CNT))]\
                         + next_code\
                         + [LABEL("for_lbl%d_2"%(JMP_LABEL_CNT))]\
                         + cond_code\
                         + [JNZ("for_lbl%d_1"%(JMP_LABEL_CNT), cond_code[-1].dst)]\
                         + [LABEL("for_lbl%d_3"%(JMP_LABEL_CNT))]
    elif isinstance(code, IFELSE):
        cond_code = assemble_expr(code.cond, local_var)
        if_stmt_code = assemble_expr(code.if_stmt, local_var)
        else_stmt_code = assemble_expr(code.else_stmt, local_var)
        IF_LABEL_CNT += 1
        return cond_code + [JZ("if_lbl%d_1"%(IF_LABEL_CNT), cond_code[-1].dst)]\
                         + if_stmt_code\
                         + [JMP("if_lbl%d_2"%(IF_LABEL_CNT))]\
                         + [LABEL("if_lbl%d_1"%(IF_LABEL_CNT))]\
                         + else_stmt_code\
                         + [LABEL("if_lbl%d_2"%(IF_LABEL_CNT))]
    elif isinstance(code, BREAK):
        return [JMP("for_lbl%d_3"%(JMP_LABEL_CNT + 1))]
    elif isinstance(code, CONTINUE):
        return [JMP("for_lbl%d_4"%(JMP_LABEL_CNT + 1))]
    elif isinstance(code, EXPR_MANY):
        expr_code = []
        for expr in code.exprs:
            res_code = assemble_expr(expr, local_var)
            expr_code += res_code
        return expr_code
    elif isinstance(code, BODY):
        expr_code = []
        for expr in code.stmts:
            res_code = assemble_expr(expr, local_var)
            expr_code += res_code
        return expr_code
    elif isinstance(code, RETURN):
        ret_code = assemble_expr(code.expr, local_var)
        return ret_code + [RET(ret_code[-1].dst)]
    return []

def assemble_body(func,  arg_var):
    global offset
    global pre_code
    global post_code
    local_var = []
    code = []
    for defv in func.body.defvs:
        size = 4
        ts = 4
        for var, val in defv.pl:
            # char is 1 byte
            if defv.type == "char":
                size = 1
                ts = 1
            # pointer size always 4
            if var.ptr_cnt != 0:
                size = 4
                ts = 4
            # if array, multiply
            if var.array_sz:
                size *= var.array_sz

            # alloc space
            offset -= size
            local_var.append([ts, var.name, offset])
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
    return code, local_var

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
    func_body, local_var = assemble_body(func, func_arg)
    return [func_type, func_label, func_arg, func_body, local_var]


STR_DATA = []
def id2addr(id, glob_var, func_arg, local_var):
    global STR_DATA
    if isinstance(id, int):
        return str(id)
    if isinstance(id, ID):
        id = id.name
    for var in local_var:
        if var[1] == id:
            return "[ebp%+d]"%(var[2])
    for var in func_arg:
        if var[1].name == id:
            return "[ebp%+d]"%(var[2])
    for typ in ["int", "float", "char"]:
        for var in glob_var.get(typ, []):
            if var[0].name == id:
                return "[__" + str(id) + "]"
    if id[0] == '"' and id[-1] == '"':
        STR_DATA.append(("str_label%d"%(len(STR_DATA)+1), id))
        return "str_label%d"%(len(STR_DATA))
    return "[%s]"%(id)

def emit_text_section(func, glob_var):
    res = "section .text\n"
    for f in func:
        last = False
        func_type, func_label, func_arg, func_body, local_var = f
        res += func_label.name + ":\n"
        res += "\tpush ebp\n"
        res += "\tmov ebp, esp;\n"
        if len(local_var) != 0:
            res += "\tsub esp, %d\n"%(-local_var[-1][2])
        for instr in func_body:
            last = False
            if isinstance(instr, MOV):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, ADD):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tadd eax, edx\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, SUB):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tsub eax, edx\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, MUL):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\timul eax, edx\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, DIV):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
            elif isinstance(instr, MOD):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
            elif isinstance(instr, AND):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tand eax, edx\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, OR):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tor eax, edx\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, XOR):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\txor eax, edx\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, LSH):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov ecx, %s\n"%(src2_addr)
                res += "\tshl eax, cl\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, RSH):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov ecx, %s\n"%(src2_addr)
                res += "\tshr eax, cl\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, RSH):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov ecx, %s\n"%(src2_addr)
                res += "\tshr eax, cl\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, DAND):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tcmp eax, 0\n"
                res += "\tsetne al\n"
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tcmp edx, 0\n"
                res += "\tsetne dl\n"
                res += "\tand al, dl\n"
                res += "\tmovzx eax, al\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, DOR):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tcmp eax, 0\n"
                res += "\tsetne al\n"
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tcmp edx, 0\n"
                res += "\tsetne dl\n"
                res += "\tor al, dl\n"
                res += "\tmovzx eax, al\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, LC):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tcmp eax, edx\n"
                res += "\tsetl al\n"
                res += "\tmovzx eax, al\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, GC):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tcmp eax, edx\n"
                res += "\tsetg al\n"
                res += "\tmovzx eax, al\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, LEC):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tcmp eax, edx\n"
                res += "\tsetle al\n"
                res += "\tmovzx eax, al\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, GEC):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tcmp eax, edx\n"
                res += "\tsetge al\n"
                res += "\tmovzx eax, al\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, MOVB):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tmovzx %s, al\n"%(dst_addr)
            elif isinstance(instr, MOVE):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, 0\n"
                res += "\tmov al, %s\n"%(src_addr)
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, SAVE):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov edx, %s\n"%(src_addr)
                res += "\tmov eax, %s\n"%(dst_addr)
                res += "\tmov [eax], edx\n"
            elif isinstance(instr, IDADDR):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tlea eax, %s\n"%(src_addr)
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, ARRIDX):
                src1_addr = id2addr(instr.src1, glob_var, func_arg, local_var)
                src2_addr = id2addr(instr.src2, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src1_addr)
                res += "\tmov edx, %s\n"%(src2_addr)
                res += "\tlea eax, [edx * 4 + eax]\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, DEREFER):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tmov eax, [eax]\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, INC):
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(dst_addr)
                res += "\tmov edx, %s\n"%(dst_addr)
                res += "\tmov edx, [edx]\n"
                res += "\tinc edx\n"
                res += "\tmov [eax], edx\n"
            elif isinstance(instr, DEC):
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(dst_addr)
                res += "\tmov edx, %s\n"%(dst_addr)
                res += "\tmov edx, [edx]\n"
                res += "\tdec edx\n"
                res += "\tmov [eax], edx\n"
            elif isinstance(instr, NEG):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tneg eax\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, NOT):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tnot eax\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, LNOT):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tcmp eax, 0\n"
                res += "\tsete al\n"
                res += "\tmovzx eax, al\n"
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, PUSH):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tpush eax\n"
            elif isinstance(instr, STR):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tmov %s, eax\n"%(dst_addr)
            elif isinstance(instr, CALLINST):
                dst_addr = id2addr(instr.dst, glob_var, func_arg, local_var)
                func_addr = id2addr(instr.func, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(func_addr)
                res += "\tcall eax\n"
                res += "\tmov %s, eax\n"%(dst_addr)
                if instr.pop != 0:
                    res += "\tadd esp, %d\n"%(instr.pop)
            elif isinstance(instr, JMP):
                res += "\tjmp %s\n"%(instr.label)
            elif isinstance(instr, JNZ):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tcmp eax, 0\n"
                res += "\tjnz %s\n"%(instr.label)
            elif isinstance(instr, JZ):
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tcmp eax, 0\n"
                res += "\tjz %s\n"%(instr.label)
            elif isinstance(instr, LABEL):
                res += "%s:\n"%(instr.label)
            elif isinstance(instr, RET):
                last = True
                src_addr = id2addr(instr.src, glob_var, func_arg, local_var)
                res += "\tmov eax, %s\n"%(src_addr)
                res += "\tleave\n"
                res += "\tret\n"
        if last == False:
            res += "\tmov eax, 0\n"
            res += "\tleave\n"
            res += "\tret\n"
    return res


def hdlr_goal(ast):
    assert isinstance(ast, GOAL)
    global STR_DATA
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
    prefix = "global _start\nextern printf\nextern exit\n"
    text_section = emit_text_section(func, glob_var)
    data_section = emit_data_section(glob_var)
    postfix = """_start:
\tpush ebp
\tmov ebp, esp
\tcall main
\tpush eax
\tcall exit"""
    for label, data in STR_DATA:
        data_section += "\t%s: db %s, 0\n"%(label, data.replace("\\n", '", 10, "'))
    return prefix + data_section + text_section + postfix

def AST_ASM(ast):
    return hdlr_goal(ast)

if __name__ == "__main__":
    with open("input.c", "r") as f:
        result = AST_ASM(AST_TYPE(AST_YACC(f.read())))
    print(result)
