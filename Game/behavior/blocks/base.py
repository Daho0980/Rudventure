from abc import ABC, abstractmethod


class BlockBehavior(ABC):
    @abstractmethod
    def interact(self, **data) -> tuple[int, int, tuple]: pass