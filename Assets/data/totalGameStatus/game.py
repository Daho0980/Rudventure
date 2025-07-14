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
enemyCount  :int = 0
vEntityCount:int = 0

currEntityCount:int = 0
maxEntityCount :int = 16

entityMap           :dict      = {  }
friendlyEntity      :list[str] = []
entityDataMaintained:dict      = { "addAnimal"  : {} }