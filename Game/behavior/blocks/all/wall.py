from ..base import BlockBehavior

from Game.entities.player.event import damagedByBlock


class Wall(BlockBehavior):
    def interact(self, **data):
        return data['ty'], data['tx'], damagedByBlock(data['block']['block'])