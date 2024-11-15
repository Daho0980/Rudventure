class Cooltime:
    def divideHalf(self):
        for key, value in self.__class__.__dict__.items():
            if key.startswith("__"): continue

            if isinstance(value, tuple):
                setattr(self, key, tuple(map(lambda num: num/2, value)))
            else:
                setattr(self, key, value/2)

class Pain(Cooltime):
    turnEnd        = (600, 810)
    

class Unrest(Cooltime):
    turnEnd        = (400, 510)
    targetted      = 0.04
    rush           = 0.09

class Resentment(Cooltime):
    turnEnd        = 350
    blink          = 0.07
    explotion      = 0.07
