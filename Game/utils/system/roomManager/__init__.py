from random import randrange, choice

from Assets.data                              import status as s
from Assets.data                              import lockers
from Game.utils.system.roomManager.roomEvents import (
    normal,
    event,
    treasure,
    boss
)

l = lockers

def main() -> None:
    if not l.isDying:
        data:dict = s.Dungeon[s.Dy][s.Dx]

        if l.jpsf and not data['interaction']:
            commentP = randrange(0, 2)

            match data['roomType']:
                case 1: normal.event(data)
                case 2:
                    choice(
                        [
                            event.event0,
                            event.event1
                        ]
                    )()
                case 3: treasure.event(commentP)
                case 4: boss.event(data)