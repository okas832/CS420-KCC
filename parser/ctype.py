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
        return super().__eq__(rhs) and self.elem_type == rhs.elem_type and \
            self.arr_size == rhs.arr_size


class TFunc(CType):
    def __init__(self, ret_type, arg_types):
        self.ret_type = ret_type
        self.arg_types = arg_types
    
    def __repr__(self):
        return '%s (%s)' % (self.ret_type, ', '.join(str(at) for at in self.arg_types))
    
    def __eq__(self, rhs):
        return super().__eq__(rhs) and self.ret_type == rhs.ret_type and \
            self.arg_types == rhs.arg_types


# char -> int
class C2I(EXPR):
    def __init__(self, expr, _):
        self.expr = expr
        super().__init__(TInt())
    
    def __repr__(self):
        return 'C2I(%s)' % self.expr


# int -> char
class I2C(EXPR):
    def __init__(self, expr, _):
        self.expr = expr
        super().__init__(TChar())
    
    def __repr__(self):
        return 'I2C(%s)' % self.expr


# int -> float
class I2F(EXPR):
    def __init__(self, expr, _):
        self.expr = expr
        super().__init__(TFloat())
    
    def __repr__(self):
        return 'I2F(%s)' % self.expr


# float -> int
class F2I(EXPR):
    def __init__(self, expr, _):
        self.expr = expr
        super().__init__(TInt())
    
    def __repr__(self):
        return 'F2I(%s)' % self.expr


# arr -> ptr
class A2P(EXPR):
    def __init__(self, expr, ptr_type):
        if expr.type.elem_type != ptr_type.deref_type:
            raise TypeError("invalid cast from %s to %s" % (expr.type, ptr_type))
        self.expr = expr
        super().__init__(ptr_type)
    
    def __repr__(self):
        return 'A2P(%s)' % self.expr


# ptr -> arr
class P2A(EXPR):
    def __init__(self, expr, arr_type):
        if expr.type.deref_type != arr_type.elem_type:
            raise TypeError("invalid cast from %s to %s" % (expr.type, arr_type))
        self.expr = expr
        super().__init__(arr_type)
    
    def __repr__(self):
        return 'P2A(%s)' % self.expr


typestr_map = {
    'int'   : TInt(),
    'float' : TFloat(),
    'char'  : TChar(),
}


# (from_type, to_type) -> cast*
__cast_rules = [
    ((TChar, TInt), [C2I]),
    ((TInt, TChar), [I2C]),
    ((TInt, TFloat), [I2F]),
    ((TFloat, TInt), [F2I]),
    ((TChar, TFloat), [C2I, I2F]),
    ((TFloat, TChar), [F2I, I2C]),
    ((TArr, TPtr), [A2P]),
    ((TPtr, TArr), [P2A]),
]


__cast_prec = [TChar(), TInt(), TFloat()]


def max_prec(expr_1, expr_2, op):
    t1, t2 = expr_1.type, expr_2.type
    if t1 not in __cast_prec or t2 not in __cast_prec:
        raise TypeError("invalid types to binary operation '%s': %s, %s" % (op, t1, t2))
    return __cast_prec[max(__cast_prec.index(t1), __cast_prec.index(t2))]


def cast(expr, to_type):
    assert isinstance(expr, EXPR)
    
    from_type = expr.type
    if from_type == to_type:
        return expr
    
    for cast_dir, cast_order in __cast_rules:
        if type(from_type) == cast_dir[0] and type(to_type) == cast_dir[1]:
            for caster in cast_order:
                expr = caster(expr, to_type)
            return expr
    
    raise TypeError("invalid cast from %s to %s" % (from_type, to_type))


def cast_unop(expr, op):
    if op in ["++", "--"]:
        res_type = expr.type
        if isinstance(res_type, TArr):
            raise TypeError("lvalue required as operand of %s" % op)
    elif op in ["+", "-"]:
        res_type = expr.type
        if type(res_type) not in [TChar, TInt, TFloat]:
            raise TypeError("wrong type argument to unary operator %s" % op)
    elif op == "~":
        res_type = expr.type
        if type(res_type) not in [TChar, TInt]:
            raise TypeError("wrong type argument to bit-complement")
    else:  # op == "!"
        res_type = TInt()
    
    return res_type
        


def cast_binop(expr_lhs, expr_rhs, op):
    if op in ["+", "-", "*", "/"]:
        res_type = max_prec(expr_lhs, expr_rhs, op)
    elif op in ["%", "&", "|", "^"]:
        res_type = max_prec(expr_lhs, expr_rhs, op)
        if res_type == TFloat():
            raise TypeError("invalid types to binary operation '%s': %s, %s" % (op, expr_lhs.type, expr_rhs.type))
    else:  # op in ["<<", ">>", "&&", "||"]
        res_type = max_prec(expr_lhs, expr_rhs, op)
        if res_type == TFloat():
            raise TypeError("invalid types to binary operation '%s': %s, %s" % (op, expr_lhs.type, expr_rhs.type))
        res_type = TInt()  # promote to TInt

    expr_lhs = cast(expr_lhs, res_type)
    expr_rhs = cast(expr_rhs, res_type)

    return (expr_lhs, expr_rhs, res_type)