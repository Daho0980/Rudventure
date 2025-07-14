from ...base import ItemBehavior

from .testWeapon import TestWeapon

from .animus      import Animus
from .anima       import Anima
from .animusAnima import AnimusAnima


behaviorMap:dict[str, ItemBehavior] = {
    "testWeapon" : TestWeapon(),
    "animus" : Animus(),
    "anima" : Anima(),
    "animusAnima" : AnimusAnima()
}