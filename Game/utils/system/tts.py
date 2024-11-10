import time

from .sound              import play
from Assets.data         import lockers   as l
from Game.utils.graphics import escapeAnsi


TCC = ['?', '!', ',', '.']

def TTS(text,
        voicePath:tuple=("player", "voice", "glagatrof"),
        delay:float|int=0.07                             ) -> None:
    if l.useSound:
        charList = escapeAnsi(text)
        for char, nextChar in zip(charList, charList[1:]+"0"):
            if char not in [' ', '.', ',', '"', '\'', '·', '~']:
                play(*voicePath)
            time.sleep(delay*4 if char in TCC and nextChar==' 'else delay)

def TTC(text, delay:float|int=0.07) -> int:
    charList = escapeAnsi(text)
    return int(sum(map(
        lambda c, nc: delay*4 if c in TCC and nc==' 'else delay,
        charList, charList[1:]+'0'
    ))*10)