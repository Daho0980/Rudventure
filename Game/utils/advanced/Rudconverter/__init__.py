import os
import json
from   zlib import compress, decompress
from   base64 import b64encode, b64decode

from Assets.data import status as s

def _encode(strings: list[str]) -> list[str]:
    encoded_data = []
    for string in strings:
        # Base64로 인코딩하여 저장
        encoded_data.append(b64encode(compress(string.encode('utf-8'))).decode('utf-8'))
    return encoded_data
    
def _decode(encoded_strings: list[str]) -> list[str]:
    decoded_data = []
    for encoded_string in encoded_strings:
        # Base64 디코딩
        decoded_base64 = b64decode(encoded_string.encode('utf-8'))
        # 압축 해제 및 UTF-8 디코딩
        decompressed_data = decompress(decoded_base64).decode('utf-8')
        decoded_data.append(decompressed_data)
    return decoded_data
    
def _changeExtention(name:str, beforeExt:str=".rud", afterExt:str=".json"):
    """
    정변환(기본값) : 
            beforeExt = ".rud"
            afterExt  = ".json"
    역변환 :
            beforeExt = ".json"
            afterExt  = ".rud"
    """
    try:
        os.rename(f"{name}{beforeExt}", f"{name}{afterExt}")
    except: return False

def save() -> int:
    Vars        = [name for name in dir(s) if not name.startswith('__')]
    uselessVars = [
        'cMarkdown',
        '_cc', 'cColors',
        'Dy', 'bfDy',
        'Dx', 'bfDx',
        'x', 'bfx',
        'y', 'bfy',
        'hpLow', 'dfCrack',
        'steppedBlock',
        'main',
        'LOGO',
        'ids', 'orbIds',
        'stepableBlocks', 'interactableBlocks',
        'enemyIds',
        's', 'TFP', 'pythonVersion',
        'Dungeon',
        'roomLock', 'killAll',
        'DROD',
        'pauseText',
        'entityCount', 'totalEntityCount', 'hitPos',
        'option',
        'maxStack', 'onDisplay', 'onTime',
        'debugScreen',
        'frame', 'frameRate',
        'showDungeonMap', 'statusDesign',
        'lightName'
        ]
    try:
        file_path = f'{s.TFP}saveData{s.s}{s.name}.json'
        saveJson  = open(file_path, 'w')

        for i in uselessVars:
            if i in Vars: Vars.remove(i)

        data         = {}
        statusData   = {}
        for i in Vars:
            # print(i+str(type(eval(f"s.{i}"))))
            statusData[i] = eval(f"s.{i}")
        data["status"] = statusData

        json.dump(data, saveJson, ensure_ascii=False)
        saveJson.close()

        # 파일 암호화 단계
        jsonForRead  = open(file_path, 'r')
        encoded      = _encode(jsonForRead.readlines())
        with open(file_path, 'w') as encodeFile:
            for line in encoded: encodeFile.write(f"{line}\n")
        _changeExtention(f"{s.TFP}saveData{s.s}{s.name}", beforeExt=".json", afterExt=".rud")
    except: return 0
    else:   return 1

def load(name:str):
    try:
        with open(f"saveData{s.s}{name}.json", 'w+') as data:
            with open(f"saveData{s.s}{name}.rud", 'r') as wcd:
                for line in _decode(wcd.readlines()): data.write(line)
            
        with open(f"saveData{s.s}{name}.json", 'r') as d:
            dictData = json.load(d)
        os.remove(f"saveData{s.s}{name}.json")
    except: return False
    else:   return dictData


# example = encode(["레포\n", "다호\n", "업로드\n"])
# print(f"input : \n\n{example}")
# print(f"output : \n\n{decode(example)}")