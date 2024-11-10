import time
from   pypresence import Presence

from .dataLoader import elm
from Assets.data import status as s


currentStatus:dict[str,dict] = {
    "essential" : {
        "large_image" : "",
        "details"     : "",
        "state"       : ""
    },
    "optional" : {
        "time" : True
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

def load(large_image:str, details:str, state:str, start:bool=False) -> None:
    currentStatus['essential']['large_image'] = large_image
    currentStatus['essential']['details']     = details
    currentStatus['essential']['state']       = state

    currentStatus['optional']['time'] = start

def update() -> bool:
    if isConnected:
        status = currentStatus['essential']
        if currentStatus['optional']['time']:
            status['start'] = int(time.time())
            
        RPC.update(**status)
        return True
    else: return False