# region Frame
frameRate :int       = -1
currFrame :float     = 0
frame     :int|float = 0

elapsedFrameCount:int = 0
currentFrameCount:int = 0

# region UISettings
statusDesign  :int  = 0b1 # 1||0
showDungeonMap:int  = 0b0 # 0||1
debug         :int  = 0b0
infoWindow    :dict = {
    "text"    : "",
    "time"    : 0,
    "setTime" : 1
}

# region Noise
currentCurseNoiseFrequency:int = 0
curseNoiseFrequency       :int = 5

# region Camera set
dynamicCameraMoving:int = 0b0 # 0||1

noisePool:dict[str,list[str]] = {
    "pattern" : [
        "█░▒\n░█", "░  ▒\n▓▓▒\n▒░", "█▓▒▓▓\n\n░▒", "███\n█\n░███░█",
        "░\n\n░█░▒", "▒\n▒▒▓▒░▒▒\n     ▒▒", "▓▓▓\n▓█▓\n▓▓", "█▒█\n\n▒▓▒█\n░",
        "█▒░▓▓█░", "██▒▒\n▓▒▒\n▒", "▓▓\n▓░░▓▓▒▓█", "           █\n▓▓██\n    ░█▒█ █",
        "    ░\n\n░▒▒░", "▒▒\n▒█░\n   ▒ ▒", "▓▓ ▓\n\n▓█▓\n▓▓░▓█ ▓█", "   ██\n  ▒▒█ █\n░░",
    ],

    "character" : [ "░", "▒", "▓", "█" ]
}