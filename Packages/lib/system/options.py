import time, json
from   Packages.lib.data        import status
from   Packages.lib.modules     import selector, makeNewListener
from   Packages.lib.system.globalFunctions import clear, play

s  = status
sc = selector.selector

def saveFile():
    Vars        = [name for name in dir(status) if not name.startswith('__')]
    uselessVars = ['LOGO', 'R', 'Wanted', 'bfx', 'bfy', 'boss', 'box', 'boxMark', 'btn1X', 'btn1Y', 'btnX', 'btnY', 'colors', 'customColor', 'doorRooms', 'doors', 'e', 'entities', 'fakeFloor', 'floor', 'goal', 'goalX', 'goalY', 'hpLow', 'item', 'jpsf', 'main', 'markdown', 'onDisplay', 'onTime', 'os', 'p1', 'p2', 'r', 'room', 's', 'squishy', 'stepableBlocks', 'steppedBlock', 'wall', 'x', 'y', 'yctuoh']

    for i in uselessVars: Vars.remove(i)

    file_path    = './savefile.json'
    data         = {}
    data[s.name] = []
    statusData   = {}
    for i in Vars: statusData[i] = eval(f"status.{i}")
    data[s.name].append({"status" : statusData})

    with open(file_path, "w") as outfile: json.dump(data, outfile, indent=4, ensure_ascii=False)

def menu():
    global s, sc

    s.jpsf = False
    time.sleep(0.1)
    play(f'{s.TFP}Packages{s.s}sounds{s.s}smash.wav')
    while True:
        mainMenu = sc.Dropdown('  _   \n /_/     _/   _  _ _/_    _ _ \n/ \ /_//_/ |//_\'/ //  /_// /_\'\n\nπ’ π­ π± π© π’\n< λ©λ΄ >', ['κ²μμΌλ‘ λμκ°κΈ°', 'κ²μ μ’λ£', 'κ²μ μ μ₯', 'λ§λ μ΄', 'λ§λ€ λ μ¬μ©ν νλ‘κ·Έλ¨', 'μλ¦¬ μ€μ ', 'μμ΄μ½ μ€μ '], [1,0,255,10], '@')
        if mainMenu == 1:
            s.jpsf = True
            clear()
            break

        elif mainMenu == 2:
            print('μΈμ  κ° λ€μ λ§λμ..')
            s.jpsf = True
            s.main = 0
            time.sleep(1)

        elif mainMenu == 3:
            print('μ μ₯μ€...')
            saveFile()
            print('μλ£!')
            time.sleep(1)
            makeNewListener.addListener();clear()
            menu()

        elif mainMenu == 4: sc.Dropdown('λ§λ μ΄:\n    λ€νΈ\n\nλμμ€ μ΄:\n    λ΄ μ λμ½\n    λ΄ μ μ λμ½\n    μ¬νλ¦¬\n    λ΄ λ\n    λ΄ μ\n    λ΄ κ°κ°μμ©μ²΄\n    λ΄ ν΄λ§\n    λ΄ λ±λΌ\n    λ΄ κ³¨λ°\n    λ΄ μ, λ°λͺ©\n    λ΄ μ±μ\n\nSpecial Thanks:\n    λ ν¬\n    μλ‘λ\n    ν', ['λμκ°κΈ°'], [1, 0, 255, 10], '@'); clear()

        elif mainMenu == 5: sc.Dropdown("IDLE:\n    Visual Studio Code\n\nνλ‘κ·Έλλ°ν μΈμ΄:\n    Python\n\nλ€λ₯Έ νλ‘κ·Έλ¨λ€:\n    μ¬μ΄λ μ μ νλ‘κ·Έλ¨:\n        bfxr\n        beepBox\n", ['λμκ°κΈ°'], [1, 0, 255, 10], '@'); clear()
        
        elif mainMenu == 6:
            while True:
                soundSet = sc.Dropdown('μλ¦¬ μ€μ ', [f'νμ¬ μλ¦¬ : {s.sound}', '', 'λμκ°κΈ°'], [1, 0, 255, 10], '@')
                if soundSet == 1: s.sound = True if s.sound == False else False
                else: break
            clear()
            
        elif mainMenu == 7:
            while True:
                styles             = ["number", "ascii"]
                showIconOptionTags = ["\'hp : 10\μ(κ³Ό) κ°μ νμμΌλ‘ λνλ©λλ€.", "\'hp : [||||||||||]\'μ(κ³Ό) κ°μ νμμΌλ‘ λνλ©λλ€."]
                soundSet           = sc.Dropdown('μμ΄μ½ μ€μ ', [f'νμ¬ μμ΄μ½ : {styles[s.showStateDesign-1]}', '', 'λμκ°κΈ°'], [1, 0, 255, 10], '@', tag=f"{s.markdown([0,2,3])}\n    {showIconOptionTags[s.showStateDesign-1]}")
                if soundSet == 1: s.showStateDesign = 1 if s.showStateDesign == 2 else 2
                else: break
            clear()
