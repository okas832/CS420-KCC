from ctype import *
from copy import copy
from logger import *


class ENV():
    def __init__(self, interface):
        printf_type = TFunc(TInt(), [])
        printf_var = VAR("printf", printf_type, VFUNC("printf", printf_type, [], BODY([], [], Ln((-1, -1)))), -1, "global")
        malloc_type = TFunc(TPtr(TChar()), [])
        malloc_var = VAR("malloc", malloc_type, VFUNC("malloc", malloc_type, [], BODY([], [], Ln((-1, -1)))), -1, "global")
        free_type = TFunc(TVoid(), [])
        free_var = VAR("free", free_type, VFUNC("free", free_type, [], BODY([], [], Ln((-1, -1)))), -1, "global")
        self.envs = [{"printf": printf_var, "malloc": malloc_var, "free": free_var}]
        self.interface = interface

    def new_env(self):
        self.envs.append({})

    def del_env(self):
        self.envs.pop()

    def add_var(self, name, ctype, value, lineno):
        scope = "global" if len(self.envs) == 1 else "main"
        if isinstance(ctype, TArr):
            self.envs[-1][name] = VAR(name, ctype, VPTR(VARRAY(name, ctype, lineno, scope)), lineno, scope)
        elif isinstance(ctype, TFunc):
            assert value is not None
            self.envs[-1][name] = value
        else:
            self.envs[-1][name] = VAR(name, ctype, None, lineno, scope)
            if value is not None:
                self.envs[-1][name].set_value(value, lineno)

    def id_resolve(self, name):
        for env in reversed(self.envs):
            if env.get(name) is not None:
                return env[name]
        raise SyntaxError("'%s' undeclared (first use in this function)" % name)

    def global_env(self):
        env = ENV(self.interface)
        env.envs[0] = self.envs[0]
        return env


class VAR():
    def __init__(self, name, ctype, value, lineno, scope="main"):
        self.name = name
        self.ctype = ctype
        self.value = VALUE(0, ctype) if scope == "global" and value is None else value
        self.history = [(lineno, self.value)]
        declare(name, self, scope)

    def set_value(self, value, lineno):
        assert self.ctype == value.ctype
        self.history.append((lineno, value))
        self.value = value
        return self.value

    def get_value(self):
        if self.value is None:
            raise RuntimeError("'%s' is uninitialized" % self.name)
        return self.value

    def __repr__(self):
        if self.value is None:
            return "N/A"
        return "%s" % self.value


class VALUE():
    def __init__(self, value, ctype):
        assert isinstance(ctype, CType)
        if ctype == TFloat():
            self.value = float(value)
        elif ctype == TInt():
            value = int(value) & 0xFFFFFFFF
            self.value = value if value < 0x80000000 else value - 0x100000000
        elif ctype == TChar():
            value = int(value) & 0xFF
            self.value = value if value < 0x80 else value - 0x100
        else:
            raise ValueError("Not Implemented Type '%s'" % ctype)
        self.ctype = ctype

    def __repr__(self):
        if self.ctype == TFloat():
            return "%f" % self.value
        return "%d" % self.value


class VARRAY(VAR):
    def __init__(self, name, ctype, lineno, scope="main"):
        assert isinstance(ctype, TArr)
        self.array = [VAR("%s[%d]" % (name, i), ctype.elem_type, None, lineno, scope) for i in range(ctype.arr_size)]
        self.name = name
        self.index = 0
        self.ctype = ctype.elem_type

    def subscr(self, idx):
        new = copy(self)
        new.index += idx
        return new

    def get_value(self):
        if self.index not in range(len(self.array)):
            raise RuntimeError("Array index out of range")
        return self.array[self.index].get_value()

    def set_value(self, val, lineno):
        if self.index not in range(len(self.array)):
            raise RuntimeError("Array index out of range")
        return self.array[self.index].set_value(val, lineno)

    def __repr__(self):
        if self.ctype == TChar():
            return "0x%08x" % ((id(self.array) & 0xFFFFFFFF) + self.index)
        return "0x%08x" % ((id(self.array) & 0xFFFFFFFF) + self.index)


class VPTR(VALUE):
    def __init__(self, deref_var):
        assert isinstance(deref_var, VAR) or isinstance(deref_var, VARRAY)
        self.ctype = TPtr(deref_var.ctype)
        self.deref_var = deref_var

    def deref(self):
        return self.deref_var

    def __repr__(self):
        return "%s" % self.deref_var


class VFUNC(VALUE):
    def __init__(self, name, ctype, arg_names, body):
        assert isinstance(body, BODY)
        assert len(ctype.arg_types) == len(arg_names)
        self.name = name
        self.ctype = ctype
        self.arg_names = arg_names
        self.body = body

    def __repr__(self):
        return "%s %s(%s) %s" % (self.ctype.ret_type, self.name,
            ', '.join('%s %s' % (self.ctype.arg_types[i], self.arg_names[i]) for i in range(len(self.arg_names))),
            self.body)
