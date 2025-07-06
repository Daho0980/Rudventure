from collections import OrderedDict
from typing      import Any


class Conveyor(OrderedDict):
    def __init__(
            self, size:int, fill:bool=False,
            *args, **kwargs                 ):
        self.size = size
        super().__init__(*args, **kwargs)

        if fill:
            for count in range(size):
                self[str(count)] = ""

    def __setitem__(self, key:Any, value:Any) -> None:
        if len(self) >= self.size:
            self.popitem(last=False)
        return super().__setitem__(key, value)
    
    def __str__(self):
        return str(dict(self))
    
    def key(self):
        return list(self.keys())
    
    def value(self):
        return list(self.values())
    
    def item(self):
        return list(self.items())
    
    def resize(self, size):
        arrayLen = len(self)

        if arrayLen > size:
            for _ in range(arrayLen-size):
                self.popitem()

        self.size = size


if __name__ == '__main__':
    a = Conveyor(3)
    a['1'] = 0
    a['2'] = 0
    a['3'] = 0
    print(a)
    print(a.key())
    print(a.value())
    print(a.item())
    print(a.items())
    a.resize(1)
    print(a)