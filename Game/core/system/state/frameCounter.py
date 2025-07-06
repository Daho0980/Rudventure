import time
from   threading import Thread

from Assets.data import totalGameStatus as s


def frameCounter():
    while True:
        time.sleep(1)
        s.currentFrameCount = s.elapsedFrameCount
        s.elapsedFrameCount = 0

Thread(target=frameCounter, name="frameCounter", daemon=True).start()