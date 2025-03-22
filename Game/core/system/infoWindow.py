from .dataLoader                 import elm
from Assets.data                 import totalGameStatus as s
from Assets.data.color           import cColors         as cc
from Assets.data.totalGameStatus import infoWindow
from .logger                     import addLog


def add(icon       :str       ,
        blockName  :str       ,
        status     :str =""   ,
        explanation:str =""   ,
        titleOnly  :bool=False,
        time       :int =30   ,) -> None:
    infoWindow['text'] = f"[ {icon} ] {blockName}"\
        if titleOnly\
    else f"""[ {icon} ] {blockName}

{f"{status}\n\n"if status else ''}{explanation}"""
    
    infoWindow['time'], infoWindow['setTime'] = time, time

def remove() -> None:
    infoWindow['text']                        = 0
    infoWindow['time'], infoWindow['setTime'] = 0, 0

def _getBlockInfo(fileName:str, target:str, Type:str):
    """
    `fileName` : 블록의 타입\n
    `target`   : 가져올 요소의 키\n
    `Type`     : 가져올 요소의 타입. 아래와 같은 종류가 있음:
    ```py
        number  : int 대응
        string  : str 대응
        boolean : bool 대응
    ```\n
    예시:
        ```py
        infoWindow.getBloclInfoData(
            fileName="block",
            target="0.explanation.observe",
            Type="string"
        )
        ```
    """
    return elm(
        f"Assets/data/block/blockInfo/{fileName}.json",
        target, Type
    )

def _dicttoStr(data   :dict     ,
               depth  :int =0   ,
               indent :int =2   ,
               lineLim:int =50  ,
               raw    :bool=False) -> str|list:
    output = []

    for key, value in data.items():
        trigger = isinstance(value, dict)
        overCut = "..." if ((depth*indent)+len(str(value))+len(str(key))+3)>lineLim and not trigger else ''

        output.append(f"{(' '*indent)*depth}{key} : {cc['fg']['Y']if key!='block'else''}{"" if trigger else value}{overCut}{cc['end']}")

        if trigger:
            output.extend(_dicttoStr(value, depth=depth+1, lineLim=lineLim, raw=True))

    return output if raw else '\n'.join(output)

def dataRegistration(blockId:str, blockType:str, **blockData) -> dict:
    try:
        output              = {}
        output["icon"]      = blockData['block']
        output["blockName"] = _getBlockInfo(blockType, f"{blockId}.name", "string")
        output["status"]    = _getBlockInfo(blockType, f"{blockId}.status", "string") if blockType == "weapon" else ""
        
        try:
            if blockData['nbt']['link'] and _getBlockInfo(blockType, f"{blockId}.dataType", "number")==2:
                output["explanation"] = _getBlockInfo(blockType, f"{blockId}.explanation.link", "string")
            else:
                output["explanation"] = _getBlockInfo(blockType, f"{blockId}.explanation.observe", "string")
        except: output["explanation"] = _getBlockInfo(blockType, f"{blockId}.explanation.observe", "string")

        output['explanation'] = output['explanation']+(f"\n\n블록 데이터 :\n{_dicttoStr(blockData, depth=1)}"if s.debug else "") # type: ignore

        if False in list(output.values()): return False # type: ignore
        else:                              return output

    except Exception as e:
        if s.debug:
            addLog(f"데이터 수집 도중 에러가 발생했습니다 : {cc['fg']['R']}{e}{cc['end']}", colorKey='R')

        return False # type: ignore