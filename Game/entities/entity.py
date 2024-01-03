"""
Global Functions 중 Entity 옵션

    ``addEntity`` : 모든 엔티티(적)을 소환할 수 있는 함수
"""

import threading
from   Assets.data      import status as s
from   Game.core.system import logger
from   Game.utils.sound import play

def addEntity(entityType:int, initHp:int, Dy:int, Dx:int, y:list, x:list) -> None:
    """
    모든 엔티티(적)을 소환할 수 있는 함수

        `entityType`(int(0~ 1)) : 적의 타입을 정해주는 매개변수, 무조건 기입해야 함
        `initHp`(int)     : 적이 처음으로 가질 체력, 무조건 기입해야 함
        `Dy`(int)         : 적이 소환될 던전 y값, 무조건 기입해야 함
        `Dx`(int)         : 적이 소환될 던전 x값, 무조건 기입해야 함
        `y`(list)         : 적이 소환될 y값, 리스트 형태로 `[방 y 최솟값, 방 y 최댓값]`과 같이 기입해도 되지만,
            특정 위치에 소환하려면 `int`형식으로 기입해야됨
                
        `x`(list)         : 적이 소환될 x값, 리스트 형태로 `[방 x 최솟값, 방 x 최댓값]`과 같이 기입해도 되지만,
            특정 위치에 소환하려면 `int`형식으로 기입해야됨
    """
    kinds:list[str]      = ["고통의_편린", "불안의_편린"]
    classType:list[str]  = ["enemy", "observer"]
    idType:list[int]     = [600, 601]
    xpType:list[int]     = [3, 5]
    atkType:list[int]    = [1, 2]
    Name:str             = kinds[entityType]
    Rname:str            = ""

    icons:list[str] = [s.ids[600], s.ids[601]]
    a:int           = 0
    while 1:
        if Name + f"_{a}" not in s.entities:
            Name  = str(      Name + f"_{a}"       )
            Rname = str(kinds[entityType] + f"_{a}")
            break
        a += 1
    nameSpace:dict[str,str|int|list] = {
        f"{Name}"    : Name,
        "Rname"      : Rname,
        "xpType"     : xpType,
        "entityType" : entityType
    }

    exec(f"""
from   Game.entities.enemy import mobs
from   Assets.data         import status as s
{Name} = mobs.{classType[entityType]}(\"{Name}\", \"{icons[entityType]}\", {idType[entityType]})
{Name}.start({initHp}+((s.stage-1)*2), {atkType[entityType]}+(s.stage-1), {Dy}, {Dx}, {y}, {x})
s.entities.append(Rname)
    """, nameSpace)
    def EntityInteraction() -> None:
        exec(f"""
import time
from   Assets.data                     import lockers, status
from   Game.utils.system import xpSystem as xps

l, s = lockers, status

while s.main == 1:
    if s.killAll: break

    if l.jpsf and not l.pause:
        if {Name}.hp <= 0:
            s.entities.remove(Rname)
            break
        {Name}.move()
    else: time.sleep(0.1)
s.Dungeon[{Name}.Dy][{Name}.Dx]['room'][{Name}.y][{Name}.x] = {{"block" : s.ids[{Name}.stepped], "id" : {Name}.stepped}}
if s.main and not s.killAll: xps.getXP(xpType[entityType])
        """, nameSpace)
        if s.main == 1 and not s.killAll:
            play("monster_dead", 'hostileMob')
            s.killCount += 1
            logger.addLog(f"{s.cColors['fg']['F']}{Name}{s.cColors['end']}이(가) 죽었습니다!")
    threading.Thread(target=EntityInteraction, name=Rname, daemon=True).start()
