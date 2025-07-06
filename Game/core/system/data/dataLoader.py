import ijson
from   copy        import deepcopy
from   collections import deque

from Assets.data import totalGameStatus as s

from Game.utils.dataStructures.conveyor import (
    Conveyor
)


objCache = Conveyor(100)
elmCache = Conveyor(100)

makePath = lambda *path: s.TFP + s.s.join(path)

def _setValue(dd, value, path):
    for i in path[:-1]: dd = dd[i]
    dd[path[-1]] = value

def _addValue(dd, value, path):
    for i in path[:-1]: dd = dd[i]
    dd[path[-1]].append(value)

def obj(path:str, target:str, **addData) -> dict:
    """
    path   : json 파일의 위치
    target : 가져올 요소의 키
    """
    global objCache

    match path:
        case "-bb" : path = s.path['data']['block']
        case "-be" : path = s.path['data']['entity']
        case "-se" : path = s.path['data']['statusEffect']

    if (path,target) in objCache:
        data = deepcopy(objCache[(path,target)])

        for key, value in addData.items():
            data[key] = value

        return data

    data     = {}
    tempPath = []
    sLock    = True

    arrayDepth = deque()

    with open(path, 'r') as f:
        for prefix, event, value in ijson.parse(f):
            if event=="map_key"and sLock and value==target:
                sLock = False

            if not sLock:
                match event:
                    case "map_key": tempPath.append(value)

                    case "start_map":
                        if arrayDepth and arrayDepth[-1]:
                            _addValue(data, {}, tempPath)
                            arrayDepth.append(0)
                            tempPath  .append(-1)
                        else:
                            _setValue(data, {}, tempPath)

                    case "start_array":
                        if arrayDepth and arrayDepth[-1]:
                            _addValue(data, [], tempPath)
                            tempPath.append(-1)

                        else: _setValue(data, [], tempPath)

                        arrayDepth.append(1)

                    case "string"|"number"|"boolean":
                        if tempPath and value!=None:
                            if prefix.endswith(".item"):
                                _addValue(data, value, tempPath)

                            else:
                                _setValue(data, value, tempPath)
                                tempPath.pop()
                            
                    case "end_map"|"end_array":
                        tempPath.pop()
                        
                        if arrayDepth:       arrayDepth.pop()
                        if prefix == target: break

    objCache[(path,target)] = data[target]

    for key, value in addData.items():
        data[target][key] = value

    return data[target]

def elm(path:str, target:str, Type:str):
    """
    json 데이터에서 단순 value값만 꺼내오는 함수

    `path`     : 불러올 데이터의 위치\n
    `target`   : 가져올 요소의 키\n
    `Type`     : 가져올 요소의 타입. 아래와 같은 종류가 있음:
    ```py
        number  : int 대응
        string  : str 대응
        boolean : bool 대응
    """
    global elmCache

    if (path,target,Type) in elmCache:
        return elmCache[(path,target,Type)]
    
    with open(path, 'r') as f:
        for prefix, event, value in ijson.parse(f):
            if (prefix, event) == (target, Type):
                elmCache[(path,target,Type)] = value
                
                return value
            
        return False