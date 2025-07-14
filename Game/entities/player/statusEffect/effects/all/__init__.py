from ..base import StatusEffect

from .fatality    import Fatality
from .combinator  import Combinator
from .angelHunter import AngelHunter

from .bloodStomping import BloodStomping
from .kitrima       import Kitrima


effectMap:dict[str, StatusEffect] = {
    "fatality" : Fatality(),
    "combinator" : Combinator(),
    "angelHunter" : AngelHunter(),
    "bloodStomping" : BloodStomping(),
    "kitrima" : Kitrima()
}