"""
Global Functions 중 Entity 옵션

    ``addMonster`` : 모든 몬스터를 소환할 수 있는 함수
"""

import threading, time

from Assets.data       import status as s
from Assets.data.color import cColors as cc
from Game.core.system  import logger


def addMonster(
        entityType:int,
        hpMtp:int,
        atkMtp:int,
        acMtp:int,
        Dy:int,
        Dx:int,
        y:list,
        x:list,
        useRoomLock:bool=False
        ) -> None:
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
    kinds:list[str]           = ["고통의 편린", "불안의 편린", "원망의 편린"]
    classType:list[str]       = ["enemy", "observer", "mine"]
    idType:list[int]          = [600, 601, 602]
    xpType:list[int]          = [3, 5, 3]
    hpType:list[int]          = [4, 10, 5]
    atkType:list[int]         = [1, 2, 7]
    entityCountType:list[int] = [1, 1, 1]
    ashChipType:list[int]     = [1, 2, 1]
    icons:list[str]           = [s.ids[600], s.ids[601], s.ids[602]]

    name:str             = kinds[entityType]
    valuableName         = classType[entityType]

    s.entityCount      += entityCountType[entityType]
    s.totalEntityCount += 1

    def EntityInteraction() -> None:
        exec(f"""
import time
             
from   Assets.data         import lockers, status
from   Game.entities.enemy import mobs
from   Game.utils.system   import xpSystem        as xps

l, s = lockers, status
             
{valuableName} = mobs.{classType[entityType]}("{name}", "{icons[entityType]}", {idType[entityType]})
{valuableName}.start({((hpType[entityType]-2 if s.ezMode else hpType[entityType])*hpMtp)+((s.stage-1)*2)}, {((atkType[entityType])*atkMtp)+(s.stage-1)}, {Dy}, {Dx}, {y}, {x})
if {useRoomLock}: s.roomLock = True

while s.main == 1:
    if s.killAll: break

    if l.jpsf and not l.pause:
        if {valuableName}.hp <= 0:
            s.entityCount      -= {entityCountType[entityType]}
            s.totalEntityCount -= 1
            break
        {valuableName}.move()
    else: time.sleep(0.1)
if s.main ==1 and not s.killAll:
    s.Dungeon[{valuableName}.Dy][{valuableName}.Dx]['room'][{valuableName}.y][{valuableName}.x] = {{
        "block" : f"{cc['fg']['G1']}{{{valuableName}.icon}}{cc['end']}",
        "id"    : 900,
        "nbt"   : {{
            "count" : {ashChipType[entityType]*acMtp}}}
        }}
if s.main and not s.killAll: xps.getXP({xpType[entityType]}*{valuableName}.xpMultiplier)
        """)
        if s.main == 1 and not s.killAll:
            s.killCount += 1
            logger.addLog(f"{cc['fg']['F']}{name}{cc['end']}이(가) 죽었습니다!")
    threading.Thread(target=EntityInteraction, name=name, daemon=True).start()
    time.sleep(0.2)
