from Assets.data             import status  as s
from Assets.data.color       import cColors as cc
from Game.core.system.logger import addLog

def event0() -> None:
    addLog(f"(슬쩍) 아직 {cc['fg']['L']}이벤트{cc['end']}는 {cc['fg']['R']}{s.cMarkdown([1,2])}안{cc['end']} 만들었답니다 ㅎㅎ;")
    s.Dungeon[s.Dy][s.Dx]['interaction'] = True

def event1() -> None:
    addLog(f"{cc['fg']['A']}신상{cc['end']} 주위의 한기가 {cc['fg']['L']}당신{cc['end']}을 감싸돕니다...")
    s.Dungeon[s.Dy][s.Dx]['interaction'] = True
def event2() -> None: ...
def event3() -> None: ...
def event4() -> None: ...
def event5() -> None: ...