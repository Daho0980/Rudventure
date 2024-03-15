import curses
import time
import threading

from Assets.data             import lockers, status
from Assets.data.color       import cColors as cc
from Game.core.system.logger import addLog
from Game.entities           import player
# from   Game.utils.sound        import play
# from Packages.lib.system                  import options


p    = player
l, s = lockers, status

def newAddListener() -> None:
    def interactions(stdscr):
        while s.main:
            if l.jpsf:
                key = stdscr.getch()
                
                if not l.pause:
                    if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                        p.move(key, 1)
                    # elif key == 113: curses.wrapper(options.menu)
                    elif key == 9:
                        s.showDungeonMap = 0 if s.showDungeonMap else 1
                    elif key == 68: # Shift + d
                        s.debugScreen = False if s.debugScreen else True
                        addLog(f"디버그 모드가 {s.debugScreen}(으)로 변경되었습니다.")
                    elif key == 83: # Shift + s
                        s.showStateDesign=1 if s.showStateDesign==2 else 2
                        addLog(f"스탯 창 디자인이 \'{['콤팩트', '코지'][s.showStateDesign-1]}\'로 변경되었습니다.")
                if key == 32:
                    s.pauseText = f"\n{s.cMarkdown(1)}{cc['fg']['L']}P a u s e{cc['end']}\n"
                    l.pause     = False if l.pause else True
            else: time.sleep(1)

    threading.Thread(name="keyListener",target=lambda: curses.wrapper(interactions)).start()