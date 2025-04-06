from random import randrange, choice
from copy   import deepcopy

from Assets.data.color           import cColors as cc
from Game.core.system.dataLoader import obj
from Game.utils.system.block     import iset

from Assets.data import (
    totalGameStatus as s,
    percentage      as per,
    rooms           as r
)


def graphicMaker(MapData:list):
    """
    맵의 데이터에서 방 아이콘만 빼내 그래픽을 출력하기 쉽게 하기 위해 만든 함수

        `MapData`(list(2d)) : `deleteBlankData`함수로 공백칸을 제거한 맵이 포함됨, 무조건 기입해야 함
    """
    grid = []
    for i in range(len(MapData)):
        grid.append([])
        for j in range(len(MapData[i])):
            if len(MapData[i][j]) > 0: grid[i].append(f"{cc['fg'][MapData[i][j]['roomIcon'][1]]}{MapData[i][j]['roomIcon'][0]}{cc['end']}")
            else                     : grid[i].append(' ')

    return grid

def makeRoom(Map:list):
    """
    `deleteBlankData`함수로 수정된 맵 데이터 중 "room" 데이터를 추가하는 함수, 맵 데이터 중 "doors"도 활용함

        `Map`(list(raw)) : `deleteBlankData`함수로 수정된 맵이 포함됨, 무조건 기입해야 함
    """
    if not Map: return Map

    output = deepcopy(Map)

    # 방 생성
    for row in range(len(output)):
        for column in range(len(output[row])):
            if len(output[row][column]) > 0:
                if output[row][column]['roomType'] == 'endPoint':
                    baseMap = deepcopy(r.bigRoom)
                    output[row][column]['name'] = 'bigRoom'

                elif output[row][column]['roomType'] == 'treasure':
                    baseMap = deepcopy(r.treasureRoom)
                    output[row][column]['name'] = 'treasureRoom'

                elif output[row][column]['roomType']=='event' and output[row][column]['eventType']in[1,2,3]:
                    baseMap = deepcopy(r.chapel)
                    output[row][column]['name'] = 'chapel'

                elif output[row][column]['roomType'] == 'startPoint':
                    baseMap = deepcopy(r.Room)
                    output[row][column]['name'] = 'Room'

                else:
                    roomNum = randrange(0, 3)
                    baseMap = deepcopy([
                        r.Room,
                        r.verticallyLongRoom,
                        r.horizonallyLongRoom
                    ][roomNum])
                    output[row][column]['name'] = [
                        "Room",
                        "verticallyLongRoom",
                        "horizonallyLongRoom"
                    ][roomNum]

                c  = {
                        'y'  : int(len(baseMap)   /2)  ,
                        'ym' : int(len(baseMap)   /2)-1,
                        'yp' : int(len(baseMap)   /2)+1,
                        'x'  : int(len(baseMap[0])/2)  ,
                        'xm' : int(len(baseMap[0])/2)-1,
                        'xp' : int(len(baseMap[0])/2)+1
                    } # 방 중심 및 주변 칸 위치 데이터

                match output[row][column]['roomType']:
                    case 'treasure':
                        treasureLocations = {
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
                        }

                        for tby, tbx in treasureLocations[output[row][column]['treasureRarity']]:
                            face = choice(['l','r'])
                            baseMap[tby][tbx] = obj('-bb', 'orbBox', block=iset(s.bids['orbBox'], Type=face), nbt={ "face" : face })

                    case 'event':
                        match output[row][column]['eventType']:
                            case 0:
                                status = [
                                    ['R',  f"{cc['fg']['R']}빈 최대 체력{cc['end']} 1칸",    "s.Mhp += 1"],
                                    ['B1', f"{cc['fg']['B1']}빈 최대 방어력{cc['end']} 1칸", "s.Mdf += 1"],
                                    ['L',  f"{cc['fg']['L']}공격력{cc['end']} 1",            "s.atk += 1"],
                                    [
                                        'G1', f"{cc['fg']['G1']}재의 그릇{cc['end']} 1개",
                                        "s.Mlvl += 1; play('system', 'ashDiskUp'); logger.addLog(f\"{cc['fg']['G1']}재의 그릇{cc['end']}이 {cc['fg']['F']}1{cc['end']} 개 증가했습니다. (최대 레벨 {cc['fg']['G1']}{s.Mlvl-1}{cc['end']} -> {cc['fg']['F']}{s.Mlvl}{cc['end']})\", colorKey='G1')"
                                    ]
                                ][randrange(0, 4)]

                                output[row][column]['roomIcon'] = [s.bids['clayModel'][:1], status[0]]
                                baseMap[c['y']][c['x']]         = obj(
                                    '-bb', 'clayModel',
                                    block=iset(f"{cc['fg'][status[0]]}{s.bids['clayModel']}{cc['end']}"),
                                    nbt={
                                        "texts" : [
                                            [f"'와우, 방금 당신 1/6의 확률을 뚫고 {cc['fg'][status[0]]}저{cc['end']}를 만나셨어요!'", "s.enemyCount += 1"],
                                            "'다른 이벤트가 없어서 실망하셨다고요? 저런...'",
                                            [f"'대신 {status[1]}(와)과 응원을 드리겠습니다.'", status[2]],
                                            ["'그럼 화이팅!'", "s.enemyCount -= 1"]
                                        ],
                                        "command" : "time.sleep(0.5); p.say(choice(c.clayModelAnswer))",
                                        "delay"   : 0.5,
                                        "voice"   : "clayModel"
                                    }
                                )

                            case 1|2|3:
                                if randrange(1,101) <= per.statueContamination:
                                    rNbt = [ ("link", False) ]
                                    ctd  = True

                                else:
                                    rNbt = [ ("linkedInteraction", True) ]
                                    ctd  = False

                                output[row][column]['roomIcon'] = ['Y', "F"if ctd else"A"]

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

                                    else: continue

                    case 'startPoint':
                        if not randrange(0,8):
                            hasEvent      = randrange(0,2)
                            face          = choice(['l','r'])
                            baseMap[1][1] = obj(
                                '-bb', 'squishy1',
                                block= iset(s.bids['squishy1'], Type=face),
                                nbt  ={
                                    "face"    : face,
                                    "count"   : 50 if hasEvent else -1,
                                    "command" : choice([
                                        f"""
play("object", "squishy", "open")
kind = choice(('aorta', 'venaCava'))
s.Dungeon[s.Dy][s.Dx]['room'][ty][tx] = {{
    "block" : iset(s.bids[kind], Type='{face}'),
    "id"    : kind,
    "type"  : 'block'
}}
""",
                                    f"""
play("object", "squishy", "explosion")
s.hp -= 5
event.bleeding(5)
s.DROD = ["{cc['fg']['B1']}말랑이{cc['end']}", 'B1']
s.Dungeon[s.Dy][s.Dx]['room'][ty][tx] = {{
    "block" : f'{cc['fg']['B1']}x {cc['end']}',
    "id"    : 'floor',
    "type"  : 'block'
}}
event.readSign(["{cc['fg']['B1']}'하하하, 터어어어얼렸구나!!'{cc['end']}"], 0.07, "clayModel")
"""
                                    ])
                                }
                            )

                RDP :list[int]       = list(output[row][column]["doors"].values())
                GRDP:list[list[int]] = [
                    [0             ,            c['x']], # U
                    [c['y']        , len(baseMap[0])-1], # R
                    [len(baseMap)-1,            c['x']], # D
                    [c['y']        ,                 0]  # L
                ]

                for DIE in range(len(RDP)):
                    if RDP[DIE] == 1:
                        baseMap[GRDP[DIE][0]][GRDP[DIE][1]] = obj('-bb', 'door')
                        match DIE:
                            case 0|2:
                                baseMap[GRDP[DIE][0]][GRDP[DIE][1]-1] = obj('-bb', 'door')
                                baseMap[GRDP[DIE][0]][GRDP[DIE][1]+1] = obj('-bb', 'door')

                            case 1|3:
                                baseMap[GRDP[DIE][0]-1][GRDP[DIE][1]] = obj('-bb', 'door')
                                baseMap[GRDP[DIE][0]+1][GRDP[DIE][1]] = obj('-bb', 'door')

                output[row][column]["room"] = baseMap

    for row in range(len(output)):
        for column in range(len(output[row])):
            if len(output[row][column]) > 0:
                if output[row][column] and output[row][column]['roomType']=="endPoint" or not randrange(0,3): continue

                p = [
                    [row-1 if row>0 else row,                      column],
                    [row+1 if row<len(output)-1 else row,          column],
                    [row,                column-1 if column>0 else column],
                    [row, column+1 if column<len(output[0])-1 else column]
                    ]
                for i, pos in enumerate(p):
                    if len(output[pos[0]][pos[1]])==0: p[i] = [row, column]
                
                c = {
                    0 : {
                        'y'  : int(len(output[row][column]['room'])/2)   ,
                        'my' : len(output[row][column]['room'])-1        ,
                        'x'  : int(len(output[row][column]['room'][0])/2),
                        'mx' : len(output[row][column]['room'][0])-1
                    },
                    'U' : { # subTarget 기준 D
                        'my' : len(output[p[0][0]][p[0][1]]['room'])-1       ,
                        'x'  : int(len(output[p[0][0]][p[0][1]]['room'][0])/2)
                    },
                    'D' : { # subTarget 기준 U
                        'x'  : int(len(output[p[1][0]][p[1][1]]['room'][0])/2)
                    },
                    'L' : { # subTarget 기준 R
                        'y'  : int(len(output[p[2][0]][p[2][1]]['room'])/2),
                        'mx' : len(output[p[2][0]][p[2][1]]['room'][0])-1
                    },
                    'R' : { # subTarget 기준 L
                        'y' : int(len(output[p[3][0]][p[3][1]]['room'])/2)
                    },
                }

                R0DPG = {
                    'U':[0         ,  c[0]['x']],
                    'R':[c[0]['y'] , c[0]['mx']],
                    'D':[c[0]['my'],  c[0]['x']],
                    'L':[c[0]['y'] ,          0]
                    }
                SBDPG = {
                    'D':[c['U']['my'],  c['U']['x']],
                    'L':[c['R']['y'] ,            0],
                    'U':[0           ,  c['D']['x']],
                    'R':[c['L']['y'] , c['L']['mx']]
                    }

                dp         = [['U', 'D'], ['D', 'U'], ['L', 'R'], ['R', 'L']]
                doorValues = list(output[row][column]['doors'].values())
                grd        = [
                    [R0DPG['U'], SBDPG['D']],
                    [R0DPG['D'], SBDPG['U']],
                    [R0DPG['L'], SBDPG['R']],
                    [R0DPG['R'], SBDPG['L']]
                ]

                while [row, column] in p:
                    del dp        [p.index([row, column])]
                    del grd       [p.index([row, column])]
                    del doorValues[p.index([row, column])]
                    del p         [p.index([row, column])]

                while 1 in doorValues:
                    del p         [doorValues.index(1)]
                    del dp        [doorValues.index(1)]
                    del grd       [doorValues.index(1)]
                    del doorValues[doorValues.index(1)]
                
                for i in range(len(p)):
                        if output[p[i][0]][p[i][1]]['roomType'] != 4:
                            output[row][column]['doors'][dp[i][0]]      = 1
                            output[p[i][0]][p[i][1]]['doors'][dp[i][1]] = 1

                            output[row][column]['room'][grd[i][0][0]][grd[i][0][1]]      = obj('-bb', 'door')
                            output[p[i][0]][p[i][1]]['room'][grd[i][1][0]][grd[i][1][1]] = obj('-bb', 'door')

                            if dp[i][0] in ['U', 'D']:
                                # mainRoom
                                output[row][column]['room'][grd[i][0][0]][grd[i][0][1]-1] = obj('-bb', 'door')
                                output[row][column]['room'][grd[i][0][0]][grd[i][0][1]+1] = obj('-bb', 'door')

                                # subRoom
                                output[p[i][0]][p[i][1]]['room'][grd[i][1][0]][grd[i][1][1]-1] = obj('-bb', 'door')
                                output[p[i][0]][p[i][1]]['room'][grd[i][1][0]][grd[i][1][1]+1] = obj('-bb', 'door')
                            elif dp[i][0] in ['L', 'R']:
                                # mainRoom
                                output[row][column]['room'][grd[i][0][0]-1][grd[i][0][1]] = obj('-bb', 'door')
                                output[row][column]['room'][grd[i][0][0]+1][grd[i][0][1]] = obj('-bb', 'door')

                                # subRoom
                                output[p[i][0]][p[i][1]]['room'][grd[i][1][0]-1][grd[i][1][1]] = obj('-bb', 'door')
                                output[p[i][0]][p[i][1]]['room'][grd[i][1][0]+1][grd[i][1][1]] = obj('-bb', 'door')

    return output

def deleteBlankData(grid:list):
    """
    맵의 데이터 중 쓸데없이 메모리만 차지하는 공백 데이터를 제거하는 함수
    
        `grid`(list(raw)) : `initBranch`함수로 생긴 맵 데이터가 포함됨, 무조건 기입해야 함
    """
    if not grid: return grid
    # 비어있는 잉여 데이터 정리
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            grid[row][column] = {} if grid[row][column]['roomType']==None else grid[row][column]

    return grid