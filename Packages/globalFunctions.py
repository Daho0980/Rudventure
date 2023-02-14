import os
import threading
import math
import time
from Packages.modules import states, rooms

s, r = states, rooms

def what(): 1 + 1

def endPrint(text): print(text, end='')

def asciiPrint():
    endPrint("hp     : [")
    for HP in range(s.hp): endPrint(f"{s.colors['R']}🁢{s.colors['end']}")
    for eHP in range(s.Mhp-s.hp): endPrint(f"{s.colors['lB1']}🁢{s.colors['end']}")
    endPrint("]\ndef    : [")
    for DEF in range(s.df): endPrint(f"{s.colors['B']}🁢{s.colors['end']}")
    for eDEF in range(s.Mdf-s.df): endPrint(f"{s.colors['lB1']}🁢{s.colors['end']}")
    endPrint(f"]\nhunger : [")
    for Hunger in range(math.ceil(((s.hunger/500)*100)/10)): endPrint(f"{s.colors['lY']}🁢{s.colors['end']}")
    if math.ceil(((s.hunger/500)*100)/10) <= 1: endPrint(f"] {s.colors['lY']}{s.hunger:0.0f}{s.colors['end']}")
    else: endPrint(f"] {s.colors['lY']}{(s.hunger/500)*100:0.0f}%{s.colors['end']}")
    endPrint("\natk    : [")
    for ATK in range(s.atk): endPrint(f"{s.colors['G']}🁢{s.colors['end']}")
    print("]\n")

def fieldPrint():
    if s.showStateDesign == 1: print(f"hp : {s.colors['R']}{s.hp}/{s.Mhp}{s.colors['end']} | def : {s.colors['B']}{s.df}/{s.Mdf}{s.colors['end']}\nhunger : {s.colors['lY']}{(s.hunger/500)*100:0.0f}%{s.colors['end']} | atk : {s.colors['G']}{s.atk}{s.colors['end']}\n")
    elif s.showStateDesign == 2: asciiPrint()
    Display = ''
    for i in range(len(s.room)): Display += ' '.join(map(str, s.room[i])); Display += '\n'
    print(Display)
    print(s.objects)

def slash():
    if os.name == 'posix': return '/'
    else: return '\\'

def play(File):
    def s1():
        playsound = __import__("playsound")
        playsound.playsound(File)
    if s.sound == True: threading.Thread(target=s1, name="sound").start()

def slowLogoPrint(text):
    for word in text:
        print(word, flush=True)
        play(f"{s.TFP}sounds{s.s}smash.wav")
        time.sleep(0.5)

def addEntity(entityName):
    def EntityInteraction(): exec(f"{entityName}.move()")
    threading.Thread(target=EntityInteraction, name=entityName).start()

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
#     with open('modules/states.py', 'r') as f:
#         data = f.readlines()
#         for i in range(len(data)):
#             if data[i].startswith('doors'): data[i] = f'doors = {s.doors}'
#             elif data[i].startswith('doorRooms'): data[i] = f'doorRooms = {s.doorRooms}\n'
#         with open('modules/states.py', 'w') as wf: wf.writelines(data)

# addDoor('field', r.field, 0, 0, 0, 0, 'room_1', r.room_1)