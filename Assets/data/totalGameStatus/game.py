# region Stage
stage:int = 0

# region Dungeon
Dungeon   :list = []
DungeonMap:list[list[tuple]] = []
roomData:dict = {
    "type" : "None",
    "cell" : 0,

    "maxWidth"  : 0,
    "maxHeight" : 0,

    "maxCharWidth" : 0
}

# region Modes
bodyPreservationMode:int = 0b0
cowardMode          :int = 0b0
sanjibaMode         :int = 0b0

# region Entity
enemyCount      :int = 0
entityCount     :int = 0
totalEntityCount:int = 0

entityHashPool:list[str]            = []
hitPos        :dict[str,list[list]] = {
    "pos" : [],
    "data": []
}
friendlyEntity      :list[str] = []
entityDataMaintained:dict      = { "addAnimal"  : {} }