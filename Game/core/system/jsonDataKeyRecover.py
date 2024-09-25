from ast import literal_eval as eval


def serializeDict(data):
    result = {}
    for k, v in data.items():
        if   isinstance(k, (int, float)): result[f"i/{k}"] = v
        elif isinstance(v, dict):         result[str(k)]   = serializeDict(v)
        else:                             result[str(k)]   = v
    return result

def deserializeDict(data):
    result = {}
    for k, v in data.items():
        if k.startswith("i/"):
            k               = k[2:]
            result[eval(k)] = v
        else: result[k] = v

        if isinstance(v, dict): result[k] = deserializeDict(v)
    return result

if __name__ == '__main__':
    data      = {0: "zero", 1: "one", 2.5: "two point five", (1, 2, 3): "tuple man", "str_key": "string value"}
    json_data = serializeDict(data)
    print(json_data)

    data_back = deserializeDict(json_data)
    print(data_back)