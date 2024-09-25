import threading
from audioplayer import AudioPlayer

from Assets.data import lockers as l
from Assets.data import status  as s


def play(*path, loop:bool=False) -> None:
    if l.useSound and path:
        threading.Thread(
            target=lambda: AudioPlayer(
                f"{s.TFP}sounds{s.s}{s.s.join(path)}.wav",
                volume=s.volume
            ).play(loop=loop, block=True),
            name  ="sound",
            daemon=True
            ).start()