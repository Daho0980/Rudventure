from ..base import ItemBehavior

from .tool       import behaviorMap as TBM
from .weapon     import behaviorMap as WBM
from .consumable import behaviorMap as CBM


behaviorMap:dict[str, dict[str, ItemBehavior]] = {
    "tool"       : TBM,
    "weapon"     : WBM,
    "consumable" : CBM
}