from inspect import currentframe, getouterframes
from operator import attrgetter
from pathlib import Path


# Full Qualified Name od obj
def fqn(obj):
    mod = getattr(obj, '__module__', None)
    cls = obj.__class__.__name__
    if 'builtin' in cls:
        mod = cls = None
    elif cls in ('type', 'function', 'method'):
        cls = None
    name = getattr(obj, '__name__', None)
    return '.'.join(n for n in (mod, cls, name) if n)


# caller's caller
def caller():
    frame = getouterframes(currentframe(), 2)[2]
    mod = Path(frame.filename).stem
    fct = frame.function
    return f'{mod}.{fct}'


# Default implementation for abstract methods
def todo(self):
    cls = self.__class__.__name__
    mth = getouterframes(currentframe())[1][3]
    raise NotImplementedError(
        f'\n ! {mth} missing in {cls} !\n'
    )


# Memoizing property decorator
def memo(fct):
    name = '_memo_' + fct.__name__
    get_val = attrgetter(name)
    @property
    def wrapper(self):
        try:
            return get_val(self)
        except AttributeError:
            val = fct(self)
            setattr(self, name, val)
            return val
    return wrapper


