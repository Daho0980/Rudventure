from Assets.data.permissions.classType import ByteFlag


class Permission(ByteFlag):
    data = {
        "invincibleBlock" : 0b1010,
        "void" : 0b0,
        "floor" : 0b1011,
        "wall" : 0b110,
        "door" : 0b110,
        "orbBox" : 0b1001,
        "exit" : 0b10,
        "squishy0" : 0b1,
        "squishy1" : 0b1,
        "hpOrbS" : 0b1001,
        "dfOrbS" : 0b1001,
        "atkOrbS" : 0b1001,
        "hgOrbS" : 0b1001,
        "csOrbS" : 0b1001,
        "hpOrbB" : 0b1001,
        "dfOrbB" : 0b1001,
        "atkOrbB" : 0b1001,
        "hgOrbB" : 0b1001,
        "csOrbB" : 0b1001,
        "clayModel" : 0b10,
        "deadClayModel" : 0b10,
        "flower" : 0b1001,
        "petal" : 0b1001,
        "item" : 0b1001,
        "corpse" : 0b1001,
        "blood" : 0b1001,
        "normalStatue" : 0b10,
        "cursedStatue" : 0b10,
        "aorta" : 0b1001,
        "venaCava" : 0b1001,
        "ashChip" : 0b1001,

        "player1" : 0b1110000,
        "player2" : 0b1110000,
        "invincibleEntity" : 0b100000,
        "cat" : 0b100000,
        "pain" : 0b100000,
        "unrest" : 0b100000,
        "resentment" : 0b100000
    }

    def __init__(self):
        self.STEP        = self.getFlag()
        self.MAINTAIN    = self.f_int()
        self.INTERACTION = self.f_int()
        self.BREAK       = self.f_int()
        self.ATTACK      = self.f_int()
        self.ENTITY      = self.f_int()
        self.ENEMY       = self.f_int()