class AST():
    pass

# goal : [def, def, ... , def]
class GOAL(AST):
    def __init__(self, defs):
        self.defs = defs

    def __add__(self, rhs):
        if not isinstance(rhs, GOAL):
            raise TypeError("Expected GOAL, but %s comes."%(type(rhs)))
        return GOAL(self.defs + rhs.defs)

    def __repr__(self):
        return "GOAL(%s)"%(str(self.defs))

# Variable DEFine
# type : define type
# pl : pair list (id, value)
#      value is None if not exist
class VDEF(AST):
    def __init__(self, type, pl):
        self.type = type
        self.pl = pl

    def __repr__(self):
        return 'VDEF(%s, %s)'%(self.type, str(self.pl))

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
        return 'FDEF(%s, %s, %s, %s)'%(self.type, self.id, self.arg, self.body)


class STMT(AST):
    pass

class EXPR(STMT):
    def __init__(self, ast):
        self.ast = ast
    
    def __repr__(self):
        return "EXPR(%s)"%(str(self.ast))