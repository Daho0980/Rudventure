from Assets.data.permissions.classType import ByteFlag


class Permission(ByteFlag):
    data = { 
        "invincibleBlock" : 0b10,
        "void" : 0b0,
        "floor" : 0b11,
        "wall" : 0b110,
        "door" : 0b110,
        "orbBox" : 0b1,
        "exit" : 0b10,
        "squishy0" : 0b1,
        "squishy1" : 0b1,
        "hpOrbS" : 0b1,
        "dfOrbS" : 0b1,
        "atkOrbS" : 0b1,
        "hgOrbS" : 0b1,
        "csOrbS" : 0b1,
        "hpOrbB" : 0b1,
        "dfOrbB" : 0b1,
        "atkOrbB" : 0b1,
        "hgOrbB" : 0b1,
        "csOrbB" : 0b1,
        "clayModel" : 0b10,
        "deadClayModel" : 0b10,
        "flower" : 0b1,
        "petal" : 0b1,
        "item" : 0b11,
        "corpse" : 0b1,
        "blood" : 0b1,
        "normalStatue" : 0b10,
        "cursedStatue" : 0b10,
        "aorta" : 0b1,
        "venaCava" : 0b1,
        "ashChip" : 0b1,

        "player1" : 0b11100,
        "player2" : 0b11100,
        "invincibleEntity" : 0b10000,
        "cat" : 0b11100,
        "pain" : 0b111000,
        "unrest" : 0b111000,
        "resentment" : 0b111000,
    }

    def __init__(self):
        self.STEP        = self.getFlag()
        self.MAINTAIN    = self.f_int()
        self.INTERACTION = self.f_int()
        self.ATTACK      = self.f_int()
        self.ENTITY      = self.f_int()
        self.ENEMY       = self.f_int()

        self.IDSet = {
            "step"  : [k for k, v in self.data.items()if(v&self.STEP) ],
            "enemy" : [k for k, v in self.data.items()if(v&self.ENEMY)]
        }