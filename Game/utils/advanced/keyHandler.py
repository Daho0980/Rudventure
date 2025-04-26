import os      ; import    curses
import asyncio ; import threading

from Assets.data.totalGameStatus       import key
from Game.core.system                  import infoWindow as iWin
from Game.core.system.logger           import addLog
from Game.entities                     import player
from Game.entities.player.statusEffect import indexConverter
from Game.utils.graphics               import level
from Game.utils.system.sound           import play

from Assets.data import (
    totalGameStatus as s,
    lockers         as l,

    color
)

cc = color.cColors


def add() -> None:
    async def interactions(stdscr):
        while s.main:
            if l.jpsf:
                k = stdscr.getch()
                
                # region Move
                if k != -1:
                    if not l.pause:
                        if s.recordKey: addLog(f"keyCode : {k}", colorKey='Y')
                        if k in [key.up, key.down, key.left, key.right]:
                            match s.playerMode:
                                case "normal":  player.move(k)
                                case "observe": player.observe(k)

                        match k:
                            # region UI
                            case key.dungeonMap:
                                s.showDungeonMap = 0 if s.showDungeonMap else 1
                                play("soundEffects", "smash")

                            case key.debug:
                                s.debug = False if s.debug else True
                                play("soundEffects", "smash")
                                addLog(f"{cc['fg']['B1']}디버그 모드{cc['end']}가 {['꺼', '켜'][s.debug]}졌습니다.", colorKey='N')

                            case key.keyRecord:
                                s.recordKey = False if s.recordKey else True
                                play("soundEffects", "smash")
                                addLog(f"{cc['fg']['B1']}키 기록 모드{cc['end']}가 {['꺼', '켜'][s.recordKey]}졌습니다. 이제부터 {cc['fg']['Y']}입력된 모든 키{cc['end']}는 게임 로그에 표시됩니다.", colorKey='N')

                            case key.statusUIDesign:
                                s.statusDesign = 0 if s.statusDesign else 1
                                play("soundEffects", "smash")
                                addLog(f"스탯 창 디자인이 {cc['fg']['Y']}{['콤팩트', '코지'][s.statusDesign]}{cc['end']}로 변경되었습니다.", colorKey='N')

                            case key.cameraMove:
                                s.dynamicCameraMoving = 0 if s.dynamicCameraMoving else 1
                                play("soundEffects", "smash")
                                addLog(f"{cc['fg']['B1']}다★이☆나★믹 카☆메★라 무☆빙{cc['end']}이 {['꺼', '켜'][s.dynamicCameraMoving]}졌습니다.", colorKey='N')

                            case key.openChat:
                                os.system(f"osascript -e 'tell application \"Terminal\" to do script \"{s.TFP}runChat.command\"' >/dev/null 2>&1")
                                os.system("osascript -e 'tell application \"Terminal\" to set bounds of front window to {0, 0, 600, 1000}'")
                                play("soundEffects", "check")
                                addLog(f"{cc['fg']['Y']}Rudventure Commandline{cc['end']}은 별도의 창에서 열립니다.", colorKey='N')

                            # region Sound
                            case key.volumeDown|key.mute|key.volumeUp:
                                sound    = "check"
                                
                                if   k==key.volumeDown and s.volume:     s.volume -= 5
                                elif k==key.volumeUp   and s.volume<100: s.volume += 5
                                elif k==key.mute:
                                    l.useSound = False if l.useSound else True
                                    sound      = "block"

                                charType = () if l.useSound else (".", "x", "Y", "X")

                                play("soundEffects", sound)
                                iWin.add(
                                    f"{cc['fg']['R']}◎{cc['end']}",
                                    f"{cc['fg']['B1']}음량 조절{cc['end']}",
                                    f"   [ {cc['fg']['Y']}{level(s.volume, 20, charType)}{cc['end']} ]   "
                                )
                                
                            # region System
                            case key.whistle: player.whistle()
                            case key.playerMode:
                                s.playerMode = "observe" if s.playerMode=="normal" else "normal"
                                
                                color = {"observe":cc['fg']['Y'], "normal":cc['fg']['L']}[s.playerMode]
                                play("soundEffects", "check")
                                addLog(
                                    f"플레이어 모드가 {color}{s.playerMode}{cc['end']}로 변경되었습니다.",
                                    colorKey={"observe":"Y", "normal":"L"}[s.playerMode]
                                )

                            case key.slot1|key.slot4|\
                            key.slot2|key.slot5|\
                            key.slot3|key.slot6:
                                if len(s.inventory['cells'])>=k-48 and not s.inventory['cells'][k-49]['disabled']:
                                    if k-49 != s.inventory['pointer']:
                                        s.inventory['pointer'] = k-49
                                        play("soundEffects", "check")
                                        
                                else: play("soundEffects", "block")
                            
                            case key.SE1|key.SE2|key.SE3|\
                            key.SE4|key.SE5|key.SE6|\
                            key.SE7|key.SE8|key.SE9:
                                effectIndex = indexConverter(k)

                                if len(s.statusEffect['line']) >= s.statusEffect['pointer']+effectIndex+1:
                                    play("soundEffects", "check")
                                    target = s.statusEffect['line'][s.statusEffect['pointer']+effectIndex]
                                    
                                    iWin.add(
                                        target['icon'],
                                        target['name'],
                                        explanation=target['description']+f"\n\n남은 틱 : {cc['fg']['Y']}{target['tick']}{cc['end']}"
                                    )
                                
                                elif not len(s.statusEffect['line']):
                                    iWin.add(
                                        f"{cc['fg']['R']}X{cc['end']}",
                                        f"{cc['fg']['R']}활성화된 효과 없음{cc['end']}"
                                    )

                                else: play("soundEffects", "block")

                            case key.SEUP:
                                if len(s.statusEffect['line']) >= s.statusEffect['pointer']+9:
                                    s.statusEffect['pointer'] += 9
                                else: s.statusEffect['pointer'] = 0
                            
                            case key.SEDOWN:
                                if s.statusEffect['pointer'] and s.statusEffect['pointer']%9==0: s.statusEffect['pointer'] -= 9
                                else:
                                    if len(s.statusEffect['line']) > 9:
                                        s.statusEffect['pointer'] = (len(s.statusEffect['line'])//9)*9
                                    else: s.statusEffect['pointer'] = 0

                    if k == key.pause:
                        l.pause     = False if l.pause else True
                        s.currFrame = 1/3   if l.pause else s.frame

                        play("soundEffects", "smash")
                
                await asyncio.sleep(0.005)

            else: await asyncio.sleep(1)

    threading.Thread(
        name  ="keyHandler",
        target=lambda: curses.wrapper(
            lambda stdscr: asyncio.run(interactions(stdscr))
        )
    ).start()
