import inspect
from types import FunctionType


def delegates(to:FunctionType=None, keep = False, but: list = []):
    "Decorator: replace `**kwargs` in signature with params from `to`"
    if but is None:
        but = []

    def _f(f):
        if to is None:
            to_f, from_f = f.__base__.__init__, f.__init__
        else:
            to_f, from_f = to.__init__ if isinstance(to, type) else to, f

        from_f = getattr(from_f, '__func__', from_f)
        to_f = getattr(to_f, '__func__', to_f)
        if hasattr(from_f, '__delwrap__'):
            return f
        sig = inspect.signature(from_f)
        sigd = dict(sig.parameters)
        k = sigd.pop('kwargs')
        s2 = {k: v.replace(kind=inspect.Parameter.KEYWORD_ONLY) for k, v in inspect.signature(to_f).parameters.items()
              if v.default != inspect.Parameter.empty and k not in sigd and k not in but}
        anno = {k: v for k, v in getattr(to_f, "__annotations__", {}).items() if k not in sigd and k not in but}
        sigd.update(s2)
        if keep:
            sigd['kwargs'] = k
        else:
            from_f.__delwrap__ = to_f

        from_f.__signature__ = sig.replace(parameters=sigd.values())

        if hasattr(from_f, '__annotations__'):
            from_f.__annotations__.update(anno)
        return f
    return _f
