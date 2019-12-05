class AST():
    pass


# goal : [def, def, ... , def]
class GOAL(AST):
    def __init__(self, defs):
        self.defs = defs

    def __add__(self, rhs):
        if not isinstance(rhs, GOAL):
            raise TypeError("Expected GOAL, but %s comes." % (type(rhs)))
        return GOAL(self.defs + rhs.defs)

    def __repr__(self):
        return "GOAL(%s)" % (str(self.defs))


# Variable DEFine
# type : define type
# pl : pair list (id, value)
#      value is None if not exist
class VDEF(AST):
    def __init__(self, type, pl):
        self.type = type
        self.pl = pl

    def __repr__(self):
        return 'VDEF(%s, %s)' % (self.type, str(self.pl))


# Function DEFine
# type : return type
# id : function name
# arg : argument (id, type) pair
# body : statements
class FDEF(AST):
    def __init__(self, type, id, arg, body):
        self.type = type
        self.id = id
        self.arg = arg
        self.body = body

    def __repr__(self):
        return 'FDEF(%s, %s, %s, %s)' % (self.type, self.id, self.arg, str(self.body))


class STMT(AST):
    pass


class BODY(STMT):
    def __init__(self, defvs, stmts):
        self.defvs = defvs
        self.stmts = stmts
    
    def __repr__(self):
        return 'BODY(%s, %s)' % (str(self.defvs), str(self.stmts))


class EMPTY_STMT(STMT):
    def __init__(self):
        pass

    def __repr__(self):
        return "EMPTY_STMT()"


class EXPR(STMT):
    def __init__(self, ast):
        self.ast = ast
    
    def __repr__(self):
        return "EXPR(%s)" % (str(self.ast))


# ID VARiable (id_adv [+ array])
# id : variable ID
# ptr_cnt : number of '*'s, int
# array_sz : array size, IVAL. None for non-array variable
class IDVAR(AST):
    def __init__(self, id, ptr_cnt, array_sz):
        self.id = id
        self.ptr_cnt = ptr_cnt
        self.array_sz = array_sz  # None for non-array
    
    def __repr__(self):
        return "LVALUE(%s, %d, %s)" % (self.id, self.ptr_cnt, str(self.array_sz))


# CONSTant values
# val: value, string
class CONST(AST):
    def __init__(self, val):
        self.val = val


# Integer VALue
class IVAL(CONST):
    def __repr__(self):
        return "IVAL(%s)" % self.val


# Float VALue
class FVAL(CONST):
    def __repr__(self):
        return "FVAL(%s)" % self.val


# String VALue
class SVAL(CONST):
    def __repr__(self):
        return "SVAL(%s)" % self.val


# Char VALue
class CVAL(CONST):
    def __repr__(self):
        return "CVAL(%s)" % self.val