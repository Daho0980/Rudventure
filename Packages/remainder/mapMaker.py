# !!!!!!!!! This code was archived. !!!!!!!!!
# !!!!!!!  Maybe I can't use anymore. !!!!!!!

import os, time, random
from modules import rooms
from globalFunctions import clear

r = rooms
blockType = {
    'field' : '.',
    'fakeField' : '∙',
    'wall' : '◼',
    'hole' : ' ',
    'goal' : '⚑',
    'box' : '☒',
    'item' : '◘',
    'door' : '▒'
}
maps = {}
errors = {
    0 : '',
    1 : 'x값이 월드의 한계를 넘어섰습니다!',
    2 : 'y값이 월드의 한계를 넘어섰습니다!',
    3 : 'x, y값에는 숫자만 넣어주세요!',
    4 : '명령어를 입력해주세요!',
    5 : '숫자가 너무 적습니다!',
    6 : '숫자만 입력해주세요!',
    7 : '리스트만 입력해주세요!'
}
rules = {
    'viewLog' : [False, '그동안 수정된 맵들을 로그 형식으로 볼 수 있습니다.'],
    'viewPos' : [False, '블록의 좌표 위치를 더 쉽게 볼 수 있습니다.']
}

class mapmaker:
    def onlyInt(text):
        while True:
            try: output = int(input(text))
            except:
                print("\n숫자만 입력해주세요!")
                time.sleep(1)
                clear()
                continue
            else: break
        clear()
        return output

    def mapNameChecker(name):
        a = 1
        Num = 0
        while True:
            try: a = exec(f'{name}_{Num}')
            except:
                output = f'{name}_{Num}'
                break
            else: Num += 1
        return output

    def makeField(x, y):
        global blockType

        mapName = mapmaker.mapNameChecker('map')
        exec(f'{mapName} = []')
        for i in range(y+1):
            exec(f'{mapName}.append([])')
            for j in range(x+1): exec(f'{mapName}[{i}].append(\'{blockType["field"]}\')')
        return eval(mapName), mapName

    def fieldPrint(Map, mapname):
        print(f'{mapname}\n')
        if rules['viewPos'][0] == True:
            for i in range(len(Map[0])): 
                print(i, end='')
                if i < 10: print('',end=' ')
            print('')
        for i in range(len(Map)):
            print(' '.join(map(str, Map[i])), end='')
            if rules['viewPos'][0] == True: print(f' {i}', end='')
            print('')

    def mapEditor(Map, mapname):
        global blockType
        global errors
        global rules

        def errorText(text):
            global errors
            RED = '\033[41m'
            STOP = '\033[0m'
            print(f'{RED}{text}{STOP}')

        errorCode = 0
        um = Map
        a = []
        while True:
            a.append(um)
            if rules['viewLog'][0] == False: clear()
            print(a)
            try: 1 + errorCode
            except: errorText(errorCode)
            else: errorText(errors[errorCode])
            mapmaker.fieldPrint(Map, mapname)
            inputs = input('>>>')
            command = inputs.split(' ')
            errorCode = 0
            if inputs == 'end':
                endQ = input('정말로 맵 수정을 종료하시겠습니까?(y/n)\n\n>>>')
                if endQ == 'y':
                    saveQ = input('맵을 저장하시겠습니까?(y/n)\n\n>>>')
                    if saveQ == 'y':
                        mapname = input('맵의 이름을 정해주세요\n\n>>>')
                        with open('modules/rooms.py', 'a') as roomfile: roomfile.writelines(f'\n\n# It made by mapMaker__\n{mapname} = {Map}')
                    break
            elif inputs == '': errorCode = 4
            elif list(inputs)[0] == '/':
                #                          0       1 2 3
                if command[0] == '/set': # command x y block
                    if len(command) < 4 or len(command) > 4:
                        errorCode = f'\'{command}\' (은)는 올바른 명령어가 아닙니다!'
                        continue
                    x, y = command[1], command[2]
                    try:
                        if int(x) > len(Map[0])-1 or int(x) < 0:
                            errorCode = 1
                            continue
                        elif int(y) > len(Map)-1 or int(y) < 0:
                            errorCode = 2
                            continue
                    except:
                        errorCode = 3
                        continue
                    if command[3] not in list(blockType): errorCode = f'\'{command[3]}\' (이)라는 블록은 존재하지 않습니다!'
                    else: Map[int(y)][int(x)] = blockType[command[3]]
                #                             0       1 2 3  4  5
                elif command[0] == '/fill': # command x y x1 y1 block
                    if len(command) < 6 or len(command) > 6:
                        errorCode = f'\'{command}\' (은)는 올바른 명령어가 아닙니다!'
                        continue
                    try:
                        if int(command[1 or 2 or 3 or 4]) != int: 1+1
                    except: 
                        errorCode = 3
                        continue
                    if int(command[1]) > int(command[3]): x, x1 = command[1], command[3]
                    else: x, x1 = command[3], command[1]
                    if int(command[2]) > int(command[4]): y, y1 = command[2], command[4]
                    else: y, y1 = command[4], command[2]
                    if (int(x) > len(Map[0])-1 or int(x) < 0) or\
                        (int(x1) > len(Map[0])-1 or int(x1) < 0):
                        errorCode = 1
                        continue
                    elif (int(y) > len(Map)-1 or int(y) < 0) or\
                        (int(y1) > len(Map)-1 or int(y1) < 0):
                        errorCode = 2
                        continue
                    if command[5] not in list(blockType):
                        errorCode = f'\'{command[5]}\' (이)라는 블록은 존재하지 않습니다!'
                        continue

                    for i in range(int(y1), int(y)+1):
                        for j in range(int(x1), int(x)+1): Map[i][j] = blockType[command[5]]
                #                              0       1 2 3  4  5
                elif command[0] == '/round': # command x y x1 y1 block
                    if len(command) < 6 or len(command) > 6:
                        errorCode = f'\'{command}\' (은)는 올바른 명령어가 아닙니다!'
                        continue
                    try:
                        if int(command[1 or 2 or 3 or 4]) != int: 1+1
                    except: 
                        errorCode = 3
                        continue
                    if int(command[1]) > int(command[3]): x, x1 = command[1], command[3]
                    else: x, x1 = command[3], command[1]
                    if int(command[2]) > int(command[4]): y, y1 = command[2], command[4]
                    else: y, y1 = command[4], command[2]
                    if (int(x) > len(Map[0])-1 or int(x) < 0) or\
                        (int(x1) > len(Map[0])-1 or int(x1) < 0):
                        errorCode = 1
                        continue
                    elif (int(y) > len(Map)-1 or int(y) < 0) or\
                        (int(y1) > len(Map)-1 or int(y1) < 0):
                        errorCode = 2
                        continue
                    if command[5] not in list(blockType):
                        errorCode = f'\'{command[5]}\' (이)라는 블록은 존재하지 않습니다!'
                        continue

                    for i in range(int(y1), int(y)+1):
                        for j in range(int(x1), int(x)+1):
                            if i == int(y) or i == int(y1): Map[i][j] = blockType[command[5]]
                            else:
                                if j == int(x) or j == int(x1): Map[i][j] = blockType[command[5]]
                                            #  0       1 2 3  4  5     6   7
                elif command[0] == '/rfill': # command x y x1 y1 block int type(t or f)
                    if len(command) < 8 or len(command) > 8:
                        errorCode = f'\'{command}\' (은)는 올바른 명령어가 아닙니다!'
                        continue
                    try:
                        for i in range(4): 1 + int(command[i+1])
                    except: 
                        errorCode = 3
                        continue
                    if int(command[1]) > int(command[3]): x, x1 = command[1], command[3]
                    else: x, x1 = command[3], command[1]
                    if int(command[2]) > int(command[4]): y, y1 = command[2], command[4]
                    else: y, y1 = command[4], command[2]
                    if (int(x) > len(Map[0])-1 or int(x) < 0) or\
                        (int(x1) > len(Map[0])-1 or int(x1) < 0):
                        errorCode = 1
                        continue
                    elif (int(y) > len(Map)-1 or int(y) < 0) or\
                        (int(y1) > len(Map)-1 or int(y1) < 0):
                        errorCode = 2
                        continue
                    if command[5] not in list(blockType):
                        errorCode = f'\'{command[5]}\' (이)라는 블록은 존재하지 않습니다!'
                        continue
                    try:
                        if int(command[6]) <= 0:
                            errorCode = 5
                            continue
                    except:
                        errorCode = 6
                        continue
                    uh = ['true', 'false']
                    if command[7] not in uh:
                        errorCode = f'\'{command[7]}\' (은)는 올바른 성질이 아닙니다!'
                        continue
                    else:
                        for i in range(int(command[6])):
                            rX = random.randrange(int(x1), int(x))
                            rY = random.randrange(int(y1), int(y))
                            if command[7] == 'true':
                                while True:
                                    rX = random.randrange(int(x1), int(x)+1)
                                    rY = random.randrange(int(y1), int(y)+1)
                                    if Map[rY][rX] != blockType['field']: continue
                                    else:
                                        Map[rY][rX] = blockType[command[5]]
                                        break
                            else: Map[rY][rX] = blockType[command[5]]
                #                             0       1           2
                elif command[0] == '/rule': # command rule-choice type(t or f)-choice
                    if len(command) > 3:
                        errorCode = f'\'{command}\' (은)는 올바른 명령어가 아닙니다!'
                        continue
                    if len(command) == 1:
                        ruleKeys, ruleValues = list(rules.keys()), list(rules.values())
                        print('rules:')
                        for i in range(len(ruleKeys)):
                            print(f'    {ruleKeys[i]}({ruleValues[i][0]}) : {ruleValues[i][1]}')
                    elif len(command) == 2:
                        if command[1] not in list(rules):
                            errorCode = f'\'{command[1]}\' (이)라는 설정은 없습니다!'
                            continue
                        print(f'현재 {command[1]}(은)는 {rules[command[1]][0]}입니다')
                    elif len(command) == 3:
                        if command[1] not in list(rules):
                            errorCode = f'\'{command[1]}\' (이)라는 설정은 없습니다!'
                            continue
                        uh, um = ['true', 'false'], [True, False]
                        if command[2] not in uh:
                            errorCode = f'\'{command[2]}\' (은)는 올바른 성질이 아닙니다!'
                            continue
                        rules[command[1]][0] = um[uh.index(command[2])]
                        print(f'이제 {command[1]}(은)는 {um[uh.index(command[2])]}입니다')
                    input('\n확인__')
                #                             0       1 2 3
                elif command[0] == '/text': # command x y text
                    if len(command) < 4:
                        errorCode = f'\'{command}\' (은)는 올바른 명령어가 아닙니다!'
                        continue
                    x, y = command[1], command[2]
                    try:
                        if int(x) > len(Map[0])-1 or int(x) < 0:
                            errorCode = 1
                            continue
                        elif int(y) > len(Map)-1 or int(y) < 0:
                            errorCode = 2
                            continue
                    except:
                        errorCode = 3
                        continue
                    txt = ''
                    for j in range(3): command.remove(command[0])
                    for i in range(len(command)): txt += command[i]+' '
                    Map[int(y)][int(x)] = txt
                #                               0       1 2 3  4  5           6
                elif command[0] == '/change': # command x y x1 y1 beforeBlock afterBlock
                    if len(command) < 7 or len(command) > 7:
                        errorCode = f'\'{command}\' (은)는 올바른 명령어가 아닙니다!'
                        continue
                    try:
                        if int(command[1 or 2 or 3 or 4]) != int: 1+1
                    except: 
                        errorCode = 3
                        continue
                    if int(command[1]) > int(command[3]): x, x1 = command[1], command[3]
                    else: x, x1 = command[3], command[1]
                    if int(command[2]) > int(command[4]): y, y1 = command[2], command[4]
                    else: y, y1 = command[4], command[2]
                    if (int(x) > len(Map[0])-1 or int(x) < 0) or\
                        (int(x1) > len(Map[0])-1 or int(x1) < 0):
                        errorCode = 1
                        continue
                    elif (int(y) > len(Map)-1 or int(y) < 0) or\
                        (int(y1) > len(Map)-1 or int(y1) < 0):
                        errorCode = 2
                        continue
                    if command[5] not in list(blockType):
                        errorCode = f'\'{command[5]}\' (이)라는 블록은 존재하지 않습니다!'
                        continue
                    elif command[6] not in list(blockType):
                        errorCode = f'\'{command[6]}\' (이)라는 블록은 존재하지 않습니다!'
                        continue

                    for i in range(int(y1), int(y)+1):
                        for j in range(int(x1), int(x)+1):
                            if Map[i][j] == blockType[command[5]]:
                                Map[i][j] = blockType[command[6]]

                else: errorCode = f'\'{command[0]}\' (이)라는 명령어는 존재하지 않습니다!'
            else: errorCode = 4

    def main():
        global blockType
        global maps

        clear()
        while True:
            maxX = mapmaker.onlyInt("최대 x 좌표를 알려주세요! : ")
            try: int(maxX)
            except:
                print('숫자만 입력해주세요!')
                time.sleep(1)
                clear()
                continue
            break
        while True:
            maxY = mapmaker.onlyInt("최대 y 좌표를 알려주세요! : ")
            try: int(maxY)
            except:
                print('숫자만 입력해주세요!')
                time.sleep(1)
                clear()
                continue
            break
        nowMap, nowMapName = mapmaker.makeField(maxX, maxY)
        maps[nowMapName] = nowMap
        print(maps)
        mapmaker.mapEditor(nowMap, nowMapName)
    

print("  _   \n /_/     _/   _  _ _/_    _ _ \n/ \ /_//_/ |//_'/ //  /_// /_'\n\n𝘢 𝘭 𝘱 𝘩 𝘢\n\nMap Maker에 오신 것을 환영합니다!")
input("확인__")
mapmaker.main()
