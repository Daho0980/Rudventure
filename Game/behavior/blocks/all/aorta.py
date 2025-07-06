from ..base import BlockBehavior

from Assets.data import totalGameStatus as s


class Aorta(BlockBehavior):
    def interact(self, **data):
        s.Mhp += 3

        return data['ty'], data['tx'], ("player", "getItem")