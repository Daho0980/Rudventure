from ..base import StatusEffect


class AngelHunter(StatusEffect):
    def tick(self, effect) -> None:
        return super().tick(effect)