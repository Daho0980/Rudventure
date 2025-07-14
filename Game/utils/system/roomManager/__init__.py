from Assets.data import (
    totalGameStatus as s,
    flags           as f
)
from .roomEvents import (
    treasure,
    normal,
    event,
    endPoint
)


def raiseRoomEvent() -> None:
    if not f.isDying:
        data = s.Dungeon[s.Dy][s.Dx]

        if f.jpsf and not data['interaction']:
            match data['roomType']:
                case "room" : normal.event(data)
                case "event":
                    match data['eventType']:
                        case 0:     event.event0(data)
                        case 1|2|3: event.event1()
                        
                case "treasure": treasure.event()
                case "endPoint": endPoint.event()
