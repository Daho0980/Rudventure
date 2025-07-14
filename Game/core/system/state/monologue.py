import time ; import threading
from   random import randrange, choices, choice

from Game.entities.player.event import sayCmt

from Assets.data import (
    totalGameStatus as s,
    comments        as c,
    flags           as f
)


def counter() -> None:
    s.monologueRange = randrange(
        c.monologue['range']['min'],
        c.monologue['range']['max']+1
    )

    while s.main:
        if f.jpsf and not f.pause and not s.enemyCount:
            if s.monologueCount == s.monologueRange:
                sayCmt(
                    choices(
                        (
                            choice(c.monologue['cmt']['ELS']),
                            choice(c.monologue['cmt'][
                                choice((
                                    "HL"  if s.hpLow                     else "ELS",
                                    "HUL" if int((s.hgr/s.Mhgr)*100)<=30 else "ELS",
                                    "CO"  if s.Mlvl-s.lvl==10            else "ELS"
                                ))
                            ])
                        ),
                        weights=(60,40),
                        k      =1
                    )[0],
                    
                    100
                )

                s.monologueRange = randrange(
                    c.monologue['range']['min'],
                    c.monologue['range']['max']+1
                )
                s.monologueCount = 0

            else: s.monologueCount += 1

            time.sleep(0.1)
            
        else: time.sleep(0.5)

threading.Thread(target=counter, name="monologueCounter", daemon=True).start()