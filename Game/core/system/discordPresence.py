import time
from   pypresence import Presence

from .dataLoader import elm
from Assets.data import totalGameStatus as s


currentStatus:dict[str,dict] = {
    "essential" : {
        "large_image" : "",
        "details"     : "",
        "state"       : ""
    },
    "optional" : {
        "time" : True,
        "small_image" : ""
    }
}

isConnected:bool = True
clientID:int     = elm(
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