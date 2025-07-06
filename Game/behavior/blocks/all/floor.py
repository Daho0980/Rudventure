from ..base import BlockBehavior


class Floor(BlockBehavior):
    def interact(self, **data):
        return data['ty'], data['tx'], data['sound']