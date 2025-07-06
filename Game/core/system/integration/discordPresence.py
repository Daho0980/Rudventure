import time
from   pypresence import Presence

from ..data.dataLoader import elm
from Assets.data       import totalGameStatus as s


currentStatus:dict[str,dict] = {
    "essential" : {
        "large_image" : "",
        "details"     : "",
        "state"       : ""
    },
    "optional" : {
        "time"        : True,
        "small_image" : ""
    }
}

isConnected:bool = True
clientID   :int  = elm(
    f"{s.TFP}config{s.s}data.json",
    "clientID",
    "number"
)

try:
    RPC = Presence(clientID)
    RPC.connect()
except: isConnected = False

def load(large_image:str, details:str, state:str, start:bool=False, small_image:str="") -> None:
    currentStatus['essential']['large_image'] = large_image
    currentStatus['essential']['details']     = details
    currentStatus['essential']['state']       = state

    currentStatus['optional']['time']        = start
    currentStatus['optional']['small_image'] = small_image.lower()

def quickLoad(Type:str) -> None:
    match Type:
        case "inMenu":
            load(
                large_image="rudventure-in_settings1",
                details    ="메인 메뉴",
                state      ="탐색 중",
                start      =True
            )

        case "enter":
            load(
                large_image="rudventure-icon1",
                small_image=s.playerColor[1],
                details    ="메인 메뉴",
                state      ="나락 입장 중"
            )

        case "inDungeon":
            load(
                large_image="rudventure-in_battle1",
                small_image=s.playerColor[1],
                details    ="나락",
                state      =f"제 -{s.stage+1}층",
                start      =True
            ) 

        case "goDeeper":
            load(
                large_image="rudventure-icon1",
                small_image=s.playerColor[1],
                details    =f"나락",
                state      ="더 깊은 곳으로 이동 중...",
            )

def update() -> bool:
    if isConnected:
        status = currentStatus['essential']
        
        if currentStatus['optional']['time']:
            status['start'] = int(time.time())

        if currentStatus['optional']['small_image'] != "":
            status['small_image'] = currentStatus['optional']['small_image']
            
        RPC.update(**status)
        return True
        
    else: return False