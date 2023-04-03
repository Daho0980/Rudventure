import time, json
from   Packages.lib.data                       import status, lockers
from   Packages.lib.modules                    import selector, Textbox
from   Packages.lib.system                     import DungeonMaker
from   Packages.lib.system.Secret.rudConverter import converter
from   Packages.lib.system.Secret.cursorType   import cursor
from   Packages.lib.system.globalFunc.graphic  import clear
from   Packages.lib.system.globalFunc.sound    import play

s, l  = status, lockers
sc    = selector.selector
dgm   = DungeonMaker

def saveFile():
    Vars        = [name for name in dir(s) if not name.startswith('__')]
    uselessVars = ["colors", "customColor", "markdown", "Dy", "bfDy", "Dx", "bfDx", "x", "bfx", "y", "bfy", "steppedBlock", "btnX", "btnY", "btn1X", "btn1Y", "goalX", "goalY", "main", "LOGO", "p1", "p2", "e", "boss", "enemies", "squishy", "wall", "R", "item", "box", "boxMark", "goal", "floor", "fakeFloor", "orbs", "stepableBlocks", "doorRooms", "doors", "nowStage", "roomName", "s", "room", "Dungeon", "roomLock", "jpsf", "TFP", "sound", "yctuoh", "entities", "Wanted", "onDisplay", "onTime", "showDungeonMap"]
    print('저장중...')
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
    except: print("저장에 실패했습니다.")
    else:   print("성공적으로 저장되었습니다.")

def menu():
    global s, sc

    clear()
    l.jpsf = 0
    time.sleep(0.1)
    play("smash")
    what = 0
    while True:
        if what == 0:
            mainMenu = sc.Dropdown(f'{s.LOGO}\n        << 메뉴 >>', ['게임으로 돌아가기', '게임 종료', '게임 저장', 'Credits', '만들 때 사용한 프로그램', '소리 설정', '아이콘 설정'], [1,0,255,10], '@', frontTag="Enter를 한 번 눌러 주세요")
            what = 1
        elif what == 1: mainMenu = sc.Dropdown(f'{s.LOGO}\n        << 메뉴 >>', ['게임으로 돌아가기', '게임 종료', '게임 저장', 'Credits', '만들 때 사용한 프로그램', '소리 설정', '아이콘 설정'], [1,0,255,10], '@')

        if mainMenu == 1:
            l.jpsf = 1
            break

        elif mainMenu == 2:
            print('당신이 다시 돌아오길 기다리겠습니다...')
            cursor.show()
            s.main = 0; break

        elif mainMenu == 3:
            saveFile()
            time.sleep(1); input("확인__")

        elif mainMenu == 4: sc.Dropdown('만든이:\n    다호\n\n도와준 이:\n    내 전두엽\n    내 전전두엽\n    사파리\n    내 눈\n    내 손\n    내 감각수용체\n    내 해마\n    내 등뼈\n    내 골반\n    내 손, 발목\n    내 책상\n\nSpecial Thanks:\n    레포\n    업로드\n    형\n    ChatGPT-3.5', ['돌아가기'], [1, 0, 255, 10], '@')

        elif mainMenu == 5: sc.Dropdown("IDLE:\n    Visual Studio Code\n\n프로그래밍한 언어:\n    Python\n\n다른 프로그램들:\n    사운드 제작 프로그램:\n        bfxr\n        beepBox\n", ['돌아가기'], [1, 0, 255, 10], '@')
        
        elif mainMenu == 6:
            while True:
                soundSet = sc.Dropdown('소리 설정', [f'현재 소리 : {s.sound}', '', '돌아가기'], [1, 0, 255, 10], '@')
                if soundSet == 1: s.sound = True if s.sound == False else False
                else: break
            clear()
            
        elif mainMenu == 7:
            while True:
                styles             = ["number", "ascii"]
                showIconOptionTags = ["\'hp : 10\' 과 같은 형식으로 나타납니다.", "\'hp : [||||||||||]\' 과 같은 형식으로 나타납니다."]
                soundSet           = sc.Dropdown('아이콘 설정', [f'현재 아이콘 : {styles[s.showStateDesign-1]}', '', '돌아가기'], [1, 0, 255, 10], '@', tag=f"{s.markdown([0,2,3])}\n    {showIconOptionTags[s.showStateDesign-1]}")
                
                if soundSet == 1: s.showStateDesign = 1 if s.showStateDesign == 2 else 2
                else: break
            clear()

def showMap():
    roomIcons = ['\033[31m§\033[0m', '•', '\033[32m*\033[0m', '\033[33m!\033[0m', '\033[34m/\033[0m']

    l.jpsf = 0
    time.sleep(0.1)
    play("smash")
    
    sc.Dropdown(
        f"{Textbox.TextBox(dgm.gridMapReturn(s.Dungeon, blank=1), Type='middle', fillChar='^', AMLS=True, endLineBreak=True, LineType='double')}\n{roomIcons[0]} = start\n{roomIcons[1]} = basic room\n{roomIcons[2]} = event room\n{roomIcons[3]} = treasurebox room\n{roomIcons[4]} = exit", 
        ["확인__"], 
        [1,0,255,10], 
        '@'
    )