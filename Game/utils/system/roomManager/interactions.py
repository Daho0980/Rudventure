import threading
from   random   import randrange, choices

from Assets.data             import totalGameStatus as s
from Assets.data.doors       import doorWayPoint    as dwp
from Game.entities.entity    import addEnemy
from Game.tools.block        import get, randPlace
from Game.utils.system.block import iset


def changeDoor(Type:str, roomName:str, doorData:dict[str,int], block:str) -> None:
    """
    Type = "open" || "close"
    """
    for n, a in doorData.items():
        if a:
            for y, x in dwp[roomName]['set'][n]:
                target = s.Dungeon[s.Dy][s.Dx]['room'][y][x]

                target['block'] = block
                if Type   == "open" : target['nbt']['lock'] = False
                elif Type == "close": target['nbt']['lock'] = True

                else: raise Exception(f"'{Type}' 타입은 유효한 타입이 아닙니다!")

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