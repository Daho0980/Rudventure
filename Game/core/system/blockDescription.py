import ijson

from Assets.data.status import blockDescription


def add(
        icon:str,
        blockName:str,
        status:str,
        explanation:str,
        titleOnly:bool=False,
        time:int      =30
        ) -> None:
    blockDescription['text'] = f"[ {icon} ] {blockName}" if titleOnly else f"[ {icon} ] {blockName}\n\n{status}\n\n{explanation}"
    blockDescription['time'], blockDescription['setTime'] = time, time

def remove() -> None:
    blockDescription['text'] = 0
    blockDescription['time'], blockDescription['setTime'] = 0, 0

def getBlockData(fileName:str, target:str, Type:str):
    """
    `fileName` : 블록의 타입.\n
    `target`   : 가져올 요소의 키.\n
    `Type`     : 가져올 요소의 타입. 아래와 같은 종류가 있음.
    ```py
        number  : int 대응
        string  : str 대응
        boolean : bool 대응
    ```\n
    예시:
        ```py
        blockDescription.getBlockData(
            fileName="block",
            target="0.explanation.observe",
            Type="string"
        )
        ```
    """
    with open(f"Assets/data/blockData/{fileName}.json", 'r') as f:
        for prefix, event, value in ijson.parse(f):
            if (prefix, event) == (target, Type):
                return value
        return False
    
def dataLoader(blockId:str, blockType:str, blockData:dict) -> dict:
    try:
        output = {}
        output["icon"]        = blockData['block']
        output["blockName"]   = getBlockData(blockType, f"{blockId}.name", "string")
        output["status"]      = getBlockData(blockType, f"{blockId}.status", "string") if blockType == "weapon" else ""
        try:
            if blockData['nbt']['link'] and getBlockData(blockType, f"{blockId}.dataType", "number") == 2:
                output["explanation"] = getBlockData(blockType, f"{blockId}.explanation.link", "string")
            else:
                output["explanation"] = getBlockData(blockType, f"{blockId}.explanation.observe", "string")
        except: output["explanation"] = getBlockData(blockType, f"{blockId}.explanation.observe", "string")

        if False in list(output.values()): return False # type: ignore
        else:               return output
    except: return False # type: ignore