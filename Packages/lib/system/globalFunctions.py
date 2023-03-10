import os
import threading
import math
import time
import random
from   Packages.lib.data    import rooms, status
from   Packages.lib.modules import logger

s, r = status, rooms

# ---------- Others ----------
def clear(): os.system("clear" if os.name == "posix" else "cls")

def slash():
    if os.name == 'posix': return '/'
    else                 : return '\\'

def play(File):
    def s1():
        playsound = __import__("playsound")
        playsound.playsound(File)
    if s.sound == True: threading.Thread(target=s1, name="sound", daemon=True).start()

def slowLogoPrint(text):
    for word in text:
        print(word, flush=True)
        play(f"{s.TFP}Packages{s.s}sounds{s.s}smash.wav")
        time.sleep(0.5)

def placeRandomBlock(Map, block, y:list, x:list, conditions):
    while True:
        Ry, Rx = random.randrange(y[0], y[1]), random.randrange(x[0], x[1])
        if Map[Ry][Rx] in conditions: continue
        Map[Ry][Rx] = block
        break

# ---------- Display ----------
def endPrint(text): print(text, end='')

def statusBarFormatPrint(status, statusName, minusStatus=0, color=s.colors['R'], tag="", space=" "):
    Display  = ""
    Display += f"{statusName} :{space}["

    for i in range(status): Display += f"{color}|{s.colors['end']}"
    if minusStatus != 0:
        for j in range(minusStatus-status): Display += f"{s.colors['lB1']}|{s.colors['end']}"

    Display += f"] {tag}\n"

    return Display

def asciiPrint():
    Display  = ""

    Display += statusBarFormatPrint(s.hp, "hp", s.Mhp, space="     ")
    Display += statusBarFormatPrint(s.df, "def", s.Mdf, s.colors['B'], space="    ")
    if s.hunger <= 50: hungerTag = s.colors['lY'] + str(s.hunger) + s.colors['end']
    else             : hungerTag = f"{s.colors['lY']}{(s.hunger/500)*100:0.0f}%{s.colors['end']}"
    Display += statusBarFormatPrint(math.ceil(((s.hunger/500)*100)/10), "hunger", color=s.colors['lY'], tag=hungerTag)
    Display += statusBarFormatPrint(s.atk, "atk", color=s.colors['G'], space="    ")

    Display += "\n"

    return Display

def fieldPrint(grid):
    Display = ""
    if s.showStateDesign == 1  : Display += f"hp : {s.colors['R']}{s.hp}/{s.Mhp}{s.colors['end']} | def : {s.colors['B']}{s.df}/{s.Mdf}{s.colors['end']}\nhunger : {s.colors['lY']}{(s.hunger/500)*100:0.0f}%{s.colors['end']} | atk : {s.colors['G']}{s.atk}{s.colors['end']}\n\n"
    elif s.showStateDesign == 2: Display += asciiPrint()
    for i in range(len(grid)): Display += ' '.join(map(str, grid[i])); Display += '\n'
    for i in s.onDisplay       : Display += f"{i}\n"
    print(Display)

# ---------- ID section ----------
def IDIncryption(DungeonPos:list, RoomPos=None):
    Dy, Dx = DungeonPos[0], DungeonPos[1]
    Ry = '?' if RoomPos == None or len(RoomPos) < 1 else RoomPos[0]
    Rx = '?' if RoomPos == None or len(RoomPos) < 2 else RoomPos[1]
    return f"Rud.{Dy}.{Dx}.room.{Ry}.{Rx}"

def IDDecryption(ID:str):
    if ID.startswith("Rud"):
        output = ID.split('.')
        del output[0]

        for i in range(len(output)):
            if output[i].isdigit(): output[i] = int(output[i])
        return output

# ---------- Thread section ----------
def addEntity(entityType, initHp, y=[1, len(s.room)], x=[1, len(s.room[0])]):
    kinds                = ["?????????", "??????"]
    classType            = ["enemy", "boss"]
    icons                = [s.e, s.boss]
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
from Packages.lib      import enemy
from Packages.lib.data import status
{Name} = enemy.{classType[entityType]}(0, 0, 0, \"{Name}\", \"{icons[entityType]}\")
{Name}.start({initHp}, {y}, {x})
status.entities.append(Rname)
    """, nameSpace)
    def EntityInteraction():
        exec(f"""
from Packages.lib.data           import status
from Packages.lib.modules.logger import addLog

while True:
    if {Name}.hp <= 0 or status.main != 1:
        status.entities.remove(Rname)
        break
    elif status.jpsf                     : {Name}.move()
status.room[{Name}.y][{Name}.x] = status.stepableBlocks[status.stepableBlocks.index({Name}.stepped)]
        """, nameSpace)
        play(f"{s.TFP}Packages{s.s}sounds{s.s}monster_dead.wav")
        logger.addLog(f"{status.colors['R']}{Name}{status.colors['end']}???(???) ???????????????!")
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
