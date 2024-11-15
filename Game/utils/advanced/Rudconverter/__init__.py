import os
import json
from   zlib   import compress, decompress
from   base64 import b64encode, b64decode

from Game.core.system        import jsonDataKeyRecover as jdkr
from Game.core.system.logger import addLog

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)


# region Local function
def _encode(strings:list[str]) -> list[str]:
    encoded_data = []
    for string in strings:
        # Base64로 인코딩하여 저장
        encoded_data.append(b64encode(compress(string.encode('utf-8'))).decode('utf-8'))
    return encoded_data
    
def _decode(encodedStrings:list[str]) -> list[str]:
    decodedData = []
    for encodedString in encodedStrings:
        # Base64 디코딩
        decodedBase64 = b64decode(encodedString.encode('utf-8'))
        # 압축 해제 및 UTF-8 디코딩
        decompressedData = decompress(decodedBase64).decode('utf-8')
        decodedData.append(decompressedData)
    return decodedData
    
def _changeExtention(name:str, beforeExt:str=".rud", afterExt:str=".json"):
    try:    os.rename(f"{name}{beforeExt}", f"{name}{afterExt}")
    except: return False

# region Global function
def save() -> int:
    commentVars  = [name for name in dir(c) if not name.startswith('__')]
    
    try:
        file_path = f'{s.TFP}saveData{s.s}{s.name}.json'
        saveJson  = open(file_path, 'w')

        Vars = [
            "name", "playerDamageIcon", "playerColor",
            "playerVoice",
            "stage", "killCount", "inventory",
            "hp", "df", "atk", "hunger", "xp", "lvl", "ashChip",
            "fairWind", "Mhp", "Mdf", "Mxp", "Mlvl", "MFairWind",
            "critRate", "critDMG", "evasionRate", "statusFormula",
            "entityDataMaintained", "gameRecord",
            "ezMode", "sanjibaMode", "bodyPreservationMode",
        ]

        data        = {}
        statusData  = {}
        commentData = {}

        for i in Vars:
            value = getattr(s, i)
            if isinstance(value, dict): value = jdkr.serializeDict(value)
            statusData[i]  = value
        for i in commentVars:
            value = getattr(c, i)
            if isinstance(value, dict): value = jdkr.serializeDict(value)
            commentData[i]  = value

        statusData["playerIcon"] = s.ids[300]
        data["status"]           = statusData
        data["comments"]         = commentData


        json.dump(data, saveJson, ensure_ascii=False)
        saveJson.close()

        # 파일 암호화 단계
        encodeData = _encode(open(file_path,'r').readlines())

        with open(file_path, 'w') as encodeFile:
            for line in encodeData: encodeFile.write(f"{line}\n")
        _changeExtention(f"{s.TFP}saveData{s.s}{s.name}", beforeExt=".json", afterExt=".rud")
    except Exception as e:
        addLog(f"세이브 저장에 실패했습니다 : {e}")
        return 0
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
    else:   return jdkr.deserializeDict(dictData)

# example = encode(["레포\n", "다호\n", "업로드\n"])
# print(f"input : \n\n{example}")
# print(f"output : \n\n{decode(example)}")