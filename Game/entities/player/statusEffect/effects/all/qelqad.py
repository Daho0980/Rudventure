from ..base import StatusEffect


class Qelqad(StatusEffect):
    def tick(self, effect) -> None:
        return super().tick(effect)