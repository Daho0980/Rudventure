from ..base import StatusEffect


class Combinator(StatusEffect):
    def tick(self, effect) -> None:
        return super().tick(effect)