from abc import ABC, abstractmethod


class StatusEffect(ABC):
    @abstractmethod
    def tick(self, effect) -> None: pass