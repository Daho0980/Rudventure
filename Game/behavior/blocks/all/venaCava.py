from ..base import BlockBehavior

from Assets.data import totalGameStatus as s


class VenaCava(BlockBehavior):
    def interact(self, **data):
        s.Mdf += 3

        return data['ty'], data['tx'], ("player", "getItem")