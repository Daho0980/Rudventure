from abc import ABC, abstractmethod


class ItemBehavior(ABC):
    @abstractmethod
    def collect(self) -> None: pass

    @abstractmethod
    def use(self) -> None: pass

    @abstractmethod
    def attack(self) -> None: pass

    @abstractmethod
    def put(self) -> None: pass

    @abstractmethod
    def tread(self, itemId:str, itemType:str, payload:int) -> str: pass