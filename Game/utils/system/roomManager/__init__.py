from random import randrange

from Assets.data import (
    totalGameStatus as s,
    percentage      as p,
    flags           as f
)
from .roomEvents import (
    treasure,
    normal,
    event,
    boss
)


def raiseRoomEvent() -> None:
    if not f.isDying:
        data = s.Dungeon[s.Dy][s.Dx]

        if f.jpsf and not data['interaction']:
            match data['roomType']:
                case "room": normal.event(data)
                case "event":
                    match data['eventType']:
                        case 0:     event.event0(data)
                        case 1|2|3: event.event1()
                        
                case "treasure": treasure.event(True if randrange(1,101)<=p.treasureComment else False)
                case "endPoint": boss.event(data)
