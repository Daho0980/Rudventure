import threading, os, time
from   Packages.lib.data import status as s

def clear(): os.system("clear" if os.name == "posix" else "cls")

def addLog(text, time=50):

    def add():
        nonlocal text
        s.onDisplay.append(text)
        s.onTime.append(time)

    def remove():
        del s.onDisplay[0]
        del s.onTime[0]

    if len(s.onDisplay) < 5   : add()
    elif len(s.onDisplay) >= 5: remove(); add()

def logChecker():
    while s.main == 1:
        if s.jpsf:
            time.sleep(0.1)
            if len(s.onTime) > 0:
                for i in range(len(s.onTime)): s.onTime[i] = s.onTime[i]-1
                
            while True:
                if 0 in s.onTime:
                    del s.onDisplay[s.onTime.index(0)]
                    del s.onTime[s.onTime.index(0)]
                else: break

threading.Thread(target=logChecker, name="logger", daemon=True).start()
