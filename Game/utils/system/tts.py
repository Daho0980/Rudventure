import re
import time

from Assets.data             import lockers   as l
from Game.utils.graphics     import escapeAnsi
from Game.utils.system.sound import play


def TTS(
        text,
        voicePath:tuple=("player", "voice", "glagatrof"),
        delay:float|int=0.07
        ) -> None:
    if l.useSound:
        for char in escapeAnsi(text):
            if char not in [' ', '.', ',', '"', '\'']:
                play(*voicePath)
            time.sleep(delay)