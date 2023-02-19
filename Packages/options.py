import time, json
from   Packages.modules             import states, selector
from   Packages.globalFunctions     import clear
from   Packages.globalFunctions     import play

s  = states
sc = selector.selector

def saveFile():
    Vars        = [name for name in dir(states) if not name.startswith('__')]
    uselessVars = ['doorRooms', 'doors', 'p1', 'e', 'wall', 'R', 'item', 'goal', 'floor', 'fakeFloor', 'TFP', 'Rooms', 'room', 'r', 's', 'os', 'LOGO', 'colors']
    for i in uselessVars: Vars.remove(i)

    file_path    = './savefile.json'
    data         = {}
    data['Data'] = []
    StatesData   = {}
    for i in Vars:
        # data['states'].append({i : eval(f'states.{i}')})
        StatesData[i] = eval(f"states.{i}")
    data['Data'].append({"states" : StatesData})

    with open(file_path, "w") as outfile: json.dump(data, outfile, indent=4, ensure_ascii=False)

def menu():
    global s, sc

    s.jpsf = False
    clear()
    time.sleep(0.1)
    play(f'{s.TFP}sounds{s.s}smash.wav')
    while True:
        mainMenu = sc.Dropdown('  _   \n /_/     _/   _  _ _/_    _ _ \n/ \ /_//_/ |//_\'/ //  /_// /_\'\n\n𝘢 𝘭 𝘱 𝘩 𝘢\n< 메뉴 >', ['게임으로 돌아가기', '게임 종료', '게임 저장', '만든이', '만들 때 사용한 프로그램', '소리 설정', '아이콘 설정'], [1,0,255,10], '@')
        if mainMenu == 1:
            s.jpsf = True
            break
        elif mainMenu == 2:
            print('언젠가 다시 만나요..')
            s.jpsf = True
            s.main = 0
            time.sleep(1)
        elif mainMenu == 3:
            print('저장중...')
            saveFile()
            print('완료!')
            time.sleep(1)
            clear()
            menu()
        elif mainMenu == 4: sc.Dropdown('만든이:\n    다호\n\n도와준 이:\n    내 전두엽\n    내 전전두엽\n    사파리\n    내 눈\n    내 손\n    내 감각수용체\n    내 해마\n    내 등뼈\n    내 골반\n    내 손, 발목\n    내 책상\n\nSpecial Thanks:\n    레포\n    업로드\n    형', ['돌아가기'], [1, 0, 255, 10], '@')
        elif mainMenu == 5: sc.Dropdown("IDLE:\n    Visual Studio Code\n\n프로그래밍한 언어:\n    Python\n\n다른 프로그램들:\n    사운드 제작 프로그램:\n        bfxr\n        beepBox\n", ['돌아가기'], [1, 0, 255, 10], '@')
        elif mainMenu == 6:
            while True:
                soundSet = sc.Dropdown('소리 설정', [f'현재 소리 : {s.sound}', '', '돌아가기'], [1, 0, 255, 10], '@')
                if soundSet == 1:
                    if s.sound == True: s.sound = False
                    else: s.sound = True
                else: break
        elif mainMenu == 7:
            while True:
                styles = ["number", "ascii"]
                showIconOptionTags = ["\'hp : 10\'과 같은 형식으로 나타납니다.", "\'hp : [🁢🁢🁢🁢🁢🁢🁢🁢🁢🁢]\'과 같은 형식으로 나타납니다."]
                soundSet = sc.Dropdown('아이콘 설정', [f'현재 아이콘 : {styles[s.showStateDesign-1]}', '', '돌아가기'], [1, 0, 255, 10], '@', tag=f"{s.markdown([0,2,3])}\n    {showIconOptionTags[s.showStateDesign-1]}")
                if soundSet == 1:
                    if s.showStateDesign == 1: s.showStateDesign = 2
                    else: s.showStateDesign = 1
                else: break
