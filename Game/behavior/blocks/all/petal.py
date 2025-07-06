from ..base import BlockBehavior

class Petal(BlockBehavior):
    def interact(self, **data):
        return data['ty'], data['tx'], data['sound']