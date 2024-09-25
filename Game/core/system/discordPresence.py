from   pypresence import Presence

from Assets.data import status as s
from Game.core.system.dataLoader import elm


isConnected:bool = True
clientID         = elm(
    f"{s.TFP}config{s.s}data.json",
    "clientID",
    "number"
)

try:
    RPC = Presence(clientID)
    RPC.connect()
except: isConnected = False

def update(**variables) -> None:
    if isConnected:
        RPC.update(**variables)