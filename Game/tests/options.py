import json
import time
from   Assets.data                       import status, lockers
from   Game.utils.modules                    import cSelector
from   Game.utils.advanced                     import DungeonMaker
from   Game.tests.Secret.rudConverter import converter
from   Game.utils.system   import cinp
from   Game.utils.sound    import play

s, l     = status, lockers
selector = cSelector.selector
dgm      = DungeonMaker

Credits = """
만든이:
    다호
    
도와준 이:
    내 전두엽
    내 전전두엽
    사파리
    내 눈
    내 손
    내 등뼈
    내 골반
    내 손
    내 발
    내 책상
    
Special Thanks:
    레포
    업로드
    형
    ChatGPT-3.5
"""
usedProgram = """
IDLE:
    Visual Studio Code
    
프로그래밍한 언어:
    Python
    
다른 프로그램들:
    사운드 제작 프로그램:
        bfxr
        beepBox
"""

def saveFile(stdscr):
    Vars        = [name for name in dir(s) if not name.startswith('__')]
    uselessVars = [
        "colors",
        "customColor",
        "markdown",
        "cMarkdown",
        "Dy",
        "bfDy",
        "Dx",
        "bfDx",
        "x",
        "bfx",
        "y",
        "bfy",
        "steppedBlock",
        "main",
        "LOGO",
        "p1",
        "p2",
        "e",
        "enemies",
        "wall",
        "R",
        "item",
        "box",
        "boxMark",
        "goal",
        "floor",
        "fakeFloor",
        "orbs",
        "stepableBlocks",
        "doorRooms",
        "doors",
        "nowStage",
        "roomName",
        "s",
        "room",
        "Dungeon",
        "roomLock",
        "jpsf",
        "TFP",
        "sound",
        "yctuoh",
        "entities",
        "hitPos",
        "onDisplay",
        "onTime",
        "showDungeonMap"
        ]
    
    stdscr.clear()
    stdscr.addstr('저장중...'); stdscr.refresh()
    try:
        file_path = f'{s.TFP}Packages{s.s}saveFiles{s.s}{s.name}.json'
        saveJson  = open(file_path, 'w')

        for i in uselessVars:
            if i in Vars: Vars.remove(i)
            else: print(i)

        data         = {}
        
        data[s.name] = []
        statusData   = {}
        for i in Vars: statusData[i] = eval(f"status.{i}")
        data[s.name].append({"status" : statusData})

        json.dump(data, saveJson, indent=4, ensure_ascii=False)
        saveJson.close()

        # 파일 암호화 단계
        jsonForRead  = open(file_path, 'r')
        encoded      = converter.encode(jsonForRead.readlines())
        with open(file_path, 'w') as encodeFile:
            for line in encoded: encodeFile.write(f"{line}\n")
        converter.changeExtention(s.name, beforeExt=".json", afterExt=".rud")
    except: stdscr.addstr("저장에 실패했습니다.")
    else:   stdscr.addstr("성공적으로 저장되었습니다.")
    stdscr.refresh()
    time.sleep(1); cinp("확인__"); stdscr.refresh()

def menu(stdscr):
    global s, sc

    # if not isinstance(stdscr, Cusser):
    #     stdscr = Cusser(stdscr)

    stdscr.clear(); stdscr.refresh()
    # stdscr.nodelay(False)
    l.jpsf = 0
    play("smash")
    while 1:
        mainMenu = selector.main(f'{s.LOGO}\n        << 메뉴 >>',
                                [
                                    "게임으로 돌아가기",
                                    "게임 종료",
                                    "게임 저장",
                                    "Credits",
                                    "만들 때 사용한 프로그램",
                                    "소리 설정",
                                    "아이콘 설정"
                                ],
                                [1,0,255,10],
                                '@'
                            )

        if mainMenu == 1:
            l.jpsf   = 1
            s.option = False
            break

        elif mainMenu == 2:
            print('당신이 다시 돌아오길 기다리겠습니다...')
            s.main = 0; break

        elif mainMenu == 3: saveFile(stdscr)

        elif mainMenu == 4:
            selector.main(Credits, ['돌아가기'], [1, 0, 255, 10], '@')

        elif mainMenu == 5:
            selector.main(usedProgram, ['돌아가기'], [1, 0, 255, 10], '@')
        
        elif mainMenu == 6:
            while 1:
                soundSet = selector.main('소리 설정', [f'현재 소리 : {s.sound}', '', '돌아가기'], [1, 0, 255, 10], '@')
                if soundSet == 1: s.sound = True if s.sound == False else False
                else: break
            stdscr.refresh()
            
        elif mainMenu == 7:
            while 1:
                styles             = ["number", "ascii"]
                showIconOptionTags = ["\'hp : 10\' 과 같은 형식으로 나타납니다.", "\'hp : [||||||||||]\' 과 같은 형식으로 나타납니다."]
                soundSet           = selector.main('아이콘 설정',[f'현재 아이콘 : {styles[s.showStateDesign-1]}', '', '돌아가기'], [1, 0, 255, 10], '@', tag=f"\n    {showIconOptionTags[s.showStateDesign-1]}")
                
                if soundSet == 1: s.showStateDesign = 1 if s.showStateDesign == 2 else 2
                else: break
            stdscr.refresh()
    stdscr.addstr("준비 중..."); stdscr.refresh()
    stdscr.nodelay(True)
