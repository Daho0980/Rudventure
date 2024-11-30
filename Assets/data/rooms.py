from itertools import chain

from Game.core.system.dataLoader import obj


dataPath = __import__("Assets.data.totalGameStatus", fromlist=["path"]).path['blockData']['block']
wall     = obj(dataPath, '1')
floor    = obj(dataPath, '0')
void     = obj(dataPath, '25')

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

horizonallyLongRoom:list[list[dict[str,str|int|dict]]] = [
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

verticallyLongRoom:list[list[dict[str,str|int|dict]]] = [
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

bigRoom:list[list[dict[str,str|int|dict]]] = [
    [wall]*23,
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    list(chain([wall],[floor]*21,[wall])),
    [wall]*23
]

treasureRoom:list[list[dict[str,str|int|dict]]] = [
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

chapel:list[list[dict[str,str|int|dict]]] = [
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
# █ ▀

del dataPath, floor, void, wall