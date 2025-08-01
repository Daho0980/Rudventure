class Cooltime:
    def divideHalf(self, exception:tuple):
        for key, value in self.__class__.__dict__.items():
            if key.startswith("__")\
            or key in exception\
            or key == "modeException": continue

            if isinstance(value, tuple):
                setattr(self, key, tuple(map(lambda num: int(num/2), value)))
            else:
                setattr(self, key, value/2)

class Pain(Cooltime):
    turnEnd = (600, 810)
    
    modeException = ()

class Unrest(Cooltime):
    turnEnd   = (400, 510)
    targetted = 0.04
    rush      = 0.09

    modeException = ("rush",)

class Resentment(Cooltime):
    turnEnd   = 350
    blink     = 0.07
    explosion = 0.07

    modeException = ()

class Craving(Cooltime): ... 