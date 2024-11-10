import time
import threading
from   random   import randrange, choices, choice

from Game.entities.player import say

from Assets.data import (
    percentage as p,
    comments   as c,
    lockers    as l,
    status     as s
)


def counter() -> None:
    s.soliloquyRange = randrange(p.soliloquy['min'], p.soliloquy['max']+1)

    while s.main:
        if l.jpsf and not l.pause and not s.enemyCount:
            if s.soliloquyCount == s.soliloquyRange:
                say(choices(
                    [
                        choice(c.soliloquyComments['ELS']),
                        choice(c.soliloquyComments[
                            choice([
                                "HL"  if s.hpLow==True          else "ELS",
                                "HUL" if round(s.hunger/20)<=30 else "ELS",
                                "CO"  if s.Mlvl-s.lvl==10       else "ELS"
                            ])
                        ])
                    ],
                    weights=[50,50],
                    k=1
                    )[0])

                s.soliloquyRange = randrange(p.soliloquy['min'], p.soliloquy['max']+1)
                s.soliloquyCount = 0
            else: s.soliloquyCount += 1
            time.sleep(0.1)
        else: time.sleep(0.5)

threading.Thread(target=counter, name="soliloquyCounter", daemon=True).start()