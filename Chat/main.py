import time
import curses
import threading

from . import (
    status        as s,
    clientSet     as cs,
    mainFunctions as mf,

    command
)


def renderChat():
    global chatWin, inputWin

    while True:
        chatWin.clear()

        for i, chat in enumerate(s.history['chat'][-(CWH-2):]):
            match len(chat):
                case 1: chatWin.addstr(i+1, 1, f"{chat[0][:x]}")
                case 2:
                    chatWin.addstr(i+1, 1,
                        f"{chat[0]} : {chat[1][:(x-len(chat[0]))]}"\
                            if chat[0]\
                        else chat[1][:(x-len(chat[0]))]             )
                
                case 3:
                    chatWin.addstr(i+1, 1,
                        f"{chat[0]} : {chat[1][:(x-len(chat[0]))]}"\
                            if chat[0]\
                        else chat[1][:(x-len(chat[0]))],
                        curses.color_pair(s.c[chat[2]])             )

        if s.serverConnection:
            if s.client.isConnect:
                systemOut = mf.receiveChat()
                if systemOut == "excepted": s.client.isConnect = False
        chatWin.refresh()

        inputWin.refresh()
        time.sleep(0.025)

while 1:
    try:
        port = input("포트를 입력해주세요 (\033[;38;5;11m'chat only'\033[0m를 입력해 오프라인 모드 진입 가능): \033[;38;5;11m")
        print("\033[0m", end="")
        if port.lower() == "chat only":
            s.serverConnection = False
            break

        port = int(port)
    except:
        print("님 제대로 입력하셈;", end='\n\n')
    else: break

if s.serverConnection:
    s.client = cs.Client(port=port)

stdscr = curses.initscr()
curses.curs_set(1)
stdscr.nodelay(True)

# region init color
if curses.has_colors():
    curses.start_color()

    curses.init_pair(1, curses.COLOR_BLACK,   curses.COLOR_BLACK) # B
    curses.init_pair(2, curses.COLOR_RED,     curses.COLOR_BLACK) # M
    curses.init_pair(3, curses.COLOR_GREEN,   curses.COLOR_BLACK) # G
    curses.init_pair(4, curses.COLOR_YELLOW,  curses.COLOR_BLACK) # O
    curses.init_pair(5, curses.COLOR_BLUE,    curses.COLOR_BLACK) # N
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # P
    curses.init_pair(7, curses.COLOR_CYAN,    curses.COLOR_BLACK) # T
    curses.init_pair(8, curses.COLOR_WHITE,   curses.COLOR_BLACK) # S
        
    curses.init_pair(9, 8,   curses.COLOR_BLACK) # G1
    curses.init_pair(10, 9,  curses.COLOR_BLACK) # R
    curses.init_pair(11, 10, curses.COLOR_BLACK) # L
    curses.init_pair(12, 11, curses.COLOR_BLACK) # Y
    curses.init_pair(13, 12, curses.COLOR_BLACK) # B1
    curses.init_pair(14, 13, curses.COLOR_BLACK) # F
    curses.init_pair(15, 14, curses.COLOR_BLACK) # A
    curses.init_pair(16, 15, curses.COLOR_BLACK) # W

    curses.init_pair(17, 92, curses.COLOR_BLACK) # CR
    curses.init_pair(18, 32, curses.COLOR_BLACK) # CU

    s.c = {
        "B"  : 1,  "M" : 2,  "G" : 3,  "O" : 4,
        "N"  : 5,  "P" : 6,  "T" : 7,  "S" : 8,
        "G1" : 9,  "R" : 10, "L" : 11, "Y" : 12,
        "B1" : 13, "F" : 14, "A" : 15, "W" : 16,
        "CR" : 17, "CU" : 18,
        "E"  : 0
    }

# region init screen
y, x = stdscr.getmaxyx()

CWH     = y-3
chatWin = stdscr.subwin(CWH, x, 0, 0)

inputWin = stdscr.subwin(3, x, CWH, 0)
# inputWin.keypad(True)

threading.Thread(
    target=renderChat,
    daemon=True       ).start()

for i in list(s.c.keys()):
    mf.addChat(["system", "colorTest", i])
mf.addChat(["system", "색상 테스트 완료", 'Y'])
if s.serverConnection:
    mf.addChat(["system", f"'{s.client.host}:{s.client.port}'로 연결되었습니다.", 'Y'])
else:
    mf.addChat(["system", f"이 프로그램은 이제 게임과 독립된 시스템으로 작동합니다.", 'Y'])


while True:
    inputWin.clear()
    inputWin.box()
    inputWin.addstr(1, 1, "> ")
    inputWin.addstr(1, 3,
        ''.join(s.inputText)[max(0, (len(s.inputText)-(inputWin.getmaxyx()[1]-5))):],
        curses.color_pair(s.c[
            'R'
                if  s.inputText
                and s.inputText[0]==s.prefix
                and ''.join(s.inputText).split()[0][1:] not in s.commands['total'].keys()
            else 'F'
                if  s.inputText
                and s.inputText[0]==s.prefix
            else 'Y'
        ]
    ))

    try:
        key = mf.escapeAnsi(inputWin.get_wch())
    except curses.error:
        continue

    if key and isinstance(key, str):
        if key == '\n': # Enter
            if s.inputText:
                if s.inputText[0] == '/':
                    command.main((''.join(s.inputText).split(' ')))
                else:
                    mf.sendChat(["client", ''.join(s.inputText)])
            s.inputText = []

        elif key in ('\b', '\x7f', curses.KEY_BACKSPACE): # Backspace
            s.inputText = s.inputText[:-1]

        else: s.inputText.append(key)
