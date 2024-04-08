# -*- coding: utf-8 -*-
import curses
import time, random
from   cusser      import Cusser

from Assets.data                                import comments, lockers, status, color
from Game.core.system                           import quests, logger
from Game.entities                              import entity, player
from Game.entities.player                       import event
from Game.scenes                                import mainSettings, mainMenu
from Game.utils                                 import graphic
from Game.utils.advanced                        import DungeonMaker, keyHandler
from Game.utils.advanced.Rudconverter           import save
from Game.utils.modules                         import Textbox, cSelector
from Game.utils.system                          import roomManager
from Game.utils.system.roomManager.interactions import placeRandomOrbs


stdscr = Cusser(curses.initscr())

quickStarter  = 0
c, s, l       = comments, status, lockers
pev           = event
p, t, dgm, kh = player, Textbox, DungeonMaker, keyHandler
ent, grp      = entity, graphic
q             = quests
cc            = color.cColors

def playerChecker():
    if not l.isDying:
        if s.df > 0: s.dfCrack = 0

        if s.hp <= int(s.Mhp*0.3) and not s.hpLow:
            s.hpLow = True
            logger.addLog(f"{cc['fg']['L']}\"{random.choice(c.lowHpComment)}\"{cc['end']}")
        elif int((s.hp / s.Mhp) * 10) > 3: s.hpLow = False
        if s.ashChip>=100:
            s.ashChip -= 100
            s.Mlvl    += 1
            logger.addLog(f"{cc['fg']['G1']}재의 그릇{cc['end']}이 {cc['fg']['F']}1{cc['end']} 개 증가했습니다. (최대 레벨 {cc['fg']['G1']}{s.Mlvl-1}{cc['end']} -> {cc['fg']['F']}{s.Mlvl}{cc['end']})")
        if s.lvl >= s.Mlvl: pev.cursedDeath()

def gameChecker(stdscr):
    if s.main == 1:
        stdscr.clear(); stdscr.refresh()
        l.jpsf = 0
        if s.hp <= 0 or s.hunger <= 0:
            s.killAll = True
            comment   = random.choice(c.defeatComment["CO"if s.lvl>=s.Mlvl else"HL"if s.hp<=0 else"HUL"])
            stdscr.nodelay(False)

            _, bx, deadSign = t.TextBox(
                    f"   사 망 하 셨 습 니 다   \n\n   \"{comment}\"   ",
                    Type        ="middle",
                    inDistance  =1,
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    LineType    ="bold",
                    coverColor=cc['fg']['F'] if s.lvl>=s.Mlvl else cc['fg']['R'],
                    returnSizeyx=True
                    )
            y, x = grp.addstrMiddle(
                stdscr,
                deadSign,
                    addOnCoordinate=[-5, 0],
                    returnEndyx    =True
                )
            y   -= 1 # type: ignore

            FBS  = (18-int(bx/2)) # type: ignore
            FBSA = f"\033[{f'{FBS}D'if FBS>0 else f'{abs(FBS)}C'}"
            
            stdscr.refresh()
            import Game.core.system.deathLogWriter

            time.sleep(1)
            achievements = {
                "            이름" : [s.lightName,                                0],
                "            사인" : [f"{s.DROD[0]}",                             1],
                "       내려간 층" : [f"{cc['fg']['Y']}{s.stage}{cc['end']}",     0],
                "  죽인 편린의 수" : [f"{cc['fg']['R']}{s.killCount}{cc['end']}", 0],
                "받은 저주의 강도" : [f"{cc['fg']['F']}{s.lvl}{cc['end']}",       0]
            }
            achievementsValues:list[list[str|int]] = list(achievements.values())
            for num, text in enumerate(achievements):
                stdscr.addstr(f"\033[{x-FBS};{y}H{text} : {achievementsValues[num][0]}\n"); stdscr.refresh() # type: ignore
                time.sleep(0.2)
                y += (1+achievementsValues[num][1]) # type: ignore
            the_choice:int = cSelector.main(
                deadSign+
                f"""
{FBSA}            이름 : {s.lightName}
{FBSA}            사인 : {s.DROD[0]}

{FBSA}       내려간 층 : {cc['fg']['Y']}{s.stage}{cc['end']}
{FBSA}  죽인 편린의 수 : {cc['fg']['R']}{s.killCount}{cc['end']}
{FBSA}받은 저주의 강도 : {cc['fg']['F']}{s.lvl}{cc['end']}
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
                    f"   지 배   성 공   \n\n   \"{random.choice(c.victoryComment[int((s.hp/s.Mhp)*3)])}\"   ",
                    Type        ="middle",
                    inDistance  =1,
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    LineType    ="bold"
                    )+cc['end']
                ); stdscr.refresh()
            logger.clear()
            s.killAll = True
            time.sleep(0.6)
            s.killAll = False

            time.sleep(1.9)
            stdscr.clear(); stdscr.refresh()


curses.noecho()
curses.curs_set(0)

mainMenu.main(stdscr)
if s.name == "":
    mainSettings.main(stdscr)
    p.set()
    if s.ezMode:
        s.hp  += 10
        s.df  += 5
        s.atk += 4

        s.Mhp += 10
        s.Mdf += 5

        s.critRate += 10
        s.critDMG  += 10
        s.hunger   += 1000
else: mainSettings.presetted(stdscr)

stdscr.nodelay(True)
kh.add()

while s.main:
    if s.cowardMode: save()
    s.Dungeon = dgm.DungeonMaker()

    p.start(4, 4, 6, 6)
    placeRandomOrbs()

    grp.showStage(
        stdscr,
        f"지 하   {cc['fg']['R']}-{s.stage}{cc['end']}   층"
        ); s.stage += 1

    l.jpsf = 1
    while not q.quest():
        if s.hp <= 0 or s.hunger <= 0 or not s.main: break
        if l.jpsf:
            playerChecker()
            grp.fieldPrint(stdscr, s.Dungeon[s.Dy][s.Dx]['room'])
            if not quickStarter: stdscr.refresh(); quickStarter=1
            roomManager.main()
            time.sleep(s.frame)
        else: time.sleep(1)
    if s.hunger <= 0: s.DROD = [f"{cc['fg']['Y']}아사{cc['end']}", 'Y']
    gameChecker(stdscr); quickStarter=0
