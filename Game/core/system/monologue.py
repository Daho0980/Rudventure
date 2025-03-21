import time ; import threading
from   random import randrange, choices, choice

from Game.entities.player import say

from Assets.data import (
    totalGameStatus as s,
    percentage      as p,
    comments        as c,
    lockers         as l
)


def counter() -> None:
    s.monologueRange = randrange(p.monologue['min'], p.monologue['max']+1)

    while s.main:
        if l.jpsf and not l.pause and not s.enemyCount:
            if s.monologueCount == s.monologueRange:
                say(choices(
                    [
                        choice(c.monologue['ELS']),
                        choice(c.monologue[
                            choice([
                                "HL"  if s.hpLow                else "ELS",
                                "HUL" if round(s.hunger/20)<=30 else "ELS",
                                "CO"  if s.Mlvl-s.lvl==10       else "ELS"
                            ])
                        ])
                    ],
                    weights=[50,50],
                    k=1
                    )[0])

                s.monologueRange = randrange(p.monologue['min'], p.monologue['max']+1)
                s.monologueCount = 0

            else: s.monologueCount += 1

            time.sleep(0.1)
            
        else: time.sleep(0.5)

threading.Thread(target=counter, name="monologueCounter", daemon=True).start()