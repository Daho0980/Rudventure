# -*- coding: utf-8 -*-
import curses
import time, random
from   cusser      import Cusser

from Game.core.system                           import discordPresence, quests, logger
from Game.entities                              import entity, player
from Game.entities.player                       import event, checkStatus
from Game.scenes                                import mainSettings, mainMenu
from Game.utils.advanced                        import DungeonMaker, keyHandler
from Game.utils.advanced.Rudconverter           import save
from Game.utils.graphics                        import escapeAnsi, anchor
from Game.utils.modules                         import Textbox, cSelector
from Game.utils.system                          import roomManager
from Game.utils.system.sound                    import play
from Game.utils.system.roomManager.interactions import placeRandomOrbs

from Assets.data import (
    comments,
    lockers,
    status,
    color
    )
from Game.utils.graphics import (
    stageRenderer,
    displayRenderer
)

c, s, l        = comments, status, lockers
pev, cs        = event, checkStatus
p, tb, dgm, kh = player, Textbox, DungeonMaker, keyHandler
ent            = entity
q              = quests
cc             = color.cColors
dcp            = discordPresence


stdscr = Cusser(curses.initscr())

def playerChecker() -> None:
    if not l.isDying:
        cs.defCheck()
        cs.hpCheck()
        cs.curseCheck()

def gameChecker(stdscr) -> None:
    if s.main == 1:
        stdscr.clear(); stdscr.refresh()
        l.jpsf = 0
        if s.hp<=0 or s.hunger<=0:
            dcp.update(
                large_image="rudventure-icon1",
                details    ="사망",
                state      =f"사인 : {escapeAnsi(s.DROD[0])}"
            )

            s.killAll = True
            comment   = random.choice(c.defeatComments["CO"if s.lvl>=s.Mlvl else"HL"if s.hp<=0 else"HUL"])
            stdscr.nodelay(False)

            play("system", "defeat")
            _, bx, deadSign = tb.TextBox(
                    f"{cc['fg']['F'] if s.lvl>=s.Mlvl else cc['fg']['R']}   사 망 하 셨 습 니 다   \n\n   {cc['fg']['F'] if s.lvl>=s.Mlvl else cc['fg']['R']}\"{comment}\"   ",
                    Type        ="middle",
                    inDistance  =1,
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    LineType    ="bold",
                    coverColor  =cc['fg']['F'] if s.lvl>=s.Mlvl else cc['fg']['R'],
                    returnSizeyx=True
                    )
            y, x = anchor(
                stdscr,
                deadSign,
                    addOnyx    =[-4, 1],
                    returnEndyx=True
                )
            y -= 1 # type: ignore

            FBS  = (18-int(bx/2)) # type: ignore
            FBSA = f"\033[{f'{FBS}D'if FBS>0 else f'{abs(FBS)}C'}"
            
            stdscr.refresh()
            import Game.core.system.deathLogWriter

            time.sleep(1)
            achievements = {
                "            이름" : [s.lightName,                                1],
                "            사인" : [f"{s.DROD[0]}",                             2],
                "       내려간 층" : [f"{cc['fg']['Y']}{s.stage}{cc['end']}",     1],
                "  죽인 편린의 수" : [f"{cc['fg']['R']}{s.killCount}{cc['end']}", 1],
                "받은 저주의 강도" : [f"{cc['fg']['F']}{s.lvl}{cc['end']}",       1]
            }
            achievementsValues = list(achievements.values())
            for num, text in enumerate(achievements):
                play("soundEffects", "smash")
                stdscr.addstr(f"\033[{x-FBS};{y}H{text} : {achievementsValues[num][0]}\n"); stdscr.refresh() # type: ignore

                time.sleep(0.2)
                y += achievementsValues[num][1]
                curses.flushinp()
            theChoice:int = cSelector.main(
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
            exit(0 if theChoice-1 else 1)

        else:
            dcp.update(
                large_image="rudventure-icon1",
                details    =f"나락",
                state      ="더 깊은 곳으로 이동 중...",
            )
            play("system", "clear")
            anchor(
                stdscr,
                tb.TextBox(
                    f"   {cc['fg']['L']}지 배   성 공{cc['end']}   \n\n   {cc['fg']['L']}\"{random.choice(c.victoryComments[int((s.hp/s.Mhp)*3)])}{cc['fg']['L']}\"{cc['end']}   ",
                    Type        ="middle",
                    inDistance  =1,
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    LineType    ="bold",
                    coverColor  =cc['fg']['L'],
                    )
                ); stdscr.refresh()
            logger.clear()
            s.clearEntity = True;  time.sleep(0.6)
            s.clearEntity = False; time.sleep(1.9)
            stdscr.clear(); stdscr.refresh()


curses.noecho()
curses.curs_set(0)

dcp.update(
    large_image="rudventure-in_settings1",
    details    ="메인 메뉴",
    state      ="탐색 중",
    start      =int(time.time())
)
mainMenu.main(stdscr)

dcp.update(
    large_image="rudventure-icon1",
    details    ="메인 메뉴",
    state      ="미궁 입장 중"
)
if s.name == "":
    mainSettings.main(stdscr)
    p.set()
    if s.ezMode:
        s.hp     *= 2
        s.df     *= 2
        s.atk    *= 5
        s.hunger *= 2

        s.Mhp       = s.hp
        s.Mdf       = s.df
        s.MFairWind *= 2

        s.critRate   *= 2
        s.critDMG    *= 2
        s.evasionRate = 80
else: mainSettings.presetted()

stdscr.nodelay(True)
kh.add()
from Game.core.system import soliloquy

while s.main:
    dcp.update(
        large_image="rudventure-icon1",
        details    ="메인 메뉴",
        state      ="나락 입장 중"
    )
    
    if s.cowardMode: s.entitySaveTrigger = True

    s.MFairWind += 10
    s.fairWind   = random.randrange(1, s.MFairWind+1)
    
    s.Dungeon = dgm.DungeonMaker()

    p.start()
    placeRandomOrbs()

    if not s.stage and not s.isLoadfromBody and s.name.lower() in ["업로드", "upload"]:
        entity.addAnimal(200, 10, 1, 3, 6, name="구름이", color=[cc['fg']['W'],'W'], friendly=True, MCBF=True, SICR=True, extraData={"loyalty":10})
    if s.isLoadfromBody:
        entity.loadEntities()
    
    stageRenderer.showStage(
        stdscr,
        f"지 하   {cc['fg']['R']}-{s.stage+1}{cc['end']}   층"
        )

    if not s.stage:
        p.say(
            random.choice(
                c.loadsaveStartComments\
                    if  s.cowardMode
                    and s.isLoadfromBody\
                else c.startCommentsWithCowardmode\
                    if s.cowardMode\
                else c.startComments
            )
        )

    dcp.update(
        large_image="rudventure-in_battle1",
        details    ="나락",
        state      =f"제 -{s.stage+1}층",
        start      =int(time.time())
    )

    if s.cowardMode:
        save()
        s.entitySaveTrigger = False

    s.stage += 1

    l.jpsf       = 1
    quickStarter = 0

    curses.flushinp()
    while not q.quest():
        if s.hp<=0 or s.hunger<=0 or not s.main: break
        if l.jpsf:
            displayRenderer.render(stdscr, s.Dungeon[s.Dy][s.Dx]['room'])
            if not l.pause:
                playerChecker()

                if not quickStarter:
                    stdscr.refresh()
                    quickStarter = 1
                roomManager.main()
            time.sleep(s.frame)
        else: time.sleep(1)

    if s.hunger<=0: s.DROD = [f"{cc['fg']['Y']}아사{cc['end']}", 'Y']
    gameChecker(stdscr)