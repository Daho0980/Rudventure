from types import MethodType


def _pronounization(pronoun:str):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            setattr(self, pronoun, MethodType(func, self))

            return func(self, *args, **kwargs)

        return wrapper
    
    return decorator

class ByteFlag:
    _flag = 0b0

    def f_int(self) -> int: return 0b0

    @_pronounization(pronoun="f_int")
    def getFlag(self) -> int:
        if self._flag == 0b0:
            self._flag = 0b1
        
        else:
            self._flag <<= 1

        return self._flag

    @classmethod
    def package(cls):
        delattr(cls, "_flag")
        delattr(cls, "getFlag")
        delattr(cls, "f_int")
        delattr(cls, "package")