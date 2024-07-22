import threading
from   random   import randrange, choice

from Assets.data          import status          as s
from Assets.data.color    import cColors         as cc
from Game.entities.entity import addMonster
from Game.utils.system    import placeRandomBlock


def changeDoorPosBlock(ID:int, data:dict) -> None:
    c = {
        'y' : int(len(s.Dungeon[s.Dy][s.Dx]['room'])/2),
        'x' : int(len(s.Dungeon[s.Dy][s.Dx]['room'][0])/2)
    }
    DPG:dict[str,list[int]] = {
        'U' : [0, c['x']],
        'R' : [c['y'], len(s.Dungeon[s.Dy][s.Dx]['room'][0])-1],
        'D' : [len(s.Dungeon[s.Dy][s.Dx]['room'])-1, c['x']],
        'L' : [c['y'], 0]
        }
        
    for i in range(len(data['doorPos'])):
        keys, values = list(data['doorPos'].keys()), list(data['doorPos'].values())
        if values[i] == 1:
            DPY, DPX = DPG[keys[i]][0], DPG[keys[i]][1]

            s.Dungeon[s.Dy][s.Dx]['room'][DPY][DPX] = {"block" : s.ids[ID], "id" : ID, "type" : 0}
            if   keys[i] in ['U','D']:
                s.Dungeon[s.Dy][s.Dx]['room'][DPY][DPX-1] = {"block" : s.ids[ID], "id" : ID, "type" : 0}
                s.Dungeon[s.Dy][s.Dx]['room'][DPY][DPX+1] = {"block" : s.ids[ID], "id" : ID, "type" : 0}
            elif keys[i] in ['R','L']:
                s.Dungeon[s.Dy][s.Dx]['room'][DPY-1][DPX] = {"block" : s.ids[ID], "id" : ID, "type" : 0}
                s.Dungeon[s.Dy][s.Dx]['room'][DPY+1][DPX] = {"block" : s.ids[ID], "id" : ID, "type" : 0}

def summonMonster(
        data:dict,
        hpMultiplier:int     =1,
        atkMultiplier:int    =1,
        ashChipMultiplier:int=1,
        monsterIndex:int     =0,
        useRandom:bool       =True,
        boss:bool            =False
        ) -> None:
    # type, hp
    def event() -> None:
        nonlocal data

        count                                = data['summonCount']
        s.Dungeon[s.Dy][s.Dx]['summonCount'] = 0
        for i in range(count):
            addMonster(
                choice([[0,1,2],[0,1]][boss])if useRandom else monsterIndex,
                hpMultiplier,
                atkMultiplier,
                ashChipMultiplier,
                Dy         =s.Dy,
                Dx         =s.Dx,
                y          =[1, len(data['room'])-2   ],
                x          =[1, len(data['room'][0])-2],
                useRoomLock=True if i == (count-1)else False
                )
    threading.Thread(target=event, daemon=True).start()
    
def placeRandomOrbs(multiple:int=1) -> None:
    # hp -> def -> atk -> hng -> exp
    orbs:dict = {
        "size" : {
            "smallOne" : [
                f"{cc['fg']['R']}o{cc['end']}",
                f"{cc['fg']['B1']}q{cc['end']}",
                f"{cc['fg']['L']}v{cc['end']}",
                f"{cc['fg']['Y']}o{cc['end']}",
                f"{cc['fg']['F']}ø{cc['end']}"
            ],
            "bigOne" : [
                f"{cc['fg']['R']}O{cc['end']}",
                f"{cc['fg']['B1']}Q{cc['end']}",
                f"{cc['fg']['L']}V{cc['end']}",
                f"{cc['fg']['Y']}O{cc['end']}",
                f"{cc['fg']['F']}Ø{cc['end']}"
            ]
        },
        "type" : {
            "hp"     : [f"{cc['fg']['R']}o{cc['end']}",  f"{cc['fg']['R']}O{cc['end']}"],
            "def"    : [f"{cc['fg']['B1']}q{cc['end']}", f"{cc['fg']['B1']}Q{cc['end']}"],
            "atk"    : [f"{cc['fg']['L']}v{cc['end']}",  f"{cc['fg']['L']}V{cc['end']}"],
            "hunger" : [f"{cc['fg']['Y']}o{cc['end']}",  f"{cc['fg']['Y']}O{cc['end']}"],
            "exp"    : [f"{cc['fg']['F']}ø{cc['end']}",  f"{cc['fg']['F']}Ø{cc['end']}"]
        }
    }
    roomGrid = s.Dungeon[s.Dy][s.Dx]['room']
    for _ in range(randrange(2, 6)*multiple):
        sizeIndex = randrange(0, 2)
        orbIDs = {
            "hp"     : [10, 15],
            "def"    : [11, 16],
            "atk"    : [12, 17],
            "hunger" : [13, 18],
            "exp"    : [14, 19]
            }

        typeIndex = None
        rate = randrange(1, 101)
        if   rate <= 45:               typeIndex = "hunger"
        elif rate > 45 and rate <= 70: typeIndex = "hp"
        elif rate > 70 and rate <= 80: typeIndex = "def"
        elif rate > 80 and rate <= 85: typeIndex = "atk"
        else                         : typeIndex = "exp"

        idIndex = orbIDs[typeIndex][sizeIndex]
        placeRandomBlock(
            orbs['type'][typeIndex][sizeIndex],
            idIndex,
            0,
            [1, len(roomGrid)-2],
            [1, len(roomGrid[0])-2],
            [0]
            )