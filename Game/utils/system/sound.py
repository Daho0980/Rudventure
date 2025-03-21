import time
import threading
from   audioplayer import AudioPlayer

from Assets.data import (
    totalGameStatus as s,
    lockers         as l
)


def play(*path, loop:bool=False, block:bool=False, volume:int=-1) -> None:
    if l.useSound and path:
        if block:
            AudioPlayer(
                f"{s.TFP}sounds{s.s}{s.s.join(path)}.wav",
                volume=volume if volume>-1 else s.volume
            ).play(loop=loop, block=True)

        else:
            threading.Thread(
                target=lambda: AudioPlayer(
                    f"{s.TFP}sounds{s.s}{s.s.join(path)}.wav",
                    volume=volume if volume>-1 else s.volume
                ).play(loop=loop, block=True),
                
                name  ="sound",
                daemon=True
            ).start()

def echo(*path,
         feedback:int       ,
         volume  :int  =-1  ,
         vVolume :int  =100 ,
         delay   :float=0.3 ,
         block   :bool =False) -> None:
    feedback = min(max(0, feedback), 100)

    if volume <0 or volume >100: volume  = s.volume
    if vVolume<0 or vVolume>100: vVolume = 100
    
    def target(v, sv):
        if v <= 0: return

        play(*path, block=False, volume=int(sv*(v/100)))
        v = int(v*feedback/100)
        time.sleep(delay)

        return target(v, sv)

    if block: target(vVolume, volume)
    else:
        threading.Thread(
            target=target,
            args  =(vVolume,volume,),
            name  ="sound_echo",
            daemon=True
        ).start()