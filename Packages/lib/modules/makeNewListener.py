import time
import curses
import threading
from pynput.keyboard                      import Key, Listener
from Packages.lib                         import player
from Packages.lib.data                    import status, lockers
from Packages.lib.system                  import options
from Packages.lib.system.globalFunc.sound import play

s, l = status, lockers

def addListener():
    def key_press(key):
        if l.jpsf == 1:
            if key in [Key.up, Key.down, Key.left, Key.right]: player.player.move(key, 1)
            time.sleep(0.001)

    def key_release(key):
        if l.jpsf == 1:
            if key == Key.esc  : options.menu()
            elif key == Key.tab:
                play("move_box")
                s.showDungeonMap = 1 if s.showDungeonMap == 0 else 0
            time.sleep(0.001)

    Listener(on_press=key_press, on_release=key_release).start()

def newAddListener():
    def interactions(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)

        while s.main == 1:
            if l.jpsf == 1:
                key = stdscr.getch()
                
                if   key in [258, 259, 260, 261]: player.player.move(key, 1)
                elif key == 113:                  options.menu()
                elif key == 9:
                    play("move_box")
                    s.showDungeonMap = 1 if s.showDungeonMap == 0 else 0

    def listenerRunner(): curses.wrapper(interactions)

    threading.Thread(target=listenerRunner).start()