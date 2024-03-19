import curses
import time
import threading

from Assets.data             import lockers, status, color
from Game.core.system.logger import addLog
from Game.entities           import player


p    = player
l, s = lockers, status
cc   = color.cColors

def add() -> None:
    def interactions(stdscr):
        while s.main:
            if l.jpsf:
                key = stdscr.getch()
                
                if not l.pause:
                    if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                        p.move(key, 1)
                    match key:
                        case 9: s.showDungeonMap = 0 if s.showDungeonMap else 1  # Tab
                        case 68: # Shift + d
                            s.debugScreen = False if s.debugScreen else True
                            addLog(f"디버그 모드가 {s.debugScreen}(으)로 변경되었습니다.")
                        case 83: # Shift + s
                            s.statusDesign = 0 if s.statusDesign else 1
                            addLog(f"스탯 창 디자인이 \'{['콤팩트', '코지'][s.statusDesign]}\'로 변경되었습니다.")

                if key == 32: l.pause = False if l.pause else True # Space
            else: time.sleep(1)

    threading.Thread(name="keyListener",target=lambda: curses.wrapper(interactions)).start()