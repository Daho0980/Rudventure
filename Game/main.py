# -*- coding: utf-8 -*-
import curses
import time, random
from   cusser      import Cusser

from   Assets.data                      import comments, lockers, status, color
from   Game.core.system                 import quests, logger
from   Game.entities                    import entity, player
from   Game.scenes                      import mainSettings, mainMenu
from   Game.utils                       import graphic
from   Game.utils.advanced              import DungeonMaker, keyHandler
from   Game.utils.advanced.Rudconverter import save
from   Game.utils.modules               import Textbox, cSelector
from   Game.utils.system                import roomChecker


stdscr = Cusser(curses.initscr())

quickStarter            = 0
c, s, l                 = comments, status, lockers
p, t, dgm, kh          = player, Textbox, DungeonMaker, keyHandler
ent, grp                = entity, graphic
q                       = quests
cc                      = color.cColors

def playerChecker():
    if s.df > 0: s.dfCrack = 0

    if s.hp <= int(s.Mhp*0.3) and s.hpLow == False:
        s.hpLow = True
        logger.addLog(f"{cc['fg']['L']}\"{random.choice(c.lowHpComment)}\"{cc['end']}")
    elif int((s.hp / s.Mhp) * 10) > 3: s.hpLow = False

def gameChecker(stdscr):
    if s.main == 1:
        stdscr.clear(); stdscr.refresh()
        l.jpsf = 0
        if s.hp <= 0 or s.hunger <= 0:
            s.killAll = True
            comment   = random.choice(c.defeatComment[f"hp 부족" if s.hp <= 0 else f"허기 부족"])
            stdscr.nodelay(False)

            y, x = grp.addstrMiddle(
                stdscr,
                cc['fg']['R']+t.TextBox(
                    f"   사 망 하 셨 습 니 다   \n\n   \"{comment}\"   ",
                    Type        ="middle",
                    inDistance  =1,
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    LineType    ="bold"
                    )+cc['end'],
                    addOnCoordinate=[-5, 0],
                    returnEndyx=True
                )
            y -= 1 # type: ignore
            stdscr.refresh()
            import Game.core.system.deathLogWriter

            time.sleep(1)
            achievements = {
                "이름"             : [s.lightName,                                0],
                "사인"             : [f"{s.DROD[0]}",                             1],
                "내려간 층"        : [f"{cc['fg']['Y']}{s.stage}{cc['end']}",     0],
                "죽인 편린의 수"   : [f"{cc['fg']['R']}{s.killCount}{cc['end']}", 0],
                "받은 저주의 강도" : [f"{cc['fg']['F']}{s.lvl}{cc['end']}",       0]
            }
            achievementsValues:list[list[str|int]] = list(achievements.values())
            for num, text in enumerate(achievements):
                stdscr.addstr(f"\033[{x};{y}H{text} : {achievementsValues[num][0]}\n"); stdscr.refresh()
                time.sleep(0.2)
                y += (1+achievementsValues[num][1]) # type: ignore
            the_choice:int = cSelector.main(
                cc['fg']['R']+t.TextBox(
                    f"   사 망 하 셨 습 니 다   \n\n   \"{comment}\"   ",
                    Type        ="middle",
                    inDistance  =1,
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    LineType    ="bold"
                    )+cc['end']+
                f"""
이름 : {s.lightName}
사인 : {s.DROD[0]}

내려간 층 : {cc['fg']['Y']}{s.stage}{cc['end']}
죽인 편린의 수 : {cc['fg']['R']}{s.killCount}{cc['end']}
받은 저주의 강도 : {cc['fg']['F']}{s.lvl}{cc['end']}
""",
                ["윤회 끝내기", "살육을 계속 즐기기"],
                [1,0,255,10],
                '@'
                )

            s.main = 0
            curses.endwin()
            exit(0 if the_choice-1 else 1)

        else:
            grp.addstrMiddle(
                stdscr,
                cc['fg']['L']+t.TextBox(
                    f"   지 배   성 공   \n\n   \"{random.choice(c.victoryComment)}\"   ",
                    Type        ="middle",
                    inDistance  =1,
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    LineType    ="bold"
                    )+cc['end']
                ); stdscr.refresh()
            time.sleep(2.5)
            stdscr.clear(); stdscr.refresh()


curses.noecho()
curses.curs_set(0)

mainMenu.main(stdscr)
if s.name == "":
    mainSettings.main(stdscr)
    p.set()
    if s.ezMode: s.atk += 4
else: mainSettings.presetted(stdscr)

stdscr.nodelay(True)
kh.add()

while s.main:
    if s.cowardMode: save()
    s.Dungeon = dgm.DungeonMaker()

    p.start(4, 4, 6, 6)
    roomChecker.placeRandomOrbs()

    grp.showStage(
        stdscr,
        f"{cc['fg']['R']}- {s.stage}{cc['end']}",
        stageName=f"{cc['fg']['R']}지 하   - {s.stage}   층{cc['end']}"
        ); s.stage += 1

    l.jpsf = 1
    while not q.quest():
        if s.hp <= 0 or s.hunger <= 0 or not s.main: break
        if l.jpsf:
            playerChecker()
            grp.fieldPrint(stdscr, s.Dungeon[s.Dy][s.Dx]['room'])
            if not quickStarter: stdscr.refresh(); quickStarter = 1
            roomChecker.main()
            time.sleep(s.frame)
        else: time.sleep(1)
    if s.hunger <= 0: s.DROD = [f"{cc['fg']['Y']}아사{cc['end']}", 'Y']
    gameChecker(stdscr); quickStarter = 0
