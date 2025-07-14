from ...base import ItemBehavior

from .testTool import TestTool
from .ásotus   import Ásotus


behaviorMap:dict[str, ItemBehavior] = {
    "testTool" : TestTool(),
    'ásotus' : Ásotus()
}