from warnings import warn

from pybrary.func import caller


class ContractError(Exception):
    ''' Contract Error '''

class PreError(ContractError):
    ''' Contract Pre Error '''

class ResultError(ContractError):
    ''' Contract Result Error '''

class PostError(ContractError):
    ''' Contract Post Error '''


class Contract:
    def __init__(self, main):
        self.main = main
        self.name = self.__class__.__name__
        self.func = f'{main.__module__}.{main.__name__}'

    def warn(self):
        warn(f'\n\n ? "{caller()}" not defined for Contract "{self.name}"\n')

    def pre(self, *a, **k):
        self.warn()

    def alt(self, *a, **k):
        self.warn()
        return 'no_alt'

    def _run(self, *a, **k):
        r = self.main(*a, **k)
        x = self.alt(*a, **k)
        if x!='no_alt':
            aa = ', '.join(map(str, a)) if a else ''
            kk = ', '+str(k) if k else ''
            assert r == x, f'{self.name} results mismatch {self.func}({aa}{kk}) returned {r} expected {x}'
        return r

    def post(self, result, *a, **k):
        self.warn()

    def __call__(self, *a, **k):
        try:
            self.pre(*a, **k)
        except Exception as x:
            raise PreError(f'\n\n ! {x} !')
        else:
            try:
                r = self._run(*a, **k)
            except Exception as x:
                raise ResultError(f'\n\n ! {x} !')
            else:
                try:
                    self.post(r, *a, **k)
                except Exception as x:
                    raise PostError(f'\n\n ! {x} !')
                else:
                    return r


def contract(cls):
    def deco(fct):
        return cls(fct) if __debug__ else fct
    return deco
