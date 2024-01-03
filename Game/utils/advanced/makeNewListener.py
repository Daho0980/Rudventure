import time
import curses
import random
import threading
from   Assets.data             import lockers, status
from   Game.core.system.logger import addLog
from   Game.entities           import player
from   Game.utils.sound        import play
# from Packages.lib.system                  import options

p    = player
l, s = lockers, status
cc   = s.cColors

def newAddListener():
    def interactions(stdscr):
        while s.main:
            if l.jpsf:
                key = stdscr.getch()
                
                if not l.pause:
                    if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                        p.move(key, 1)
                    # elif key == 113: curses.wrapper(options.menu)
                    elif key == 9:
                        play("move_box")
                        s.showDungeonMap = 1 if not s.showDungeonMap else 0
                    elif key == 68: # Shift + d
                        play("move_box")
                        s.debugScreen = False if s.debugScreen else True
                        addLog(f"디버그 모드가 {s.debugScreen}(으)로 변경되었습니다.")
                        
                if key == 32:
                    play("move_box")
                    s.pauseText = f"\n{s.cMarkdown([1])}{cc['fg']['R']}쫄 ?   ㅋ{cc['end']}\n" if random.randrange(0, 3001)==1215 else f"\n{s.cMarkdown([1])}{cc['fg']['L']}P a u s e{cc['end']}\n"
                    l.pause     = False if l.pause else True
            else: time.sleep(1)

    threading.Thread(name="keyListener",target=lambda: curses.wrapper(interactions)).start()