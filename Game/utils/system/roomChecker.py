import threading, random

from   Assets.data          import comments, lockers, status
from   Game.core.system     import logger
from   Game.entities.entity import addEntity
from   Game.utils.modules   import cSelector
from   Game.utils.system    import placeRandomBlock
from   Game.utils.sound     import play


c, l, s  = comments,          lockers, status
selector = cSelector
cc       = s.cColors

def changeDoorPosBlock(ID:int, data:dict) -> None:
    DPG:dict[str,list[int]] = {
        'U' : [0,  6],
        'R' : [6, 12],
        'D' : [12, 6],
        'L' : [6,  0]
        }
        
    for i in range(len(data['doorPos'])):
        keys, values = list(data['doorPos'].keys()), list(data['doorPos'].values())
        if values[i] == 1:
            DPY, DPX = DPG[keys[i]][0], DPG[keys[i]][1]

            s.Dungeon[s.Dy][s.Dx]['room'][DPY][DPX] = {"block" : s.ids[ID], "id" : ID}
            if   keys[i] in ['U','D']: s.Dungeon[s.Dy][s.Dx]['room'][DPY][DPX-1], s.Dungeon[s.Dy][s.Dx]['room'][DPY][DPX+1] = {"block" : s.ids[ID], "id" : ID}, {"block" : s.ids[ID], "id" : ID}
            elif keys[i] in ['R','L']: s.Dungeon[s.Dy][s.Dx]['room'][DPY-1][DPX], s.Dungeon[s.Dy][s.Dx]['room'][DPY+1][DPX] = {"block" : s.ids[ID], "id" : ID}, {"block" : s.ids[ID], "id" : ID}

def summonRandomMonster(data:dict) -> None:
    # type, hp
    def event() -> None:
        nonlocal data

        count = data['summonCount']
        s.Dungeon[s.Dy][s.Dx]['summonCount'] = 0
        monsterData = [[0, 4], [1, 10]]
        for _ in range(count):
            choiced = random.choice(monsterData)
            addEntity(
                choiced[0],
                choiced[1],
                Dy=s.Dy,
                Dx=s.Dx,
                y =[1, len(data['room'])-2   ],
                x =[1, len(data['room'][0])-2],
                useRoomLock=True if _==count-1 else False
                )
    threading.Thread(target=event, daemon=True).start()
    
def placeRandomOrbs() -> None:
    # hp -> def -> atk -> hng -> exp
    orbs:dict = {
        "size" : {
            "smallOne" : [
                f"{cc['fg']['R']}o{cc['end']}",
                f"{cc['fg']['B1']}o{cc['end']}",
                f"{cc['fg']['L']}o{cc['end']}",
                f"{cc['fg']['Y']}o{cc['end']}",
                f"{cc['fg']['F']}ø{cc['end']}"
            ],
            "bigOne" : [
                f"{cc['fg']['R']}O{cc['end']}",
                f"{cc['fg']['B1']}O{cc['end']}",
                f"{cc['fg']['L']}O{cc['end']}",
                f"{cc['fg']['Y']}O{cc['end']}",
                f"{cc['fg']['F']}Ø{cc['end']}"
            ]
        },
        "type" : {
            "hp"     : [f"{cc['fg']['R']}o{cc['end']}",  f"{cc['fg']['R']}O{cc['end']}"],
            "def"    : [f"{cc['fg']['B1']}o{cc['end']}", f"{cc['fg']['B1']}O{cc['end']}"],
            "atk"    : [f"{cc['fg']['L']}o{cc['end']}",  f"{cc['fg']['L']}O{cc['end']}"],
            "hunger" : [f"{cc['fg']['Y']}o{cc['end']}",  f"{cc['fg']['Y']}O{cc['end']}"],
            "exp"    : [f"{cc['fg']['F']}ø{cc['end']}",  f"{cc['fg']['F']}Ø{cc['end']}"]
        }
    }
    roomGrid = s.Dungeon[s.Dy][s.Dx]['room']
    for _ in range(random.randrange(2, 6)):
        orbIDs = {"hp" : [10, 15], "def" : [11, 16], "atk" : [12, 17], "hunger" : [13, 18], "exp" : [14, 19]}
        sizeIndex = random.randrange(0, 2)

        typeIndex = None
        rate = random.randrange(1, 101)
        if   rate > 0  and rate <= 45: typeIndex = "hunger"
        elif rate > 45 and rate <= 70: typeIndex = "hp"
        elif rate > 70 and rate <= 80: typeIndex = "def"
        elif rate > 80 and rate <= 85: typeIndex = "atk"
        else                         : typeIndex = "exp"

        idIndex = orbIDs[typeIndex][sizeIndex]
        placeRandomBlock(
            orbs['type'][typeIndex][sizeIndex],
            idIndex,
            [1, len(roomGrid)-2],
            [1, len(roomGrid)-2],
            [0]
            )

def main() -> None:
    data:dict = s.Dungeon[s.Dy][s.Dx]

    if l.jpsf and data['interaction'] == False:
        commentP = True if random.randrange(1, 3) == 1 else False
        match data['roomType']:
            case 1:
                if data['summonCount'] > 0:
                    play("close_door", 'interaction')
                    summonRandomMonster(data)

                    changeDoorPosBlock(1, data)
                elif not s.entities and s.roomLock:
                    play("open_door", 'interaction')

                    s.roomLock = False
                    s.Dungeon[s.Dy][s.Dx]['interaction'] = True
                    placeRandomOrbs()
                    changeDoorPosBlock(2, data)

            case 2:
                logger.addLog(f"(슬쩍) 아직 {cc['fg']['L']}이벤트{cc['end']}는 {cc['fg']['R']}{s.cMarkdown([1,2])}안{cc['end']} 만들었답니다 ㅎㅎ;")
                s.Dungeon[s.Dy][s.Dx]['interaction'] = True

            case 3:
                rewardP = random.randrange(1, 101)
                comment = ""

                if rewardP > 30:
                    s.Dungeon[s.Dy][s.Dx]['room'][6][6] = {"block" : s.ids[4], "id" : 4}
                    if commentP: comment = random.choice(c.treasureRoomComment[0])
                elif rewardP >= 10 and rewardP < 30:
                    for i in range(5, 8): s.Dungeon[s.Dy][s.Dx]['room'][i][i] = {"block" : s.ids[4], "id" : 4}
                    if commentP: comment = random.choice(c.treasureRoomComment[1])
                else:
                    for i in range(5, 8): s.Dungeon[s.Dy][s.Dx]['room'][i][i] = {"block" : s.ids[4], "id" : 4}
                    s.Dungeon[s.Dy][s.Dx]['room'][5][7] = {"block" : s.ids[4], "id" : 4}
                    s.Dungeon[s.Dy][s.Dx]['room'][7][5] = {"block" : s.ids[4], "id" : 4}
                    if commentP: comment = random.choice(c.treasureRoomComment[2])
                if commentP: logger.addLog(f"{cc['fg']['L']}\"{comment}\"{cc['end']}")
                s.Dungeon[s.Dy][s.Dx]['interaction'] = True

            case 4:
                if data['summonCount'] > 0:
                    play("close_door", 'interaction')
                    summonRandomMonster(data)

                    s.Dungeon[s.Dy][s.Dx]['room'][6][6] = {"block" : s.ids[0], "id" : 0}
                    changeDoorPosBlock(1, data)
                elif not s.entities and s.roomLock:
                    play("open_door", 'interaction')

                    s.roomLock = False
                    s.Dungeon[s.Dy][s.Dx]['room'][6][6]  = {"block" : s.ids[5], "id" : 5}
                    s.Dungeon[s.Dy][s.Dx]['interaction'] = True
                    placeRandomOrbs()
                    changeDoorPosBlock(2, data)