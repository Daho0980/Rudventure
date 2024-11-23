# region Frame
frameRate:int    = -1
frame:int|float  = 0
renderTime:float = 0

elapsedFrame:int = 0
currentFrame:int = 0

# region UISettings
statusDesign:int   = 1 # 1||0
showDungeonMap:int = 0 # 0||1
debugConsole:bool  = False
infoWindow:dict    = {
    "text"    : "",
    "time"    : 0,
    "setTime" : 1
}

# region Noise
currentCurseNoiseFrequency:int = 0
curseNoiseFrequency:int        = 5

# region Camera set
dynamicCameraMoving:int = 0 # 0||1