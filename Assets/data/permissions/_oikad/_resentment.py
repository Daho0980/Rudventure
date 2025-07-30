from Assets.data.permissions.classType import BitFlag


class Permission(BitFlag):
    data = {
        "invincibleBlock" : 0b0,
        "void" : 0b0,
        "floor" : 0b11,
        "wall" : 0b0,
        "door" : 0b0,
        "orbBox" : 0b11,
        "exit" : 0b0,
        "squishy0" : 0b1,
        "squishy1" : 0b1,
        "hpOrbS" : 0b11,
        "dfOrbS" : 0b11,
        "atkOrbS" : 0b11,
        "hgOrbS" : 0b11,
        "csOrbS" : 0b11,
        "hpOrbB" : 0b11,
        "dfOrbB" : 0b11,
        "atkOrbB" : 0b11,
        "hgOrbB" : 0b11,
        "csOrbB" : 0b11,
        "clayModel" : 0b1,
        "deadClayModel" : 0b1,
        "flower" : 0b11,
        "petal" : 0b11,
        "item" : 0b11,
        "corpse" : 0b11,
        "blood" : 0b11,
        "normalStatue" : 0b0,
        "cursedStatue" : 0b0,
        "aorta" : 0b11,
        "venaCava" : 0b11,
        "ashChip" : 0b11,

        "player1" : 0b1100,
        "player2" : 0b1100,
        "invincibleEntity" : 0b100,
        "cat" : 0b100,
        "pain" : 0b100,
        "unrest" : 0b100,
        "resentment" : 0b100
    }

    def __init__(self):
        self.STEP      = self.getFlag()
        self.EXPLOSION = self.f_int()
        self.ENTITY    = self.f_int()
        self.ENEMY     = self.f_int()