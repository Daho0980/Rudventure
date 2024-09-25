from random import randrange

from Assets.data import status, lockers, percentage

from Game.utils.system.roomManager.roomEvents import (
    treasure,
    normal,
    event,
    boss
)

s, l = status, lockers
per  = percentage

def main() -> None:
    if not l.isDying:
        data = s.Dungeon[s.Dy][s.Dx]

        if l.jpsf and not data['interaction']:
            match data['roomType']:
                case 1: normal.event(data)
                case 2:
                    match data['eventType']:
                        case 0:     event.event0(data)
                        case 1|2|3: event.event1()
                case 3: treasure.event(True if randrange(1,101)<=per.treasureComment else False)
                case 4: boss.event(data)