import threading
from   random   import randrange, choices

from Assets.data             import totalGameStatus as s
from Game.entities.entity    import addMonster
from Game.utils.system.block import iset

from Game.core.system.data.dataLoader import (
    obj
)


def changeDoor(blockID:str, data:dict, icon:str="None") -> None:
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
    block = obj('-bb', blockID, block=iset(s.bids[blockID]if icon=="None"else icon))
    room  = s.Dungeon[s.Dy][s.Dx]['room']

    for pos, activate in zip(*map(list, zip(*data['doors'].items()))):
        if activate:
            DPY, DPX = DPG[pos][:2]

            room[DPY][DPX] = block
            match pos:
                case 'U'|'D': room[DPY][DPX-1], room[DPY][DPX+1] = block, block
                case 'R'|'L': room[DPY-1][DPX], room[DPY+1][DPX] = block, block

def summonEnemy(data             :list ,
                hpMultiplier     :int=1,
                atkMultiplier    :int=1,
                ashChipMultiplier:int=1) -> None:
    def event() -> None:
        nonlocal data

        s.Dungeon[s.Dy][s.Dx]['summonData'] = []
        # for i in range(count, 0, -1):
        for eid, i in zip(data, range(len(data),0,-1)):
            addMonster(
                eid,
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
    
def randPlaceBlock(block        :str         ,
                   ID           :str         ,
                   y            :list[int]   ,
                   x            :list[int]   ,
                   allowedBlocks:list[str]   ,
                   face         :str      ='s') -> None:
    """
    방에서 블럭 등을 랜덤하게 배치할 수 있게 만든 함수

    `block`(char) : 랜덤하게 배치될 블럭의 아이콘
    `y`(list)     : 방의 y 최솟값과 최댓값 데이터
    - `ex) y = [최솟값, 최댓값]`

    `x`(list): 방의 x 최솟값과 최댓값 데이터
    - `ex) x = [최솟값, 최댓값]`

    `allowedBlocks`(list) : 블록을 놓을 수 있는 블록의 id
    """
    data      = { "block" : iset(block, Type=face) }
    stackable = True\
            if obj('-bb', ID).get('blockData' , False)\
        else False

    while 1:
        Ry, Rx = randrange(*y), randrange(*x)
        if s.Dungeon[s.Dy][s.Dx]['room'][Ry][Rx]["id"] not in allowedBlocks: continue

        if stackable:
            data["blockData"] = s.Dungeon[s.Dy][s.Dx]['room'][Ry][Rx]
            
        break
        
    s.Dungeon[s.Dy][s.Dx]['room'][Ry][Rx] = obj('-bb', ID, **data)

def randPlaceOrb(multiple:int=1) -> None:
    for _ in range(randrange(2, 6)*multiple):
        orbId = f"{choices(
            ('hg', 'hp', 'df', 'atk', 'cs'),
            weights=(45, 15, 10, 5, 15),
            k      =1
        )[0]}Orb{choices(
            ('S', 'B'),
            weights=(60, 40),
            k      =1
        )[0]}"

        randPlaceBlock(
            s.bids[orbId],
            orbId,
            [1, s.roomData['maxHeight']-2],
            [1,  s.roomData['maxWidth']-2],
            
            ['floor']
        )