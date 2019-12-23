class INSTR():
    pass

"""
mov eax, src
mov dst, eax
"""
class MOV(INSTR):
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def __repr__(self):
        return "MOV(%s, %s)"%(self.dst, self.src)

"""
mov eax, src1
mov edx, src2
operations...
mov dst, eax
"""
class ADD(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "ADD(%s, %s, %s)"%(self.dst, self.src1, self.src2)

class SUB(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "SUB(%s, %s, %s)"%(self.dst, self.src1, self.src2)

class MUL(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "MUL(%s, %s, %s)"%(self.dst, self.src1, self.src2)

"""
LOOK IDIV instruction!
"""
class DIV(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "DIV(%s, %s, %s)"%(self.dst, self.src1, self.src2)

class MOD(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "MOD(%s, %s, %s)"%(self.dst, self.src1, self.src2)

class AND(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "AND(%s, %s, %s)"%(self.dst, self.src1, self.src2)

class OR(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "OR(%s, %s, %s)"%(self.dst, self.src1, self.src2)

class XOR(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "XOR(%s, %s, %s)"%(self.dst, self.src1, self.src2)


class LSH(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "LSH(%s, %s, %s)"%(self.dst, self.src1, self.src2)


class RSH(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "RSH(%s, %s, %s)"%(self.dst, self.src1, self.src2)


class DAND(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "DAND(%s, %s, %s)"%(self.dst, self.src1, self.src2)


class DOR(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "DOR(%s, %s, %s)"%(self.dst, self.src1, self.src2)


class LC(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "LC(%s, %s, %s)"%(self.dst, self.src1, self.src2)

class GC(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "GC(%s, %s, %s)"%(self.dst, self.src1, self.src2)

class LEC(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "LEC(%s, %s, %s)"%(self.dst, self.src1, self.src2)

class GEC(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "GEC(%s, %s, %s)"%(self.dst, self.src1, self.src2)

"""
mov eax, src
mov dst, al
"""
class MOVB(INSTR):
     def __init__(self, dst, src):
        self.dst = dst
        self.src = src

     def __repr__(self):
        return "MOVB(%s, %s)"%(self.dst, self.src)

"""
mov al, src
mov dst, eax
"""
class MOVE(INSTR):
     def __init__(self, dst, src):
        self.dst = dst
        self.src = src

     def __repr__(self):
        return "MOVE(%s, %s)"%(self.dst, self.src)


"""
mov edx, src
mov eax, dst
mov [eax], edx
"""
class SAVE(INSTR):
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def __repr__(self):
        return "SAVE(%s, %s)"%(self.dst, self.src)

class IDADDR(INSTR):
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def __repr__(self):
        return "IDADDR(%s, %s)"%(self.dst, self.src)

class ARRIDX(INSTR):
    def __init__(self, dst, src1, src2):
        self.dst = dst
        self.src1 = src1
        self.src2 = src2

    def __repr__(self):
        return "ARRIDX(%s, %s, %s)"%(self.dst, self.src1, self.src2)

"""
class REFER(INSTR):
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def __repr__(self):
        return "REFER(%s, %s)"%(self.dst, self.src)
"""
class DEREFER(INSTR):
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def __repr__(self):
        return "DEREFER(%s, %s)"%(self.dst, self.src)

class INC(INSTR):
    def __init__(self, dst):
        self.dst = dst

    def __repr__(self):
        return "INC(%s)"%(self.dst)

class DEC(INSTR):
    def __init__(self, dst):
        self.dst = dst

    def __repr__(self):
        return "DEC(%s)"%(self.dst)

class NEG(INSTR):
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def __repr__(self):
        return "NEG(%s, %s)"%(self.dst, self.src)

class NOT(INSTR):
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def __repr__(self):
        return "NOT(%s, %s)"%(self.dst, self.src)

class LNOT(INSTR):
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def __repr__(self):
        return "LNOT(%s, %s)"%(self.dst, self.src)

class PUSH(INSTR):
    def __init__(self, src):
        self.src = src

    def __repr__(self):
        return "PUSH(%s)"%(self.src)

class STR(INSTR):
    def __init__(self, dst, src):
        self.dst = dst
        self.src = src

    def __repr__(self):
        return "STR(%s, %s)"%(self.dst, self.src)

class CALLINST(INSTR):
    def __init__(self, dst, func, pop):
        self.dst = dst
        self.func = func
        self.pop = pop

    def __repr__(self):
        return "CALL(%s, %s), POP(%d)"%(self.dst, self.func, self.pop)

class FORF(INSTR):
    def __init__(self, init, comp, post, body):
        self.init = init
        self.comp = comp
        self.post = post
        self.body = body

    def __repr__(self):
        return "FOR(%s, %s, %s, %s)"%(self.init, self.body, self.post, self.comp)

class IFELSEF(INSTR):
    def __init__(self, cond, if_stmt, else_stmt):
        self.cond = cond
        self.if_stmt = if_stmt
        self.else_stmt = else_stmt

    def __repr__(self):
        return 'IFELSE(%s, %s, %s)' % (self.cond, self.if_stmt, self.else_stmt)

class RET(INSTR):
    def __init__(self, src):
        self.src = src

    def __repr__(self):
        return "RETURN(%d)"%(self.src)
