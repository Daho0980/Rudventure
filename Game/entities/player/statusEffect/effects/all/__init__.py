from ..base import StatusEffect

from .fatality    import Fatality
from .combinator  import Combinator
from .angelHunter import AngelHunter

from .bloodStomping import BloodStomping

from .kitrima import Kitrima
from .ovitem  import Ovitem
from .qelqad  import Qelqad
from .bijolóa import Bijolóa


effectMap:dict[str, StatusEffect] = {
    "fatality" : Fatality(),
    "combinator" : Combinator(),
    "angelHunter" : AngelHunter(),
    "bloodStomping" : BloodStomping(),
    "kitrima" : Kitrima(),
    "ovitem" : Ovitem(),
    "qelqad" : Qelqad(),
    "bijoloa" : Bijolóa()
}