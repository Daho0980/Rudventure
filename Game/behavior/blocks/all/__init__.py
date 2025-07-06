from ..base import BlockBehavior

from .floor  import Floor
from .wall   import Wall
from .orbBox import OrbBox
from .door   import Door

from .squishy0 import Squishy0
from .squishy1 import Squishy1

from .normalStatue import NormalStatue
from .cursedStatue import CursedStatue

from .clayModel     import ClayModel
from .deadClayModel import DeadClayModel

from .hpOrbS  import HpOrbS
from .dfOrbS  import DfOrbS
from .atkOrbS import AtkOrbS
from .hgOrbS  import HgOrbS
from .csOrbS  import CsOrbS

from .hpOrbB  import HpOrbB
from .dfOrbB  import DfOrbB
from .atkOrbB import AtkOrbB
from .hgOrbB  import HgOrbB
from .csOrbB  import CsOrbB

from .ashChip import AshChip

from .aorta    import Aorta
from .venaCava import VenaCava

from .flower import Flower
from .petal  import Petal

from .blood import Blood

behaviorMap:dict[str, BlockBehavior] = {
    "floor"  : Floor(),
    "wall"   : Wall(),
    "orbBox" : OrbBox(),
    "door"   : Door(),
    "squishy0" : Squishy0(),
    "squishy1" : Squishy1(),
    "normalStatue" : NormalStatue(),
    "cursedStatue" : CursedStatue(),
    "clayModel" : ClayModel(),
    "deadClayModel" : DeadClayModel(),
    "hpOrbS" : HpOrbS(),
    "dfOrbS" : DfOrbS(),
    "atkOrbS" : AtkOrbS(),
    "hgOrbS" : HgOrbS(),
    "csOrbS" : CsOrbS(),
    "hpOrbB" : HpOrbB(),
    "dfOrbB" : DfOrbB(),
    "atkOrbB" : AtkOrbB(),
    "hgOrbB" : HgOrbB(),
    "csOrbB" : CsOrbB(),
    "ashChip" : AshChip(),
    "aorta" : Aorta(),
    "venaCava" : VenaCava(),
    "flower" : Flower(),
    "petal" : Petal(),
    "blood" : Blood()
}