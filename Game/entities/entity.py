import time ; import threading
from   random import randrange

from Assets.data.color           import cColors as cc
from functions.grammar           import pstpos  as pp
from Game.core.system.logger     import addLog
from Game.core.system.dataLoader import obj
from Game.utils.system.sound     import play
from Game.utils.advanced         import hashGenerator

from Assets.data import (
    totalGameStatus as s
)


extraParameters = lambda data: ','.join(f"{k}={v}" for k, v in data.items())

def addTag() -> str:
    while 1:
        tag = hashGenerator.main()
        if tag in s.entityHashPool: continue
        break
    s.entityHashPool.append(tag)

    return tag

# region Monster
def addMonster(ID        :str       ,
               hpMtp     :int       ,
               atkMtp    :int       ,
               acMtp     :int       ,
               Dy        :int       ,
               Dx        :int       ,
               y         :list|int  ,
               x         :list|int  ,
               lock      :bool=False,
               sendEffect:bool =True ) -> None:
    """
    모든 적을 소환할 수 있는 함수

        `ID`(str)                    : 몬스터의 고유 id
        `hpMtp`(int)                 : 몬스터의 기본 체력 배수값
        `atkMtp`(int)                : 몬스터의 기본 공격력 배수값
        `acMtp`(int)                 : 몬스터의 기본 사체 잿가루 배수값
        `Dy`(int), `Dx`(int)         : 엔티티가 소환될 미궁 y, x값
        `y`(list|int), `x`(list|int) : 엔티티가 소환될 방 y, x값
            랜덤하게 소환하려면 list([min, max])로 기입,
            특정한 곳에 소환하려면 int로 기입해야 함. 이 둘은 모두 독립적으로 결정될 수 있음
        `lock`(bool=False)           : 해당 몬스터 소환 시 방 잠금 여부, 기본적으로 `False`로\
                                       설정되어 있음
        `sendEffect`(bool=True)      : 몬스터 사망 시 사망 이펙트 전송 여부, 기본적으로 `True`로\
                                       설정되어 있음
    """
    data = obj(s.path['data']['enemySpd'], ID)
    tag  = addTag()

    mClass      = data['class']
    name        = data['kinds']
    mID         = data['id']
    curse       = data['curse']
    hp          = data['hp']
    atk         = data['atk']
    icon        = data['icon']
    entityCount = data['entityCount']
    ashChip     = data['ashChip']

    s.enemyCount       += entityCount
    s.entityCount      += entityCount
    s.totalEntityCount += 1

    def EntityInteraction() -> None:
        exec(f"""
import time

from Assets.data.permissions import {mClass} as perm
from Game.entities.enemy     import mobs
from Game.utils.system       import xpSystem as xps
             
from Assets.data import (
    totalGameStatus as s,
    lockers         as l
)
             
             
{mClass} = mobs.{mClass}("{name}", "{icon}", '{mID}', "{tag}")
{mClass}.start(
    {((hp-2 if s.cowardMode else hp)*hpMtp)+((s.stage-1)*2)},
    {((atk)*atkMtp)+(s.stage-1)},
    {Dy}, {Dx}, {y}, {x},
    perm
)

if {lock}: s.roomLock = True

while s.main:
    if s.killAll or s.clearEntity: break

    if l.jpsf and not l.pause:
        if {mClass}.hp <= 0:
            s.enemyCount       -= {entityCount}
            s.entityCount      -= {entityCount}
            s.totalEntityCount -= 1
            break
        {mClass}.move()
    else: time.sleep(0.05)

if s.target['tag'] == {mClass}.tag:
    s.target = {{"tag" : "", "attackable" : False, "command" : False}}

if s.main and not (s.killAll or s.clearEntity):
    xps.getXP({curse}*{mClass}.xpMultiplier)
    s.Dungeon[{mClass}.Dy][{mClass}.Dx]['room'][{mClass}.y][{mClass}.x] = {{
        'block' : f"{cc['fg']['G1']}{{{mClass}.icon}}{cc['end']}",
        'id'    : 'ashChip',
        'type'  : 'block',
        'nbt'   : {{
            'count' : {ashChip*acMtp}}}
        }}
        """)
        s.entityHashPool.remove(tag)
        if s.main and not (s.killAll or s.clearEntity):
            s.killCount += 1
            if sendEffect:
                play("player", "slash")
                play("entity", "enemy", "dead")
                addLog(f"{cc['fg']['F']}{name}{cc['end']}{pp(name,'sub',True)} 죽었습니다!", colorKey='F')
    threading.Thread(target=EntityInteraction, name=name, daemon=True).start()
    time.sleep(0.2)

# region Animal
def addAnimal(ID      :str                      ,
              hp      :int                      ,
              atk     :int                      ,
              y       :list|int                 ,
              x       :list|int                 ,
              Dy      :int     =0               ,
              Dx      :int     =0               ,

              icon    :str =""                  ,
              name    :str =""                  ,
              color   :list=[cc['fg']['W'], 'W'],
              friendly:bool=False               ,

              MCBF:bool=False                   ,
              SICR:bool=True                    ,

              extraData  :dict={}               ,
              preloadData:dict={}                ) -> None:
    """
    모든 동물을 소환할 수 있는 함수

        `ID`(int)            : 엔티티의 고유 id
        `hp`(int)            : 엔티티가 가질 체력
        `atk`(int)           : 엔티티가 가질 공격력
        `Dy`(int), `Dx`(int) : 엔티티가 소환될 미궁 y, x값
        `y`(int), `x`(int)   : 엔티티가 소환될 방 y, x값
            랜덤하게 소환하려면 list([min, max])로 기입,
            특정한 곳에 소환하려면 int로 기입해야 함.
            이 둘은 모두 독립적으로 결정될 수 있음

        `icon`(str)                    : 엔티티의 아이콘
        `name`(str)                    : 엔티티의 고유 이름
        `color`(tuple[color, colorKey]): 엔티티의 색
        `friendly`(bool)               : 엔티티 우호 여부. 활성화 시 플레이어는 해당 엔티티를 공격할 수 없음
        `MCBG`(bool)                   : 엔티티 유지 여부. 활성화 시 죽지 않고 계속 남아있음(던전 새로 생성 시 listIndexOutofRange 주의)
        `SICR`(bool)                   : 엔티티를 현재 주목된 방에 소환할지에 대한 여부. 활성화 시 매개변수 `Dy`, `Dx`를 무시함
    """
    data = obj(s.path['data']['animalSpd'], ID)
    if preloadData:
        tag = preloadData['tag']
        s.entityHashPool.append(tag)
        
    else: tag = addTag()

    entity      = data['entity']
    icon        = icon or data['icon']
    name        = name or data['name']
    entityCount = data['entityCount']

    endowmentofFragment = randrange(0,2)

    s.entityCount      += entityCount
    s.totalEntityCount += 1

    if friendly: s.friendlyEntity.append(tag)
    if SICR:     Dy, Dx = s.Dy, s.Dx

    def EntityInteraction() -> None:
        exec(f"""
import time

from Assets.data.permissions import {entity} as perm
from Game.entities.animal    import {entity}
from Game.utils.system       import xpSystem as xps

from Assets.data import (
    totalGameStatus as s,
    lockers         as l
)

             
{entity} = {entity}.{entity}(
    "{entity}", "{name}", "{icon}", '{ID}',
    "{color[0]}", "{color[1]}",
    "{tag}",
    [
        '{ID}',
        {hp}, {atk}, {y}, {x}, {Dy}, {Dx},
        "{icon}", "{name}", {color}, {friendly},
        {MCBF}, {SICR}
    ]
)

{entity}.start(
    {hp}, {atk},
    {Dy}, {Dx}, {y}, {x},
    perm,
    {extraParameters(extraData)}
)

if {preloadData}: {entity}.loadData({preloadData})

while s.main:
    {entity}.waitingGame()
    if   s.killAll:                    break
    elif s.clearEntity and not {MCBF}: break

    if l.jpsf and not l.pause:
        if {entity}.hp <= 0:
            s.entityCount -= {entityCount}
            s.totalEntityCount -= 1
            break
        {entity}.move()
    else:
        time.sleep(0.05)

if s.main and not (s.killAll or s.clearEntity):
    if {endowmentofFragment}:
        addMonster(
            0,
            {int(hp/2) or 1},
            {int(atk/2)or 1},
            {int(hp/4) or 1},
            
            Dy        =s.Dy,
            Dx        =s.Dx,
            y         ={entity}.y,
            x         ={entity}.x,
            lock      =True,
            sendEffect=False
            )
    else:
        s.Dungeon[{entity}.Dy][{entity}.Dx]['room'][{entity}.y][{entity}.x] = {{
            "block" : f"{cc['fg']['M']}{{{entity}.icon}}{cc['end']}",
            'id'    : 'corpse',
            'type'  : 'block',
            'nbt'   : {{
                'link' : True
            }}
        }}"""
        )
        s.entityHashPool.remove(tag)
        if tag in s.friendlyEntity: s.friendlyEntity.remove(tag)
        
        if s.main and not (s.killAll or s.clearEntity):
            s.killCount += 1
            play("player", "slash")
            play("entity", "enemy", "dead")
            addLog(f"{color[0]}{name}{cc['end']}{pp(name,'sub',True)} 죽었습니다!", colorKey='F')

    threading.Thread(target=EntityInteraction, name=name, daemon=True).start()

def loadEntities() -> None:
    for func, data in s.entityDataMaintained.items():
        for entity in list(data.values()):
            eval(func)(*entity['funcParams'], preloadData=entity['selfParams'])