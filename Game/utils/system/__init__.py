import curses

from Game.utils.graphics import (
    escapeAnsi,
    anchor
)


def cinp(stdscr,
         text:str       ="",
         end:str        ='',
         echo:bool      =True,
         cursor:bool    =False,
         useMiddle:bool =True,
         y:int          =0,
         x:int          =0,
         backGround:str ="",
         clearAfter:bool=False ) -> str:
    if echo:   curses.echo()
    if cursor: curses.curs_set(1)

    if not text.isspace():
        stdscr.addstr(backGround)
        if useMiddle: anchor(stdscr, f"{text}{end}", x=x, y=y)
        else:         stdscr.addstr(f"{text}{end}")
        stdscr.refresh()
        
    try:    Inp = stdscr.getstr().decode("utf-8")
    except: Inp = ""

    if echo:   curses.noecho()
    if cursor: curses.curs_set(0)
    if clearAfter: stdscr.erase()

    return escapeAnsi(Inp)
