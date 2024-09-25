import threading, time

from Assets.data import status, lockers


s, l = status, lockers

def add(text, duration):
    s.onDisplay.append(text)
    s.onTime.append(duration)

def addLog(text:str, duration:int=50) -> None:
    """
    게임 내 최하단에 출력되는 로그를 작성하는 함수

        `text`(str) : 로그의 내용, 무조건 기입해야 함.
        `time`(int) : 로그가 표시될 시간, 1초는 10으로 계산함, 기본적으로 `50`으로 설정되어 있음.
    """

    if   len(s.onDisplay) <  s.maxStack: add(text, duration)
    elif len(s.onDisplay) >= s.maxStack:
        s.onDisplay.pop(0)
        s.onTime.pop(0)
        add(text, duration)

def clear() -> None:
    s.onDisplay.clear()
    s.onTime.clear()

def logChecker() -> None:
    while s.main:
        if l.jpsf and not l.pause:
            time.sleep(0.1)
            if s.onTime: s.onTime = list(map(lambda t: t-1, s.onTime))

            s.infoWindow['time'] -= 1 if s.infoWindow['time'] else 0
            if not s.infoWindow['time']: s.infoWindow['text'] = ""
            
            while 0 in s.onTime:
                del s.onDisplay[s.onTime.index(0)]
                del s.onTime   [s.onTime.index(0)]
        else: time.sleep(0.5)

threading.Thread(target=logChecker, name="logger", daemon=True).start()
