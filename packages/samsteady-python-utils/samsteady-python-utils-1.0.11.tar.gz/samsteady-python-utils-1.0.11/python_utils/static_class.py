import types

def staticclass(cls):
    def init(*args, **kwargs):
        raise Exception("Cannot make an instance of a static class.")
    cls.__init__ = init
    for name, value in vars(cls).items():
        if isinstance(value, types.FunctionType):
            setattr(cls, name, staticmethod(value))
    return cls