import threading, time
from   Assets.data     import status, lockers

s, l = status, lockers

def addLog(text, time=50) -> None:
    """
    게임 내 최하단에 출력되는 로그를 작성하는 함수

        `text`(str) : 로그의 내용, 무조건 기입해야 함
        `time`(int) : 로그가 표시될 시간, 1초는 10으로 계산함
    """
    def add():
        nonlocal text
        s.onDisplay.append(text)
        s.onTime.append   (time)

    def remove():
        del s.onDisplay[0]
        del s.onTime   [0]

    if len(s.onDisplay) < s.maxStack   : add()
    elif len(s.onDisplay) >= s.maxStack: remove(); add()

def clear() -> None: s.onDisplay, s.onTime = [], []

def logChecker() -> None:
    while s.main:
        if l.jpsf and not l.pause:
            time.sleep(0.1)
            if len(s.onTime) > 0: s.onTime = list(map(lambda t: t-1, s.onTime))
            while 0 in s.onTime:
                del s.onDisplay[s.onTime.index(0)]
                del s.onTime   [s.onTime.index(0)]
        else: time.sleep(1)

threading.Thread(target=logChecker, name="logger", daemon=True).start()
