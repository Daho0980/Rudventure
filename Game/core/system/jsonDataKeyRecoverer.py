from ast import literal_eval as eval

from base64 import (
    b64encode as b64e,
    b64decode as b64d
)


_encode = lambda t: str(b64e(str(t).encode()))[2:-1]
_decode = lambda t: b64d(t[2:]).decode()

def _detector(data, d):
    output = []

    for item in data:
        if isinstance(item, (list, tuple)): item = _detector(item, d)
        elif isinstance(item, dict):
            match d:
                case "for":  item = serializeDict(item)
                case "back": item = deserializeDict(item)

        output.append(item)
    
    return output

def serializeDict(data):
    result = {}
    for k, v in data.items():
        if   isinstance(k, (int,       float)): k = f"n/{_encode(k)}"
        elif isinstance(k, (tuple, frozenset)): k = f"t/{_encode(k)}"
        else                                  : k = str(k)

        if   isinstance(v, tuple): v = _detector    (v, 'for')+["/t"]
        elif isinstance(v,  list): v = _detector    (v, 'for')
        elif isinstance(v,  dict): v = serializeDict(v)

        result[k] = v
    return result

def deserializeDict(data):
    result = {}
    for k, v in data.items():
        if k[:2] in ("n/","t/"): k = eval(_decode(k))

        if   isinstance(v, dict): v = deserializeDict(v)
        elif isinstance(v, list):
            v = _detector(v, 'back')
            if v and v[-1]=="/t": v = tuple(v[:-1])

        result[k] = v
        
    return result

if __name__ == '__main__':
    data = {0: "zero", 1: "one", 2.5: "two point five", (1, 2, 3): ("tuple", "man"), "str_key": "string value", ("very", 9006): ({"I":"lovin", (1) : "t"}, "fr")}

    print(f"Original data : {data}\n")

    json_data = serializeDict(data)
    print(json_data, end="\n\n")

    data_back = deserializeDict(json_data)
    print(data_back)