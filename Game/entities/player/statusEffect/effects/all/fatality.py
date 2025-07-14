from ..base import StatusEffect


class Fatality(StatusEffect):
    def tick(self, effect) -> None:
        return super().tick(effect)