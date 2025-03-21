import threading
from   random   import randrange, choice

from Assets.data                 import totalGameStatus as s
from Game.core.system.dataLoader import obj
from Game.entities.entity        import addMonster
from Game.utils.system.block     import iset


def changeDoor(blockID:int, data:dict, icon:str="None") -> None:
    c = {
        'y' : s.roomData['maxHeight']//2,
        'x' : s.roomData['maxWidth'] //2
    }
    DPG = {
        'U' : [0,                         c['x']],
        'R' : [c['y'],  s.roomData['maxWidth']-1],
        'D' : [s.roomData['maxHeight']-1, c['x']],
        'L' : [c['y'],                         0]
    }
    block = obj('-bb', str(blockID), block=iset(s.ids[blockID]if icon=="None"else icon))
    room  = s.Dungeon[s.Dy][s.Dx]['room']

    for pos, activate in zip(*map(list, zip(*data['doors'].items()))):
        if activate:
            DPY, DPX = DPG[pos][:2]

            room[DPY][DPX] = block
            match pos:
                case 'U'|'D': room[DPY][DPX-1], room[DPY][DPX+1] = block, block
                case 'R'|'L': room[DPY-1][DPX], room[DPY+1][DPX] = block, block

def summonMonster(count            :int       ,
                  hpMultiplier     :int  =1   ,
                  atkMultiplier    :int  =1   ,
                  ashChipMultiplier:int  =1   ,
                  monsterType      :int  =0   ,
                  useRandom        :bool =True,
                  boss             :bool =False) -> None:
    def event() -> None:
        nonlocal count

        s.Dungeon[s.Dy][s.Dx]['summonCount'] = 0
        for i in range(count, 0, -1):
            addMonster(
                choice([[0,1,2],[0,1]][boss])if useRandom else monsterType,
                hpMultiplier,
                atkMultiplier,
                ashChipMultiplier,
                Dy  =s.Dy,
                Dx  =s.Dx,
                y   =[1, s.roomData['maxHeight']-2],
                x   =[1,  s.roomData['maxWidth']-2],
                lock=True if i==1 else False
            )
            
    threading.Thread(target=event, daemon=True).start()
    
def randPlaceBlock(block        :str      ,
                   ID           :int      ,
                   y            :list[int],
                   x            :list[int],
                   allowedBlocks:list[int] ) -> None:
    """
    방에서 블럭 등을 랜덤하게 배치할 수 있게 만든 함수

    `block`(char) : 랜덤하게 배치될 블럭의 아이콘
    `y`(list)     : 방의 y 최솟값과 최댓값 데이터
    - `ex) y = [최솟값, 최댓값]`

    `x`(list): 방의 x 최솟값과 최댓값 데이터
    - `ex) x = [최솟값, 최댓값]`

    `allowedBlocks`(list) : 블록을 놓을 수 있는 블록의 id
    """
    while 1:
        Ry, Rx = randrange(*y), randrange(*x)
        if s.Dungeon[s.Dy][s.Dx]['room'][Ry][Rx]["id"] not in allowedBlocks: continue
        break
        
    s.Dungeon[s.Dy][s.Dx]['room'][Ry][Rx] = obj('-bb', str(ID), block=iset(block, Type='s'))

def randPlaceOrb(multiple:int=1) -> None:
    room = s.Dungeon[s.Dy][s.Dx]['room']
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
        rate      = randrange(1, 101)

        if        rate <= 45: typeIndex = "hunger"
        elif 45 < rate <= 70: typeIndex = "hp"
        elif 70 < rate <= 80: typeIndex = "def"
        elif 80 < rate <= 85: typeIndex = "atk"
        else                : typeIndex = "exp"

        randPlaceBlock(
            s.ids[s.orbIds['type'][typeIndex][sizeIndex]],
            orbIDs[typeIndex][sizeIndex],
            [1, s.roomData['maxHeight']-2],
            [1,  s.roomData['maxWidth']-2],
            
            [0]
        )