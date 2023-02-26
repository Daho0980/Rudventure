import threading, os
from   Packages.modules import states as s

def clear(): os.system("clear" if os.name == "posix" else "cls")

def addLog(text):

    def add():
        nonlocal text
        s.onDisplay.append(text)
        s.onTime.append(s.maxOnTime)

    def remove():
        del s.onDisplay[0]
        del s.onTime[0]

    if len(s.onDisplay) < 5: add()
    elif len(s.onDisplay) >= 5: remove(); add()

def logChecker():
    time = __import__("time")
    while True:
        time.sleep(1)
        if len(s.onTime) > 0:
            for i in range(len(s.onTime)): s.onTime[i] = s.onTime[i]-1
        while True:
            if 0 in s.onTime:
                del s.onDisplay[s.onTime.index(0)]
                del s.onTime[s.onTime.index(0)]
            else: break

threading.Thread(target=logChecker, name="logger").start()
