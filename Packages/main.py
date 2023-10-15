# -*- coding: utf-8 -*-
import curses
import time, random
from   cusser                                  import Cusser
from   Packages.lib                            import player,       quests
from   Packages.lib.data                       import comments,     lockers,         status
from   Packages.lib.modules                    import logger,       makeNewListener, Textbox
from   Packages.lib.system                     import DungeonMaker, mainSettings
from   Packages.lib.system.globalFunc          import entity,       graphic,         idRelated, osRelated, system
from   Packages.lib.system.globalFunc.sound    import play

stdscr = curses.initscr()
if not isinstance(stdscr, Cusser):
    stdscr = Cusser(stdscr)

quickStarter            = 0
roomNames               = [
    "\033[31mStart\033[0m",
    "Normal Room",
    "\033[32mEvent Room\033[0m",
    "\033[33mTreasure Room\033[0m",
    "\033[34mExit\033[0m"
    ]

c, s, l                 = comments,      status,  lockers
p, t, dgm, mnl          = player.player, Textbox, DungeonMaker, makeNewListener
ent, grp, idr           = entity,        graphic, idRelated
q                       = quests

s.s                     = osRelated.slash()


def deadReason():
    if   s.hp     <= 0: s.deadReason = f"{s.cColors['fg']['R']}hp{s.cColors['end']} 부족"
    elif s.hunger <= 0: s.deadReason = f"{s.cColors['fg']['Y']}허기{s.cColors['end']} 부족"

def playerChecker():
    if s.df > 0   : s.dfCrack = 0

    if s.hp <= int(s.Mhp*0.3) and s.hpLow == False:
        s.hpLow = True
        play(f"hp_low")
        logger.addLog(f"\"{random.choice(c.lowHpComment)}\"")
    elif int((s.hp / s.Mhp) * 100) > 30: s.hpLow = False

def gameChecker(stdscr):
    if s.main == 1:
        stdscr.clear(); stdscr.refresh()
        l.jpsf = 0
        if s.hp <= 0 or s.hunger <= 0:
            s.killAll = True
            stdscr.nodelay(False)
            comment = random.choice(c.defeatComment[s.deadReason])
            play("defeat")
            stdscr.addstr(f"{s.cColors['fg']['R']}")
            stdscr.addstr(t.TextBox(f"   사 망 하 셨 습 니 다   \n\n   \"{comment}\"   ", Type="middle", inDistance=1, outDistance=1, AMLS=True, endLineBreak=True, LineType="bold"))
            stdscr.addstr(s.cColors['end']); stdscr.refresh()
            time.sleep(2.5)
            Achievements = {
                "이름"             : s.lightName,
                "사인"             : f"{s.deadReason}\n",
                "내려간 깊이"      : f"{s.cColors['fg']['Y']}{s.stage}{s.cColors['end']}",
                "최대 레벨"        : f"{s.cColors['fg']['F']}{s.lvl}{s.cColors['end']}",
                "죽인 몬스터 횟수" : f"{s.cColors['fg']['R']}{s.killCount}{s.cColors['end']}"
            }
            for num, text in enumerate(Achievements):
                stdscr.addstr(f"{text} : {list(Achievements.values())[num]}\n"); stdscr.refresh()
                play("smash")
                time.sleep(0.2)
            play("smash")
            system.cinp(stdscr, "\nEnter를 눌러 윤회 끝내기__", echo=False)
            play("crack")
            curses.endwin()
            s.main = 0

        else:
            play("clear")
            stdscr.addstr(s.cColors['fg']['L'])
            stdscr.addstr(t.TextBox(f"   지 배   성 공   \n\n   \"{random.choice(c.victoryComment)}\"   ", Type="middle", inDistance=1, outDistance=1, AMLS=True, endLineBreak=True, LineType="bold"))
            stdscr.addstr(s.cColors['end']); stdscr.refresh()
            time.sleep(2.5)
            stdscr.clear(); stdscr.refresh()

curses.noecho()
curses.curs_set(0)

mainSettings.init(stdscr)
stdscr.nodelay(True)
p.set()

mnl.newAddListener()

while s.main:
    if not s.stage: SN = f"{s.cColors['fg']['L']}지 상{s.cColors['end']}"
    else:           SN = f"{s.cColors['fg']['R']}{s.stage} 번 째   나 락{s.cColors['end']}"
    s.stage  += 1
    s.Dungeon = dgm.DungeonMaker()

    p.start(4, 4, 6, 6)
    system.roomChecker.placeRandomOrbs()
    grp.showStage(
        stdscr,
        f"{s.cColors['fg']['R']}- {s.stage}{s.cColors['end']}",
        stageName=SN
        )

    l.jpsf = 1
    while not q.quest():
        if s.hp <= 0 or s.hunger <= 0 or s.main != 1: break
        if l.jpsf:
            stdscr.erase()
            playerChecker()
            grp.fieldPrint(stdscr, s.Dungeon[s.Dy][s.Dx]['room'])
            if not quickStarter: stdscr.refresh(); quickStarter += 1
            system.roomChecker.main()
            if s.frame > 0: time.sleep(1/s.frame)
        else: time.sleep(1)
    quickStarter = 0
    deadReason()
    gameChecker(stdscr)
