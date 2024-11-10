import curses
import random

from Assets.data import status as s

from Game.utils.graphics import (
    escapeAnsi,
    anchor
)


def cinp(stdscr,
         text:str      ="",
         end:str       ='',
         echo:bool     =True,
         cursor:bool   =False,
         useMiddle:bool=True,
         y:int         =0,
         x:int         =0,
         backGround:str=""    ) -> str:
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

    return escapeAnsi(Inp)

def placeRandomBlock(block:str,
                     ID:int,
                     blockType:int,
                     y:list[int],
                     x:list[int],
                     allowedBlocks:list[int]) -> None:
    """
    방에서 블럭 등을 랜덤하게 배치할 수 있게 만든 함수

    `block`(char)      : 랜덤하게 배치될 블럭의 아이콘, 무조건 기입해야 됨
    `y`(list)          : 방의 y 최솟값과 최댓값 데이터를 포함함, 무조건 기입해야 함
        ex) `y` = `[최솟값, 최댓값]`

    `x`(list)          : 방의 x 최솟값과 최댓값 데이터를 포함함, 무조건 기입해야 함
        ex) `x` = `[최솟값, 최댓값]`

    `allowedBlocks`(list) : 블럭 랜덤 설치 시 놓을 수 있는 블럭 설정, 무조건 기입해야 함
    """
    while 1:
        Ry, Rx = random.randrange(y[0], y[1]), random.randrange(x[0], x[1])
        if s.Dungeon[s.Dy][s.Dx]['room'][Ry][Rx]["id"] not in allowedBlocks: continue
        break
        
    s.Dungeon[s.Dy][s.Dx]['room'][Ry][Rx] = {"block":block, "id":ID, "type":blockType}

# def upgradeStatus():
#     print(f"{s.markdown([2, 3])}Enter를 한 번 눌러주세요{cc['end']}")
#     selectStat = selector.main("올릴 스탯을 선택해주세요", {"체력 증가":"체력의 최대치가 1 증가합니다.", "방어력 증가":"방어력의 최대치가 1 증가합니다.","공격력 증가":"공격력이 1 상승합니다."}, [1,0,255,10], '@')
#     if selectStat == 1:
#         s.Mhp += 1
#         if s.Mhp < s.hp: s.hp += 1
#     elif selectStat == 2:
#         s.Mdf += 1
#         if s.Mdf < s.df: s.df += 1
#     else: s.atk += 1
    
#     if random.randrange(1,4) == 3:
#         if s.hp < s.Mhp and s.Mhp - s.hp == 1: s.hp += 1
#         elif s.hp < s.Mhp and s.Mhp - s.hp >= 2: s.hp += random.randrange(1,3)

#     if s.Mdf < s.df: s.df += 1