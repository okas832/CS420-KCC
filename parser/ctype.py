class CType():
    pass

class TInt(CType):
    pass


class TFloat(CType):
    pass


class TChar(CType):
    pass


class TPtr(CType):
    def __init__(self, deref_type):
        self.deref_type = deref_type


class TArr(CType):
    def __init__(self, elem_type, arr_size):
        self.elem_type = elem_type
        self.arr_size = arr_size