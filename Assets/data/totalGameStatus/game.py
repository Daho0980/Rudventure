# region Stage
stage:int = 0

# region Dungeon
Dungeon :list = []
roomData:dict = {
    "type"      : "None",
    "cell"      : 0,

    "maxWidth"  : 0,
    "maxHeight" : 0,

    "maxCharWidth" : 0
}

roomLock   :bool = False
killAll    :bool = False
clearEntity:bool = False

# region Modes
bodyPreservationMode:bool = False
ezMode              :bool = False
sanjibaMode         :bool = False

# region Entity
enemyCount      :int = 0
entityCount     :int = 0
totalEntityCount:int = 0

entityHashPool  :list[str]            = []
hitPos          :dict[str,list[list]] = {
    "pos" : [],
    "data": []
}
friendlyEntity      :list[str] = []
entityDataMaintained:dict      = { "addAnimal"  : {} }
entitySaveTrigger   :bool      = False

isLoadfromBody:bool = False