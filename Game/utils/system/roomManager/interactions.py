import threading
from   random   import randrange, choices

from Assets.data             import totalGameStatus as s
from Game.entities.entity    import addEnemy
from Game.tools.block        import get, randPlace
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

def summonEnemy(data:list) -> None:
    def event() -> None:
        nonlocal data

        s.Dungeon[s.Dy][s.Dx]['summonData'] = []
        for eid, i in zip(data, range(len(data),0,-1)):
            addEnemy(
                eid,
                Dy  =s.Dy,
                Dx  =s.Dx,
                y   =[1, s.roomData['maxHeight']-2],
                x   =[1,  s.roomData['maxWidth']-2],
                lock=True if i==1 else False
            )
            
    threading.Thread(target=event, daemon=True).start()

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

        randPlace(
            get(orbId, block=iset(s.bids[orbId], Type='s')),
            (1, s.roomData['maxHeight']-2),
            (1,  s.roomData['maxWidth']-2),
            
            ['floor']
        )