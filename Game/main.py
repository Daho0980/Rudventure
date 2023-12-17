# -*- coding: utf-8 -*-
import curses
import time, random
from   cusser                                  import Cusser
from   Game.entities                     import player
from   Game.core.system                  import quests
from   Assets.data                       import comments,     lockers,         status
from   Game.utils.modules                    import Textbox
from Game.core.system                          import logger
from   Game.scenes                             import mainSettings
from   Game.utils.advanced                     import DungeonMaker, makeNewListener
from   Game.utils          import entity,       graphic,         idRelated, system
from   Game.utils.sound    import play

stdscr = curses.initscr()
if not isinstance(stdscr, Cusser): stdscr = Cusser(stdscr)

quickStarter            = 0

c, s, l                 = comments,      status,  lockers
p, t, dgm, mnl          = player.player, Textbox, DungeonMaker, makeNewListener
ent, grp, idr           = entity,        graphic, idRelated
q                       = quests
cc                      = s.cColors

def playerChecker():
    if s.df > 0: s.dfCrack = 0

    if s.hp <= int(s.Mhp*0.3) and s.hpLow == False:
        s.hpLow = True
        play(f"hp_low")
        logger.addLog(f"{cc['fg']['L']}\"{random.choice(c.lowHpComment)}\"{cc['end']}")
    elif int((s.hp / s.Mhp) * 100) > 30: s.hpLow = False

def gameChecker(stdscr):
    if s.main == 1:
        stdscr.clear(); stdscr.refresh()
        l.jpsf = 0
        if s.hp <= 0 or s.hunger <= 0:
            s.killAll = True
            stdscr.nodelay(False)
            s.deadReason = f"{cc['fg']['R']}hp{cc['end']} 부족" if s.hp <= 0 else f"{cc['fg']['Y']}허기{cc['end']} 부족"
            comment      = random.choice(c.defeatComment[s.deadReason])

            play("defeat")
            stdscr.addstr(f"{cc['fg']['R']}")
            y, x = grp.addstrMiddle(
                stdscr,
                t.TextBox(
                    f"   사 망 하 셨 습 니 다   \n\n   \"{comment}\"   ",
                    Type        ="middle",
                    inDistance  =1,
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    LineType    ="bold"
                    ),
                    returnEndyx=True
                )
            y -= 1
            stdscr.addstr(cc['end']); stdscr.refresh()
            time.sleep(2.5)
            Achievements = {
                "이름"             : s.lightName,
                "사인"             : f"{s.deadReason}",
                "내려간 깊이"      : f" {cc['fg']['Y']}{s.stage}{cc['end']}",
                "최대 레벨"        : f"{cc['fg']['F']}{s.lvl}{cc['end']}",
                "죽인 몬스터 횟수" : f"{cc['fg']['R']}{s.killCount}{cc['end']}"
            }
            for num, text in enumerate(Achievements):
                stdscr.addstr(f"\033[{x};{y}H{text} : {list(Achievements.values())[num]}\n"); stdscr.refresh()
                play("smash")
                time.sleep(0.2)
                y += 2 if text == "사인" else 1
            play("smash")
            system.cinp(stdscr, "Enter를 눌러 윤회 끝내기__", echo=False, y=y+2, x=x)

            play("crack")
            s.main = 0
            curses.endwin()
            exit()

        else:
            play("clear")
            stdscr.addstr(cc['fg']['L'])
            grp.addstrMiddle(
                stdscr,
                t.TextBox(
                    f"   지 배   성 공   \n\n   \"{random.choice(c.victoryComment)}\"   ",
                    Type        ="middle",
                    inDistance  =1,
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    LineType    ="bold"
                    )
                )
            stdscr.addstr(cc['end']); stdscr.refresh()
            time.sleep(2.5)
            stdscr.clear(); stdscr.refresh()


curses.noecho()
curses.curs_set(0)

mainSettings.init(stdscr)
stdscr.nodelay(True)
p.set()

mnl.newAddListener()

while s.main:
    if not s.stage: SN = f"{cc['fg']['L']}지 상{cc['end']}"
    else:           SN = f"{cc['fg']['R']}{s.stage} 번 째   나 락{cc['end']}"
    s.stage  += 1
    s.Dungeon = dgm.DungeonMaker()

    p.start(4, 4, 6, 6)
    system.roomChecker.placeRandomOrbs()
    # stdscr.addstr("flag - 1"); stdscr.refresh()
    grp.showStage(
        stdscr,
        f"{cc['fg']['R']}- {s.stage}{cc['end']}",
        stageName=SN
        )

    l.jpsf = 1
    while not q.quest():
        if s.hp <= 0 or s.hunger <= 0 or not s.main: break
        if l.jpsf:
            playerChecker()
            grp.fieldPrint(stdscr, s.Dungeon[s.Dy][s.Dx]['room'])
            if not quickStarter: stdscr.refresh(); quickStarter += 1
            system.roomChecker.main()
            if s.frame > 0: time.sleep(1/s.frame)
        else: time.sleep(1)
    quickStarter = 0
    gameChecker(stdscr)
