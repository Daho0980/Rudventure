from random import randrange, choice
from copy   import deepcopy

from Assets.data.color           import cColors      as cc
from Assets.data.doors           import doorWayPoint as dwp
from Assets.data.probs           import dungeon      as per
from Game.behavior.blocks.events import squishy
from Game.utils.system.block     import iset

from Assets.data import (
    totalGameStatus as s,
    rooms           as r
)
from Game.behavior.blocks.events.clayModel import (
    Orb,
    Life,

    afterAction
)
from Game.core.system.data.dataLoader import (
    obj
)


def graphicMaker(MapData:list):
    """
    맵의 데이터에서 방 아이콘만 빼내 그래픽을 출력하기 쉽게 하기 위해 만든 함수

        `MapData`(list(2d)) : `deleteBlankData`함수로 공백칸을 제거한 맵이 포함됨
    """
    grid = []
    for i in range(len(MapData)):
        grid.append([])
        for j in range(len(MapData[i])):
            if len(MapData[i][j]) > 0: grid[i].append(f"{cc['fg'][s.DungeonMap[i][j][1]]}{s.DungeonMap[i][j][0]}{cc['end']}")
            else                     : grid[i].append(' ')

    return grid

def _isPosAvailable(pos    :tuple[int,int],
                    name   :str           ,
                    mapArea:tuple[int,int] ) -> bool:
    y , x  = pos
    my, mx = mapArea
    return (
        name=='U' and y>=0  or
        name=='R' and x< mx or
        name=='D' and y< my or
        name=='L' and x>=0
    )

locator:dict[str,str] = {'U' : 'D', 'R' : 'L', 'D' : 'U', 'L' : 'R'}
def _setDoor(Map:list) -> list:
    mapArea = (len(Map), len(Map[0]))

    for row in range(mapArea[0]):
        for col in range(mapArea[1]):
            if Map[row][col]:
                if Map[row][col]['roomType']=='endPoint': continue

                roomName = Map[row][col]['name']

                for name, rp in {
                    n : p
                    for n, p in {
                        'U' : (row-1, col  ),
                        'R' : (row  , col+1),
                        'D' : (row+1, col  ),
                        'L' : (row  , col-1)
                    }.items()
                    if  _isPosAvailable(p, n, mapArea)
                    and Map[p[0]][p[1]]
                    and (
                        Map[p[0]][p[1]]['doors'][locator[n]]
                        or not randrange(0, 3)
                    )
                }.items():
                    targetRoomName = Map[rp[0]][rp[1]]['name']

                    Map[row][col]['doors'][name]              = 1
                    Map[rp[0]][rp[1]]['doors'][locator[name]] = 1

                    for dp, wp in zip(
                        dwp[roomName]['set'][name],
                        dwp[targetRoomName]['out'][locator[name]]
                    ):
                        Map[row][col]['room'][dp[0]][dp[1]] = obj(
                            '-bb', 'door',
                            nbt={
                                'wp'   : (*rp, *wp),
                                'lock' : False
                            }
                        )

                    for sdp, swp in zip(
                        dwp[targetRoomName]['set'][locator[name]],
                        dwp[roomName]['out'][name]
                    ):
                        Map[rp[0]][rp[1]]['room'][sdp[0]][sdp[1]] = obj(
                            '-bb', 'door',
                            nbt={
                                'wp'   : (row, col, *swp),
                                'lock' : False
                            }
                        )

    return Map

def makeRoom(Map:list) -> list:
    """
    방을 추가함

    Map: 원본 던전 데이터
    """
    if not Map: return Map

    for row in range(len(Map)):
        for col in range(len(Map[row])):
            if Map[row][col]:
                match Map[row][col]['roomType']:
                    case 'endPoint':
                        baseMap = deepcopy(r.EndPoint)
                        Map[row][col]['name'] = "EndPoint"
                    
                    case 'treasure':
                        baseMap = deepcopy(r.TreasureRoom)
                        Map[row][col]['name'] = "TreasureRoom"

                    case 'event':
                        if Map[row][col]['eventType']in[1,2,3]:
                            baseMap = deepcopy(r.Chapel)
                            Map[row][col]['name'] = "Chapel"

                        else: Map[row][col]['roomType'] = "room"

                    case 'startPoint':
                        baseMap = deepcopy(r.Room)
                        Map[row][col]['name'] = "Room"

                if Map[row][col]['roomType'] == 'room':
                    roomNum = randrange(0, 4)
                    baseMap = deepcopy((
                        r.Room,
                        r.VerticallyLongRoom,
                        r.HorizonallyLongRoom,
                        r.Diamond
                    )[roomNum])
                    Map[row][col]['name'] = (
                        "Room",
                        "VerticallyLongRoom",
                        "HorizonallyLongRoom",
                        "Diamond"
                    )[roomNum]

                c = {
                    'y'  : int(len(baseMap)   /2)  ,
                    'ym' : int(len(baseMap)   /2)-1,
                    'yp' : int(len(baseMap)   /2)+1,
                    'x'  : int(len(baseMap[0])/2)  ,
                    'xm' : int(len(baseMap[0])/2)-1,
                    'xp' : int(len(baseMap[0])/2)+1
                } # 방 중심 및 주변 칸 위치 데이터

                match Map[row][col]['roomType']:
                    case 'treasure':
                        treasureLocs = {
                            0 : [
                                [c['y'], c['x']]
                            ],
                            1 : [
                                [c['ym'], c['xm']],
                                [c['y'],  c['x'] ],
                                [c['yp'], c['xp']]
                            ],
                            2 : [
                                [c['ym'], c['xm']],
                                [c['ym'], c['xp']],
                                [c['y'],  c['x'] ],
                                [c['yp'], c['xm']],
                                [c['yp'], c['xp']]
                            ]
                        }[Map[row][col]['treasureRarity']]

                        for tby, tbx in treasureLocs:
                            face = choice(['l','r'])
                            baseMap[tby][tbx] = obj(
                                '-bb', 'orbBox',
                                block=iset(s.bids['orbBox'], Type=face),
                                nbt  ={ "face" : face }
                            )

                    case 'event':
                        match Map[row][col]['eventType']:
                            case 0:
                                status = (
                                    ('R',  f"{cc['fg']['R']}빈 최대 체력{cc['end']} 1칸"   , Orb.hp     ),
                                    ('B1', f"{cc['fg']['B1']}빈 최대 방어력{cc['end']} 1칸", Orb.df     ),
                                    ('L',  f"{cc['fg']['L']}공격력{cc['end']} 1"           , Orb.atk    ),
                                    ('G1', f"{cc['fg']['G1']}재의 그릇{cc['end']} 1개"     , Orb.ashChip)
                                )[randrange(0,4)]

                                s.DungeonMap[row][col] = (s.bids['clayModel'][:1], status[0])
                                baseMap[c['y']][c['x']]   = obj(
                                    '-bb', 'clayModel',
                                    block=iset(f"{cc['fg'][status[0]]}{s.bids['clayModel']}{cc['end']}"),
                                    nbt={
                                        "texts" : [
                                            (f"'와우, 여긴 어떻게 오신 거예요?'", Life.awake),
                                            "'다른 이벤트가 없어서 실망하셨다고요? 저런...'",
                                            (f"'대신 {status[1]}와/과 응원을 드리겠습니다.'", status[2]),
                                            ("'그럼 화이팅!'", Life.kill)
                                        ],
                                        "delay"   : 0.5,
                                        "voice"   : "clayModel",
                                        "command" : afterAction
                                    }
                                )

                            case 1|2|3:
                                if randrange(1,101) <= per.statueContamination:
                                    rNbt = [ ("link", False) ]
                                    ctd  = True

                                else:
                                    rNbt = [ ("linkedInteraction", True) ]
                                    ctd  = False

                                s.DungeonMap[row][col] = ('Y', "F"if ctd else"A")

                                for y, x, icon in (
                                    [c['ym'], c['xm'], f"{cc['fg']['F'if ctd else'A']}‾\\{cc['end']}"],
                                    [c['ym'], c['x'] , f"{cc['fg']['F'if ctd else'A']}ㅇ{cc['end']}" ],
                                    [c['ym'], c['xp'], f"{cc['fg']['F'if ctd else'A']}/‾{cc['end']}" ],
                                    [c['y'],  c['x'] , f"{cc['fg']['F'if ctd else'A']}뮤{cc['end']}" ],
                                    [c['yp'], c['xm'], f"{cc['fg']['F'if ctd else'A']}[ {cc['end']}" ],
                                    [c['yp'], c['x'] , f"{cc['fg']['F'if ctd else'A']}ㅍ{cc['end']}" ],
                                    [c['yp'], c['xp'], f"{cc['fg']['F'if ctd else'A']} ]{cc['end']}" ],
                                ):
                                    baseMap[y][x] = obj('-bb', 'cursedStatue'if ctd else'normalStatue', block=iset(icon), nbt=dict(rNbt))

                                for _ in range(25):
                                    ty, tx = randrange(c['y']-3, c['y']+4), randrange(c['x']-3, c['x']+4)

                                    if (baseMap[ty][tx]['id'], baseMap[ty][tx]['block']) == ('floor' , '  '):
                                        color = choice(['F', 'R', 'M'])

                                        baseMap[ty][tx] = {
                                            "block" : iset(f"{cc['fg'][color]}{choice(['*', ',', '.', '_'])}{cc['end']}", Type='s'),
                                            "id"    : 'flower',
                                            "type"  : 'block',
                                            "nbt"   : {
                                                "color" : color,
                                                "step"  : 1
                                            }
                                        }

                    case 'startPoint':
                        if not randrange(0,8):
                            hasEvent = randrange(0,2)
                            face     = choice(('l','r'))

                            baseMap[1][1] = obj(
                                '-bb', 'squishy1',
                                block= iset(s.bids['squishy1'], Type=face),
                                nbt  ={
                                    "face"    : face,
                                    "count"   : 50 if hasEvent else -1,
                                    "command" : choice((
                                        squishy.giveLoot,
                                        squishy.explosion
                                    ))
                                }
                            )

                    case 'endPoint':
                        for y, x in ((6,6), (16,6), (6,16), (16,16)):
                            block  = "▓░" if x == 6 else "░▓"
                            change = randrange(1,101) <= per.endPointPillarBonus
                            baseMap[y][x] = obj(
                                '-bb',
                                'orbBox' if change else 'wall',
                                block=block,
                                nbt={ "face" : 's' } if change else {  }
                            )

                Map[row][col]["room"] = baseMap

    return _setDoor(Map)

def deleteBlankData(grid:list):
    """
    맵의 데이터 중 쓸데없이 메모리만 차지하는 공백 데이터를 제거하는 함수
    
        `grid`(list(raw)) : `initBranch`함수로 생긴 맵 데이터가 포함됨, 무조건 기입해야 함
    """
    if not grid: return grid
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            grid[row][col] = {} if grid[row][col]['roomType']==None else grid[row][col]

    return grid