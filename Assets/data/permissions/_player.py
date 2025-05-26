from .classType import BitFlag


class Permission(BitFlag):
    data = {
        "invincibleBlock" : 0b10,
        "void" : 0b0,
        "floor" : 0b11,
        "wall" : 0b110,
        "door" : 0b111,
        "orbBox" : 0b100,
        "exit" : 0b111,
        "squishy0" : 0b100,
        "squishy1" : 0b100,
        "hpOrbS" : 0b101,
        "dfOrbS" : 0b101,
        "atkOrbS" : 0b101,
        "hgOrbS" : 0b101,
        "csOrbS" : 0b101,
        "hpOrbB" : 0b101,
        "dfOrbB" : 0b101,
        "atkOrbB" : 0b101,
        "hgOrbB" : 0b101,
        "csOrbB" : 0b101,
        "clayModel" : 0b110,
        "deadClayModel" : 0b110,
        "flower" : 0b101,
        "petal" : 0b1,
        "item" : 0b101,
        "corpse" : 0b1,
        "blood" : 0b101,
        "normalStatue" : 0b110,
        "cursedStatue" : 0b110,
        "aorta" : 0b101,
        "venaCava" : 0b101,
        "ashChip" : 0b101,

        "player1" : 0b11110,
        "player2" : 0b11110,
        "invincibleEntity" : 0b10000,
        "cat" : 0b111110,
        "pain" : 0b111110,
        "unrest" : 0b111110,
        "resentment" : 0b111110
    }

    def __init__(self):
        self.STEP        = self.getFlag()
        self.MAINTAIN    = self.f_int()
        self.INTERACTION = self.f_int()
        self.ATTACK      = self.f_int()
        self.ENTITY      = self.f_int()
        self.ENEMY       = self.f_int()