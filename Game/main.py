# -*- coding: utf-8 -*-
import curses ; import random
from   cusser   import Cusser
from   time     import sleep, perf_counter

from .                   import _main_extended as ME
from .core.system.io     import logger
from .core.system.state  import quests as q
from .entities           import player
from .entities.player    import checkStatus           as cs
from .pages              import mainSettings, mainMenu
from .utils.advanced     import DungeonMaker, keyHandler
from .utils.graphics     import escapeAnsi, anchor, renderer, stage
from .utils.modules      import Textbox, cSelector
from .utils.system       import roomManager
from .utils.system.sound import play

from Assets.data import (
    totalGameStatus as s,
    comments        as c,
    flags           as f,

    color
)
from .core.system.integration import (
    discordPresence as dp
)
from .utils.advanced.Rudconverter import (
    save
)
from .utils.system.roomManager.interactions import (
    randPlaceOrb
)


stdscr = Cusser(curses.initscr())

cc = color.cColors

def playerChecker() -> None:
    if not f.isDying:
        cs.defCheck    ()
        cs.hpCheck     ()
        cs.curseCheck  ()
        cs.ashChipCheck()

def gameChecker(stdscr) -> None:
    if s.main == 1:
        stdscr.clear(); stdscr.refresh()
        f.jpsf = 0b0

        if s.hp<=0 or s.hgr<=0:
            dp.load(
                large_image="rudventure-icon1",
                small_image=s.playerColor[1],
                details    ="사망",
                state      =f"사인 : {escapeAnsi(s.DROD[0])}"
            ); dp.update()

            f.killAll = True
            comment   = random.choice(c.defeat["CO"if s.lvl>=s.Mlvl else"HL"if s.hp<=0 else"HUL"])

            stdscr.nodelay(False)

            play("system", "defeat")
            _, bx, deadSign = Textbox.TextBox(
                f"{cc['fg']['F'if s.lvl>=s.Mlvl else'R']}   사 망 하 셨 습 니 다   \n\n   {cc['fg']['F'if s.lvl>=s.Mlvl else 'R']}\"{comment}\"   ",

                Type        ="middle",
                inDistance  =(1, 0b11),
                outDistance =(1, 0b11),
                AMLS        =True,
                endLineBreak=True,
                LineType    ="bold",
                coverColor  =cc['fg']['F'if s.lvl>=s.Mlvl else'R'],
                returnSizeyx=True
            )

            y, x = map(
                lambda d:d[0]+d[1], # type: ignore
                zip(
                    anchor(stdscr,
                        deadSign,
                        addOnyx    =[-4, 1],
                        returnEndyx=True
                    ),
                    [-1,0]
                )
            )

            FBS  = (18-int(bx/2)) # type: ignore
            FBSA = f"\033[{f'{(FBS)}D'if FBS>0 else f'{abs(FBS)}C'}"
            
            stdscr.refresh()
            if s.gameRecord: import Game.core.system.io.deathLogWriter

            sleep(1)
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

                stdscr.addstr(f"\033[{x-FBS};{y}H{text} : {achievementsValues[num][0]}\n")
                stdscr.refresh()
                sleep(0.2)

                y += achievementsValues[num][1]

            curses.flushinp()
            theChoice = cSelector.main(
deadSign+
f"""
{FBSA}            이름 : {s.lightName}
{FBSA}            사인 : {s.DROD[0]}

{FBSA}       내려간 층 : {cc['fg']['Y']}{s.stage}{cc['end']}
{FBSA}  죽인 편린의 수 : {cc['fg']['R']}{s.killCount}{cc['end']}
{FBSA}받은 저주의 강도 : {cc['fg']['F']}{s.lvl}{cc['end']}
""",
                [(cc['fg']['R'], "{ 숙명을 거부하기 }"), "{ 숙명을 이어가기 }"],
                [1,0,255,10],
                '@>'
            )

            s.main = 0
            curses.endwin()
            exit((theChoice-1)^1)

        else:
            dp.quickLoad('goDeeper')
            dp.update()

            play("system", "clear")
            anchor(stdscr,
                Textbox.TextBox(
                    f"   {cc['fg']['L']}지 배   성 공{cc['end']}   \n\n   {cc['fg']['L']}\"{random.choice(c.victory[int((s.hp/s.Mhp)*3)])}{cc['fg']['L']}\"{cc['end']}   ",

                    Type        ="middle",
                    inDistance  =(1, 0b11),
                    outDistance =(1, 0b11),
                    AMLS        =True,
                    endLineBreak=True,
                    LineType    ="bold",
                    coverColor  =cc['fg']['L'],
                )
            ); stdscr.refresh()
            
            logger.clear()
            f.clearEntity = True ; sleep(0.6)
            f.clearEntity = False; sleep(1.9)
            stdscr.refresh()


curses.noecho()
curses.curs_set(0)

dp.quickLoad('inMenu')
dp.update()

mainMenu.main(stdscr)

if s.name == "":
    mainSettings.main(stdscr)
    player      .set ()
    if s.cowardMode:
        s.hp  *= 2
        s.df  *= 2
        s.atk *= 5
        s.hgr *= 2

        s.Mhp = s.hp
        s.Mdf = s.df

        s.critRate   *= 2
        s.critDMG    *= 2
        s.evasionRate = 80
else: mainSettings.presetted()

stdscr.nodelay(True)


keyHandler.add()
from Game.core.system.state import (
    frameCounter,
    exaltation,
    monologue
) # 스레드 연결

if not dp.isConnected:
    logger.addLog(
        f"{cc['fg']['Y']}인터넷{cc['end']}에 연결되어 있지 않습니다. 게임을 다시 시작할 때까지 {cc['fg']['B1']}DiscordPresence{cc['end']}가 사용되지 않습니다.",
        colorKey='B1'
    )

else: logger.addLog(f"포트는 {cc['fg']['L']}{s.port}{cc['end']}입니다.", colorKey='Y')


while s.main:
    dp.quickLoad('enter')
    dp.update()
    
    if s.bodyPreservationMode and s.gameRecord:
        f.saveEntity = True
    
    s.Dungeon = DungeonMaker.DungeonMaker()

    player.start()
    randPlaceOrb()

    ME.spawnCompanion()
    
    stage.showStage(stdscr,
        f"{cc['fg']['R']}-{s.stage+1}{cc['end']}   층"
    )

    ME.startComment()

    dp.quickLoad('inDungeon')
    dp.update()

    if f.saveEntity:
        save()
        f.saveEntity = False

    s.stage += 1

    f.jpsf       = 0b1
    quickStarter = 0

    curses.flushinp()
    while not q.quest():
        if s.hp<=0 or s.hgr<=0 or not s.main: break
        if f.jpsf:
            a_render = perf_counter()
            renderer.render(stdscr)
            if not f.pause:
                playerChecker()

                if not quickStarter:
                    stdscr.refresh()
                    quickStarter = 1

                roomManager.raiseRoomEvent()

            sleep(max((s.currFrame-(perf_counter()-a_render)), 0))
            
        else: sleep(1)

    if s.hgr <= 0: s.DROD = [f"{cc['fg']['Y']}아사{cc['end']}", 'Y']
    gameChecker(stdscr)