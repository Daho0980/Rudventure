import time
import curses
import threading
from Packages.lib                         import player
from Packages.lib.data                    import lockers, status
from Packages.lib.system                  import options
from Packages.lib.system.globalFunc.sound import play

p    = player.player
l, s = lockers, status

def newAddListener():
    def interactions(stdscr):
        while s.main:
            if l.jpsf:
                key = stdscr.getch()
                
                if   key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]: p.move(key, 1)
                elif key == 113: curses.wrapper(options.menu)
                elif key == 9:
                    play("move_box")
                    s.showDungeonMap = 1 if s.showDungeonMap == 0 else 0
            else: time.sleep(1)

    threading.Thread(name="keyListener",target=lambda: curses.wrapper(interactions)).start()