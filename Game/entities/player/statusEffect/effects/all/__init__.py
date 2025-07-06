from ..base import StatusEffect

from .bloodStomping import BloodStomping
from .kitrima       import Kitrima


effectMap:dict[str, StatusEffect] = {
    "bloodStomping" : BloodStomping(),
    "kitrima" : Kitrima()
}