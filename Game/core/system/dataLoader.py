import ijson
from   collections import deque


def _setValue(dd, value, path):
    for i in path[:-1]: dd = dd[i]
    dd[path[-1]] = value

def _addValue(dd, value, path):
    for i in path[:-1]: dd = dd[i]
    dd[path[-1]].append(value)

def obj(path:str, target:str) -> dict:
    data     = {}
    tempPath = []
    sLock    = True

    arrayDepth = deque()

    with open(path, 'r') as f:
        for prefix, event, value in ijson.parse(f):
            if event == "map_key" and sLock and value==target:
                sLock = False

            if not sLock:
                match event:
                    case "map_key": tempPath.append(value)

                    case "start_map":
                        if arrayDepth and arrayDepth[-1]:
                            _addValue(data, {}, tempPath)
                            arrayDepth.append(0)
                            tempPath.append(-1)
                        else:
                            _setValue(data, {}, tempPath)

                    case "start_array":
                        if arrayDepth and arrayDepth[-1]:
                            _addValue(data, [], tempPath)
                            tempPath.append(-1)
                        else:
                            _setValue(data, [], tempPath)
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
                        if arrayDepth: arrayDepth.pop()
                        if prefix == target: break

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
    with open(path, 'r') as f:
        for prefix, event, value in ijson.parse(f):
            if (prefix, event) == (target, Type):
                return value
        return False