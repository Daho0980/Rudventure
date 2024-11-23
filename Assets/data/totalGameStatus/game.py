# region Stage
stage:int = 0

# region Dungeon
Dungeon:list     = []
roomLock:bool    = False
killAll:bool     = False
clearEntity:bool = False

# region Modes
bodyPreservationMode:bool = False
ezMode:bool               = False
sanjibaMode:bool          = False

# region Entity
enemyCount:int              = 0
entityCount:int             = 0
totalEntityCount:int        = 0
entityHashPool:list[str]    = []
hitPos:dict[str,list[list]] = {
    "pos" : [],
    "data": []
}
friendlyEntity:list[str] = []
entityDataMaintained     = {"addAnimal"  : {}}
entitySaveTrigger        = False

isLoadfromBody:bool = False

# NOTE: this list holds string codes before starting the stage
RPL:list[str] = []