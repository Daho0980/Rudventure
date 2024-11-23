# region OS
s:str         = ''
TFP:str       = ""
pythonVersion = __import__("sys").version_info

# region Game init
version:str|int = "???"
main:int        = 1
gameRecord:bool = True

# region Logger
maxStack:int        = 10
onDisplay:list[str] = []
onTime:list[int]    = []
port:int            = -1

# region Sound
volume:int = 50

# region Terminal
# 'S'creen'S'ize'S' LMAO
sss:dict[str, tuple] = {
    "minimum"     : (58, 122),
    "recommended" : (67, 195)
}
autoTerminalSize:bool|None  = None
checkTerminalSize:bool|None = None

# region Key
key            = __import__("Game.core.system.keyBind", fromlist=["KeyBind"]).KeyBind()
recordKey:bool = False

# region Time record
startTime:float   = 0
elapsedTime:float = 0

# region Dead reason
DROD:list = [None, '']