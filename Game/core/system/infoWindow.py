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
    
    infoWindow['time'] = infoWindow['setTime'] = time

def remove() -> None:
      infoWindow['text']\
    = infoWindow['time']\
    = infoWindow['setTime']\
    = 0

def _getBlockInfo(fileName:str, target:str, Type:str):
    """
    `fileName` : 블록의 타입\n
    `target`   : 가져올 요소의 키\n
    `Type`     : 가져올 요소의 타입. 아래와 같은 종류가 있음:
        ```
            number  : int 대응
            string  : str 대응
            boolean : bool 대응
        ```\n
    예시:
    ```
    infoWindow.getBloclInfoData(
        fileName="block",
        target  ="floor.explanation.observe",
        Type    ="string"
    )
    ```
    """
    return elm(
        f"Assets/data/info/{fileName}.json",
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

def dataExtraction(blockId:str, blockType:str, **blockData) -> dict|None:
    try:
        output              = {}
        output["icon"]      = blockData['block']
        output["blockName"] = _getBlockInfo(blockType, f"{blockId}.name", "string")
        output["status"]    = _getBlockInfo(blockType, f"{blockId}.status", "string") if blockType=="weapon" else ""
        
        try:
            if blockData['nbt']['link'] and _getBlockInfo(blockType, f"{blockId}.dataType", "number")==2:
                output["explanation"] = _getBlockInfo(blockType, f"{blockId}.explanation.link", "string")
            else:
                output["explanation"] = _getBlockInfo(blockType, f"{blockId}.explanation.observe", "string")

        except:
            output["explanation"] = _getBlockInfo(blockType, f"{blockId}.explanation.observe", "string")

        output['explanation'] = output['explanation']+(f"\n\n타입 : {cc['fg']['L']}{blockType}{cc['end']}\n블록 데이터 :\n{_dicttoStr(blockData, depth=1)}"if s.debug else "") # type: ignore

        if  False in list(output.values()): return None
        else                              : return output

    except Exception as e:
        if s.debug:
            addLog(f"데이터 수집 도중 에러가 발생했습니다 : {cc['fg']['R']}{e}{cc['end']}", colorKey='R')

        return None