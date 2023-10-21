import threading, time
from   Packages.lib.data import status, lockers

s, l = status, lockers

def addLog(text, time=50):
    """
    게임 내 최하단에 출력되는 로그를 작성하는 함수

        `text`(str) : 로그의 내용, 무조건 기입해야 함
        `time`(int) : 로그가 표시될 시간, 1초는 10으로 계산함
    """
    def add():
        nonlocal text
        s.onDisplay.append(text)
        s.onTime.append(time)

    def remove():
        del s.onDisplay[0]
        del s.onTime[0]

    if len(s.onDisplay) < s.maxStack   : add()
    elif len(s.onDisplay) >= s.maxStack: remove(); add()

def clear(): s.onDisplay, s.onTime = [], []

def logChecker():
    while s.main == 1:
        if l.jpsf == 1:
            time.sleep(0.1)
            if len(s.onTime) > 0:
                for i in range(len(s.onTime)): s.onTime[i] = s.onTime[i]-1
                
            while 1:
                if 0 in s.onTime:
                    del s.onDisplay[s.onTime.index(0)]
                    del s.onTime[s.onTime.index(0)]
                else: break
        else: time.sleep(1)

threading.Thread(target=logChecker, name="logger", daemon=True).start()
