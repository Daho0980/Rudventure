from ..data.dataLoader           import elm
from .logger                     import addLog
from Assets.data                 import totalGameStatus as s
from Assets.data.color           import cColors         as cc
from Assets.data.totalGameStatus import infoWindow
from Game.utils.system           import sieve

from functions.grammar import (
    pstpos as pp
)


class BlockInfoFlag:
    NONE   = 0b00
    NORMAL = 0b01
    LINK   = 0b10

class ItemInfoFlag:
    NONE    = 0b000
    NORMAL  = 0b001
    LINK    = 0b010
    SURFACE = 0b100

def add(icon       :str       ,
        name       :str       ,
        status     :str =""   ,
        explanation:str =""   ,
        subStatus  :str =""   ,
        titleOnly  :bool=False,
        time       :int =30   ,) -> None:
    infoWindow['text'] = f"[ {icon} ] {name}"\
        if titleOnly\
    else f"""[ {icon} ] {name}

{
    f"{status}\n\n" if status else ""
}{explanation}{
    f"\n\n{subStatus}" if subStatus else ""
}"""
    
    infoWindow['time'] = infoWindow['setTime'] = time

def remove() -> None:
      infoWindow['text']\
    = infoWindow['time']\
    = infoWindow['setTime']\
    = 0

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

# region Block

def _getBlockInfo(fileName:str, target:str, Type:str):
    return elm(
        f"Assets/data/info/{fileName}.json",
        target, Type
    )

def blockDataExtraction(blockId:str, blockType:str, **blockData) -> dict|None:
    try:
        infoType = _getBlockInfo(blockType, f"{blockId}.dataType", "number")
        output   = {
            "icon"        : blockData['block'],
            "name"        : _getBlockInfo(blockType, f"{blockId}.name", "string"),
            "status"      : "",
            "explanation" : [],
            "subStatus"   : ""
        }

        if infoType&BlockInfoFlag.NORMAL:
            if  blockData.get('nbt')        \
            and blockData['nbt'].get('link')\
            and infoType&BlockInfoFlag.LINK:
                output['explanation'].append(
                    _getBlockInfo(blockType, f"{blockId}.explanation.link", "string")
                )

            else:
                output['explanation'].append(
                    _getBlockInfo(blockType, f"{blockId}.explanation.observe", "string")
                )

        else: output['explanation'].append("정체를 알 수 없다.")

        if blockData.get('blockData'):
            blockName = _getBlockInfo(
                blockData['blockData']['type'],
                f"{blockData['blockData']['id']}.name",
                "string"
            )
            output['explanation'].append(
                f"\n\n아래에는 {cc['fg']['Y']}'{blockName}'{cc['end']}{pp(blockName, 'sub', True)} 있다." # type: ignore
            )

        if s.debug:
            output['explanation'].append(
                f"\n\n타입 : {cc['fg']['L']}{blockType}{cc['end']}\n블록 데이터 :\n{_dicttoStr(blockData, depth=1)}"
            )

        output['explanation'] = ''.join(output['explanation'])

        if  False in list(output.values()): return None
        else                              : return output

    except Exception as e:
        if s.debug:
            addLog(f"데이터 수집 도중 에러가 발생했습니다 : {cc['fg']['R']}{e}{cc['end']}", colorKey='R')

        return None

# region Item

def _getItemInfo(fileName:str, target:str, Type:str):
    return elm(
        f"Assets/data/info/item/{fileName}.json",
        target, Type
    )

def itemDataExtraction(itemId:str, itemType:str, onInventory:bool=False, **itemData) -> dict|None:
    try:
        infoType = _getItemInfo(itemType, f"{itemId}.dataType", "number")
        output   = {
            "icon"        : itemData['icon'],
            "name"        : _getItemInfo(itemType, f"{itemId}.name", 'string'),
            "status"      : "",
            "explanation" : [],
            "subStatus"   : []
        }

        if onInventory:
            output['status'] = f"{cc['fg']['L']}{itemData['status']['atk']} 공격력{cc['end']}"

        durability = itemData['status']['durability']
        infection  = itemData['status']['infection']

        output['subStatus'].append(
            f"{cc['fg']['Y']}{
            s.statRatioComments['infinite']['durability']
                if durability[0] == '∞'
            else sieve(
                s.statRatioComments['durability'],
                int((durability[0]/durability[1])*100)
            )}{cc['end']}"
        )

        output['subStatus'].append(f"{cc['fg']['F']}{
            s.statRatioComments['infinite']['infection']
                if infection[0] == '∞'
            else sieve(
                s.statRatioComments['infection'],
                int((infection[0]/infection[1])*100),
            )}{cc['end']}"
        )

        del infection, durability

        output['subStatus'] = '\n'.join(output['subStatus'])

        if onInventory and infoType&ItemInfoFlag.NORMAL:
            if  itemData.get('nbt')        \
            and itemData['nbt'].get('link')\
            and infoType&ItemInfoFlag.LINK:
                output['explanation'].append(
                    _getItemInfo(itemType, f"{itemId}.explanation.link", "string")
                )

            else:
                output['explanation'].append(
                    _getItemInfo(itemType, f"{itemId}.explanation.observe", "string")
                )
        
        elif infoType & ItemInfoFlag.SURFACE:
            output['explanation'].append(
                _getItemInfo(itemType, f"{itemId}.explanation.surface", "string")
            )
        
        else: output['explanation'].append("그냥 봐서는 알 수 없다.")

        output['explanation'].append(
            f"\n\n타입 : {cc['fg']['L']}{itemType}{cc['end']}\n아이템 데이터 :\n{_dicttoStr(itemData, depth=1)}"
                if s.debug
            else ""
        )

        output['explanation'] = ''.join(output['explanation'])

        if  False in list(output.values()): return None
        else                              : return output

    except Exception as e:
        if s.debug:
            addLog(f"데이터 수집 도중 에러가 발생했습니다 : {cc['fg']['R']}{e}{cc['end']}", colorKey='R')

        return None