# region OS
pythonVersion = __import__("sys").version_info

s  :str = ''
TFP:str = ""

# region Game init
version   :str|int = "???"
main      :int     = 1
gameRecord:bool    = True

# region Logger
maxStack :int       = 10
onDisplay:list[str] = []
onTime   :list[int] = []
port     :int       = -1

# region Sound
volume:int = 50

currSoundCount:int = 0
maxSoundCount :int = 64

# region Terminal
# NOTE(it's TMI actually btw): The origin of this name is 'S'creen'S'ize'S' LMAO
sss:dict[str, tuple[int,int]] = {
    "minimum"     : ( 58, 122 ),
    "recommended" : ( 67, 195 )
}
autoTerminalSize :bool = False
checkTerminalSize:bool = False

# region Key
key           = __import__("Game.core.system.config.keyBind", fromlist=("KeyBind",)).KeyBind()
recordKey:int = 0b0

# region Time record
startTime  :float = 0
elapsedTime:float = 0

# region Dead reason
DROD:tuple[str, str] = ("None", '')