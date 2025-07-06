import time
from   threading import Thread

from Assets.data import (
    totalGameStatus as s,
    flags           as f
)


def exaltationCounter():
    while True:
        time.sleep(1)
        if f.jpsf and not f.pause and s.exaltation:
            s.exaltation -= 1

Thread(target=exaltationCounter, name="exaltationCounter", daemon=True).start()