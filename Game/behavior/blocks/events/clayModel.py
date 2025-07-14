from time   import sleep

from Game.entities.player.event import sayCmt

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)


class Orb:
    @staticmethod
    def hp() -> None: s.Mhp += 1

    @staticmethod
    def df() -> None: s.Mdf += 1

    @staticmethod
    def atk() -> None: s.atk += 1

    @staticmethod
    def ashChip() -> None: s.ashChip = 100

class Life:
    @staticmethod
    def awake() -> None: s.enemyCount += 1

    @staticmethod
    def kill() -> None: s.enemyCount -= 1

def afterAction() -> None:
    sleep(0.5)
    sayCmt(
        c.clayModelAnswer['cmt'],
        c.clayModelAnswer['prob']
    )