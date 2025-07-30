from itertools import chain

from Game.core.system.data.dataLoader import obj


dataPath = __import__("Assets.data.totalGameStatus", fromlist=["path"]).path['data']['block']

wall  = obj(dataPath, 'wall')
wallL = obj(dataPath, 'wall', block="▓░")
wallR = obj(dataPath, 'wall', block="░▓")
floor = obj(dataPath, 'floor')
void  = obj(dataPath, 'void')

Room:list[list[dict[str,str|int|dict]]] = [
    [wall]*13, 
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    [wall]*13
]

HorizonallyLongRoom:list[list[dict[str,str|int|dict]]] = [
    [wall]*27,
    list(chain([wall],[floor]*25,[wall])),
    list(chain([wall],[floor]*25,[wall])),
    list(chain([wall],[floor]*25,[wall])),
    list(chain([wall],[floor]*25,[wall])),
    list(chain([wall],[floor]*25,[wall])),
    list(chain([wall],[floor]*25,[wall])),
    list(chain([wall],[floor]*25,[wall])),
    list(chain([wall],[floor]*25,[wall])),
    list(chain([wall],[floor]*25,[wall])),
    list(chain([wall],[floor]*25,[wall])),
    list(chain([wall],[floor]*25,[wall])),
    [wall]*27
]

VerticallyLongRoom:list[list[dict[str,str|int|dict]]] = [
    [wall]*13,
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    list(chain([wall],[floor]*11,[wall])),
    [wall]*13
]

Diamond:list[list[dict[str,str|int|dict]]] = [
    list(chain([void]*5,[wall]*5,[void]*5)),
    list(chain([void]*4,[wall],[floor]*5,[wall],[void]*4)),
    list(chain([void]*3,[wall],[floor]*7,[wall],[void]*3)),
    list(chain([void]*2,[wall],[floor]*9,[wall],[void]*2)),
    list(chain([void],[wall],[floor]*11,[wall],[void])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([void],[wall],[floor]*11,[wall],[void])),
    list(chain([void]*2,[wall],[floor]*9,[wall],[void]*2)),
    list(chain([void]*3,[wall],[floor]*7,[wall],[void]*3)),
    list(chain([void]*4,[wall],[floor]*5,[wall],[void]*4)),
    list(chain([void]*5,[wall]*5,[void]*5)),
]

TreasureRoom:list[list[dict[str,str|int|dict]]] = [
    [wall]*9,
    list(chain([wall],[floor]*7,[wall])),
    list(chain([wall],[floor]*7,[wall])),
    list(chain([wall],[floor]*7,[wall])),
    list(chain([wall],[floor]*7,[wall])),
    list(chain([wall],[floor]*7,[wall])),
    list(chain([wall],[floor]*7,[wall])),
    list(chain([wall],[floor]*7,[wall])),
    [wall]*9
]

Chapel:list[list[dict[str,str|int|dict]]] = [
    list(chain([void]*3,[wall]*9,[void]*3)),
    list(chain([void]*3,[wall],[floor]*7,[wall],[void]*3)),
    list(chain([void]*3,[wall],[floor]*7,[wall],[void]*3)),
    list(chain([wall]*4,[floor]*7,[wall]*4)),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall],[floor]*13,[wall])),
    list(chain([wall]*4,[floor]*7,[wall]*4)),
    list(chain([void]*3,[wall],[floor]*7,[wall],[void]*3)),
    list(chain([void]*3,[wall],[floor]*7,[wall],[void]*3)),
    list(chain([void]*3,[wall]*9,[void]*3))
]

EndPoint:list[list[dict[str,str|int|dict]]] = [
    list(chain([void]*9,[wall]*5,[void]*9)),
    list(chain([void]*8,[wall]*2,[floor]*3,[wall]*2,[void]*8)),
    list(chain([void]*8,[wall],[floor]*5,[wall],[void]*8)),
    list(chain([void]*8,[wall],[floor]*5,[wall],[void]*8)),
    list(chain([void]*4,[wall]*4,[floor]*7,[wall]*4,[void]*4)),
    list(chain([void]*4,[wall],[floor]*13,[wall],[void]*4)),
    list(chain([void]*4,[wall],[floor],[wallL],[floor]*9,[wallR],[floor],[wall],[void]*4)),
    list(chain([void]*4,[wall],[floor]*13,[wall],[void]*4)),
    list(chain([void],[wall]*3,[floor]*15,[wall]*3,[void])),
    list(chain([wall]*2,[floor]*19,[wall]*2)),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall]*2,[floor]*19,[wall]*2)),
    list(chain([void],[wall]*3,[floor]*15,[wall]*3,[void])),
    list(chain([void]*4,[wall],[floor]*13,[wall],[void]*4)),
    list(chain([void]*4,[wall],[floor],[wallL],[floor]*9,[wallR],[floor],[wall],[void]*4)),
    list(chain([void]*4,[wall],[floor]*13,[wall],[void]*4)),
    list(chain([void]*4,[wall]*4,[floor]*7,[wall]*4,[void]*4)),
    list(chain([void]*8,[wall],[floor]*5,[wall],[void]*8)),
    list(chain([void]*8,[wall],[floor]*5,[wall],[void]*8)),
    list(chain([void]*8,[wall]*2,[floor]*3,[wall]*2,[void]*8)),
    list(chain([void]*9,[wall]*5,[void]*9)),
]

del dataPath, floor, void, wall, wallL, wallR