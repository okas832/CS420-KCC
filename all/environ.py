from ctype import *


class ENV():
    def __init__(self):
        self.envs = [{}]

    def new_env(self):
        self.envs.append({})

    def del_env(self):
        self.envs.pop()

    def add_var(self, name, ctype):
        if isinstance(ctype, TArr):
            self.envs[-1][name] = [VAR("%s[%d]" % (name, i), ctype.elem_type, self) for i in range(ctype.arr_size)]
        else:
            self.envs[-1][name] = VAR(name, ctype, self)

    def id_resolve(self, name):
        for env in reversed(self.envs):
            if env.get(name) is not None:
                return env[name]
        raise SyntaxError("'%s' undeclared (first use in this function)" % name)


class VALUE():
    def __init__(self, value, ctype):
        assert isinstance(ctype, CType)
        if ctype == TFloat():
            self.value = float(value)
        elif ctype == TInt():
            value = int(value) & 0xFFFFFFFF
            self.value = value if value < 0x80000000 else value - 0x100000000
        elif ctype == TChar():
            value = int(result) & 0xFF
            self.value = value if value < 0x80 else value - 0x100
        else:
            raise ValueError("Not Implemented Type '%s'" % ctype)
        self.ctype = ctype

    def __repr__(self):
        if self.ctype == TVoid():
            return "(void)"
        return "(%s) %d" % (self.ctype, self.value)


class VAR(VALUE):
    def __init__(self, name, ctype, env):
        self.name = name
        self.ctype = ctype
        self.env = env
        self.value = VALUE(0, self.ctype)

    def set_value(self, value):
        assert self.ctype == value.ctype
        self.value = value
        return self.value

    def get_value(self):
        return self.value

    def __repr__(self):
        if self.ctype == TVoid():
            return "(void)"
        return "%s (%s)" % (self.value, self.name)


class VPTR(VALUE):
    def __init__(self, deref_var):
        assert isinstance(deref_var, VAR)
        self.deref_var = deref_var

    def deref(self):
        return self.deref_var

    def __repr__(self):
        return "&%s" % self.deref_var


class VFUNC(VALUE):
    def __init__(self, name, ctype, arg_names, body):
        assert isinstance(body, TFunc)
        assert len(ctype.arg_types) == len(ctype.arg_names)
        self.name = name
        self.ctype = ctype
        self.arg_names = arg_names
        self.body = body

    def __repr__(self):
        return "%s %s(%s) %s" % (self.ctype.ret_type, self.name,
            ', '.join('%s %s' % (self.ctype.arg_types[i], self.ctype.arg_names[i]) for i in range(len(this.arg_names))),
            self.body)
