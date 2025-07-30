from ..base import StatusEffect


class Ovitem(StatusEffect):
    def tick(self, effect) -> None:
        return super().tick(effect)