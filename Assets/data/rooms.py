from itertools import chain

Room:list[list[dict[str,str|int|dict]]] = [
    [{"block":'■', "id":1, "type" : 0}]*13, 
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    [{"block":'■', "id":1, "type" : 0}]*13
]

horizonallyLongRoom:list[list[dict[str,str|int|dict]]] = [
    [{"block":'■', "id":1, "type" : 0}]*27,
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*25,[{"block":'■', "id":1, "type" : 0}])),
    [{"block":'■', "id":1, "type" : 0}]*27
]

verticallyLongRoom:list[list[dict[str,str|int|dict]]] = [
    [{"block":'■', "id":1, "type" : 0}]*13,
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*11,[{"block":'■', "id":1, "type" : 0}])),
    [{"block":'■', "id":1, "type" : 0}]*13
]

bigRoom:list[list[dict[str,str|int|dict]]] = [
    [{"block":'■', "id":1, "type" : 0}]*23,
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*21,[{"block":'■', "id":1, "type" : 0}])),
    [{"block":'■', "id":1, "type" : 0}]*23
]

treasureRoom:list[list[dict[str,str|int|dict]]] = [
    [{"block":'■', "id":1, "type" : 0}]*9,
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}])),
    [{"block":'■', "id":1, "type" : 0}]*9
]

chapel:list[list[dict[str,str|int|dict]]] = [
    list(chain([{"block":' ', "id":25, "type" : 0}]*3,[{"block":'■', "id":1, "type" : 0}]*9,[{"block":' ', "id":25, "type" : 0}]*3)),
    list(chain([{"block":' ', "id":25, "type" : 0}]*3,[{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":25, "type" : 0}]*3)),
    list(chain([{"block":' ', "id":25, "type" : 0}]*3,[{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":25, "type" : 0}]*3)),
    list(chain([{"block":'■', "id":1, "type" : 0}]*4,[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}]*4)),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*13,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*13,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*13,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*13,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*13,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*13,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*13,[{"block":'■', "id":1, "type" : 0}])),
    list(chain([{"block":'■', "id":1, "type" : 0}]*4,[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}]*4)),
    list(chain([{"block":' ', "id":25, "type" : 0}]*3,[{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":25, "type" : 0}]*3)),
    list(chain([{"block":' ', "id":25, "type" : 0}]*3,[{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":0, "type" : 0}]*7,[{"block":'■', "id":1, "type" : 0}],[{"block":' ', "id":25, "type" : 0}]*3)),
    list(chain([{"block":' ', "id":25, "type" : 0}]*3,[{"block":'■', "id":1, "type" : 0}]*9,[{"block":' ', "id":25, "type" : 0}]*3))
]
# █ ▀