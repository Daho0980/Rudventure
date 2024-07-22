import curses
import random
import asyncio
import threading

from Assets.data             import lockers, status, color
from Game.core.system        import blockDescription      as bd
from Game.core.system.logger import addLog
from Game.entities           import player
from Game.utils.system.sound import play


p    = player
l, s = lockers, status
cc   = color.cColors

def add() -> None:
    async def interactions(stdscr):
        while s.main:
            if l.jpsf:
                key = stdscr.getch()
                
                if not l.pause:
                    if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                        match s.playerMode:
                            case "normal":  p.move(key, 1)
                            case "observe": p.observe(key)
                    match key:
                        case 9: # Tab
                            s.showDungeonMap = 0 if s.showDungeonMap else 1
                            play("soundEffects", "smash")
                        case 68: # Shift + d
                            s.debugConsole = False if s.debugConsole else True
                            play("soundEffects", "smash")
                            addLog(f"디버그 모드가 {['꺼', '켜'][s.debugConsole]}졌습니다.")
                        case 83: # Shift + s
                            s.statusDesign = 0 if s.statusDesign else 1
                            play("soundEffects", "smash")
                            addLog(f"스탯 창 디자인이 '{['콤팩트', '코지'][s.statusDesign]}'로 변경되었습니다.")
                        case 66: # Shift + b
                            s.dynamicCameraMoving = 0 if s.dynamicCameraMoving else 1
                            play("soundEffects", "smash")
                            addLog(f"다★이☆나★믹 카☆메★라 무☆빙이 {['꺼', '켜'][s.dynamicCameraMoving]}졌습니다.")
                        case 77: # Shift + m
                            l.useSound = False if l.useSound else True
                            play("soundEffects", "check")
                            addLog(["거기 안 들리는 거 맞죠-??", "이제 잘 들리시나요-??"][l.useSound]
                                   if random.randrange(1,51)==50
                                   else f"음소거{['되었습니다.', '가 풀렸습니다.'][l.useSound]}")
                        case 109: # m
                            s.playerMode = "observe" if s.playerMode == "normal" else "normal"
                            color = {"observe":cc['fg']['Y'], "normal":cc['fg']['L']}[s.playerMode]
                            play("soundEffects", "check")
                            addLog(f"플레이어 모드가 '{color}{s.playerMode}{cc['end']}'로 변경되었습니다.")
                        case 91: # [
                            if s.volume:
                                s.volume -= 10
                                play("soundEffects", "check")
                                addLog(f"음량 : {s.volume}%")
                            else: addLog("이미 음량이 최저치에 도달했습니다!")
                        case 93: # ]
                            if s.volume < 100:
                                s.volume += 10
                                play("soundEffects", "check")
                                addLog(f"음량 : {s.volume}%")
                            else:
                                play("soundEffects", "block")
                                addLog("이미 음량이 최고치에 도달헀습니다!")
                        case 49|50|51|52|53|54:
                            if len(s.inventory['cells'])>=key-48 and not s.inventory['cells'][key-49]['disabled']:
                                if key-49 != s.inventory['pointer']:
                                    s.inventory['pointer'] = key-49
                                    play("system", "selector", "select")
                            else: play("system", "selector", "block")

                if key == 32: # Space
                    l.pause = False if l.pause else True
                    play("soundEffects", "smash")
                
                await asyncio.sleep(0.005)
            else: await asyncio.sleep(1)

    threading.Thread(name="keyHandler",target=lambda: curses.wrapper(lambda stdscr: asyncio.run(interactions(stdscr)))).start()
