import os
import threading
import math
import time
from   Packages.modules import status, rooms

s, r = status, rooms

# ---------- Others ----------
def clear(): os.system("clear" if os.name == "posix" else "cls")

def slash():
    if os.name == 'posix': return '/'
    else: return '\\'

def play(File):
    def s1():
        playsound = __import__("playsound")
        playsound.playsound(File)
    if s.sound == True: threading.Thread(target=s1, name="sound", daemon=True).start()

def slowLogoPrint(text):
    for word in text:
        print(word, flush=True)
        play(f"{s.TFP}sounds{s.s}smash.wav")
        time.sleep(0.5)

# ---------- Display ----------
def endPrint(text): print(text, end='')

def statusBarFormatPrint(status, statusName, minusStatus=0, color=s.colors['R'], tag="", space=" "):
    Display = ""
    Display += f"{statusName} :{space}["
    for i in range(status): Display += f"{color}🁢{s.colors['end']}"
    if minusStatus != 0:
        for j in range(minusStatus-status): Display += f"{s.colors['lB1']}🁢{s.colors['end']}"
    Display += f"] {tag}\n"

    return Display

def asciiPrint():
    Display = ""
    Display += statusBarFormatPrint(s.hp, "hp", s.Mhp, space="     ")
    Display += statusBarFormatPrint(s.df, "def", s.Mdf, s.colors['B'], space="    ")
    if math.ceil(((s.hunger/500)*10)) <= 1: hungerTag = str(s.hunger)
    else: hungerTag = f"{s.colors['lY']}{(s.hunger/500)*100:0.0f}%{s.colors['end']}"
    Display += statusBarFormatPrint(math.ceil(((s.hunger/500)*100)/10), "hunger", color=s.colors['lY'], tag=hungerTag)
    Display += statusBarFormatPrint(s.atk, "atk", color=s.colors['G'], space="    ")
    Display += "\n"

    return Display

def fieldPrint():
    Display = ""
    if s.showStateDesign == 1: Display += f"hp : {s.colors['R']}{s.hp}/{s.Mhp}{s.colors['end']} | def : {s.colors['B']}{s.df}/{s.Mdf}{s.colors['end']}\nhunger : {s.colors['lY']}{(s.hunger/500)*100:0.0f}%{s.colors['end']} | atk : {s.colors['G']}{s.atk}{s.colors['end']}\n\n"
    elif s.showStateDesign == 2: Display += asciiPrint()
    for i in range(len(s.room)): Display += ' '.join(map(str, s.room[i])); Display += '\n'
    for i in s.onDisplay: Display += f"{i}\n"
    print(Display)

# ---------- Thread section ----------
def addEntity(entityType, initHp, x=0, y=0):
    kinds                = ["몬스터", "보스"]
    classType            = ["enemy", "boss"]
    additionalProperties = ["", f", {y}, {x}"]
    Name                 = kinds[entityType]
    a = 0
    while True:
        if Name + f"_{a}" not in s.entities:
            Name  = Name + f"_{a}"
            Rname = kinds[entityType] + f"_{a}"
            break
        a += 1
    nameSpace = {f"{Name}" : Name, "Rname" : Rname}
    exec(f"""
from Packages.modules import enemy, status
{Name} = enemy.{classType[entityType]}(0, 0, 0, \"{Name}\")
{Name}.start({initHp}{additionalProperties[entityType]})
status.entities.append(Rname)
    """, nameSpace)
    def EntityInteraction():
        exec(f"""
from Packages.modules        import status
from Packages.modules.logger import addLog

while True:
    if {Name}.hp > 0 and status.main == 1 and status.jpsf == True: {Name}.move()
status.entities.remove(Rname)
status.room[{Name}.y][{Name}.x] = status.stepableBlocks[{Name}.stepped]
addLog(f\"{status.colors['R']}{Name}{status.colors['end']}이(가) 죽었습니다!\")
        """, nameSpace)
    threading.Thread(target=EntityInteraction, name=Rname).start()

# def addDoor(roomName, room, x, y, x1, y1, afterroomName, afterroom):
#     print(s.Rooms)
#     print(s.doorRooms)
#     if roomName not in s.Rooms or\
#     afterroomName not in s.Rooms: return
#     if room not in s.doorRooms:
#         data[i] = str(data[i])[:-2] + (', r.'+roomName+']\n')
#         s.doors.append([])
#     print(s.doorRooms)
#     s.doors[s.doorRooms.index(room)].append([x,y,x1,y1,'r.'+afterroomName])
#     with open('modules/status.py', 'r') as f:
#         data = f.readlines()
#         for i in range(len(data)):
#             if data[i].startswith('doors'): data[i] = f'doors = {s.doors}'
#             elif data[i].startswith('doorRooms'): data[i] = f'doorRooms = {s.doorRooms}\n'
#         with open('modules/status.py', 'w') as wf: wf.writelines(data)

# addDoor('field', r.field, 0, 0, 0, 0, 'room_1', r.room_1)
