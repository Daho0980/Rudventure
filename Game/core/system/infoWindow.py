from .dataLoader        import elm
from Assets.data.status import infoWindow


def add(icon:str,
        blockName:str,
        status:str,
        explanation:str="",
        titleOnly:bool =False,
        time:int       =30,   ) -> None:
    infoWindow['text']                        = f"[ {icon} ] {blockName}" if titleOnly else f"[ {icon} ] {blockName}\n\n{status}\n\n{explanation}"
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
    return elm(f"Assets/data/blockInfo/{fileName}.json", target, Type)
    
def dataLoader(blockId:str, blockType:str, blockData:dict) -> dict:
    try:
        output = {}
        output["icon"]        = blockData['block']
        output["blockName"]   = _getBlockInfo(blockType, f"{blockId}.name", "string")
        output["status"]      = _getBlockInfo(blockType, f"{blockId}.status", "string") if blockType == "weapon" else ""
        try:
            if blockData['nbt']['link'] and _getBlockInfo(blockType, f"{blockId}.dataType", "number") == 2:
                output["explanation"] = _getBlockInfo(blockType, f"{blockId}.explanation.link", "string")
            else:
                output["explanation"] = _getBlockInfo(blockType, f"{blockId}.explanation.observe", "string")
        except: output["explanation"] = _getBlockInfo(blockType, f"{blockId}.explanation.observe", "string")

        if False in list(output.values()): return False # type: ignore
        else:               return output
    except: return False # type: ignore