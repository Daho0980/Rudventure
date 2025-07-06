from abc import ABC, abstractmethod


class EntityBehavior(ABC):
    @abstractmethod
    def hit(self, **data): pass