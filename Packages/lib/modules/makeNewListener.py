import time
import curses
import random
import threading
from Packages.lib                         import player
from Packages.lib.data                    import lockers, status
from Packages.lib.modules.logger          import addLog
# from Packages.lib.system                  import options
from Packages.lib.system.globalFunc.sound import play

p    = player.player
l, s = lockers, status
cc   = s.cColors

def newAddListener():
    def interactions(stdscr):
        while s.main:
            if l.jpsf:
                key = stdscr.getch()
                
                if key in  [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]\
                   and not l.pause: p.move(key, 1)
                # elif key == 113: curses.wrapper(options.menu)
                elif key == 9 and not l.pause:
                    play("move_box")
                    s.showDungeonMap = 1 if not s.showDungeonMap else 0
                elif key == 32:
                    play("move_box")
                    s.jjol  = f"\n{s.cMarkdown(1)}{cc['fg']['R']}쫄 ?   ㅋ{cc['end']}\n" if random.randrange(0, 30001)==1215 else f"\n{s.cMarkdown(1)}{cc['fg']['L']}P a u s e{cc['end']}\n"
                    l.pause = False if l.pause else True
            else: time.sleep(1)

    threading.Thread(name="keyListener",target=lambda: curses.wrapper(interactions)).start()