from ast import *

class CType():
    def __eq__(self, rhs):
        return type(self) is type(rhs)


class TInt(CType):
    def __repr__(self):
        return 'int'


class TFloat(CType):
    def __repr__(self):
        return 'float'


class TChar(CType):
    def __repr__(self):
        return 'char'


class TPtr(CType):
    def __init__(self, deref_type):
        self.deref_type = deref_type
    
    def __repr__(self):
        return '*%s' % self.deref_type
    
    def __eq__(self, rhs):
        return super().__eq__(rhs) and self.deref_type == rhs.deref_type


class TArr(CType):
    def __init__(self, elem_type, arr_size):
        self.elem_type = elem_type
        self.arr_size = arr_size
    
    def __repr__(self):
        return '%s[%d]' % (self.elem_type, self.arr_size)
    
    def __eq__(self, rhs):
        return super().__eq__(rhs) and self.elem_type == rhs.elem_type and self.arr_size == rhs.arr_size


typestr_map = {
    'int'   : TInt(),
    'float' : TFloat(),
    'char'  : TChar(),
}


# (from_type, to_type) -> cast*
__cast_rules = {
    (TChar, TInt)   : [C2I],
    (TInt, TChar)   : [I2C],
    (TInt, TFloat)  : [I2F],
    (TFloat, TInt)  : [F2I],
    (TChar, TFloat) : [C2I, I2F],
    (TFloat, TChar) : [F2I, I2C],
}


def cast(expr, to_type):
    assert (isinstance(expr, EXPR))
    
    from_type = expr.type
    if from_type == to_type:
        return expr
    
    for cast_dir, cast_order in __cast_rules.items():
        if type(from_type) is cast_dir[0] and type(to_type) == cast_dir[1]:
            for cast in cast_order:
                expr = cast(expr)
            return expr
    
    raise TypeError("invalid cast from %s to %s" % (from_type, to_type))